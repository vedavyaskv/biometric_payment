import smtplib
import random

def send_otp(receiver_email):
    otp = random.randint(100000, 999999)

    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password"  # Gmail App Password

    message = f"Your OTP for payment verification is: {otp}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, message)
    server.quit()

    return otp
