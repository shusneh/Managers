import mysql.connector
import os

# 🚨 EMAIL FUNCTIONALITY START
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Fill in your Gmail credentials
sender_email = "shubhanshusneh4@gmail.com"          # 🔁 your Gmail
receiver_email = "anupam.nilav11@gmail.com" 
app_password = "yewp sulp wcvy amms"             # 🔁 16-char Gmail App Password
cc_recipients = ['sweta3038@gmail.com','rishavrajjha24@gmail.com']  # 🔁 CC recipients

def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Cc"] = ", ".join(cc_recipients)  # Add CC recipients
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    recipients = [receiver_email] + cc_recipients
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.send_message(msg)
        print("📧 Email sent.")
    except Exception as e:
        print("❌ Failed to send email:", e)
# 🚨 EMAIL FUNCTIONALITY END

# Step 1: Get all .sql files from Desktop
desktop_path = os.path.expanduser("~/Desktop/New folder")
sql_files = sorted([f for f in os.listdir(desktop_path) if f.endswith(".sql")])

try:
    # Step 2: Initial connection to create the database if not exists
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Managers"
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ourdb")
    conn.commit()
    cursor.close()
    conn.close()

    try:
        # Step 3: Reconnect to the created database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Managers",
            database="ourdb"
        )
        cursor = conn.cursor()

        # Step 4: Loop through each .sql file and execute queries
        for filename in sql_files:
            full_path = os.path.join(desktop_path, filename)
            print(f"\n📂 Executing file: {filename}")
            email_log = f"📁Executing File: {filename}\n"

            try:
                with open(full_path, 'r') as file:
                    sql_script = file.read()

                queries = [q.strip() for q in sql_script.split(';') if q.strip()]

                for query in queries:
                    try:
                        cursor.execute(query)
                        if query.lower().startswith("select"):
                            rows = cursor.fetchall()
                        else:
                            conn.commit()
                            email_log += f"✅ Executed:\n\n"
                    except Exception as e:
                        error_msg = f"⚠️ Error in query:\n{query}\nError: {e}\n"
                        email_log += error_msg
                        print(error_msg)

            except Exception as e:
                fail_msg = f"❌ Failed to read or execute {filename}: {e}\n"
                email_log += fail_msg
                print(fail_msg)

            # 🚨 Send email after each file
            email_log += f"✅ Executed: {filename}\n"
            send_email(f"SQL Execution Report: {filename}", email_log)

        # Step 5: Cleanup
        cursor.close()
        conn.close()
        print("\n✅ All SQL files executed successfully.")

    except mysql.connector.Error as err:
        print("❌ MySQL Error during execution:", err)

except mysql.connector.Error as err:
    print("❌ MySQL Connection Error:", err)

except Exception as e:
    print("❌ General Error:", e)