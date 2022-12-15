import re
import os
import pandas as pd
from datetime import date
from process_csv import get_id_from_url


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
        step=0,
        id_conversation="null",
        contact_id=contact_id,
        final_step=0,
        df_action=df_action,
    )

    return df_contact, df_action


def add_new_contact(
    contact_id,
    last_name,
    first_name,
    full_name,
    keyword,
    url,
    company,
    job,
    df_contact,
    sent_mail=0,
):

    new_contact = pd.DataFrame(
        [
            [
                contact_id,
                last_name,
                first_name,
                full_name,
                keyword,
                url,
                company,
                job,
                sent_mail,
            ]
        ],
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
        ],
    )
    df_contact = pd.concat([df_contact, new_contact])
    return df_contact


def add_new_action(
    action_id: str,
    step: int,
    id_conversation: str,
    contact_id: str,
    final_step: int,
    df_action,
):
    today = date.today()
    # dd-mm-YY
    today = today.strftime("%d-%m-%Y")
    new_action = pd.DataFrame(
        [[action_id, today, step, id_conversation, contact_id, final_step]],
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


def get_actions_with_max_num(df_action, step: int, greater_than=False):
    df_action = (
        df_action.groupby(
            ["Id", "Date", "Id_conversation", "Id_contact", "Final_step"]
        )["Step"]
        .max()
        .reset_index()
    )

    if not greater_than:
        df_action = df_action[df_action.Step == step]
    else:
        df_action = df_action[df_action.Step >= step]

    return df_action


def update_step(
    date,
    df_action,
    id_contact=-1,
    actual_step=-1,
    id_conversation=-1,
    final_step=0,
    df_connexion=None,
):
    new_step = actual_step + 1
    action_id = id_contact + "_" + str(new_step)

    if new_step == 0:
        return add_new_action(
            action_id=action_id,
            step=new_step,
            id_conversation=id_conversation,
            contact_id=id_contact,
            final_step=final_step,
            df_action=df_action,
        )
    elif new_step == 1:
        return add_new_action(
            action_id=action_id,
            step=new_step,
            id_conversation=id_conversation,
            contact_id=id_contact,
            final_step=final_step,
            df_action=df_action,
        )

    elif new_step == 2:
        if df_connexion is None:
            print("error")
            return df_action

        df_action_update = get_actions_with_max_num(df_action, 1)
        list_connexion = df_connexion["Url"].apply(get_id_from_url)
        list_connexion = list_connexion["Id"].to_list()

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
    else:
        return None


def update_final_step(df_final_step, df_action, df_contact):
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

    df_update_action = df_update_action[
        df_update_action["Id_contact"].isin(df_final_step["Id_contact"])
    ]

    df_update_action["Final_step"] = df_update_action["Final_step"].replace(0, 1)
    df_update_action["Date"] = df_final_step["Date"]

    df_action = df_action[~df_action["Id"].isin(df_update_action["Id"])]
    df_action = pd.concat([df_action, df_update_action])
    return df_action


if __name__ == "__main__":
    # df_final_step = pd.read_csv("test_database/final_step.csv")
    # df_action_test = pd.read_csv("test_database/action_test.csv")

    # print(update_final_step(df_final_step=df_final_step, df_action=df_action_test))

    df1 = pd.DataFrame(
        data=[["thomas", "lépine"], ["charles", "Henri"]], columns=["prenom", "nom"]
    )
    df2 = pd.DataFrame(data=[["charles", "Henri"]], columns=["prenom", "nom"])
    print(df2)
    print(df1[df1["prenom"].isin(df2["prenom"])])
