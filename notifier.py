import smtplib
from email.mime.text import MIMEText

EMAIL_SENDER = "franck.gasseau@email.com"
EMAIL_PASSWORD = "6cT7@#@in8oZ&a"
EMAIL_RECEIVER = "franck.gasseau@email.com"

def send_alert(ad, category):
    msg = MIMEText(f"NOUVELLE ANNONCE [{category}]\n\n{ad['title']}\n{ad['price']}\n{ad['url']}")
    msg['Subject'] = f"Nouvelle annonce sur LeBonCoin - {category}"
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
