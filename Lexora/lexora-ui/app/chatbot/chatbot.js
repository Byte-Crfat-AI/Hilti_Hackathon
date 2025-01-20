"use client";

import { useEffect, useState } from "react";
import styles from "./chatbot.module.css";

export default function Chatbot({ directoryPath }) {
  const [isChatOpen, setIsChatOpen] = useState(!!directoryPath);
  const [messages, setMessages] = useState([{ role: "bot", content: "Hello! How can I assist you?" }]);
  const [input, setInput] = useState("");

  useEffect(() => {
    if (directoryPath) setIsChatOpen(true);
  }, [directoryPath]);

  const addMessage = (role, content) => setMessages((prev) => [...prev, { role, content }]);

  const handleSend = () => {
    if (!input.trim()) return;

    addMessage("user", input);
    addMessage("bot", `You said: "${input}". Current directory: ${directoryPath}`);
    setInput("");
  };

  return (
    <div className={`${styles.chatbot} ${isChatOpen ? styles.open : ""}`}>
      {isChatOpen ? (
        <div className={styles.container}>
          <header className={styles.header}>
            <h3>Chatbot</h3>
            <button onClick={() => setIsChatOpen(false)} className={styles.closeButton}>
              ✕
            </button>
          </header>
          <div className={styles.chatbox}>
            <div className={styles.messages}>
              {messages.map((msg, idx) => (
                <div key={idx} className={`${styles.message} ${styles[msg.role]}`}>
                  {msg.content}
                </div>
              ))}
            </div>
            <footer className={styles.footer}>
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                className={styles.input}
                placeholder="Type your message..."
              />
              <button onClick={handleSend} className={styles.sendButton}>
                Send
              </button>
            </footer>
          </div>
        </div>
      ) : (
        <button onClick={() => setIsChatOpen(true)} className={styles.openButton}>
          Open Chat
        </button>
      )}
    </div>
  );
}
