import time
import requests
from tqdm import tqdm
from random import randrange
import json
import pandas as pd
from datetime import datetime
import logging


class LinkedinAPI:
    def __init__(self, cookiesPath, headersPath):
        with open(headersPath, "r") as f:
            self.headers = json.load(f)
        with open(cookiesPath, "r") as f:
            self.cookies = json.load(f)

    def preparQueries(keywords):
        q_list = []
        for q in keywords:
            # q = "%22" + q + "%22"
            q_list.append(q.replace(" ", "%20"))
        return q_list

    def getProfiles(self, keywords):
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
                    response = requests.get(
                        query, cookies=self.cookies, headers=self.headers
                    )
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
                print(
                    response.status_code, keyword, "c'est mort au niveau du ce keyword"
                )
        return totalData

    def saveResults(data, cols, out_file):
        linkedin_df = pd.DataFrame(data, columns=cols)
        linkedin_df["invitation"] = 0
        linkedin_df.to_csv(out_file, index=False)

    def sendConnection(self, invitation_file, random=20):
        """
        Input:
            file: csv of linkedin profiles
            output_file: name of file to save the result
            cookies
            headers
            random: number of profiles to send connection
        Output:
            csv file for each row if the invitation sent or no
        """
        params = {
            "action": "verifyQuotaAndCreate",
        }
        df = pd.read_csv(invitation_file)
        random_20 = df[df["invitation"] == 0].sample(random)
        if random_20.shape[0] > 0:
            random_20 = random_20.reset_index()
            for index, row in random_20.iterrows():
                prenom = row["First_name"]
                url = row["Url"]
                id = url.split("/")[-1]
                message = f"Bonjour {prenom},\nImpressionné par votre parcours. J'entends parler de vous via notre réseau commun. J'aimerais faire partie de votre réseau pour échanger sur vos projets tech & data.\nCordialement,\nMatthieu"
                json_data = {
                    "inviteeProfileUrn": f"urn:li:fsd_profile:{id}",
                    "customMessage": message,
                }
                response = requests.post(
                    "https://www.linkedin.com/voyager/api/voyagerRelationshipsDashMemberRelationships",
                    params=params,
                    cookies=self.cookies,
                    headers=self.headers,
                    json=json_data,
                )
                if response:
                    print(response.status_code)
                    print(url, index)
                    # update invitation
                    df.loc[(df["Url"] == url), "invitation"] = 1
                    time.sleep(randrange(20))
                else:
                    print(response.status_code)
                    break
            # save updated csv file
            df.to_csv(invitation_file, index=False)
        else:
            logging.info(
                "tout les utilisateurs de ce fichier ont recu une invitation !"
            )

    def getConnections(self, nbr=1000):
        params = {
            "decorationId": "com.linkedin.voyager.dash.deco.web.mynetwork.ConnectionListWithProfile-15",
            "count": f"{nbr}",
            "q": "search",
            "sortType": "RECENTLY_ADDED",
        }
        response = requests.get(
            "https://www.linkedin.com/voyager/api/relationships/dash/connections",
            params=params,
            cookies=self.cookies,
            headers=self.headers,
        )
        if response.status_code == 200:
            pd.DataFrame(
                map(
                    lambda x: ["https://www.linkedin.com/in/" + x.split(":")[-1]],
                    response.json()["data"]["*elements"],
                ),
                columns=["Url_relation"],
            ).to_csv("./relations/matthieu_relations.csv", index=False)
        else:
            return response.status_code
