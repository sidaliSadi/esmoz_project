import pandas as pd
import sys, os
from unittest.mock import MagicMock
from data_samples import *
from pandas.testing import assert_frame_equal

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(os.path.dirname(current))
sys.path.append(parent)
sys.path.append(parent + "/src")

from src.crud_table import (
    add_new_contact,
    add_new_action,
    get_actions_with_max_num,
    update_step,
)
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


def test_get_actions_with_max_num():
    df_action = pd.DataFrame(data=list_action, columns=Action.columns)
    action_2_step_3 = Action(
        "action_id_2",
        datetime.fromtimestamp(8678926400),
        3,
        "conversation_id_2",
        "contact_id_2",
        0,
    )
    df_action = add_new_action(
        action_id=action_2_step_3.action_id,
        step=action_2_step_3.step,
        id_conversation=action_2_step_3.conversation_id,
        contact_id=action_2_step_3.contact_id,
        final_step=action_2_step_3.final_step,
        df_action=df_action,
        action_date=action_2_step_3.action_date,
    )

    result = get_actions_with_max_num(df_action=df_action, step=3)
    expected_output = pd.DataFrame(
        data=[action_2_step_3.to_list()], columns=Action.columns
    )

    assert_frame_equal(
        expected_output.reset_index(drop=True)[Action.columns],
        result.reset_index(drop=True)[Action.columns],
    )


def test_update_step():
    # for step = 1 & 2
    df_action = pd.DataFrame(data=list_action, columns=Action.columns)
    expected_output = add_new_action(
        action_id="contact_id_1_1",
        step=1,
        action_date=datetime.fromtimestamp(1671926400),
        id_conversation="conversation_id_1",
        contact_id="contact_id_1",
        final_step=0,
        df_action=df_action,
    )
    result = update_step(
        date=datetime.fromtimestamp(1671926400),
        df_action=df_action,
        id_contact="contact_id_1",
        actual_step=0,
        id_conversation="conversation_id_1",
    )

    assert_frame_equal(
        expected_output.reset_index(drop=True)[Action.columns],
        result.reset_index(drop=True)[Action.columns],
    )

    # for step = 2
