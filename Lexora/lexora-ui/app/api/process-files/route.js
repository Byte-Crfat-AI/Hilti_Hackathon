import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';
import { NextResponse } from 'next/server';

// Correct path to the Python script
const PROCESSING_SCRIPT = '/home/dev303/Documents/Hilti_Hackathon/Lexora/lexora-ui/public/Backend.py';
let rootFolderCache = null; // Cache the processed folder path globally

export async function POST(request) {
  try {
    const body = await request.json();
    const { folderPath, query } = body;

    if (!folderPath && !query) {
      return NextResponse.json(
        { success: false, message: 'Folder path or query is required.' },
        { status: 400 }
      );
    }

    if (folderPath) {
      if (!fs.existsSync(folderPath)) {
        return NextResponse.json(
          { success: false, message: 'Folder path does not exist.' },
          { status: 404 }
        );
      }

      try {
        const processingResult = await runPythonScript(PROCESSING_SCRIPT, ['setup', folderPath]);
        rootFolderCache = folderPath;

        return NextResponse.json({
          success: true,
          cached: false,
          message: `Files in '${folderPath}' processed successfully.`,
          data: processingResult,
        });
      } catch (error) {
        console.error('Error during folder processing:', error);
        return NextResponse.json(
          { success: false, message: 'Error processing files.', error: error.message },
          { status: 500 }
        );
      }
    }

    if (query) {
      if (!rootFolderCache) {
        return NextResponse.json(
          {
            success: false,
            message: 'No processed folder available for query. Process a folder first.',
          },
          { status: 400 }
        );
      }

      try {
        const retrievalResult = await runPythonScript(PROCESSING_SCRIPT, ['query', query]);

        return NextResponse.json({
          success: true,
          message: 'Query processed successfully.',
          data: retrievalResult,
        });
      } catch (error) {
        console.error('Error during query processing:', error);
        return NextResponse.json(
          { success: false, message: 'Error processing query.', error: error.message },
          { status: 500 }
        );
      }
    }
  } catch (error) {
    console.error('Unexpected error:', error);
    return NextResponse.json(
      { success: false, message: 'An unexpected error occurred.', error: error.message },
      { status: 500 }
    );
  }
}

async function runPythonScript(scriptPath, args = []) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', [scriptPath, ...args]);

    let outputData = '';
    let errorData = '';

    pythonProcess.stdout.on('data', (chunk) => {
      outputData += chunk.toString();
    });

    pythonProcess.stderr.on('data', (chunk) => {
      errorData += chunk.toString();
    });

    pythonProcess.on('close', (code) => {
      if (code === 0) {
        try {
          const parsedData = JSON.parse(outputData);
          resolve(parsedData);
        } catch (e) {
          reject(new Error('Failed to parse output from script.'));
        }
      } else {
        reject(new Error(`Script failed with code ${code}: ${errorData}`));
      }
    });
  });
}
