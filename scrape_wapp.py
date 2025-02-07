#from seleniumwire import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
import requests
import re

#change path according to your chrome broswer
DRIVER_PATH = "C:/Users/makwa/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"

driver_exec_path = Service(DRIVER_PATH)

chrome_options = Options()
#chrome_options.add_experimental_option("detach", True)    #uncomment to keep browser running when 
                                                            #manual chrome debugging/logging in is required 

chrome_options.add_argument("user-data-dir=C:/Users/makwa/VS-code/.env/scrape/cve/cookies_for_wapp")
#chrome_options.add_argument("--headless")       #comment this option to view chrome browser and in addition with 
                                                #uncommenting the "detach" chrome option

# check if website exists
def checkWebsite(url):
    try:
        response = requests.get(f'https://{url}')
        if response.status_code == 200:
            print("Website exists")
            return True
        else:
            print('No such website found')
            return False
    except:
        print('No such website found')
        return False

# sanitize url to only contain the netloc option
def sanitizeUrl(url):
    url = urlparse(url)
    if(url.netloc == ''):
        url = url.path
    else:
        url = url.netloc
    sanitized_url = re.sub(r'^www\.', '', url)
    return  sanitized_url

# full scraping logic 
def scrape(url):

    scraped_dep_dict = {"Exist": True}

    url = sanitizeUrl(url)

    if not checkWebsite(url):
        scraped_dep_dict["Exist"] = False
        return scraped_dep_dict

    #initialize chrome driver
    driver = webdriver.Chrome(service=driver_exec_path, options=chrome_options)

    #-----------------------------------------------------Wappalyzer-----------------------------------------------------
    wapp_dep_list = []
    try:
        driver.get(f'https://www.wappalyzer.com/lookup/{url}/')

        # wait for website to load by checking presence of element
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.ml-2.d-flex.align-center.text-decoration-none'))
        )

        # scraping logic for wappalyzer
        wapp_dep_list= driver.execute_script('''
            var vers=document.querySelectorAll("div.ml-2.d-flex.align-center.text-decoration-none");
            var list=[];
            vers.forEach((ver)=>{
                if(ver.children.length > 1){
                    splitlist = ver.children[0].textContent.trim().split(' ');
                    splitlist.push(ver.children[1].textContent.trim().replace(/[\(\)]/g,''))
                    list.push(splitlist)
                }
            });
            return list;
        ''')

        # print("Wappalyzer dependencies: ",wapp_dep_list)
    except:
        wapp_dep_list = []
        print("no dependency found on Wappalyzer")

    #-----------------------------------------------------BuiltWith--------------------------------------------------------

    driver.get(f'https://builtwith.com/{url}')

    try:
        # wait for website to load by checking presence of element
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.card.mt-4.mb-2'))
        )

        # scraping logic for BuiltWith
        bw_dep_list=driver.execute_script('''
            list = [];
            titles=document.querySelectorAll("div.card-body.pb-0");
            titles.forEach((title)=>{
                tit = title.querySelector("h6").textContent.trim();
                if(/javascript.*/i.test(tit) || /web.*/i.test(tit) || /framework.*/i.test(tit)){
                    list.push(title);
                }
            })

            bw_dep_list = [];        
            list.forEach((item)=>{
                h5s=item.querySelectorAll("h5");
                h5s.forEach((h5)=>{
                    if(h5.children.length > 0 && /\d+/g.test(h5.textContent.trim()))
                        bw_dep_list.push(h5.textContent.trim())
                })
            })

            return bw_dep_list;
        ''')

        for i in range(len(bw_dep_list)):
            bw_dep_list[i]=bw_dep_list[i].split()

        #print("BuiltWith dependencies: ",bw_dep_list)

    except:
        bw_dep_list = []
        print("no dependency found on BuiltWith")


    #------------------------------------------------------WhatRuns-----------------------------------------------------

    driver.get(f'https://www.whatruns.com/website/{url}')

    try:
        # wait for website to load by checking presence of element
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.tech-name'))
        )

        # scraping logic for WhatRuns
        wr_dep_list = driver.execute_script('''
            wr_dep_list = [];
            tech = document.querySelectorAll("div.tech-name");

            tech.forEach((item)=>{
                name = item.textContent.trim();
                if(/\d+/g.test(name))
                    wr_dep_list.push(name)
            });
                    
            return wr_dep_list;
        ''')

        for i in range(len(wr_dep_list)):
            wr_dep_list[i]=wr_dep_list[i].split()

        # print("WhatRuns dependencies: ",wr_dep_list)

    except:
        wr_dep_list = []
        print("no dependency found on WhatRuns")


    #--------------------------------------------------------W3techs--------------------------------------------------

    driver.get(f'https://w3techs.com/sites/info/{url}')


    try:
        # wait for website to load by checking presence of element
        WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((By.ID, 'submit_button'))
        )

        # if w3tech hasnt crawled the url by itself
        driver.execute_script('''
            btn = document.getElementsByName("add_site");
            btn[0].click()
        ''')

    except:
        pass

    try:
        # wait for website to load by checking presence of element
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'p.si_tech'))
        )

        # w3techs scarpe logic
        wt_dep_list = driver.execute_script('''
            wt_dep_list = [];
            tech = document.querySelectorAll("p.si_tech");                       

            tech.forEach((item)=>{
                let cont = item.textContent.trim();
                if(/\w*\s\d+/g.test(cont)){
                    cont = cont.replace(/0%\s.*/g,"");
                    cont = cont.replace(/\d\d%.*/g,"");
                    cont = cont.replace(/used.*/g,"");
                    cont = cont.replace(/version.*/g,"");
                    wt_dep_list.push(cont)
                }
            });
                                            
            return wt_dep_list;
        ''')

    except:
        wt_dep_list = []
        print("no dependency found on W3techs")

    for i in range(len(wt_dep_list)):
            wt_dep_list[i]=wt_dep_list[i].split()

    #print("W3tech dependencies: ",wt_dep_list)

    #quit driver
    driver.quit()

    final_list = wapp_dep_list + bw_dep_list + wr_dep_list + wt_dep_list

    final_list = listCorrection(final_list)

    scraped_dep_dict.update({"Wappalyzer": wapp_dep_list, "BuiltWith": bw_dep_list, "WhatRuns": wr_dep_list, "W3Techs": wt_dep_list, "final_list": final_list})

    return  scraped_dep_dict     # returning dictionary for api

#-----------------------------------------------------------------list sanitization-----------------------------------------------------

correctionDict = {
    "wordpress": {
        "keep" : True,
        "keywords": ["cms"],
        "version_len": 5
    },
    "apache": {
        "keep" : True,
        "keywords": ["http", "server"],
        "version_len": 5
    },
    "php": {
        "keep" : True,
        "keywords": [],
        "version_len": 5
    },
    "google": {
        "keep" : False,
        "keywords": [],
        "version_len": 0
    }
}

def listCorrection(final_list):

    for dlist in final_list[:]:

        #lower all keywords in dependencies for simple macthing
        dlist[:-1] = [word.lower() for word in dlist[:-1]]

        #remove letters from versions
        dlist[-1] = re.sub('[a-zA-Z]', '', dlist[-1])

        if dlist[0] in correctionDict:
            #remove unwanted dependencies
            if(correctionDict[dlist[0]]["keep"] == False):
                final_list.remove(dlist)
            else:
                #insert missing keywords in list after index 1
                if(len(dlist) == 2):
                    dlist[1:1] = correctionDict[dlist[0]]["keywords"]
            
                #remove dependencies with vague version numbers
                if(len(dlist[-1]) < correctionDict[dlist[0]]["version_len"]):
                    final_list.remove(dlist)
        
    # remove recurring dependencies and create a unique list
    uniqueTuples = {tuple(lst) for lst in final_list}
    uniqueLists = [list(tpl) for tpl in uniqueTuples]

    return uniqueLists


#wapp_dep_list, bw_dep_list, wr_dep_list, wt_dep_list, final_list = scrape('geeksforgeeks.org')

#print("Wappalyzer dependencies: ",wapp_dep_list)
#print("BuiltWith dependencies: ",bw_dep_list)
#print("WhatRuns dependencies: ",wr_dep_list)
#print("W3tech dependencies: ",wt_dep_list)
#print(final_list)

#print("\nFinal List: ",final_list," ",len(final_list))

# ----------------------------------------------------local test--------------------------------------------------

if __name__ == "__main__":

    url = input("Enter Website URL: ")
    scraped_dep_dict = scrape(url)

    if (scraped_dep_dict["Exist"] != False):
        final_list = scraped_dep_dict["final_list"]
        print(final_list)

    #from scrape.cve import cve_fetch
    #cve_fetch.start_fetch(final_list)
