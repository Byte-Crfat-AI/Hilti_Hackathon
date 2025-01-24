"use client";

import { useState } from "react";
import DirectoryInput from "./directory/directoryInput";
import Chatbot from "./chatbot/chatbot";

export default function Home() {
  const [directoryPath, setDirectoryPath] = useState(null);

  const handlePathSubmit = (path) => {
    setDirectoryPath(path); 
  };

  const handleChatClose = () => {
    setDirectoryPath(null)
  };

  return (
    <div>
      {!directoryPath ? (
        <DirectoryInput onPathSubmit={handlePathSubmit} />
      ) : (
        <Chatbot directoryPath={directoryPath} onClose={handleChatClose} />
      )}
    </div>
  );
}

