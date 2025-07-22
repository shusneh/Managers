import React, { useState } from 'react';
import axios from 'axios';
import "tailwindcss";

const FileUploader = () => {
  const [folderPath, setFolderPath] = useState('');
  const [log, setLog] = useState('');
  const [loading, setLoading] = useState(false); // 🆕 loading state

  const handleExecute = async () => {
    setLoading(true); // 🟡 Start loading
    setLog('');       // Optional: clear old log

    try {
      const response = await axios.post("http://localhost:5000/execute", { folderPath });
      setLog(response.data.log);
    } catch (err) {
      setLog("❌ Execution failed. " + err.message);
    } finally {
      setLoading(false); // ✅ Stop loading
    }
  };
 
  return (
    <div style={{ padding: 30 }} >
      <h2 class="text-4xl font-bold underline">📂 SQL Automation Tool</h2> 

      <input
        type="text"
        disabled={loading}
        value={folderPath}
        onChange={(e) => setFolderPath(e.target.value)}
        placeholder="Enter absolute path to SQL folder"
        style={{ width: 400, marginRight: 10 }}
      />

      <button onClick={handleExecute} disabled={loading} style={{ marginLeft: 10 }}>
        {loading ? 'Running...' : 'Run SQL'}
      </button>

      {/* 🕐 Loading indicator */}
      {loading && (
        <div style={{ marginTop: 20, fontWeight: 'bold', color: 'blue' }}>
          Please wait while the SQL files are being executed... ⏳
        </div>
      )}

      {/* 📋 Execution log output */}
      {!loading && log && (
        <pre style={{ marginTop: 20, whiteSpace: 'pre-wrap' }}>{log}</pre>
      )}
    </div>
  );
};

export default FileUploader;

