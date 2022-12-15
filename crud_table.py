import re
import os
import pandas as pd
from datetime import date


def create_new_entry(
    first_name: str,
    last_name: str,
    full_name: str,
    job: str,
    company: str,
    url: str,
    action_id: str,
    df_contact,
    df_action,
):
    contact_id = re.split("/", url)[-1]
    df_contact = add_new_contact(
        contact_id=contact_id,
        last_name=last_name,
        first_name=first_name,
        full_name=full_name,
        url=url,
        company=company,
        job=job,
        df_contact=df_contact,
    )
    df_action = add_new_action(
        action_id=action_id,
        etape=0,
        id_conversation="null",
        contact_id=contact_id,
        etape_finale=0,
        df_action=df_action,
    )

    return df_contact, df_action


def add_new_contact(
    contact_id, last_name, first_name, full_name, url, company, job, df_contact
):

    new_contact = pd.DataFrame(
        [[contact_id, last_name, first_name, full_name, url, company, job]],
        columns=[
            "Id",
            "Last_name",
            "First_name",
            "Full_name",
            "Url",
            "Company",
            "Job",
        ],
    )
    df_contact = pd.concat([df_contact, new_contact])
    return df_contact


def add_new_action(
    action_id: str,
    etape: int,
    id_conversation: str,
    contact_id: str,
    etape_finale: int,
    df_action,
):
    today = date.today()
    # dd-mm-YY
    today = today.strftime("%d-%m-%Y")
    new_action = pd.DataFrame(
        [[action_id, today, etape, id_conversation, contact_id, etape_finale]],
        columns=[
            "Id",
            "Date",
            "Step",
            "Id_conversation",
            "Id_contact",
            "Final_step",
        ],
    )
    df_action = pd.concat([df_action, new_action])
    return df_action


def get_actions_with_max_num(df, step: int):
    df_action = (
        df.groupby(["Id_contact", "Id_conversation"])["Step"].max().reset_index()
    )

    df_action = df_action[df_action.Step == step]
    return df_action


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

    df_action_updated = pd.concat(
        [df_action, df_action_update], verify_integrity=True, ignore_index=True
    )

    return df_action_updated


def get_action_from_contact_invitation_file(file_path_action, df_contact):
    if not os.path.isfile(file_path_action):
        df_action = new_action = pd.DataFrame(
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
            etape=0,
            id_conversation=-1,
            contact_id=contact_id,
            etape_finale=0,
            df_action=df_action,
        )
        if step > 0:
            df_action = update_step01(id_contact=contact_id, df_action=df_action)

    return df_action


if __name__ == "__main__":

    file_path_contact = "contact/2022-11-04_thales_invitations.csv"
    file_path_action = "action/Action.csv"
    file_path_actual_connexion = "database/Connexion_test.csv"

    df_contact = pd.read_csv(file_path_contact)

    df_action = get_action_from_contact_invitation_file(
        file_path_action=file_path_action, df_contact=df_contact
    )
    df_action.to_csv(path_or_buf=file_path_action, index=False)
