import React, { useState } from "react";

function App() {
  const [postId, setPostId] = useState("");
  const [link, setLink] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch("https://auto-link-bot-1.onrender.com/save_mapping", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ post_id: postId, link }),
    });

    const data = await res.json();
    setMessage(data.message || "Some error");
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h2>🔥 Insta Auto Link Bot</h2>
      <form onSubmit={handleSubmit}>
        <input
          placeholder="Post ID"
          value={postId}
          onChange={(e) => setPostId(e.target.value)}
        /><br /><br />
        <input
          placeholder="Product Link"
          value={link}
          onChange={(e) => setLink(e.target.value)}
        /><br /><br />
        <button type="submit">Save Mapping</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default App;
