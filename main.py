from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
#from fastapi.encoders import jsonable_encoder

from scrape.cve.scrape_wapp import scrape
from scrape.cve.cve_fetch import start_fetch

app = FastAPI()

class FinalList(BaseModel):
    final_list: list


@app.post("/getcve")
async def getCves(finalListObj: FinalList):
    cve_dict: dict = start_fetch(finalListObj.final_list)
    return(cve_dict)


@app.get("/{url}")
def getDeps(url: str):
    print(url)
    #scraped_dep = {"wtf"}
    scraped_dep: dict = scrape(url)
    return scraped_dep

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host='127.0.0.1', port=8080, reload=True)

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)