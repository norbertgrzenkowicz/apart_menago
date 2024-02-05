import smtplib
from email.mime.text import MIMEText
import config
import logging


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
        logging.debug("Sending the Email Message")
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
    logging.info("Message sent!")


if __name__ == "__main__":
    send_email(
        config.EMAIL_SUBJECT,
        config.EMAIL_BODY,
        config.EMAIL_SENDER,
        config.EMAIL_RECIPIENTS,
        config.EMAIL_PASSWORD,
    )
