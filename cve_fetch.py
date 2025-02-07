#import requests

# import re
# from cpe import CPE

# r = requests.get("https://services.nvd.nist.gov/rest/json/cves/2.0", params={"cpeName":"cpe:2.3:a:\@nubosoftware\/node-static_project:\@nubosoftware\/node-static:-:*:*:*:*:node.js:*:*"})

# prod = "requirejs"
# ver = "2.3.6" 
# myCPE = f"cpe:2.3:a:{prod}:{prod}:{ver}:*:*:*:*:*:*:*"

# print(myCPE)

# finalCPE = CPE(myCPE, CPE.VERSION_2_3)
# print(finalCPE)

# print(re.search(myCPE, "cpe:2.3:a:php:php:5.6.0:*.*.*"))
# print(myCPE)

#------------------------------------------------------------nvd api fetch------------------------------------------------------

# response = requests.get("https://services.nvd.nist.gov/rest/json/2.0", params={"keywordSearch":"apache http server 2.4.18"})

# #response = requests.get("https://api.wappalyzer.com/v2/lookup/?urls=https://www.geeksforgeeks.org&sets=all", headers={"api-key":"ur1387667-0be04391f303532dfe10b42f"})

# print(response.content)
# jsonData = response.json()
# print(jsonData)

#--------------------------------------------------------------------------------------------------------------------------------

# vulnerabilities = jsonData.get('vulnerabilities', [])

# for vuln in jsonData['vulnerabilities']:
#     cve_id = vuln['cve']['id']
#     desc = vuln['cve']['descriptions'][0]['value']
#     print(cve_id)
#     print(desc)

#-------------------------------------------------------------Manual Fetch---------------------------------------------------------

import ijson
import ijson.dump
from packaging.version import Version, parse
import re
import threading
from concurrent.futures import ThreadPoolExecutor

from tqdm import tqdm
from rich.progress import track

def tenseCheck(value, string):  #before\s(?:v?|(?:version\s))?
    return bool(re.search("before\s(?:v?|(?:version\s))?"+value, string, re.IGNORECASE)) or bool(re.search("prior\sto\s(?:v?|(?:version\s))?"+value, string, re.IGNORECASE)) or bool(re.search(value+"\sand\searlier", string, re.IGNORECASE))

def versionValidity(vers):
    for i in range(len(vers)):
        vers[i] = vers[i].strip()

    for ver in vers[:]:
        ver = ver.strip()
        try:
            parse(ver)
        except:
            vers.remove(ver)
    return vers

def getCvss(record):
    cvss3 = 'undefined'
    cvss2 = 'undefined'
    if ("baseMetricV3" in record["impact"]):
            cvss3 = record["impact"]["baseMetricV3"]["cvssV3"]["baseScore"]
    if ("baseMetricV2" in record["impact"]):
            cvss2 = record["impact"]["baseMetricV2"]["cvssV2"]["baseScore"]
    return cvss3, cvss2

#print(tenseCheck('2.4.20',string))

#exit()
#print(re.findall(matchOtherVer, string))

lock = threading.Lock()

def fetch_cve_from_json_files(i, prod_name, version, matchString, matchVersion, matchOtherVer):
    cve_list = []
    #print(version)
    with open(f"C:/Users/makwa/VS-code/.env/scrape/cve/cve_data_feed/nvdcve-1.1-{i}.json","rb") as file:
        for record in ijson.items(file, "CVE_Items.item"):
            description = record["cve"]["description"]["description_data"][0]["value"]
            
            matchVersionHi = "0.0.0"
            matchVersionLo = "0.0.0"

            if bool(re.search(matchString, description, re.IGNORECASE)):

                cveID = record["cve"]["CVE_data_meta"]["ID"]
                #print(description)
                cpeNoMatch = 0
                cpes = ''
                try:
                    #print("enterrrrr")
                    if ("cpe_match" in record["configurations"]["nodes"][0] and len(record["configurations"]["nodes"][0]["cpe_match"]) != 0):
                        cpes = record["configurations"]["nodes"][0]["cpe_match"]
                        #print("thissssssssss ",cpes)
                    else:
                        cpes = record["configurations"]["nodes"][0]["children"][0]["cpe_match"]
                        #print("thatttttttttt ",cpes)
                    #print("hereeeeeee")
                    for cpe in cpes:
                        #print(cpe["cpe23Uri"])

                        if not (bool(re.search(":"+prod_name+":",cpe['cpe23Uri'], re.IGNORECASE))):
                            cpeNoMatch += 1
                            break
                        if("versionStartIncluding" in cpe and "versionEndExcluding" in cpe):
                            matchVersionLo = cpe["versionStartIncluding"]
                            matchVersionHi = cpe["versionEndExcluding"]
                            #print("vHI: ",matchVersionHi)
                            #print("vLO: ",matchVersionLo)

                            if(parse(matchVersionHi) >= version and parse(matchVersionLo) <= version):
                                #print(1)
                                cvss3, cvss2 = getCvss(record)
                                cve_list.append({'ID':cveID, 'Description':description, 'Cvss3': cvss3, 'Cvss2': cvss2})
                                # cve_list.append(cveID)
                                cpeNoMatch += 1
                                break
                except:
                    pass

                #print(cpeNoMatch)
                if(cpeNoMatch != 0 or matchVersionHi != '0.0.0'):
                    continue
                #vers = re.findall(f"{version.major}\.{version.minor}\.?\d*", description)
                vers = re.findall(matchVersion, description)
                vers = versionValidity(vers)

                #print(cveID)
                #print("vers: ",vers)
                # print(versLo)
                # print(versHi)
                
                if(len(vers)!=0):
                    if parse(vers[0]) == version:
                        #print(2)
                        with lock:
                            cvss3, cvss2 = getCvss(record)
                            cve_list.append({'ID':cveID, 'Description':description, 'Cvss3': cvss3, 'Cvss2': cvss2})
                            # cve_list.append(cveID)
                    elif (parse(vers[0]) > version and tenseCheck(vers[0], description)):
                            #print(3)
                            with lock:
                                cvss3, cvss2 = getCvss(record)
                                cve_list.append({'ID':cveID, 'Description':description, 'Cvss3': cvss3, 'Cvss2': cvss2})
                                # cve_list.append(cveID)
                    elif (len(vers) > 1 and parse(vers[0]) <= version and parse(vers[1]) >= version):
                            #print(4)
                            with lock:
                                cvss3, cvss2 = getCvss(record)
                                cve_list.append({'ID':cveID, 'Description':description, 'Cvss3': cvss3, 'Cvss2': cvss2})
                                # cve_list.append(cveID)
                else:
                    otherVer = re.findall(matchOtherVer, description)
                    otherVer = versionValidity(otherVer)
                    if (len(otherVer) != 0 and parse(otherVer[0]) >= version and tenseCheck(otherVer[0], description)):
                        #print("otv ",otherVer[0])
                        #print(5)
                        with lock:
                            cvss3, cvss2 = getCvss(record)
                            cve_list.append({'ID':cveID, 'Description':description, 'Cvss3': cvss3, 'Cvss2': cvss2})
                            # cve_list.append(cveID)
    return cve_list



def start_fetch(prods):
    cve_dict = {}
    for prod in track(prods, total=len(prods)):
        version = parse(prod[-1])
        
        matchString = "\s.*".join(prod[:-1])
        matchString += ".*[v]?"+str(version.major)+"?"
        #print(matchString)

        ############# MAYBE REMOVE THE [^\.] FROM THE FRONT AND TEST, LAST CHANGE MADE TO THE CODE ###############
        matchVersion = "[^\.]"+str(version.major)+"\.[0-9]+\.?\d*"
        #print(matchVersion)

        matchOtherVer = "[0-9]+\.[0-9]+\.?\d*"

        file_numbers = range(2002, 2025)

        results = []
        # for i in range(2002, 2025):
        #     thread = threading.Thread(target=fetch_cve_from_json_files, args=(i, prod[0], version, matchString, matchVersion, matchOtherVer, cveList))
        #     threads.append(thread)
        #     thread.start()

        # for thread in threads:
        #     thread.join()


        with ThreadPoolExecutor(max_workers=20) as executor:

            futures = [executor.submit(fetch_cve_from_json_files, i, prod[0], version, matchString, matchVersion, matchOtherVer) for i in file_numbers]

            for future in futures:
                if len(future.result()) != 0:
                    results.append(future.result())

        if(len(results) != 0):
            cve_dict[' '.join(prod)] = results
            #print(f"\n{' '.join(prod)}: {results}")

    return cve_dict;

# prods = [['apache','http','server','2.4.18']]
# start_fetch(prods)

if __name__ == "__main__":
    prods = [["jquery","3.3.1"]]
    cve_dict = start_fetch(prods)
    print(cve_dict)

    #prod = ['WordPress', '6.4.4']
#prod = ["apache","http","server","2.4.18"]
#prod = ["jquery","3.3.1"]
#prod = ["php", "8.3.12"]
#prod = ["next.js","12.3.4"]
#prod = ['Popper', '1.14.7']

#matchVersion = str(version.major)+"\.?[0-9]*\.?\d*"

# if(version.micro != 0):
#     matchVersionExact = str(version.major)+"\."+str(version.minor)+"\.\d+"
#     matchVersionHi = str(version.major+1)+"(?:\..+)+"
#     matchVersionLo = str(version.major-1)+"(?:\..+)+"
    
# else:
#     matchVersion = str(version.major)+"\."+str(version.minor)

# print(matchVersion)
# print(matchOtherVer)
# print(version)
# #print(version.micro)

#string = "Apache HTTP Server version 2.4.20 to 2.4.43 When trace/debug was enabled for the HTTP/2 module and on certain traffic edge patterns, logging statements were made on the wrong connection, causing concurrent use of memory pools. Configuring the LogLevel of mod_http2 above 'info' will mitigate this vulnerability for unpatched servers."

# print(re.findall(matchVersion, string))