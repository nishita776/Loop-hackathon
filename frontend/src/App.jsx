import { useState, useEffect } from "react";
import { motion } from "framer-motion";

const API = "http://localhost:5000";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [user, setUser] = useState("");
  const [text, setText] = useState("");

  // Fetch messages once (on load or after sending)
  const fetchMessages = async () => {
    const res = await fetch(API + "/chat/messages");
    const data = await res.json();
    setMessages(data);
  };

  const sendMessage = async () => {
    if (!user.trim() || !text.trim()) return;

    await fetch(API + "/chat/send", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user, text }),
    });

    setText("");
    fetchMessages();
  };

  // Fetch messages ONLY on page load
  useEffect(() => {
    fetchMessages();
  }, []);

  return (
    <div className="h-screen bg-gray-100 flex flex-col p-4">
      <h1 className="text-xl font-bold mb-2">Team Chat</h1>

      <div className="flex-1 bg-white rounded shadow p-3 overflow-auto">
        {messages.map((m, i) => (
          <motion.div
            key={i}
            initial={{ x: 40, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            className="mb-1"
          >
            {m.type === "vague" && "⚠️ "}
            {m.type === "commitment" && "📌 "}
            {m.type === "ai" && "🤖 "}
            <b>{m.user}:</b> {m.text}
          </motion.div>
        ))}
      </div>

      <div className="mt-3 flex gap-2">
        <input
          className="border p-2 flex-1"
          placeholder="Your name"
          value={user}
          onChange={(e) => setUser(e.target.value)}
        />

        <input
          className="border p-2 flex-1"
          placeholder="Type message"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") sendMessage();
          }}
        />

        <button
          className="bg-blue-500 text-white px-4 rounded disabled:opacity-50"
          onClick={sendMessage}
          disabled={!user.trim() || !text.trim()}
        >
          Send
        </button>
      </div>
    </div>
  );
}

