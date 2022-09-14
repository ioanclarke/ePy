import os
from dataclasses import dataclass
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from main import Recipient


@dataclass
class Email:
    recipient: Recipient
    message: str


class EmailBuilder:
    def __init__(self, recipients: list[Recipient], sender_address: str, subject: str):
        self.recipients = recipients
        self.sender_address = sender_address
        self.subject = subject
        self.message_template = open("template.txt", "r", encoding="utf-8").read()

    def build_emails(self) -> list[Email]:
        return [self.build_email(recipient) for recipient in self.recipients]

    def build_email(self, recipient: Recipient) -> Email:
        message = MIMEMultipart()
        message["From"] = self.sender_address
        message["To"] = recipient.address
        message["Subject"] = self.subject

        body = self.message_template.replace("{NAME}", recipient.name)
        message.attach(MIMEText(body, "plain"))

        message_str = self.add_attachments(message)
        return Email(recipient, message_str)

    @staticmethod
    def add_attachments(message: MIMEMultipart) -> str:
        for filename in os.listdir("docs/attachments"):
            with open(f"docs/attachments/{filename}", "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", "attachment", filename=f"{filename}")
            message.attach(part)

        return message.as_string()
