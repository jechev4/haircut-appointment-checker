import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Hardcoded email credentials and recipient email (Outlook is required for security reasons; Gmail may not work)
sender_email = "****************"
sender_password = "****************"
recipient_email = "****************"

# Function to send an email when a new, earlier appointment is found
def send_new_appointment_email(appointment_info):
    subject = "New Earlier Appointment Available"
    body = f"An earlier appointment has been found:\n\nDate: {appointment_info[0]}\nProvider: {appointment_info[1]}\nTime: {appointment_info[2]}"

    # Set up the email structure
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to the Outlook SMTP server and send the email
        server = smtplib.SMTP("smtp.office365.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.close()
        print("Notification email sent for new earlier appointment.")
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to notify when the previously found earliest appointment is no longer available
def send_appointment_no_longer_available_email():
    subject = "Appointment No Longer Available"
    body = "The earliest appointment you had has now been taken or removed."

    # Set up the email structure
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to the Outlook SMTP server and send the email
        server = smtplib.SMTP("smtp.office365.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.close()
        print("Notification email sent: Appointment no longer available.")
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to check the website for available appointments
def check_appointments(provided_date, saved_appointment):
    # Set up Selenium WebDriver (make sure to have ChromeDriver installed)
    driver = webdriver.Chrome()

    try:
        # Open the Resurva booking page
        driver.get("https://handcraftedbarbershop.resurva.com/book?cancel=1")

        # Use WebDriverWait to ensure elements load properly before interaction
        wait = WebDriverWait(driver, 20)

        # Select the haircut service using its XPath
        haircut_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='service-54965']")))
        haircut_option.click()

        # Click the "Next" button to proceed with booking
        next_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='page-new-booking']/div[1]/div[3]/span"))
        )
        next_button.click()

        # Wait for available time slots to load
        time.sleep(5)  # Adjust this wait time if needed

        # Extract HTML content and parse it using BeautifulSoup
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Debugging: Print a preview of the HTML to ensure correct extraction
        print("HTML Snippet:")
        print(html[:500])  # Displaying only the first 500 characters to avoid excessive output

        # Find appointment time slots
        appointment_headers = soup.find_all('h3')

        # Extract relevant appointment information
        appointments = []
        for header in appointment_headers:
            if 'in' in header.text and 'days' in header.text:
                parts = header.text.split()
                days_from_today = int(parts[1])
                appointment_date = datetime.today() + timedelta(days=days_from_today)
                provider = ' '.join(parts[4:-2])
                time_slot = parts[-2] + ' ' + parts[-1]
                appointments.append((appointment_date, provider, time_slot))

        # Check if any appointments were found
        if not appointments:
            print("No appointments currently available.")
        else:
            # Find the earliest appointment available
            closest_appointment = min(appointments, key=lambda x: x[0])

            # Compare with the user-provided date
            if closest_appointment[0] < provided_date:
                print("An earlier appointment has been found!")
                print(f"Date: {closest_appointment[0]}")
                print(f"Provider: {closest_appointment[1]}")
                print(f"Time: {closest_appointment[2]}")

                # If this appointment is earlier than the saved one, send an email
                if saved_appointment is None or closest_appointment[0] < saved_appointment[0]:
                    send_new_appointment_email(closest_appointment)
                    saved_appointment = closest_appointment
            elif saved_appointment and saved_appointment not in appointments:
                # If the previously saved appointment is no longer available, notify the user
                send_appointment_no_longer_available_email()
                saved_appointment = None
    finally:
        # Always close the WebDriver session when done
        driver.quit()

    return saved_appointment


# Prompt user for a date to compare against available appointments
user_date_input = input("Enter a date in MM/DD/YYYY format to check for earlier appointments: ")
provided_date = datetime.strptime(user_date_input, "%m/%d/%Y")

# Initialize variable to track the saved appointment
saved_appointment = None

# Continuously check for new appointments at regular intervals
while True:
    saved_appointment = check_appointments(provided_date, saved_appointment)
    print("Appointment check completed. Next check in 30 minutes.")
    time.sleep(1800)  # Wait for 30 minutes before checking again
