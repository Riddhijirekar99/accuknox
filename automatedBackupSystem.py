import subprocess
import datetime
import smtplib
import os

def backup_to_remote_server(source_dir, destination_dir, exclude_list=[]):
    """
    Backs up a local directory to a remote server using rsync.

    Args:
        source_dir: The local directory to back up.
        destination_dir: The remote destination directory.
        exclude_list: A list of files or directories to exclude from the backup.
    """

    exclude_options = ""
    for exclude_item in exclude_list:
        exclude_options += f"--exclude='{exclude_item}' "

    rsync_command = f"rsync -avz {exclude_options} {source_dir} {destination_dir}"

    try:
        subprocess.run(rsync_command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Backup failed: {e}")
        return False

def send_email_report(success, source_dir, destination_dir, error_message=None):
    """
    Sends an email report on the backup status.

    Args:
        success: Whether the backup was successful.
        source_dir: The source directory.
        destination_dir: The destination directory.
        error_message: Optional error message if the backup fails.
    """

    # Use environment variables for email credentials for better security
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    receiver_email = os.getenv("RECEIVER_EMAIL")

    subject = "Backup Report"
    body = f"Backup of {source_dir} to {destination_dir} {'succeeded' if success else 'failed'}."

    if error_message:
        body += f"\n\nError details:\n{error_message}"

    # Build email message with proper headers
    message = f"Subject: {subject}\n\n{body}"

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.sendmail(sender_email, receiver_email, message)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    # Define directories and exclusions
    source_dir = "C:/Users/HP/Desktop/AccuKnox"
    destination_dir = "C:/Users/HP/Documents/Riddhidoc"
    exclude_list = ["*.log", "tmp"]

    # Run backup
    success = backup_to_remote_server(source_dir, destination_dir, exclude_list)

    # Prepare error message if backup failed
    error_message = None
    if not success:
        error_message = "The backup process encountered an error."

    # Send email report
    send_email_report(success, source_dir, destination_dir, error_message)
