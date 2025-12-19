import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def send_email(self, to_email: str, subject: str, body: str):
        if not settings.SMTP_USER or settings.SMTP_USER == "your-email@gmail.com":
            logger.warning("SMTP not configured, skipping email sending.")
            print(f"--- Mock Email ---\nTo: {to_email}\nSubject: {subject}\nBody: {body}\n------------------")
            return

        try:
            msg = MIMEMultipart()
            msg['From'] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
            msg['To'] = to_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'html'))

            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            text = msg.as_string()
            server.sendmail(settings.EMAILS_FROM_EMAIL, to_email, text)
            server.quit()
            logger.info(f"Email sent to {to_email}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise e

    def send_verification_email(self, to_email: str, code: str):
        subject = "验证您的邮箱 - Designer"
        body = f"""
        <html>
            <body>
                <h2>欢迎注册 Designer</h2>
                <p>您的验证码是：<strong style="font-size: 24px; color: #165DFF;">{code}</strong></p>
                <p>请输入此验证码完成注册。如果您没有请求此代码，请忽略此邮件。</p>
            </body>
        </html>
        """
        self.send_email(to_email, subject, body)

    def send_reset_password_email(self, to_email: str, token: str):
        subject = "重置密码 - Designer"
        body = f"""
        <html>
            <body>
                <h2>重置密码</h2>
                <p>您收到了这封邮件是因为您（或者其他人）请求重置您的账户密码。</p>
                <p>您的重置验证码是：<strong style="font-size: 24px; color: #165DFF;">{token}</strong></p>
                <p>请在重置密码页面输入此验证码。</p>
                <p>如果您没有请求重置密码，请忽略此邮件。</p>
            </body>
        </html>
        """
        self.send_email(to_email, subject, body)

email_service = EmailService()
