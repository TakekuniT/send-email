import csv
import os
import smtplib
import time
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

CALENDLY_LINK = "https://calendly.com/takekuni-muxen/15-minute-meeting"
FORM_LINK = "https://forms.gle/8Nhexr75ftWUEddx5"
WAITLIST_LINK = "https://www.muxen.net/"

def formatBody(name):
    return f"""<p>Hi {name},</p>

<p>My name is Takekuni, or Taki, and I'm messaging a few tech content creators, including you, that have piqued my interest.</p>

<p>There are many tech content creators that have landed partnerships averaging $5,000, but the issue is getting that first big deal.</p>

<p>We plan to solve this. We are also currently in discussions with several major technology and creator-focused companies, including OpenAI, AWS, Replit, Cursor, Capcut, and more as we explore ways to bring valuable opportunities and partnerships to creators on the platform after launch.</p>

<p>If you'd like to be one of the first few to leverage our platform, I would love to hear about your experience as a content creator trying to land brand deals. I've heard a lot of pain points, ranging from not being able to get any sponsorships to having too many irrelevant brand deals in their inbox. Let's hop on a <a href="{CALENDLY_LINK}">10-15 minute call</a> whenever you're free!</p>

<p>In the meantime, please fill out this super duper quick <a href="{FORM_LINK}">form</a> so we can learn more about your experience and to join our exclusive waitlist <a href="{WAITLIST_LINK}">here</a>, that would be really helpful! 😊</p>

<p>Thank you,<br>Taki</p>"""

def parseCSV(path):
    results = []
    with open(path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append({
                'username': row['username'],
                'email': row['email']
            })
    return results
    
def sendEmail(content, recipient, sender="takekuni@muxen.net"):
    app_password = os.getenv("APP_PASSWORD")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Partnership Opportunity for Tech Creators 🚀"
    msg["From"] = sender
    msg["To"] = recipient
    msg.attach(MIMEText(content, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(sender, app_password)
        server.sendmail(sender, recipient, msg.as_string())

def sendBatch(contacts, delay_min=3, delay_max=8):
    for contact in contacts:
        body = formatBody(contact["username"])
        sendEmail(body, contact["email"])
        print(f"Sent to {contact['email']}")
        time.sleep(random.uniform(delay_min, delay_max))

if __name__ == '__main__':
    contacts = parseCSV('emailCSV/cs_emails_thousand.csv')
    print(f"Loaded {len(contacts)} contacts")
    print(contacts[:3])
    
    sampleList = [ { 'username': 'taki', 'email':'takekuni@tanemori.org' } ]
    sendBatch(sampleList)

 