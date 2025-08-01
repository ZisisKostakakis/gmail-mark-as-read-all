import ast
import imaplib
import logging
import re
from typing import Sequence
import os
import boto3
import boto3.session
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()
dont_touch_list = [
    "Bitbucket",
    "Gitlab",
    "Jira",
    "INBOX",
    "[Gmail]",
    "Traceback Errors",
]


def get_secret() -> str:
    secret_name = os.getenv("SECRET_NAME")
    region_name = os.getenv("AWS_REGION")

    sts_client = boto3.client("sts")

    response = sts_client.assume_role(
        RoleArn=os.getenv("ROLE_ARN"), RoleSessionName=os.getenv("SESSION_NAME")
    )

    credentials = response["Credentials"]
    session = boto3.session.Session(
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
    )
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e

    return get_secret_value_response["SecretString"]


def connect_to_gmail_imap(secret: dict) -> imaplib.IMAP4_SSL:
    user, password = secret["user"], secret["password"]
    imap_url = "imap.gmail.com"
    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(user, password)
        mail.select("inbox")
        return mail
    except Exception as e:
        logging.error("Connection failed: {}".format(e))
        raise


def get_unread_label_message_ids(mail: imaplib.IMAP4_SSL, label: str) -> list[int]:
    try:
        status, messages = mail.select(f'"{label}"')
        if status != "OK":
            logging.error(f"Failed to select label {label}: {messages}")
            return []

        status, messages = mail.search(None, "UNSEEN")
        if status == "OK":
            message_ids = [int(msg) for msg in messages[0].split()]
            return message_ids
        else:
            logging.error(f"Failed to search for unread messages in {label}: {messages}")
            return []
    except Exception as e:
        logging.error(f"Failed to retrieve unread message IDs from {label}: {e}")
        raise


def get_labels(mail: imaplib.IMAP4_SSL) -> Sequence:
    try:
        _, labels = mail.list()
        return labels
    except Exception as e:
        logging.error("Failed to retrieve label list: {}".format(e))
        raise


def extract_last_elements(mailboxes: Sequence) -> list[str]:
    try:
        decoded_mailboxes = [mailbox.decode() for mailbox in mailboxes]  # type: ignore
        joined_mailboxes = " ".join(decoded_mailboxes)
        pattern = re.compile(r'"([^"]+)"')
        return list(filter(lambda x: "/" not in x, pattern.findall(joined_mailboxes)))
    except Exception as e:
        logging.error(f"Failed to extract last elements: {e}")
        raise


def mark_as_read(mail: imaplib.IMAP4_SSL, message_ids: list[int], mailbox: str) -> None:
    try:
        mail.select(f'"{mailbox}"')

        for msg_id in message_ids:
            mail.store(str(msg_id), "+FLAGS", "\\Seen")
            print(f"Marked message ID {msg_id} as read.")

    except Exception as e:
        print(f"Failed to mark messages as read: {e}, {mailbox}")


def lambda_handler(event, context) -> None:
    secret = get_secret()
    gmail = connect_to_gmail_imap(secret=ast.literal_eval(secret))

    for label in extract_last_elements(get_labels(gmail)):
        if label in dont_touch_list:
            continue

        mark_as_read(
            mail=gmail,
            message_ids=get_unread_label_message_ids(mail=gmail, label=str(label)),
            mailbox=label,
        )
