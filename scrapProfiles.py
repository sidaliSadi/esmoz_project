import time
import requests
from tqdm import tqdm
from random import randrange
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime


def loadParams():
    load_dotenv()
    return os.getenv("COOKIES"), os.getenv("HEADERS")


cookies, headers = loadParams()


def getProfiles(keywords, cookies, headers):
    date = datetime.today().strftime("%Y-%m-%d")
    totalData = []
    for keyword in keywords:
        start = 0
        query = f"https://www.linkedin.com/voyager/api/search/dash/clusters?decorationId=com.linkedin.voyager.dash.deco.search.SearchClusterCollection-167&origin=FACETED_SEARCH&q=all&query=(keywords:{keyword},flagshipSearchIntent:SEARCH_SRP,queryParameters:(currentCompany:List(1951),geoUrn:List(90009659,104246759),resultType:List(PEOPLE)),includeFiltersInResponse:false)&start={start}"
        response = requests.get(query, cookies=cookies, headers=headers)
        if response.status_code == 200:
            number_pages = int(response.json()["data"]["paging"]["total"] // 10)
            print("nombre de page est :", number_pages)
            for i in tqdm.tqdm(range(0, number_pages + 1)):
                query = f"https://www.linkedin.com/voyager/api/search/dash/clusters?decorationId=com.linkedin.voyager.dash.deco.search.SearchClusterCollection-167&origin=FACETED_SEARCH&q=all&query=(keywords:{keyword},flagshipSearchIntent:SEARCH_SRP,queryParameters:(currentCompany:List(1951),geoUrn:List(90009659,104246759),resultType:List(PEOPLE)),includeFiltersInResponse:false)&start={start}"
                response = requests.get(query, cookies=cookies, headers=headers)
                time.sleep(randrange(10))
                # check if code_status is ok
                if response.status_code == 200:
                    # check if we got something
                    if len(response.json()["included"]):
                        for p in response.json()["included"]:
                            if "template" in p.keys():
                                try:
                                    nom_prenom = p["title"]["text"]
                                except:
                                    nom_prenom = ""
                                try:
                                    job = p["primarySubtitle"]["text"]
                                except:
                                    job = ""
                                try:
                                    summary = p["summary"]["text"]
                                except:
                                    summary = ""
                                try:
                                    url = (
                                        "https://www.linkedin.com/in/"
                                        + p["image"]["attributes"][0][
                                            "detailDataUnion"
                                        ]["nonEntityProfilePicture"][
                                            "profileUrn"
                                        ].split(
                                            ":"
                                        )[
                                            -1
                                        ]
                                    )
                                except:
                                    url = ""
                                totalData.append(
                                    [nom_prenom, summary, job, url, keyword, date]
                                )
                        start = start + 10
                else:
                    print(response.status_code, keyword, start)

        else:
            print(response.status_code, keyword, "c'est mort au niveau du ce keyword")
    return totalData


def saveResults(data, cols):
    linkedin_df = pd.DataFrame(data, cols)
    linkedin_df.to_csv(f'data/{datetime.today().strftime("%Y-%m-%d")}.csv')
