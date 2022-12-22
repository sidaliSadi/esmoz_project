import pandas as pd
import sys, os
from data_samples import *
from pandas.testing import assert_frame_equal

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(os.path.dirname(current))
sys.path.append(parent)
sys.path.append(parent + "/src")

from src.crud_contact import Contact


def test_add_contact_to_dataframe():

    df_contact = pd.DataFrame(data=list_contact, columns=Contact.columns)

    new_list_contact = list_contact + [new_contact.to_list()]
    expected_df_contact = pd.DataFrame(new_list_contact, columns=Contact.columns)

    output_df_contact = new_contact.add_contact_to_dataframe(df_contact=df_contact)

    assert_frame_equal(
        expected_df_contact.reset_index(drop=True),
        output_df_contact.reset_index(drop=True),
    )
