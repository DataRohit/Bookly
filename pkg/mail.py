from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import aiosmtplib
from jinja2 import Environment, FileSystemLoader

from pkg.config import Config

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_FOLDER = Path(BASE_DIR, "templates")

env = Environment(loader=FileSystemLoader(str(TEMPLATE_FOLDER)))


async def create_message(
    recipients: list[str], subject: str, template_name: str, context: dict
):
    template = env.get_template(template_name)
    body = template.render(context)

    message = MIMEMultipart()
    message["From"] = Config.MAIL_FROM
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject

    message.attach(MIMEText(body, "html"))

    return message


async def send_email(
    recipients: list[str], subject: str, template_name: str, context: dict
):
    message = await create_message(recipients, subject, template_name, context)

    try:
        await aiosmtplib.send(
            message,
            sender=Config.MAIL_USER,
            recipients=recipients,
            hostname=Config.MAIL_SERVER,
            port=Config.MAIL_PORT,
            use_tls=False,
        )
    except Exception as e:
        print(f"Error sending email: {e}")
