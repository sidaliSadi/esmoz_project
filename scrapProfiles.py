import time
import requests
from tqdm import tqdm
from random import randrange
import json
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime


def loadCredentials(cookies_path, headers_path):
    with open(headers_path, "r") as f:
        headers = json.load(f)
    with open(cookies_path, "r") as f:
        cookies = json.load(f)
    return cookies, headers


def preparQueries(keywords):
    q_list = []
    for q in keywords:
        # q = "%22" + q + "%22"
        q_list.append(q.replace(" ", "%20"))
    return q_list


def getProfiles(keywords, c, h):
    date = datetime.today().strftime("%Y-%m-%d")
    totalData = []
    for keyword in keywords:
        start = 0
        query = f"https://www.linkedin.com/voyager/api/search/dash/clusters?decorationId=com.linkedin.voyager.dash.deco.search.SearchClusterCollection-167&origin=FACETED_SEARCH&q=all&query=(keywords:{keyword},flagshipSearchIntent:SEARCH_SRP,queryParameters:(currentCompany:List(1951),geoUrn:List(90009659,104246759),resultType:List(PEOPLE)),includeFiltersInResponse:false)&start={start}"
        response = requests.get(query, cookies=c, headers=h)
        if response.status_code == 200:
            number_pages = int(response.json()["data"]["paging"]["total"] // 10)
            print("nombre de page est :", number_pages)
            for i in tqdm(range(0, number_pages + 1)):
                query = f"https://www.linkedin.com/voyager/api/search/dash/clusters?decorationId=com.linkedin.voyager.dash.deco.search.SearchClusterCollection-167&origin=FACETED_SEARCH&q=all&query=(keywords:{keyword},flagshipSearchIntent:SEARCH_SRP,queryParameters:(currentCompany:List(1951),geoUrn:List(90009659,104246759),resultType:List(PEOPLE)),includeFiltersInResponse:false)&start={start}"
                response = requests.get(query, cookies=c, headers=h)
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


def saveResults(data, cols, out_file):
    linkedin_df = pd.DataFrame(data, columns=cols)
    linkedin_df["invitation"] = 0
    linkedin_df.to_csv(out_file, index=False)
