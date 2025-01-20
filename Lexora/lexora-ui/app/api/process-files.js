import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';

let root_folder = null;
let root_folder_cache = null;

const PROCESSING_SCRIPT = 'Lexora/Processing/main_processing.py';
const EXTRACTION_SCRIPT = 'Lexora/Keyword_Extraction/main_keyword_extraction.py';
const RETRIEVAL_SCRIPT = 'Lexora/Retrival/main_retrieval.py';

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const { folderPath, query } = req.body;

    if (!folderPath && !query) {
      return res.status(400).json({ message: 'Folder path or query is required' });
    }

    if (folderPath) {
      try {
        if (!root_folder || root_folder !== folderPath) {
          root_folder = folderPath;
          root_folder_cache = folderPath;

          const processedFiles = await runPythonScript(PROCESSING_SCRIPT, [folderPath]);
          const extractionResult = await runPythonScript(EXTRACTION_SCRIPT, [processedFiles]);

          return res.status(200).json({
            success: true,
            message: `Files in '${folderPath}' processed successfully.`,
            data: extractionResult,
          });
        } else {
          return res.status(200).json({
            success: true,
            message: 'Folder already processed',
            cached: true
          });
        }
      } catch (error) {
        console.error('Processing error:', error);
        return res.status(500).json({
          success: false,
          message: 'Error processing files',
          error: error.message
        });
      }
    }

    if (query) {
      try {
        if (!root_folder_cache) {
          return res.status(400).json({
            success: false,
            message: 'No processed folder available for query'
          });
        }

        const retrievalResult = await runPythonScript(RETRIEVAL_SCRIPT, [query, root_folder_cache]);
        return res.status(200).json({
          success: true,
          message: 'Query processed successfully',
          data: retrievalResult
        });
      } catch (error) {
        console.error('Retrieval error:', error);
        return res.status(500).json({
          success: false,
          message: 'Error processing query',
          error: error.message
        });
      }
    }
  }
  
  return res.status(405).json({ message: 'Method not allowed' });
}

async function runPythonScript(scriptPath, args = []) {
  return new Promise((resolve, reject) => {
    const absolutePath = path.resolve(scriptPath);
    const pythonProcess = spawn('python', [absolutePath, ...args]);

    let data = '';
    let error = '';

    pythonProcess.stdout.on('data', (chunk) => {
      data += chunk.toString();
    });

    pythonProcess.stderr.on('data', (chunk) => {
      error += chunk.toString();
    });

    pythonProcess.on('close', (code) => {
      if (code === 0) {
        try {
          resolve(JSON.parse(data));
        } catch (parseError) {
          reject(new Error(`Failed to parse output: ${parseError.message}`));
        }
      } else {
        reject(new Error(`Script failed (${code}): ${error}`));
      }
    });
  });
}
