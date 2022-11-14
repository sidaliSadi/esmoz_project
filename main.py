from scrapProfiles import saveResults, getProfiles, loadCredentials, preparQueries
from send_connections import sendConnection

queries = [
    "head of data",
    "responsable data",
    "responsable analytics",
    "program manager data",
    "responsable infra",
    "responsable devops",
    "head of mlops",
    "datalab",
    "datafactory",
]
COOKIES_PATH = "credentials/cookies.json"
HEADERS_PATH = "credentials/headers.json"

cookies, headers = loadCredentials(COOKIES_PATH, HEADERS_PATH)
# keywords = preparQueries(queries)
# print(keywords)
# data = getProfiles(keywords, cookies, headers)
# saveResults(data, ["Name", "Summary", "job", "Url", "Keyword", "Date"])

sendConnection(
    "/home/sadi/Bureau/esmoz_linkedin/esmoz_project/data/2022-11-04_processed_updated.csv",
    "/home/sadi/Bureau/esmoz_linkedin/esmoz_project/data/2022-11-04_processed_updated.csv",
    cookies,
    headers,
)
