# Handcrafted Barbershop Appointment Checker

This Python script automatically checks for earlier available appointments at Handcrafted Barbershop and notifies you via email if one is found. It continuously monitors the booking site and alerts you when an earlier slot opens up or if the previously found appointment is no longer available.

## Features
- Uses **Selenium** to navigate the booking website and extract available appointment times.
- Compares available appointments against a **user-provided date**.
- **Email notifications** for:
  - A newly found earlier appointment.
  - The previously saved appointment no longer being available.
- Runs on a **30-minute loop**, continuously checking for updates.

## Requirements
### **Python Dependencies**
Make sure you have the following installed:
- `selenium`
- `beautifulsoup4`
- `requests`

Install them using:
```bash
pip install selenium beautifulsoup4 requests
