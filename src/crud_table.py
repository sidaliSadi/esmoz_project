import pandas as pd
from datetime import date, datetime
from .process_csv import get_id_from_url


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
    action_date=None,
):
    if action_date is None:
        today = date.today()
        # dd-mm-YY
        action_date = today.strftime("%d-%m-%Y")

    new_action = pd.DataFrame(
        [[action_id, action_date, step, id_conversation, contact_id, final_step]],
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
    df_action,
    date=-1,
    id_contact=-1,
    actual_step=-1,
    id_conversation=-1,
    final_step=0,
    df_connexion=None,
):
    new_step = actual_step + 1
    action_id = str(id_contact) + "_" + str(new_step)

    if id_contact == -1:
        print("missing contact id in update step")
        exit(1)

    if new_step == 0:
        if date == -1:
            print("error, invalid date")

        return add_new_action(
            action_id=action_id,
            step=new_step,
            id_conversation=id_conversation,
            contact_id=id_contact,
            final_step=final_step,
            action_date=date,
            df_action=df_action,
        )
    elif new_step == 1:
        if date == -1:
            print("error, invalid date")

        return add_new_action(
            action_id=action_id,
            step=new_step,
            id_conversation=id_conversation,
            contact_id=id_contact,
            final_step=final_step,
            action_date=date,
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
        df_action_update["Id"] = df_action_update["Id_contact"].apply(
            lambda x: x + "_2"
        )
        if date == -1:
            date = date.today()

        (df_action_update["Final_step"], df_action_update["Date"]) = (0, date)

        df_action_updated = pd.concat(
            [df_action, df_action_update], verify_integrity=True, ignore_index=True
        )

        return df_action_updated
    else:
        return None


def update_final_step(df_final_step, df_action):
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
    df_update_action["Date"] = df_final_step["Delivered_at_date"]

    df_action = df_action[~df_action["Id"].isin(df_update_action["Id"])]
    df_action = pd.concat([df_action, df_update_action])
    return df_action


class Action:
    def __init__(
        self,
        action_id: str,
        action_date: datetime.date,
        step: int,
        conversation_id: str,
        contact_id: str,
        final_step: int,
    ):
        self.action_id = action_id
        self.action_date = action_date
        self.step = step
        self.conversation_id = conversation_id
        self.contact_id = contact_id
        self.final_step = final_step

    columns = [
        "Id",
        "Date",
        "Step",
        "Id_conversation",
        "Id_contact",
        "Final_step",
    ]

    def to_list(self):
        return [
            self.action_id,
            self.action_date,
            self.step,
            self.conversation_id,
            self.contact_id,
            self.final_step,
        ]

    def from_list(self, source_list):
        self.action_id = source_list[0]
        self.action_date = source_list[1]
        self.step = source_list[2]
        self.conversation_id = source_list[3]
        self.contact_id = source_list[4]
        self.final_step = source_list[5]


class Contact:
    def __init__(
        self,
        contact_id: str,
        last_name: str,
        first_name: str,
        full_name: str,
        keyword: str,
        url: str,
        company: str,
        job: str,
        sent_mail: int,
    ):
        self.last_name = last_name
        self.contact_id = contact_id
        self.first_name = first_name
        self.full_name = full_name
        self.keyword = keyword
        self.url = url
        self.company = company
        self.job = job
        self.sent_mail = sent_mail

    columns = [
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

    def to_list(self):
        return [
            self.last_name,
            self.contact_id,
            self.first_name,
            self.full_name,
            self.keyword,
            self.url,
            self.company,
            self.job,
            self.sent_mail,
        ]

    def from_list(self, source_list):
        self.last_name = source_list[0]
        self.contact_id = source_list[1]
        self.first_name = source_list[2]
        self.full_name = source_list[3]
        self.keyword = source_list[4]
        self.url = source_list[5]
        self.company = source_list[6]
        self.job = source_list[7]
        self.sent_mail = source_list[8]
