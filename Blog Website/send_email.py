from dotenv import load_dotenv
import smtplib
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load .env file
load_dotenv()

# Get the environment variable
sender_email = os.getenv('SENDER_EMAIL')
reciever_email = os.getenv('RECIEVER_EMAIL')
app_password = os.getenv('APP_PASSWORD')


# Send Message Email
def send_message(data):
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=sender_email, password=app_password)
            
            # Construct the email with a subject
            subject = "New Message Notification"
            body = f"""Name: {data.get("name")}
Email: {data.get("email")}
Phone: {data.get("phone")}
Message: {data.get("message")}"""
            
            # Format the email with subject and body
            msg = f"Subject: {subject}\n\n{body}"
            
            connection.sendmail(
                from_addr=sender_email,
                to_addrs=reciever_email,
                msg=msg
            )
            logging.info("Email sent successfully.")
            return True
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error occurred: {e}")
        return False
    except Exception as e:
        logging.error(f"Error in sending mail: {e}")
        return False


if __name__ == "__main__":
    send_message("This is a test email sent through smtplib python")