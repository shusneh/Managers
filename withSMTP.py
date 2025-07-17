import mysql.connector
import os

# 🚨 ADDED FOR EMAIL NOTIFICATION
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Path to your SQL file on Desktop
sql_file = os.path.expanduser("~/Desktop/my_queries.sql")

# 🚨 ADDED FOR EMAIL NOTIFICATION – Add your own values here
sender_email = "your_email@gmail.com"         # 🔁 YOUR GMAIL
receiver_email = "receiver_email@gmail.com"   # 🔁 SAME OR DIFFERENT
app_password = "your_app_password"            # 🔁 GMAIL APP PASSWORD

# 🚨 ADDED FOR EMAIL NOTIFICATION
def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.send_message(msg)
        print("📧 Email sent successfully.")
    except Exception as e:
        print("❌ Failed to send email:", e)


try:
    # Step 1: Initial connection (no DB yet) to create the database if needed
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Managers"
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS mydb")
    conn.commit()
    cursor.close()
    conn.close()

    try:
        # Step 2: Reconnect using the created database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Managers",
            database="mydb"
        )
        cursor = conn.cursor()

        # Step 3: Read and split SQL queries from file
        with open(sql_file, 'r') as file:
            sql_script = file.read()

        # Step 4: Split by semicolon and remove empty strings
        queries = [q.strip() for q in sql_script.split(';') if q.strip()]

        execution_log = ""  # 🚨 ADDED to collect log for email

        # Step 5: Execute each query
        for query in queries:
            try:
                cursor.execute(query)
                if query.lower().startswith("select"):
                    rows = cursor.fetchall()  # ✅ Prevents "Unread result found"
                    execution_log += f"\n🔎 Results for query:\n{query}\n"
                    for row in rows:
                        execution_log += str(row) + "\n"
                else:
                    conn.commit()
                    execution_log += f"\n✅ Executed: {query}\n"
            except Exception as e:
                error_msg = f"\n⚠️ Error in query:\n{query}\nError: {e}\n"
                execution_log += error_msg
                print(error_msg)

        # Step 6: Clean up
        cursor.close()
        conn.close()

        # 🚨 ADDED – Email after all queries
        send_email("SQL File Execution Completed ✅", execution_log)

        print("\n✅ All queries executed successfully.")

    except mysql.connector.Error as err:
        print("❌ MySQL Error during execution:", err)

except mysql.connector.Error as err:
    print("❌ MySQL Connection Error:", err)

except Exception as e:
    print("❌ General Error:", e)