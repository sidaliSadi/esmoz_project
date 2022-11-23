import pandas as pd
import re


def get_id(url: str):
    split_url = re.split("/", url)
    id = split_url[-1]
    return pd.Series([id], index=["id"])


if __name__ == "__main__":

    file_path = "2022-11-04_thales_invitations.csv"
    df = pd.read_csv(file_path)
    print(df.head())
    ids = df["Url"].apply(get_id)
    df_contact = df[["First_name", "Last_name", "Name", "job", "Url", "Company"]]
    df_contact["id"] = ids
    df_contact = df_contact.rename(
        columns={
            "First_name": "first_name",
            "Last_name": "last_name",
            "Date": "date",
            "Url": "url",
            "Company": "company",
            "Name": "full_name",
        }
    )
    df_action = df[["Date", "invitation"]]
    df_action["id_contact"] = ids
    df_action = df_action.rename(columns={"invitation": "etape", "Date": "date"})
    df_action[["id_conversation", "id", "etape_finale"]] = [-1, -1, 0]

    df_contact = df_contact.reindex(
        columns=["id", "last_name", "first_name", "full_name", "job", "company", "url"]
    )
    df_action = df_action.reindex(
        columns=["id", "date", "etape", "id_conversation", "id_contact", "etape_finale"]
    )
    print(df_action.head())
    # df_contact = df.First_name.to_frame()
    # df_contact["Last_name"] = df.Last_name
    print(df_contact.head())
    # process_csv(file_path=file_path)

    df_contact.to_csv("Contact.csv", index=False)
    df_action.to_csv("Action.csv", index=False)
