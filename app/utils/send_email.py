from  fastapi import status
from fastapi.responses import JSONResponse
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

def send_verification_email(email: str):
    """
    Send a verification email to the user.
    - **email**: User's email address.
    """
    # Create the email content
    verification_link = f"http://127.0.0.1:8000/api/v1/users/auth/verify?email={email}"
    message = MIMEText(f"Click the link to verify your email: {verification_link}")
    message["Subject"] = "Verify Your Email"
    message["From"] = os.getenv("EMAIL_USER")
    message["To"] = email

    try:
        
        with smtplib.SMTP(os.getenv("EMAIL_HOST"), int(os.getenv("EMAIL_PORT"))) as server:
            server.starttls() 
            server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))
            server.sendmail(os.getenv("EMAIL_USER"), [email], message.as_string())
        print(f"Verification email sent to {email}")
    except:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Failed to send verification email."})