from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from googleapiclient.http import MediaFileUpload

from googleapiclient.errors import HttpError


def write_to_drive(name, parents, path):
    # If modifying these scopes, delete the file token.json.
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)
        # get file of the dir  (parenets)
        children = service.files().list(q="'" + parents + "' in parents").execute()
        # delete old files
        for file in children["files"]:
            service.files().delete(fileId=file["id"]).execute()

        # Upload new files
        file_metadata = {
            "name": f"{name}",
            "mimeType": "application/vnd.google-apps.spreadsheet",
            "parents": [f"{parents}"],
        }
        media = MediaFileUpload(f"{path}", mimetype="text/csv", resumable=True)
        # pylint: disable=maybe-no-member
        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        print(f'File with ID: "{file.get("id")}" has been uploaded.')
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    write_to_drive(
        "Action.csv", "1zM0dodjPCe9xCMOPJh2wi_XaKAzNl9-y", "action/Action.csv"
    )
    write_to_drive(
        "Contact.csv", "1-ZIf4z0n0KqbaDhdPaff4O_lv8AX9OTu", "contact/Contacts.csv"
    )
    write_to_drive(
        "Responses.csv",
        "1UkdJ4ZMYzQD8-nKTHszz-mXY1eco0apW",
        "conversations/responses.csv",
    )
