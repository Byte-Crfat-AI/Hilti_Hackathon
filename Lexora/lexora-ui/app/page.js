"use client";

import { useState } from "react";
import DirectoryInput from "./directory/directoryInput";
import Chatbot from "./chatbot/chatbot";

export default function Home() {
  const [directoryPath, setDirectoryPath] = useState(null);
  const [directQuery, setDirectQuery] = useState(null);

  const handlePathSubmit = (path, query = null) => {
    setDirectoryPath(path);
    setDirectQuery(query);
  };

  const handleChatClose = () => {
    setDirectoryPath(null);
    setDirectQuery(null);
  };

  return (
    <div>
      {!directoryPath && !directQuery ? (
        <DirectoryInput onPathSubmit={handlePathSubmit} />
      ) : (
        <Chatbot 
          directoryPath={directoryPath} 
          directQuery={directQuery} 
          onClose={handleChatClose} 
        />
      )}
    </div>
  );
}