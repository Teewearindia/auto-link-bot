import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const BACKEND_URL = "https://auto-link-bot-6uxa.onrender.com";

function App() {
  const [postId, setPostId] = useState('');
  const [link, setLink] = useState('');
  const [status, setStatus] = useState('');

  const handleSave = async () => {
    if (!postId || !link) {
      setStatus("⚠️ Post ID and link required");
      return;
    }

    try {
      const res = await axios.post(`${BACKEND_URL}/save_mapping`, {
        post_id: postId,
        link: link
      });
      setStatus("✅ Mapping saved!");
    } catch (err) {
      console.error(err);
      setStatus("❌ Error saving mapping");
    }
  };

  return (
    <div className="App">
      <h1>📩 Insta Auto Link Bot</h1>
      <input
        type="text"
        placeholder="Enter Reel Post ID"
        value={postId}
        onChange={(e) => setPostId(e.target.value)}
      />
      <input
        type="text"
        placeholder="Enter Product Link"
        value={link}
        onChange={(e) => setLink(e.target.value)}
      />
      <button onClick={handleSave}>Save Mapping</button>
      <p>{status}</p>
    </div>
  );
}

export default App;
