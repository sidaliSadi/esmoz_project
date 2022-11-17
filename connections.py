import pandas as pd
import requests
from random import randrange
import time
import logging


def sendConnection(file, output_file, cookies, headers, random=20):
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
    df = pd.read_csv(file)
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
                cookies=cookies,
                headers=headers,
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
        df.to_csv(output_file, index=False)
    else:
        logging.info("tout les utilisateurs de ce fichier ont recu une invitation !")


def getConnections(cookies, headers, nbr=1000):
    params = {
        "decorationId": "com.linkedin.voyager.dash.deco.web.mynetwork.ConnectionListWithProfile-15",
        "count": f"{nbr}",
        "q": "search",
        "sortType": "RECENTLY_ADDED",
    }
    response = requests.get(
        "https://www.linkedin.com/voyager/api/relationships/dash/connections",
        params=params,
        cookies=cookies,
        headers=headers,
    )
    if response.status_code == 200:
        pd.DataFrame(
            map(
                lambda x: ["https://www.linkedin.com/in/" + x.split(":")[-1]],
                response.json()["data"]["*elements"],
            ),
            columns=["Url_relation"],
        ).to_csv("./relations/matthieu_relations.csv")
    else:
        return response.status_code
