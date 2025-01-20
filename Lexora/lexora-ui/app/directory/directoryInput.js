"use client";

import { useState } from "react";
import styles from "./directoryInput.module.css";

export default function DirectoryInput({ onPathSubmit }) {
  const [directory, setDirectory] = useState(""); // User input for the directory path
  const [rootFolder, setRootFolder] = useState(null); // Tracks the set folder path
  const [statusMessage, setStatusMessage] = useState(""); // Status messages for the user

  const handleSetFolder = (e) => {
    e.preventDefault();
    if (directory.trim()) {
      setRootFolder(directory.trim()); // Set the folder path and lock the input
    }
  };

  const handleProcessFiles = () => {
    if (rootFolder) {
      onPathSubmit(rootFolder); // Pass the folder path to the parent component
    }
  };

  return (
    <div className={styles.container}>
      <form className={styles.form} onSubmit={handleSetFolder}>
        <h1 className={styles.title}>Enter a Directory Path</h1>
        <p className={styles.description}>
          Please provide the directory path you want to access.
        </p>
        <div className={styles.inputGroup}>
          {/* If the folder is not set, show the input field; otherwise, display the set path */}
          {!rootFolder ? (
            <>
              <input
                type="text"
                value={directory}
                onChange={(e) => setDirectory(e.target.value)}
                className={styles.input}
                placeholder="/path/to/directory"
                required
              />
              <button type="submit" className={styles.button}>
                Set Folder
              </button>
            </>
          ) : (
            <div className={styles.setPath}>
              <span className={styles.pathLabel}>Set Folder Path:</span>
              <span className={styles.path}>{rootFolder}</span>
              <button
                type="button"
                onClick={handleProcessFiles}
                className={styles.processButton}
              >
                Process Files
              </button>
            </div>
          )}
        </div>
      </form>
      {statusMessage && <p className={styles.statusMessage}>{statusMessage}</p>}
    </div>
  );
}
