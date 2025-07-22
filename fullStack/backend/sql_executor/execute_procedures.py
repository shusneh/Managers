import os
import mysql.connector
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

# ---------- ✉️ Email Configuration ----------
sender_email = "shubhanshusneh4@gmail.com"
receiver_email = "anupam.nilav11@gmail.com"
cc_emails = ["shubhanshusneh@gmail.com", "sweta3038@gmail.com"]
app_password = "yewp sulp wcvy amms"

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
        print(f"❌ Failed to send email: {e}")

# ---------- 📄 SQL Statement Parser ----------
def split_sql_statements(script):
    statements = []
    statement = ""
    in_procedure = False

    for line in script.splitlines():
        stripped = line.strip()

        # Start of stored procedure
        if re.match(r"^CREATE\s+(DEFINER=`[^`]+`@`[^`]+`\s+)?PROCEDURE", stripped, re.IGNORECASE):
            in_procedure = True

        statement += line + "\n"

        if in_procedure:
            if re.search(r"\bEND\s*[$;]*", stripped, re.IGNORECASE):
                statements.append(statement.strip())
                statement = ""
                in_procedure = False
        else:
            if stripped.endswith(";"):
                statements.append(statement.strip())
                statement = ""

    if statement.strip():
        statements.append(statement.strip())

    return statements

# ---------- 🛠️ Main Execution Function ----------
def execute_sql_files(folder_path):
    logs = []

    sql_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".sql")])
    if not sql_files:
        return "❌ No .sql files found."

    try:
        # Create DB if not exists
        conn = mysql.connector.connect(host="localhost", user="root", password="Managers")
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ourdb")
        conn.commit()
        cursor.close()
        conn.close()

        # Connect to ourdb
        conn = mysql.connector.connect(host="localhost", user="root", password="Managers", database="ourdb")
        cursor = conn.cursor()

        # Create tables if not exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INT PRIMARY KEY,
                salary DECIMAL(10,2),
                department_id INT
            )
        """)
        cursor.execute("""t
            CREATE TABLE IF NOT EXISTS employee_reports (
                department_id INT,
                total_employees INT,
                avg_salary DECIMAL(10,2)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_logs (
                user_id INT,
                action VARCHAR(50)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_summary (
                user_id INT,
                status VARCHAR(20)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS managers (
                id INT,
                name VARCHAR(100)
            )
        """)
        conn.commit()

        # Run SQL files
        for filename in sql_files:
            full_path = os.path.join(folder_path, filename)
            email_log = f"📁 Executing File: {filename} at {datetime.now()}\n"

            try:
                with open(full_path, 'r') as file:
                    sql_script = file.read()

                queries = split_sql_statements(sql_script)

                for query in queries:
                    try:
                        cursor.execute(query)
                        if cursor.with_rows:
                            result = cursor.fetchall()
                            email_log += f"📄 Query:\n✅ \n\n"
                        else:
                            conn.commit()
                            email_log += f"📄 Query:\n✅ Executed successfully\n\n"
                    except Exception as e:
                        email_log += f"⚠️ {datetime.now()} Error: {e}\nQuery:\n{query}\n\n"

            except Exception as e:
                email_log += f"❌ {datetime.now()} Could not read {filename}: {e}\n"

            email_log += f"✅ Finished: {filename} at {datetime.now()}\n"
            logs.append(email_log)

            send_email(f"SQL Execution Report: {filename}", email_log)

        cursor.close()
        conn.close()
        return "\n".join(logs)

    except mysql.connector.Error as e:
        return f"❌ MySQL Error: {e}"
    except Exception as e:
        return f"❌ General Error: {e}"

# ---------- 🚀 Entry Point ----------
if __name__ == "__main__":
    folder_path = "sql_scripts"  # Path to .sql files
    print("⏳ Starting SQL Execution...")
    log_result = execute_sql_files(folder_path)
    print(log_result)
