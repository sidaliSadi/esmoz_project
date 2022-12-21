import re
import os
import pandas as pd
from datetime import date
from utils import get_id_from_url
from crud_table import *


def update_step01(id_contact: str, df_action):
    today = date.today()
    entry = [today, 1, 0, -1, id_contact, id_contact + "_" + str(1)]
    df_action = pd.concat(
        [
            df_action,
            pd.DataFrame(
                [entry],
                columns=[
                    "Date",
                    "Step",
                    "Final_step",
                    "Id_conversation",
                    "Id_contact",
                    "Id",
                ],
            ),
        ],
    )

    return df_action


def update_step12(df_action, list_connexion: list):
    df_action_update = get_actions_with_max_num(df_action, 1)

    df_action_update = df_action_update[
        df_action_update["Id_contact"].isin(list_connexion)
    ]
    df_action_update["Step"] = df_action_update["Step"].replace(1, 2)

    today = date.today()
    (df_action_update["Final_step"], df_action_update["Date"]) = (0, today)
    df_action_update["Id"] = df_action_update["Id_contact"].apply(lambda x: x + "_2")

    df_action_updated = pd.concat(
        [df_action, df_action_update], verify_integrity=True, ignore_index=True
    )

    return df_action_updated


def update_final(df_action, df_responses):
    df_update_action = get_actions_with_max_num(
        df_action=df_action, step=2, greater_than=True
    )
    df_update_action = (
        df_update_action.groupby(
            ["Id", "Date", "Step", "Id_conversation", "Id_contact"]
        )["Final_step"]
        .max()
        .reset_index()
    )
    df_update_action = df_update_action[df_update_action.Final_step == 0]
    df_update_action = df_update_action[
        df_update_action["Id_contact"].isin(df_responses["id_contact"])
    ]

    df_update_action["Final_step"] = df_update_action["Final_step"].replace(0, 1)

    df_update_action = pd.merge(
        df_update_action,
        df_responses,
        left_on="Id_contact",
        right_on="id_contact",
        how="left",
    ).drop(
        [
            "msg",
            "Date",
            "delivered_at_tmsp",
            "id_contact",
            "id_conversation",
        ],
        axis=1,
    )
    df_update_action = df_update_action.rename(columns={"delivered_at_date": "Date"})

    df_action = df_action[~df_action["Id"].isin(df_update_action["Id"])]
    df_action = pd.concat([df_action, df_update_action])

    return df_action


def get_action_from_contact_invitation_file(file_path_action, df_contact):
    if not os.path.isfile(file_path_action):
        df_action = pd.DataFrame(
            columns=[
                "Id",
                "Date",
                "Step",
                "Id_conversation",
                "Id_contact",
                "Final_step",
            ]
        )
    else:
        df_action = pd.read_csv(file_path_action)

    for row in df_contact.iterrows():
        url = row[1]["Url"]
        contact_id = re.split("/", url)[-1]
        step = row[1]["invitation"]
        action_id = contact_id + "_" + str(0)
        df_action = add_new_action(
            action_id=action_id,
            step=0,
            id_conversation=-1,
            contact_id=contact_id,
            final_step=0,
            df_action=df_action,
        )
        if step > 0:
            df_action = update_step01(id_contact=contact_id, df_action=df_action)

    return df_action


def get_contact_from_contact_invitation_file(file_path_contact, df_contact_invitation):
    if not os.path.isfile(file_path_contact):
        df_contact = pd.DataFrame(
            columns=[
                "Id",
                "Last_name",
                "First_name",
                "Full_name",
                "Keyword",
                "Url",
                "Company",
                "Job",
                "Sent_mail",
            ]
        )
    else:
        df_contact = pd.read_csv(file_path_contact)

    for row in df_contact_invitation.iterrows():
        Url = row[1]["Url"]
        Contact_id = re.split("/", Url)[-1]
        First_name = row[1]["First_name"]
        Last_name = row[1]["Last_name"]
        Company = row[1]["Company"]
        Keyword = row[1]["Keyword"]
        Job = row[1]["job"]
        Name = row[1]["Name"]

        df_contact = add_new_contact(
            contact_id=Contact_id,
            url=Url,
            last_name=Last_name,
            first_name=First_name,
            company=Company,
            keyword=Keyword,
            job=Job,
            full_name=Name,
            df_contact=df_contact,
        )

    df_contact.to_csv(file_path_contact, index=False)


if __name__ == "__main__":

    file_path_contact_invit = "contact/2022-11-04_thales_invitations.csv"
    file_path_contact = "contact/Contacts.csv"
    file_path_responses = "conversations/responses.csv"
    file_path_action = "action/Action.csv"
    file_path_actual_connexion = "database/Connexion_test.csv"

    df_contact_invitation = pd.read_csv(file_path_contact_invit)
    df_contact = get_contact_from_contact_invitation_file(
        file_path_contact=file_path_contact, df_contact_invitation=df_contact_invitation
    )

    df_responses = pd.read_csv(filepath_or_buffer=file_path_responses)
    df_action = get_action_from_contact_invitation_file(
        df_contact=df_contact_invitation, file_path_action=file_path_action
    )
    df_relation = pd.read_csv("relations/matthieu_relations.csv")
    list_connexion = df_relation["Url_relation"].apply(get_id_from_url)
    list_connexion = list_connexion["Id"].to_list()

    df_action = update_step12(df_action=df_action, list_connexion=list_connexion)
    df_action = update_final(df_action=df_action, df_responses=df_responses)
    df_action.to_csv(file_path_action, index=False)
