import mysql.connector
import os

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
    cursor.execute("CREATE DATABASE IF NOT EXISTS mydb")
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

            try:
                with open(full_path, 'r') as file:
                    sql_script = file.read()

                queries = [q.strip() for q in sql_script.split(';') if q.strip()]

                for query in queries:
                    try:
                        cursor.execute(query)
                        if query.lower().startswith("select"):
                            rows = cursor.fetchall()
                            print(f"\n🔎 Results for query:\n{query}")
                            for row in rows:
                                print(row)
                        else:
                            conn.commit()
                            print(f"✅ Executed: {query}")
                    except Exception as e:
                        print(f"⚠️ Error in query:\n{query}")
                        print("Error:", e)

            except Exception as e:
                print(f"❌ Failed to read or execute {filename}: {e}")

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