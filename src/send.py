# send email and sms to the user

#sending email 
import smtplib

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"  # Gmail's SMTP server
SMTP_PORT = 587  # TLS Port
SENDER_EMAIL = "ehteshammohammed612@gmail.com"
SENDER_PASSWORD = "kfmtconxcvlnvqck"
RECEIVER_EMAIL = "mdkabir3350@gmail.com"
SUBJECT = "Student Update"

BODY = "Hello, this is a test email sent using Python's smtplib."
# Create email message


def send_email(message):
    message = f"Subject: {SUBJECT}\n\n{message}"
    try:
        # Connect to SMTP Server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Upgrade connection to secure encrypted TLS
        server.login(SENDER_EMAIL, SENDER_PASSWORD)  # Authenticate
        
        # Send email
        server.sendmail(from_addr=SENDER_EMAIL, to_addrs=RECEIVER_EMAIL,msg= message)
        print("Email sent successfully!")

    except Exception as e:
        print("Error:", e)

    finally:
        server.quit()  # Close connection




    