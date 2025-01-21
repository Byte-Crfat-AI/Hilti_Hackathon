"use client";

import { useEffect, useState } from "react";
import styles from "./chatbot.module.css";

export default function Chatbot({ directoryPath }) {
  const [isChatOpen, setIsChatOpen] = useState(!!directoryPath);
  const [messages, setMessages] = useState([
    { role: "bot", content: "Hello! How can I help you with your documents?" }
  ]);
  const [input, setInput] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);

  useEffect(() => {
    if (directoryPath) {
      setIsChatOpen(true);
      processDirectory(directoryPath);
    }
  }, [directoryPath]);

  const processDirectory = async (path) => {
    try {
      setIsProcessing(true);
      const response = await fetch('/api/process-files', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ folderPath: path })
      });

      const result = await response.json();
      
      if (result.success) {
        addMessage("bot", result.cached 
          ? "Directory already processed. Ready for questions!"
          : "Directory processed successfully. What would you like to know?");
      } else {
        addMessage("bot", "Sorry, I had trouble processing the directory. Please try again.");
      }
    } catch (error) {
      addMessage("bot", "Error processing directory. Please check the path and try again.");
    } finally {
      setIsProcessing(false);
    }
  };

  const handleQuery = async (query) => {
    try {
      setIsProcessing(true);
      const response = await fetch('/api/process-files', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });

      const result = await response.json();
      
      if (result.success) {
        addMessage("bot", result.data.response || "I found relevant information but couldn't format it properly.");
      } else {
        addMessage("bot", "Sorry, I couldn't process your query. Please try again.");
      }
    } catch (error) {
      addMessage("bot", "Error processing your query. Please try again.");
    } finally {
      setIsProcessing(false);
    }
  };

  const addMessage = (role, content) => {
    setMessages(prev => [...prev, { role, content }]);
  };

  const handleSend = async () => {
    if (!input.trim() || isProcessing) return;

    const userMessage = input.trim();
    setInput("");
    addMessage("user", userMessage);
    await handleQuery(userMessage);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className={`${styles.chatbot} ${isChatOpen ? styles.open : ""}`}>
      {isChatOpen ? (
        <div className={styles.container}>
          <header className={styles.header}>
            <h3>Document Assistant</h3>
            <button 
              onClick={() => setIsChatOpen(false)} 
              className={styles.closeButton}
              aria-label="Close chat"
            >
              ✕
            </button>
          </header>
          <div className={styles.chatbox}>
            <div className={styles.messages}>
              {messages.map((msg, idx) => (
                <div 
                  key={idx} 
                  className={`${styles.message} ${styles[msg.role]}`}
                >
                  {msg.content}
                </div>
              ))}
              {isProcessing && (
                <div className={`${styles.message} ${styles.bot}`}>
                  Processing...
                </div>
              )}
            </div>
            <footer className={styles.footer}>
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                className={styles.input}
                placeholder="Ask about your documents..."
                disabled={isProcessing}
              />
              <button 
                onClick={handleSend} 
                className={styles.sendButton}
                disabled={isProcessing}
              >
                Send
              </button>
            </footer>
          </div>
        </div>
      ) : (
        <button 
          onClick={() => setIsChatOpen(true)} 
          className={styles.openButton}
        >
          Open Chat
        </button>
      )}
    </div>
  );
}
