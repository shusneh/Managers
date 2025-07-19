import React, { useState } from 'react';
import axios from 'axios';

const FileUploader = () => {
  const [folderPath, setFolderPath] = useState('');
  const [log, setLog] = useState('');

  const handleExecute = async () => {
    try {
      const response = await axios.post("http://localhost:5000/execute", { folderPath });
      setLog(response.data.log);
    } catch (err) {
      setLog("❌ Execution failed. " + err.message);
    }
  };

  return (
    <div style={{ padding: 30 }}>
      <h2>📂 SQL Automation Tool</h2>
      <input
        type="text"
        value={folderPath}
        onChange={(e) => setFolderPath(e.target.value)}
        placeholder="Enter absolute path to SQL folder"
        style={{ width: 400, marginRight: 10 }}
      />
      <button onClick={handleExecute}>Run SQL</button>
      <pre style={{ marginTop: 20, whiteSpace: 'pre-wrap' }}>{log}</pre>
    </div>
  );
};

export default FileUploader;