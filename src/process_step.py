from linkedinAPI import *
import linkedinSelenium
from src.crud_action import Action


def process_step_0(
    linkedinapi: LinkedinAPI,
    keywords: list,
    path_file_contact: str,
    path_file_action: str,
    columns: list,
):
    totalData = linkedinapi.getProfiles(keywords=keywords)
    linkedinapi.saveResults(
        totalData=totalData,
        cols=columns,
        out_file_contact=path_file_contact,
        out_file_action=path_file_action,
    )


def process_step_1(
    linkedinapi: LinkedinAPI,
    path_file_contact: str,
    path_file_action: str,
    new_connexion_number=20,
):
    linkedinapi.sendConnection(
        action_file=path_file_action,
        contact_file=path_file_contact,
        random=new_connexion_number,
    )


def process_step_2(linkedinapi: LinkedinAPI, path_file_action):
    df_connexion = linkedinapi.getConnections()
    df_action = pd.read_csv(path_file_action)

    df_action = Action.update_step(
        df_action=df_action,
        actual_step=1,
        df_connexion=df_connexion,
    )
    df_action.to_csv(path_file_action)


def process_final_step(
    linkedinapi: LinkedinAPI,
    path_file_contact,
    path_file_action,
    id_conversations_path,
    responses_path,
    email,
    password,
):

    df_action = pd.read_csv(path_file_action)
    df_contact = pd.read_csv(path_file_contact)

    lSelenium = linkedinSelenium.LinkedinSelenium(
        email,
        password,
        id_conversations_path,
    )
    lSelenium.getMessagesIds()

    df_final_step = linkedinapi.getMessages(
        id_conversations_path=id_conversations_path, responses_path=responses_path
    )
    df_action = Action.update_final_step(
        df_final_step=df_final_step, df_action=df_action
    )

    df_action.to_csv(path_file_action)
