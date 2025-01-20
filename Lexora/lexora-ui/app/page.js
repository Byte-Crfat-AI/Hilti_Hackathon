"use client";

import { useState } from "react";
import DirectoryInput from "./directory/directoryInput";
import Chatbot from "./chatbot/chatbot";

export default function Home() {
  const [directoryPath, setDirectoryPath] = useState(null); // Tracks the folder path for the chatbot

  const handlePathSubmit = (path) => {
    setDirectoryPath(path); // Set the directory path and trigger chatbot
  };

  return (
    <div>
      {!directoryPath ? (
        <DirectoryInput onPathSubmit={handlePathSubmit} />
      ) : (
        <Chatbot directoryPath={directoryPath} />
      )}
    </div>
  );
}
