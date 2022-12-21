import os, sys
from datetime import datetime

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(os.path.dirname(current))
sys.path.append(parent)
sys.path.append(parent + "/src")

from src.crud_contact import Contact
from src.crud_action import Action

list_contact = [
    [
        "contact_id_1",
        "Last_Name_1",
        "First_Name_1",
        "First_Name_1 Last_Name_1",
        "Keyword_1",
        "https://url_1/contact_id_1",
        "Company_1",
        "This is job number 1",
        0,
    ],
    [
        "contact_id_2",
        "Last_Name_2",
        "First_Name_2",
        "First_Name_2 Last_Name_2",
        "Keyword_2",
        "https://url_2/contact_id_2",
        "Company_2",
        "This is job number 2",
        0,
    ],
    [
        "contact_id_3",
        "Last_Name_3",
        "First_Name_3",
        "First_Name_3 Last_Name_3",
        "Keyword_3",
        "https://url_3/contact_id_3",
        "Company_3",
        "This is job number 3",
        0,
    ],
    [
        "contact_id_4",
        "Last_Name_4",
        "First_Name_4",
        "First_Name_4 Last_Name_4",
        "Keyword_4",
        "https://url_4/contact_id_4",
        "Company_4",
        "This is job number 4",
        0,
    ],
]

new_contact = Contact(
    "contact_id_New",
    "Last_Name_New",
    "First_Name_New",
    "First_Name_New Last_Name_New",
    "Keyword_New",
    "https://url_New/contact_id_New",
    "Company_New",
    "This is job number New",
    0,
)

list_action = [
    [
        "action_id_1",
        datetime.fromtimestamp(1671926400),
        0,
        "conversation_id_1",
        "contact_id_1",
        0,
    ],
    [
        "action_id_2",
        datetime.fromtimestamp(2672926400),
        0,
        "conversation_id_2",
        "contact_id_2",
        0,
    ],
    [
        "action_id_3",
        datetime.fromtimestamp(3673936400),
        0,
        "conversation_id_3",
        "contact_id_3",
        0,
    ],
    [
        "action_id_4",
        datetime.fromtimestamp(4674926400),
        0,
        "conversation_id_4",
        "contact_id_4",
        0,
    ],
]


new_action = Action(
    "action_id_new",
    datetime.fromtimestamp(8678926400),
    0,
    "conversation_id_new",
    "contact_id_new",
    0,
)

list_connexion = [
    "https://www.linkedin.com/in/contact_id_1",
    "https://www.linkedin.com/in/contact_id_4",
]

columns_messages = [
    "Msg",
    "Delivered_at_date",
    "Delivered_at_tmsp",
    "Id_contact",
    "Id_conversation",
]
list_messages = [
    [
        "Bonjour Contact_1, je serais ravi d'échanger avec vous !",
        datetime.fromtimestamp(6671926400),
        1671926400,
        "contact_id_1",
        "conversation_id_1",
    ],
    [
        "Bonjour Contact_2, je serais ravi d'échanger avec vous !",
        datetime.fromtimestamp(7671926400),
        1671226400,
        "contact_id_2",
        "conversation_id_2",
    ],
]
