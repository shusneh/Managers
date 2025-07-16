import mysql.connector
import os

# Path to your SQL file on Desktop
sql_file = os.path.expanduser("~/Desktop/my_queries.sql")

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

        # Step 5: Execute each query
        for query in queries:
            try:
                cursor.execute(query)
                if query.lower().startswith("select"):
                    rows = cursor.fetchall()  # ✅ Prevents "Unread result found"
                    print(f"\n🔎 Results for query:\n{query}")
                    for row in rows:
                        print(row)
                else:
                    conn.commit()
                    print(f"✅ Executed: {query}")
            except Exception as e:
                print(f"⚠️ Error in query:\n{query}")
                print("Error:", e)

        # Step 6: Clean up
        cursor.close()
        conn.close()
        print("\n✅ All queries executed successfully.")

    except mysql.connector.Error as err:
        print("❌ MySQL Error during execution:", err)

except mysql.connector.Error as err:
    print("❌ MySQL Connection Error:", err)

except Exception as e:
    print("❌ General Error:", e)
