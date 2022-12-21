import pandas as pd
from datetime import date, datetime
from process_csv import get_id_from_url


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

    def add_contact_to_dataframe(self, df_contact):

        new_contact = pd.DataFrame(
            [self.to_list()],
            columns=self.columns,
        )

        df_contact = pd.concat([df_contact, new_contact])
        return df_contact
