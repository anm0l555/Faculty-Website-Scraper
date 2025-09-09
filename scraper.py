import requests
from bs4 import BeautifulSoup
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# ----------- CONFIGURATION ------------
URL = "https://homecse.iitd.ac.in/faculty/"   # replace with actual university faculty page
YOUR_EMAIL = "thisisanmol15@gmail.com"
YOUR_PASSWORD = "egcv dovc pmzt uynz"   # use App password if using Gmail/Outlook
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
RESUME_PATH="./Anmol_Tiwari_Resume.pdf"

# ----------- SCRAPER FUNCTION ------------
def get_professors(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    professors = []

    for prof_div in soup.find_all("div", class_="single-team-area"):
        # Extract name
        name = None
        name_tag = prof_div.find("span", class_="team-name")
        if name_tag:
            name = name_tag.get_text(strip=True)

        # Extract email
        email = None
        email_li = prof_div.find("li", class_="tlp-email")
        if email_li:
            a_tag = email_li.find("a", href=True)
            if a_tag and a_tag["href"].startswith("mailto:"):
                email = a_tag["href"].replace("mailto:", "").strip()

        if name and email:
            professors.append((name, email))

    return professors


# ----------- EMAIL GENERATOR ------------
def generate_mail(prof_name):
    subject = f"Request to Contribute to Research under Your Guidance"
    body = f"""
Dear Prof. {prof_name},

I hope this message finds you well.  
My name is Anmol Tiwari, and I recently graduated in 2023 with a CGPA of 8.7/10 from Thapar Institute of Engineering and Technology, Patiala. 

Currently, I am working as a Stress Testing Senior Analyst at NatWest Group, where I design and automate reporting processes within the securitization sector and apply stress testing practices to improve financial resilience. Prior to this, I worked as an Analyst at BlackRock, where I built a regression framework that streamlined financial data validation and reporting. These roles have given me a strong foundation in quantitative analysis, programming, and problem-solving, which I am eager to apply in an academic research setting.

I am very interested in exploring opportunities to contribute to research under your guidance. I believe that engaging with your research group would not only help me deepen my knowledge but also allow me to meaningfully contribute through the technical and analytical skills I have gained in industry.

For your reference, I am attaching my résumé, which provides further details about my background.  
I would be very grateful if you could consider my request and let me know if there might be an opportunity to assist in your ongoing or upcoming research projects.

Thank you for your time and consideration. I look forward to hearing from you.

Best regards,  
Anmol Tiwari  
Email: {YOUR_EMAIL}  
Ph No. 9711843423
    """
    return subject, body

# ----------- SENDER FUNCTION ------------
def send_emails(professors):
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(YOUR_EMAIL, YOUR_PASSWORD)

    for name, email in professors:
        subject, body = generate_mail(name)
        msg = MIMEMultipart()
        msg["From"] = YOUR_EMAIL
        msg["To"] = email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # attach resume
        with open(RESUME_PATH, "rb") as f:
            part = MIMEApplication(f.read(), Name="Anmol_Tiwari_Resume.pdf")
            part['Content-Disposition'] = 'attachment; filename="Anmol_Tiwari_Resume.pdf"'
            msg.attach(part)

        try:
            server.sendmail(YOUR_EMAIL, email, msg.as_string())
            print(f"[SENT] Email to {name} ({email})")
        except Exception as e:
            print(f"[FAILED] {email}: {e}")

    server.quit()

# ----------- MAIN ------------
if __name__ == "__main__":
    profs = get_professors(URL)
    print(f"Found {len(profs)} professors")
    for p in profs:
        print(p)
    
    # Uncomment below to actually send mails
    send_emails(profs)
