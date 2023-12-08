#!/usr/bin/python3
"""Module to send emails"""

from app.config import settings
from typing import Any, Dict, List
from pydantic import BaseModel, EmailStr
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

class Mail(BaseModel):
    """Class that defines email instances"""
    email: List[EmailStr]
    content: Dict[str, Any]

class MailSender:
    def __init__(self):
        self.fm = FastMail(
            ConnectionConfig(
                MAIL_USERNAME=settings.MAIL_USERNAME,
                MAIL_PASSWORD=settings.MAIL_PASSWORD,
                MAIL_FROM=settings.MAIL_FROM,
                MAIL_PORT=settings.MAIL_PORT,
                MAIL_SERVER=settings.MAIL_SERVER,
                MAIL_TLS=settings.MAIL_TLS,
                MAIL_SSL=settings.MAIL_SSL,
                MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
                MAIL_STARTTLS=settings.MAIL_STARTTLS
            )
        )

    async def _create_message(self, mail: Mail, template: str):
        return MessageSchema(
            subject=mail.content.get('subject') or 'AfriLegal API Password Reset',
            recipients=mail.email,
            body=template.format(**mail.content),
            subtype="html"
        )

    async def simple_send(self, mail: Mail, template: str):
        message = await self._create_message(mail, template)
        await self.fm.send_message(message)

    async def send_in_background(self, background_tasks, mail: Mail, template: str):
        message = await self._create_message(mail, template)
        background_tasks.add_task(self.fm.send_message, message)
