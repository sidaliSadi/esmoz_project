import pandas as pd
import logging
import csv
import re

CSV_REQUIERED_FIELD_NAMES = {"Name", "Summary", "job", "Url", "Keyword", "Date"}


def check_csv_field_names(file_path: str, requiered_field_names: dict):
    """
    Check that the columns necessary to use the csv file are present

    Parameters
    ----------
    file_name: str
        name of the csv file
    file_path: str
        path to the folder containing the file
    requiered_field_names: dict
        requiered field names of the tabular data

    Returns
    -------
    bool
        True or False whether it succeeds or fails
    """
    try:
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)

            if not requiered_field_names.issubset(reader.fieldnames):
                logging.error(
                    'CSV file "%s" does not have the required fields' % file_path
                )
                return False
            logging.info('File "%s" contains the required fields' % file_path)

    except Exception as e:
        logging.error(str(e))
        return False

    return True


def process_csv(file_path: str, out_path: str):
    """
    Function used to process a file in csv format. Checks the conformity of the table fields.

    Parameters
    ----------
    file_name: str
        name of the json file

    Returns
    -------
    bool
        True or False whether it succeeds or fails
    """
    if not check_csv_field_names(
        file_path=file_path,
        requiered_field_names=CSV_REQUIERED_FIELD_NAMES,
    ):
        return False
    else:
        df = remove_doublon(file_path)
        df = remove_user(user_name="Utilisateur LinkedIn", df=df)
        df = split_data_name(df=df)
        df = split_data_summary(df=df)
        df = encode_keyword(df=df)
        df.to_csv(out_path, index=False)
        logging.info("Success")
        return True


def remove_doublon(file_path):
    """
    Remove duplicate profiles, leaving the current company if possible

    Parameters
    ----------
    file_name: str
        name of the csv file

    Returns
    -------
    DataFrame
        processing results of the loaded file
    """
    df = pd.read_csv(file_path)
    df = df.sort_values(["Summary"])
    df = df.drop_duplicates(subset=["Url"], keep="first")
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    return df


def remove_user(user_name: str, df):
    """
    Remove lines corresponding to a certain user

    Parameters
    ----------
    user_name: str
        name of the user

    df: DataFrame
        pandas dataframe

    Returns
    -------
    DataFrame
        processing results
    """
    return df[df.Name != user_name]


def split_name(names: str):
    """
    Split first and last name of a given string

    Parameters
    ----------
    names: str
        string to split

    Returns
    -------
    Pandas Series
        series containing first and last name
    """
    names = re.sub("\(.*\)", "", names)
    names = re.sub("[A-Z]\.", "", names)
    first = re.split("\s{0,1}[A-Z][A-Z'\-]*\s|\s{0,1}[A-Z][A-Z'\-]*$", names)
    last = re.split(
        "\s{0,1}[A-Z]{0,1}[^A-Z_\W\d]+\-{0,1}\s{0,1}|\s{0,1}[A-Z]{0,1}[^A-Z_\W\d]+\-{0,1}$",
        names,
    )
    first = list(filter(None, first))
    last = list(filter(None, last))
    first = " ".join(first)
    last = " ".join(last)

    if len(last) < 3 or len(first) < 3:
        first, *last = names.split()
        last = " ".join(last)
    return pd.Series([first, last], index=["first_name", "last_name"])


def split_data_name(df):
    """
    Split the column of names into two new column first_name and last_name, keeping the "name" one

    Parameters
    ----------
    df: DataFrame
        dataframe

    Returns
    -------
    DataFrame
        processing results
    """
    df[["First_name", "Last_name"]] = df["Name"].apply(split_name)
    first_name = df.pop("First_name")
    last_name = df.pop("Last_name")
    df.insert(0, "Last_name", last_name)
    df.insert(0, "First_name", first_name)
    return df


def split_company_job(text: str):
    """
    Split company and job name of a given string on the keyword "chez" when there is "Entreprise actuelle" in the line

    Parameters
    ----------
    names: str
        string to split

    Returns
    -------
    Pandas Series
        series containing first and last name
    """
    if not isinstance(text, str):
        return pd.Series(["NaN", "NaN"], index=["job", "company"])
    if "Entreprise actuelle" in text:
        text = re.split("Entreprise actuelle.{2}:\s", text)
        text = text[-1]
        if not "chez" in text:
            return pd.Series([text, "NaN"], index=["job", "company"])
    else:
        return pd.Series(["NaN", "NaN"], index=["job", "company"])
    job, *company = re.split("chez", text)

    if type(company) == list:
        company = company[-1]

    if "- " in company:
        company = re.split("-\s.*", company)
        company = company[0]

    company = re.sub("^\s{0,1}", "", company)

    return pd.Series([job, company], index=["job", "company"])


def split_data_summary(df):
    """
    Split the column of summary into two new column company and current_job, keeping the "summary" one

    Parameters
    ----------
    df: DataFrame
        dataframe

    Returns
    -------
    DataFrame
        processing results
    """
    df[["Current_job", "Company"]] = df["Summary"].apply(split_company_job)
    company = df.pop("Company")
    current_job = df.pop("Current_job")
    df.insert(3, "Company", company)
    df.insert(3, "Current_job", current_job)
    return df


def encode_space(text: str):
    """
    change %20 in a string to " "

    Parameters
    ----------
    text: str
        texte to change

    Returns
    -------
    str
        new string
    """
    return text.replace("%20", " ")


def encode_keyword(df):
    """
    Change the values of the keyword column. Turns the "%20" into " "

    Parameters
    ----------
    df: DataFrame
        source dataframe

    Returns
    -------
    DataFrame
        processed dataframe
    """
    df["Keyword"] = df["Keyword"].apply(encode_space)
    return df


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    file_path = "./2022-11-04.csv"
    out_path = file_path.replace(".csv", "_processed.csv")
    process_csv(file_path=file_path, out_path=out_path)
