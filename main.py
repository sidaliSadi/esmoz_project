from linkedinAPI import LinkedinAPI
from dotenv import load_dotenv
import os
from src.process_step import *

COOKIES_PATH = "credentials/cookies.json"
HEADERS_PATH = "credentials/headers.json"
INVITATION_FILE = "./contact/2022-11-04_thales_invitations.csv"
CONVERSATIONS_ID = "conversations/conversations_id.csv"
RESPONSES = "conversations/responses.csv"
PATH_FILE_CONTACT = "./contact/Contacts.csv"
PATH_FILE_ACTION = "./action/Action.csv"

lAPI = LinkedinAPI(COOKIES_PATH, HEADERS_PATH)
load_dotenv()
password = os.getenv("PASSWORD")
email = os.getenv("EMAIL")


while not lAPI.login(email, password):
    time.sleep(5)
    print("Login failed trying again")
    lAPI.login(email, password)
print("Logged in ................")
print("- * 50")
print("Sending connection request and update action table ...")
process_step_1(
    lAPI, path_file_contact=PATH_FILE_CONTACT, path_file_action=PATH_FILE_ACTION
)
print("Get relations and update action table ...")
process_step_2(lAPI, PATH_FILE_ACTION)
