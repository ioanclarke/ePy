from dataclasses import dataclass

import pandas as pd
import toml

from builder import Email, EmailBuilder
from sender import EmailSender


@dataclass
class Recipient:
    name: str
    address: str


def main():
    config: dict = toml.load("config.toml")["config"]

    recipients: list[Recipient] = read_names_and_emails(config["emails_source_file"])
    print("Names and emails retrieved\n")

    builder = EmailBuilder(recipients, config["sender_email"], config["email_subject"])
    emails: list[Email] = EmailBuilder.build_emails()

    sender = EmailSender(
        emails,
        config["sender_email"],
        config["sender_password"],
        config["SMTP_server"],
        config["port"],
    )
    sender.send()
    print("Done")


def read_names_and_emails(filename: str) -> list[Recipient]:
    df = pd.read_excel(f"docs/{filename}")

    names = list(df["Name"])
    addresses = list(df["Email"])
    return [Recipient(name, address) for name, address in zip(names, addresses)]


if __name__ == "__main__":
    main()
