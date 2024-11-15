import psutil
import smtplib
import time

# Define thresholds
cpu_threshold = 80
memory_threshold = 80
disk_threshold = 90

# Function to send email alerts
def send_email(subject, body):
    # Replace with your email credentials
    sender_email = "riddhijirekar5@gmail.com"
    sender_password = "Riddhi@99"
    receiver_email = "pinjariasif0203@gmail.com"

    message = f"Subject: {subject}\n\n{body}"

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.sendmail(sender_email, receiver_email, message)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to check system health and send alerts
def check_system_health():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    running_processes = len(psutil.pids())

    if cpu_usage > cpu_threshold:
        print(f"CPU usage is high: {cpu_usage}%")
        send_email("High CPU Usage Alert", f"CPU usage is currently at {cpu_usage}%.")

    if memory_usage > memory_threshold:
        print(f"Memory usage is high: {memory_usage}%")
        send_email("High Memory Usage Alert", f"Memory usage is currently at {memory_usage}%.")

    if disk_usage > disk_threshold:
        print(f"Disk usage is high: {disk_usage}%")
        send_email("High Disk Usage Alert", f"Disk usage is currently at {disk_usage}%.")

    # You can add more specific checks for running processes as needed
    # For example, check for specific processes or resource-intensive processes

# Main loop
while True:
    check_system_health()
    time.sleep(60)  # Check every 60 seconds