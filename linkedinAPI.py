import time
import requests
from tqdm import tqdm
from random import randrange
import json
import pandas as pd
import ast
from datetime import datetime
import logging


class LinkedinAPI:
    def __init__(self, cookiesPath, headersPath):
        self.s = requests.Session()
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 OPR/67.0.3575.97"
        }
        with open(headersPath, "r") as f:
            self.headers_model = json.load(f)
        with open(cookiesPath, "r") as f:
            self.cookies_model = json.load(f)

    def login(self, email, password):
        # creates a session
        try:
            sc = self.s.get("https://www.linkedin.com/login", headers=self.headers).text
        except:
            return False
        csrfToken = sc.split('csrfToken" value="')[1].split('"')[0]
        sid = sc.split('sIdString" value="')[1].split('"')[0]
        pins = sc.split('pageInstance" value="')[1].split('"')[0]
        lcsrf = sc.split('loginCsrfParam" value="')[1].split('"')[0]
        data = {
            "csrfToken": csrfToken,
            "session_key": email,
            "ac": "2",
            "sIdString": sid,
            "parentPageKey": "d_checkpoint_lg_consumerLogin",
            "pageInstance": pins,
            "trk": "public_profile_nav-header-signin",
            "authUUID": "",
            "session_redirect": "https://www.linkedin.com/feed/",
            "loginCsrfParam": lcsrf,
            "fp_data": "default",
            "_d": "d",
            "showGoogleOneTapLogin": "true",
            "controlId": "d_checkpoint_lg_consumerLogin-login_submit_button",
            "session_password": password,
            "loginFlow": "REMEMBER_ME_OPTIN",
        }
        try:
            after_login = self.s.post(
                "https://www.linkedin.com/checkpoint/lg/login-submit",
                headers=self.headers,
                data=data,
            ).text
        except:
            return False
        is_logged_in = after_login.split("<title>")[1].split("</title>")[0]
        if is_logged_in == "LinkedIn":
            my_cookies = requests.utils.dict_from_cookiejar(self.s.cookies)
            self.cookies_model = {**self.cookies_model, **my_cookies}
            self.headers_model["csrf-token"] = self.cookies_model["JSESSIONID"]
            self.headers_model = ast.literal_eval(
                json.dumps(self.headers_model).replace('\\"', "")
            )

            return True
        else:
            return False

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
            response = requests.get(
                query, cookies=self.cookies_model, headers=self.headers_model
            )
            if response.status_code == 200:
                number_pages = int(response.json()["data"]["paging"]["total"] // 10)
                print("nombre de page est :", number_pages)
                for i in tqdm(range(0, number_pages + 1)):
                    query = f"https://www.linkedin.com/voyager/api/search/dash/clusters?decorationId=com.linkedin.voyager.dash.deco.search.SearchClusterCollection-167&origin=FACETED_SEARCH&q=all&query=(keywords:{keyword},flagshipSearchIntent:SEARCH_SRP,queryParameters:(currentCompany:List(1951),geoUrn:List(90009659,104246759),resultType:List(PEOPLE)),includeFiltersInResponse:false)&start={start}"
                    response = requests.get(
                        query, cookies=self.cookies_model, headers=self.headers_model
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
                    cookies=self.cookies_model,
                    headers=self.headers_model,
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
            cookies=self.cookies_model,
            headers=self.headers_model,
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

    def getMessages(self, id_conversations_path, responses_path):
        id_conversations_df = pd.read_csv(id_conversations_path)
        response_df = pd.read_csv(responses_path)
        id_conversations_df = id_conversations_df[
            ~id_conversations_df["ID"].isin(response_df["id_conversation"])
        ]
        # id_concersations to list of id_conversations
        ids = id_conversations_df["ID"].tolist()

        for id in tqdm(ids[:2]):
            response = requests.get(
                f"https://www.linkedin.com/voyager/api/voyagerMessagingGraphQL/graphql?queryId=messengerMessages.08934c39ffb80ef0ba3206c05dd01362&variables=(conversationUrn:urn%3Ali%3Amsg_conversation%3A%28urn%3Ali%3Afsd_profile%3AACoAAD7eJgAB86HN-PPLacOIKh5sveuc4KvVpz0%2C{id}%3D%3D%29)",
                cookies=self.cookies_model,
                headers=self.headers_model,
            )
            time.sleep(1)
            if response.status_code == 200:
                messages = []
                for message in response.json()["included"]:
                    if (
                        "reactionSummaries" in message.keys()
                        and message["*sender"].split(":")[-1]
                        != "ACoAAD7eJgAB86HN-PPLacOIKh5sveuc4KvVpz0"
                    ):
                        messages.append(message)
                print("len(messages) = {}".format(len(messages)))
                if len(messages) >= 1:
                    last_response = messages[-1]
                    msg = last_response["body"]["text"]
                    delivered_at_tmsp = last_response["deliveredAt"]
                    delivered_at_date = datetime.fromtimestamp(
                        int(last_response["deliveredAt"]) / 1000
                    ).strftime("%d-%m-%y")
                    id_contact = last_response["*sender"].split(":")[-1]
                    # insert line to conversations file
                    line = [
                        msg,
                        delivered_at_date,
                        delivered_at_tmsp,
                        id_contact,
                        id,
                    ]
                    response_df.loc[len(response_df)] = line
                    # save response_df to csv file
                    response_df.to_csv(
                        responses_path,
                        index=False,
                    )
            else:
                print(response.status_code)
