from linkedinAPI import LinkedinAPI
from linkedinSelenium import LinkedinSelenium

# queries = [
#     "head of data",
#     "responsable data",
#     "responsable analytics",
#     "program manager data",
#     "responsable infra",
#     "responsable devops",
#     "head of mlops",
#     "datalab",
#     "datafactory",
# ]
COOKIES_PATH = "credentials/cookies.json"
HEADERS_PATH = "credentials/headers.json"
INVITATION_FILE = "./processed_data/2022-11-04_thales_invitations.csv"

lAPI = LinkedinAPI(COOKIES_PATH, HEADERS_PATH)
lAPI.sendConnection(invitation_file=INVITATION_FILE)
# keywords = preparQueries(queries)
# print(keywords)
# data = getProfiles(keywords, cookies, headers)
# saveResults(data, ["Name", "Summary", "job", "Url", "Keyword", "Date"], 'thales.csv')
# logging.basicConfig(level=logging.DEBUG)

# file_path = "./source_data/2022-11-04_thales.csv"
# out_path = "./processed_data/2022-11-04_thales.csv"
# process_csv(file_path=file_path, out_path=out_path)


# lSelenium = LinkedinSelenium(
#     "matthieu@esmoz.fr",
#     "Esmoz2022?",
#     "./browser/",
#     "conversations/conversations_id.csv",
# )
# lSelenium.getMessagesIds()
