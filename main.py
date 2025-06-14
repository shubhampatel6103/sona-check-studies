from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options

load_dotenv()  # Load environment variables from .env file

receivers = [
    "shubhampatelspam@gmail.com", 
    "rushildeep1@gmail.com", 
    "sohamsant@gmail.com", "spence.pilkey2@gmail.com", 
    "hudson.l.vance@gmail.com", 
    "ameya.soman12@gmail.com"
]

def send_email(receiver):
    sender = "shubhampatelspam@gmail.com"  # Replace with your email
    password = os.getenv("EMAIL_PASSWORD")   # Use an app password if using Gmail
    subject = "Sona Studies Update"
    body = "There are studies available or the message has changed."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
        print("Notification email sent.")
    except Exception as e:
        print("Failed to send email:", e)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = "/usr/bin/chromium-browser" 

driver = driver = webdriver.Chrome(options=chrome_options)

driver.get("https://wlu-ls.sona-systems.com/default.aspx")

user_input = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_userid")
user_input.send_keys(os.getenv("SONA_ID"))
password_input = driver.find_element(By.ID, "pw")
password_input.send_keys(os.getenv("SONA_PW"))
password_input.send_keys(Keys.RETURN)

driver.get("https://wlu-ls.sona-systems.com/all_exp_participant.aspx")

# Find the div and check its text
try:
    # Navigate to the studies page
    driver.get("https://wlu-ls.sona-systems.com/all_exp_participant.aspx")
    
    # Get the current time (Eastern Time)
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time() - 5*3600))
    
    # Get the page source after navigation
    page_source = driver.page_source
    
    if "No studies are available at this time." in page_source:
        print(f"{current_time} - No studies are available at this time.")
    else:
        print(f"{current_time} - Studies are available or the message is different.")
        for receiver in receivers:
            send_email(receiver)
except Exception as e:
    print("An error occurred while reading the page:", e)

driver.quit()
