import pandas as pd
import sys, os
from data_samples import *
from pandas.testing import assert_frame_equal
from unittest.mock import MagicMock

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(os.path.dirname(current))
sys.path.append(parent)
sys.path.append(parent + "/src")

from src.crud_contact import Contact
from src.crud_action import Action

from src.crud_table import *


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

    output_df_action = new_action.add_new_action(df_action=df_action)

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
    df_action = action_2_step_3.add_new_action(df_action=df_action)

    result = Action.get_actions_with_max_num(df_action=df_action, step=3)
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
    action_to_add = Action(
        action_id="contact_id_1_1",
        step=1,
        action_date=datetime.fromtimestamp(1671926400),
        conversation_id="conversation_id_1",
        contact_id="contact_id_1",
        final_step=0,
    )

    expected_output = action_to_add.add_new_action(df_action=df_action)

    action_to_add.set_action(
        action_id="contact_id_1_0",
        step=0,
        action_date=datetime.fromtimestamp(1671926400),
        conversation_id="conversation_id_1",
        contact_id="contact_id_1",
        final_step=0,
    )

    result = action_to_add.update_step(df_action=df_action, actual_step=0)

    assert_frame_equal(
        expected_output.reset_index(drop=True)[Action.columns].drop(columns=["Date"]),
        result.reset_index(drop=True)[Action.columns].drop(columns=["Date"]),
    )

    # for step = 2
    action_to_add.set_action(
        action_id="contact_id_1_2",
        step=2,
        action_date=datetime.fromtimestamp(6671926400),
        conversation_id="conversation_id_1",
        contact_id="contact_id_1",
        final_step=0,
    )

    expected_output = action_to_add.add_new_action(df_action=result)

    df_connexion = pd.DataFrame(data=list_connexion, columns=["Url"])

    result = Action.update_step(
        self=None,
        actual_step=1,
        df_action=result,
        df_connexion=df_connexion,
    )

    assert_frame_equal(
        expected_output.reset_index(drop=True)[Action.columns].drop(columns=["Date"]),
        result.reset_index(drop=True)[Action.columns].drop(columns=["Date"]),
    )


def test_update_final_step():
    df_action = pd.DataFrame(data=list_action, columns=Action.columns)
    df_final_step = pd.DataFrame(data=list_messages, columns=columns_messages)

    action_to_add = Action(
        action_id="contact_id_1_1",
        step=1,
        action_date=datetime.fromtimestamp(1671926400),
        conversation_id="conversation_id_1",
        contact_id="contact_id_1",
        final_step=0,
    )

    df_action = action_to_add.add_new_action(df_action=df_action)

    action_to_add.set_action(
        action_id="contact_id_1_2",
        step=2,
        action_date=datetime.fromtimestamp(6671926400),
        conversation_id="conversation_id_1",
        contact_id="contact_id_1",
        final_step=1,
    )

    expected_output = action_to_add.add_new_action(df_action=df_action)

    action_to_add.set_action(
        action_id="contact_id_1_2",
        step=2,
        action_date=datetime.fromtimestamp(1671926400),
        conversation_id="conversation_id_1",
        contact_id="contact_id_1",
        final_step=0,
    )

    df_action = action_to_add.add_new_action(df_action=df_action)

    result = Action.update_final_step(df_final_step=df_final_step, df_action=df_action)

    assert_frame_equal(
        expected_output.reset_index(drop=True)[Action.columns],
        result.reset_index(drop=True)[Action.columns],
    )
