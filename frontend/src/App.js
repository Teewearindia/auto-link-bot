import React, { useState } from "react";

function App() {
  const [postId, setPostId] = useState("");
  const [link, setLink] = useState("");
  const [message, setMessage] = useState("");

  const apiBase = "https://auto-link-bot-1.onrender.com";

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch(`${apiBase}/save_mapping`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ post_id: postId, link })
    });

    const data = await res.json();
    setMessage(data.message || "Something went wrong");
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>📌 Insta Auto Link Bot</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Post ID:</label>
          <input value={postId} onChange={(e) => setPostId(e.target.value)} required />
        </div>
        <div>
          <label>Product Link:</label>
          <input value={link} onChange={(e) => setLink(e.target.value)} required />
        </div>
        <button type="submit">Save Mapping</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default App;