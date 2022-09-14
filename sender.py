import smtplib
import ssl

from main import Email


class EmailSender:
    def __init__(
        self,
        emails: list[Email],
        sender_email: str,
        sender_password: str,
        smtp_server_address: str,
        port: int,
    ):
        self.emails = emails
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server_address = smtp_server_address
        self.port = port

    def send_emails(self):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(
            self.smtp_server_address, self.port, context=context
        ) as server:
            server.login(self.sender_email, self.sender_password)

            print(f"Logged in as {self.sender_email}\n")

            for email in self.emails:
                server.sendmail(
                    self.sender_email, email.recipient.address, email.message
                )
                print(f"Sent email to {email.recipient.address}\n")
