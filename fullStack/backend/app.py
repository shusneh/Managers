from flask import Flask, request, jsonify
from execute_sql import execute_sql_files
from flask_cors import CORS

app = Flask(__name__)  # ✅ Fix here: use __name__ instead of name
CORS(app)

@app.route("/execute", methods=["POST"])
def execute_sql():
    data = request.json
    folder_path = data.get("folderPath")
    if not folder_path:
        return jsonify({"success": False, "message": "Folder path is missing"}), 400

    result = execute_sql_files(folder_path)
    return jsonify({"success": True, "log": result})

if __name__ == "__main__":  # ✅ Fix here too
    app.run(port=5000, debug=True)
