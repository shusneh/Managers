import os
import mysql.connector
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "shubhanshusneh4@gmail.com"
receiver_email = "anupam.nilav11@gmail.com"
cc_emails = ["shubhanshusneh@gmail.com", "sweta3038@gmail.com"]
app_password = "yewp sulp wcvy amms"  # Gmail App Password

def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Cc"] = ", ".join(cc_emails)
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    recipients = [receiver_email] + cc_emails

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, recipients, msg.as_string())
    except Exception as e:
        return f"❌ Failed to send email: {e}"

def execute_sql_files(folder_path):
    logs = []

    sql_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".sql")])
    if not sql_files:
        return "❌ No .sql files found."

    try:
        # Step 1: Create database if not exists
        conn = mysql.connector.connect(host="localhost", user="root", password="Managers")
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ourdb")
        conn.commit()
        cursor.close()
        conn.close()

        # Step 2: Connect to the database
        conn = mysql.connector.connect(host="localhost", user="root", password="Managers", database="ourdb")
        cursor = conn.cursor()

        # Step 3: Execute SQL files
        for filename in sql_files:
            full_path = os.path.join(folder_path, filename)
            email_log = f"📁 Executing File: {filename} at {datetime.now()}\n"

            try:
                with open(full_path, 'r') as file:
                    sql_script = file.read()
                queries = [q.strip() for q in sql_script.split(';') if q.strip()]

                for query in queries:
                    try:
                        cursor.execute(query)

                        # ✅ Fix: Read results to avoid "Unread result found"
                        if cursor.with_rows:
                            cursor.fetchall()
                        else:
                            conn.commit()

                        # email_log += f"✅ {datetime.now()} Executed: {query}\n"
                    except Exception as e:
                        email_log += f"⚠️ {datetime.now()} Error: {e} in query: {query}\n"

            except Exception as e:
                email_log += f"❌ {datetime.now()} Failed to read {filename}: {e}\n"
                
            email_log = f"✅ Executed Successfully: {filename} at {datetime.now()}\n"
            logs.append(email_log)
            send_email(f"SQL Execution Report: {filename}", email_log)

        # Step 4: Cleanup
        cursor.close()
        conn.close()
        return "\n".join(logs)

    except mysql.connector.Error as e:
        return f"❌ MySQL Error: {e}"
    except Exception as e:
        return f"❌ General Error: {e}"
