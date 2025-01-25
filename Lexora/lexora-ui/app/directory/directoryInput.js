"use client";

import { useState, useCallback, useRef } from "react";
import { Folder, FolderOpen, RefreshCw, Check, X, Clock, FileText, Send } from "lucide-react";
import styles from "./directoryInput.module.css";

export default function DirectoryInput({ onPathSubmit }) {
  const [directory, setDirectory] = useState("");
  const [rootFolder, setRootFolder] = useState(null);
  const [statusMessage, setStatusMessage] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [directoryHistory, setDirectoryHistory] = useState([]);
  const [validationError, setValidationError] = useState("");
  const [directQuery, setDirectQuery] = useState("");
  const [isDirectQueryMode, setIsDirectQueryMode] = useState(false);
  const fileInputRef = useRef(null);

  const handleSetFolder = async (e) => {
    e.preventDefault();
    const path = directory.trim();

    if (!path) {
      setValidationError("Please enter a directory path");
      return;
    }

    try {
      setIsProcessing(true);
      setValidationError("");
      setStatusMessage("Validating directory...");

      // Simulated directory validation 
      await new Promise((resolve) => setTimeout(resolve, 1000));

      // Enhanced validation checks
      if (path.length < 3) {
        throw new Error("Invalid directory path");
      }

      setRootFolder(path);
      setDirectoryHistory((prev) => {
        const updatedHistory = [path, ...prev.filter(p => p !== path)];
        return updatedHistory.slice(0, 5); // Limit history to 5 recent paths
      });
      setStatusMessage("");
    } catch (error) {
      setValidationError(error.message || "Directory validation failed");
    } finally {
      setIsProcessing(false);
    }
  };

  const handleProcessFiles = async () => {
    if (rootFolder) {
      setStatusMessage("Processing files...");
      setProgress(0);
      setIsProcessing(true);

      try {
        // Simulated file processing with more realistic progress
        for (let i = 1; i <= 10; i++) {
          await new Promise((resolve) => setTimeout(resolve, 250));
          setProgress(i * 10);
        }

        setStatusMessage("File processing completed!");
        onPathSubmit(rootFolder);
      } catch (error) {
        setStatusMessage("File processing failed");
      } finally {
        setIsProcessing(false);
      }
    }
  };

  const handleDirectQuery = () => {
    const query = directQuery.trim();
    if (query) {
      // Pass null as directory path to indicate direct query mode
      onPathSubmit(null, query);
    } else {
      setValidationError("Please enter a query");
    }
  };

  const handleReset = () => {
    setRootFolder(null);
    setDirectory("");
    setStatusMessage("");
    setProgress(0);
    setValidationError("");
    setDirectQuery("");
    setIsDirectQueryMode(false);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleHistorySelect = (path) => {
    setDirectory(path);
    setValidationError("");
  };

  const handleFileInputChange = (e) => {
    const selectedPath = e.target.files[0]?.path;
    if (selectedPath) {
      setDirectory(selectedPath);
      setValidationError("");
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <form className={styles.form} onSubmit={handleSetFolder}>
          <div className={styles.formHeader}>
            <FolderOpen className={styles.icon} />
            <h1 className={styles.title}>Lexora</h1>
            <p className={styles.description}>
              {isDirectQueryMode 
                ? "Enter a direct query without processing files" 
                : "Select a directory containing your documents"}
            </p>
          </div>

          <div className={styles.inputSection}>
            {!rootFolder ? (
              <>
                {!isDirectQueryMode ? (
                  <>
                    <div className={styles.inputWrapper}>
                      <input
                        type="text"
                        value={directory}
                        onChange={(e) => {
                          setDirectory(e.target.value);
                          setValidationError("");
                        }}
                        className={`${styles.input} ${validationError ? styles.inputError : ''}`}
                        placeholder="/path/to/documents"
                        disabled={isProcessing}
                      />
                      <input
                        type="file"
                        ref={fileInputRef}
                        onChange={handleFileInputChange}
                        webkitdirectory="true"
                        directory="true"
                        className={styles.fileInput}
                      />
                      <button 
                        type="button" 
                        onClick={() => fileInputRef.current?.click()}
                        className={styles.folderSelectButton}
                        disabled={isProcessing}
                      >
                        <Folder />
                      </button>
                    </div>
                    {validationError && (
                      <p className={styles.errorMessage}>{validationError}</p>
                    )}
                    <div className={styles.buttonGroup}>
                      <button
                        type="submit"
                        className={styles.button}
                        disabled={isProcessing}
                      >
                        {isProcessing ? "Validating..." : "Set Folder"}
                      </button>
                      <button
                        type="button"
                        onClick={() => setIsDirectQueryMode(true)}
                        className={styles.alternateButton}
                      >
                        Direct Query
                      </button>
                    </div>
                  </>
                ) : (
                  <>
                    <div className={styles.inputWrapper}>
                      <input
                        type="text"
                        value={directQuery}
                        onChange={(e) => {
                          setDirectQuery(e.target.value);
                          setValidationError("");
                        }}
                        className={`${styles.input} ${validationError ? styles.inputError : ''}`}
                        placeholder="Enter your query..."
                        disabled={isProcessing}
                      />
                    </div>
                    {validationError && (
                      <p className={styles.errorMessage}>{validationError}</p>
                    )}
                    <div className={styles.buttonGroup}>
                      <button
                        type="button"
                        onClick={handleDirectQuery}
                        className={styles.button}
                        disabled={isProcessing}
                      >
                        Send Query
                      </button>
                      <button
                        type="button"
                        onClick={() => setIsDirectQueryMode(false)}
                        className={styles.alternateButton}
                      >
                        Back to Folder
                      </button>
                    </div>
                  </>
                )}
              </>
            ) : (
              <div className={styles.selectedPathSection}>
                <div className={styles.selectedPathInfo}>
                  <Check className={styles.successIcon} />
                  <div>
                    <span className={styles.pathLabel}>Selected Directory:</span>
                    <span className={styles.path}>{rootFolder}</span>
                  </div>
                </div>
                <div className={styles.actionButtons}>
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
                    <X /> Reset
                  </button>
                </div>
              </div>
            )}
          </div>

          {progress > 0 && (
            <div className={styles.progressContainer}>
              <div className={styles.progressBar}>
                <div
                  className={styles.progress}
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
              <span className={styles.progressText}>{progress}% Complete</span>
            </div>
          )}

          {statusMessage && (
            <div className={`${styles.statusMessageContainer} ${isProcessing ? styles.processing : ''}`}>
              <Clock className={styles.statusIcon} />
              <p className={styles.statusMessage}>{statusMessage}</p>
            </div>
          )}
        </form>

        {directoryHistory.length > 0 && (
          <div className={styles.historySection}>
            <h2 className={styles.historyTitle}>
              <FileText /> Recent Directories
            </h2>
            <ul className={styles.historyList}>
              {directoryHistory.map((path, index) => (
                <li
                  key={index}
                  className={styles.historyItem}
                  onClick={() => handleHistorySelect(path)}
                >
                  {path}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}