from flask import Flask, request, jsonify
from sql_executor.execute_procedures import execute_sql_files

from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/execute", methods=["POST"])
def execute_sql():
    data = request.json
    folder_path = data.get("folderPath")

    # ✅ Validate path
    if not folder_path:
        return jsonify({"success": False, "message": "❌ Folder path is missing."}), 400
    if not os.path.isdir(folder_path):
        return jsonify({"success": False, "message": f"❌ '{folder_path}' is not a valid directory."}), 400

    try:
        result = execute_sql_files(folder_path)
        return jsonify({"success": True, "log": result})
    except Exception as e:
        return jsonify({"success": False, "message": f"❌ Error: {e}"}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
