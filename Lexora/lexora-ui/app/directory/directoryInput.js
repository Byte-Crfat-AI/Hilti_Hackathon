"use client";

import { useState } from "react";
import styles from "./directoryInput.module.css";

export default function DirectoryInput({ onPathSubmit }) {
  const [directory, setDirectory] = useState("");
  const [rootFolder, setRootFolder] = useState(null);
  const [statusMessage, setStatusMessage] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);

  const handleSetFolder = async (e) => {
    e.preventDefault();
    const path = directory.trim();
    
    if (path) {
      try {
        setIsProcessing(true);
        setStatusMessage("Validating directory...");
        
        //directory validation logic
        setRootFolder(path);
        setStatusMessage("");
      } catch (error) {
        setStatusMessage("Error validating directory: " + error.message);
      } finally {
        setIsProcessing(false);
      }
    }
  };

  const handleProcessFiles = () => {
    if (rootFolder) {
      setStatusMessage("Initiating file processing...");
      onPathSubmit(rootFolder);
    }
  };

  const handleReset = () => {
    setRootFolder(null);
    setDirectory("");
    setStatusMessage("");
  };

  return (
    <div className={styles.container}>
      <form className={styles.form} onSubmit={handleSetFolder}>
        <h1 className={styles.title}>Document Processing System</h1>
        <p className={styles.description}>
          Enter the directory path containing your documents for processing.
        </p>
        
        <div className={styles.inputGroup}>
          {!rootFolder ? (
            <>
              <input
                type="text"
                value={directory}
                onChange={(e) => setDirectory(e.target.value)}
                className={styles.input}
                placeholder="/path/to/documents"
                required
                disabled={isProcessing}
              />
              <button 
                type="submit" 
                className={styles.button}
                disabled={isProcessing}
              >
                {isProcessing ? "Validating..." : "Set Folder"}
              </button>
            </>
          ) : (
            <div className={styles.setPath}>
              <span className={styles.pathLabel}>Selected Directory:</span>
              <span className={styles.path}>{rootFolder}</span>
              <div className={styles.buttonGroup}>
                <button
                  type="button"
                  onClick={handleProcessFiles}
                  className={styles.processButton}
                  disabled={isProcessing}
                >
                  Process Files
                </button>
                <button
                  type="button"
                  onClick={handleReset}
                  className={styles.resetButton}
                  disabled={isProcessing}
                >
                  Reset
                </button>
              </div>
            </div>
          )}
        </div>
      </form>
      
      {statusMessage && (
        <p className={`${styles.statusMessage} ${isProcessing ? styles.processing : ''}`}>
          {statusMessage}
        </p>
      )}
    </div>
  );
}