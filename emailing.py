import smtplib
import imghdr
from email.message import EmailMessage

PASSWORD = "niebebuvyofouwit"
SENDER = "lxinin1999@gmail.com"
RECEIVER = "lxinin1999@gmail.com"

def send_email(image_path):
    email_message = EmailMessage()
    # note that email_message is a dictionary
    email_message["Subject"] = "New customer showed up!"
    email_message.set_content("Hey, we just saw a new customer!")

    # note that image is a binary file, we have to use 'rb'
    with open(image_path, 'rb') as file:
        content = file.read()

    # imghdr.what() finds out what kind of image is this content
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()

if __name__ == "__main__":
    send_email(image_path="images/1.png")
