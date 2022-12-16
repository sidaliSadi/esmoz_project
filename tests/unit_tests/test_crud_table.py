import pandas as pd
import sys, os
from unittest.mock import MagicMock
from data_samples import *
from pandas.testing import assert_frame_equal

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(os.path.dirname(current))
sys.path.append(parent)
sys.path.append(parent + "/src")

from src.crud_table import add_new_contact, add_new_action
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


def test_add_new_action():
    df_action = pd.DataFrame(data=list_action, columns=Action.columns)

    new_list_action = list_action + [new_action.to_list()]
    expected_df_action = pd.DataFrame(new_list_action, columns=Action.columns)

    output_df_action = add_new_action(
        action_id=new_action.action_id,
        step=new_action.step,
        id_conversation=new_action.conversation_id,
        contact_id=new_action.contact_id,
        final_step=new_action.final_step,
        df_action=df_action,
        action_date=new_action.action_date,
    )

    assert_frame_equal(
        expected_df_action.reset_index(drop=True),
        output_df_action.reset_index(drop=True),
    )
