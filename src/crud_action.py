import pandas as pd
from datetime import date, datetime
from src.utils import get_id_from_url


class Action:
    def __init__(
        self,
        action_id=-1,
        action_date=-1,
        step=-1,
        conversation_id=-1,
        contact_id=-1,
        final_step=0,
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

    def set_action(
        self,
        contact_id: str,
        action_id=-1,
        action_date=-1,
        step=-1,
        conversation_id=-1,
        final_step=0,
    ):
        self.action_id = action_id
        self.action_date = action_date
        self.step = step
        self.conversation_id = conversation_id
        self.contact_id = contact_id
        self.final_step = final_step

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

    def add_new_action(self, df_action):

        if self.action_date is None:
            self.action_date = int(datetime.today().timestamp())

        new_action = pd.DataFrame(
            [
                [
                    self.action_id,
                    self.action_date,
                    self.step,
                    self.conversation_id,
                    self.contact_id,
                    self.final_step,
                ]
            ],
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
        df_action_cut = df_action.groupby(["Id_contact"])["Step"].max().reset_index()

        if not greater_than:
            df_action_cut = df_action_cut[df_action_cut.Step == step]
        else:
            df_action_cut = df_action_cut[df_action_cut.Step >= step]

        new_df_action = df_action[
            df_action["Id_contact"].isin(df_action_cut["Id_contact"])
        ]

        if not greater_than:
            new_df_action = new_df_action[new_df_action.Step == step]
        else:
            new_df_action = new_df_action[new_df_action.Step >= step]

        return new_df_action

    def update_step(
        self,
        df_action,
        actual_step: int,
        df_connexion=None,
    ):
        new_step = actual_step + 1

        if new_step == 1 or new_step == 0:
            action_id = str(self.contact_id) + "_" + str(new_step)
            if self.contact_id == -1:
                print("missing contact id in update step")
                exit(1)
            if self is None:
                print("Action not set")
                exit(1)

            if self.action_date == -1:
                print("error, invalid date")

            self.action_id = action_id
            self.step = new_step
            return self.add_new_action(df_action=df_action)

        elif new_step == 2:
            if df_connexion is None:
                print("error: df of connexion not given")
                return df_action

            df_action_update = Action.get_actions_with_max_num(df_action, 1)

            list_connexion = df_connexion["Url"].apply(get_id_from_url)
            list_connexion = list_connexion["Id"].to_list()

            df_action_update = df_action_update[
                df_action_update["Id_contact"].isin(list_connexion)
            ]
            df_action_update["Step"] = df_action_update["Step"].replace(1, 2)
            df_action_update["Id"] = df_action_update["Id_contact"].apply(
                lambda x: x + "_2"
            )

            (df_action_update["Final_step"], df_action_update["Date"]) = (
                0,
                int(datetime.today().timestamp()),
            )

            df_action_updated = pd.concat(
                [df_action, df_action_update], verify_integrity=True, ignore_index=True
            )

            return df_action_updated
        else:
            return None

    def update_final_step(df_final_step, df_action):
        df_update_action = Action.get_actions_with_max_num(
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
        df_update_action["Date"] = df_final_step["Delivered_at_tmsp"]

        df_action = df_action[~df_action["Id"].isin(df_update_action["Id"])]
        df_action = pd.concat([df_action, df_update_action])
        return df_action
