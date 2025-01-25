"use client";

import { useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";
import styles from "./chatbot.module.css";

export default function Chatbot({ directoryPath, directQuery, onClose }) {
  const router = useRouter();
  const [isChatOpen, setIsChatOpen] = useState(true);
  const [messages, setMessages] = useState([
    { role: "bot", content: "Hello! I'm Lexora, How can I help you with your documents?" },
  ]);
  const [input, setInput] = useState(directQuery || "");
  const [isProcessing, setIsProcessing] = useState(false);
  const [hasProcessedInitialQuery, setHasProcessedInitialQuery] = useState(false);
  
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isProcessing]);

  useEffect(() => {
    if (directoryPath) {
      processDirectory(directoryPath);
    } else if (directQuery && !hasProcessedInitialQuery) {
      handleQuery(directQuery);
      setHasProcessedInitialQuery(true);
    }
  }, [directoryPath, directQuery]);

  const processDirectory = async (path) => {
    try {
      setIsProcessing(true);
      const response = await fetch("/api/process-files", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ folderPath: path }),
      });

      const result = await response.json();

      if (result.success) {
        addMessage(
          "bot",
          result.cached
            ? "Directory already processed. Ready for questions!"
            : "Directory processed successfully. What would you like to know?"
        );
      } else {
        addMessage(
          "bot",
          "Sorry, I had trouble processing the directory. Please try again."
        );
      }
    } catch (error) {
      addMessage(
        "bot",
        "Error processing directory. Please check the path and try again."
      );
    } finally {
      setIsProcessing(false);
    }
  };

  const handleQuery = async (query) => {
    try {
      setIsProcessing(true);
      const response = await fetch("/api/process-files", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      const result = await response.json();

      if (result.success) {
        addMessage(
          "bot",
          result.data.response ||
            "I found relevant information but couldn't format it properly."
        );
      } else {
        addMessage(
          "bot",
          "Sorry, I couldn't process your query. Please try again."
        );
      }
    } catch (error) {
      addMessage("bot", "Error processing your query. Please try again.");
    } finally {
      setIsProcessing(false);
    }
  };

  const addMessage = (role, content) => {
    setMessages((prev) => [...prev, { role, content }]);
  };

  const handleSend = async () => {
    if (!input.trim() || isProcessing) return;

    const userMessage = input.trim();
    setInput("");
    addMessage("user", userMessage);
    await handleQuery(userMessage);
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleClose = () => {
    onClose(); // Notify parent to clear directoryPath and directQuery
    router.push("/"); // Redirect to directory input page
  };

  return (
    <div className={`${styles.chatbot} ${isChatOpen ? styles.open : ""}`}>
      <div className={styles.container}>
        <header className={styles.header}>
          <h3>Lexora</h3>
          <button
            onClick={handleClose}
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
            {/* Add a dummy div to scroll to */}
            <div ref={messagesEndRef} />
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
    </div>
  );
}