import React, { useState } from 'react';
import axios from 'axios';
import './FileUploader.css'; // 👈 Create this CSS file

const FileUploader = () => {
  const [folderPath, setFolderPath] = useState('');
  const [log, setLog] = useState('');
  const [loading, setLoading] = useState(false);

  const handleExecute = async () => {
    setLoading(true);
    setLog('');

    try {
      const response = await axios.post("http://localhost:5000/execute", { folderPath });
      setLog(response.data.log);
    } catch (err) {
      setLog("❌ Execution failed. " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h2 className="heading">📂 SQL Automation Tool</h2>

      <input
        type="text"
        disabled={loading}
        value={folderPath}
        onChange={(e) => setFolderPath(e.target.value)}
        placeholder="Enter absolute path to SQL folder"
        className="input"
      />

      <button onClick={handleExecute} disabled={loading} className="button">
        {loading ? 'Running...' : 'Run SQL'}
      </button>

      {loading && <div className="loading">⏳</div>}

      {!loading && log && <pre className="log">{log}</pre>}
    </div>
  );
};

export default FileUploader;
