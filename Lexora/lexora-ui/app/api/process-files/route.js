import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';
import { NextResponse } from 'next/server';

function getLexoraPath(currentPath) {
  const match = currentPath.match(/^(.*[\\/](Lexora))(?:[\\/]|$)/);
  if (match) {
    return match[1];
  }
  return null;
}

const lexoraPath = getLexoraPath(process.cwd());
if (!lexoraPath) {
  throw new Error("Lexora path not found in the current working directory");
}
console.log('Lexora path:', lexoraPath);
const PROCESSING_SCRIPT = path.join(lexoraPath, 'lexora-ui/public/Backend.py');
console.log('Processing script:', PROCESSING_SCRIPT);
let rootFolderCache = null;

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
      try {
        // Directly attempt to query without setup
        console.log('Query:', query);
        const retrievalResult = await runPythonScript(PROCESSING_SCRIPT, ['query', query]);

        return NextResponse.json({
          success: true,
          message: 'Direct query processed.',
          data: { response: retrievalResult },
        });
      } catch (error) {
        console.error('Error during direct query processing:', error);
        return NextResponse.json(
          {
            success: false,
            message: 'Error processing direct query.',
            error: error.message
          },
          { status: 500 }
        );
      }
    }
  } catch (error) {
    console.error('Error in POST request:', error);
    return NextResponse.json(
      { success: false, message: 'Internal server error.', error: error.message },
      { status: 500 }
    );
  }
}

async function runPythonScript(scriptPath, args) {
  return new Promise((resolve, reject) => {
    const process = spawn('python', [scriptPath, ...args]);

    let output = '';
    process.stdout.on('data', (data) => {
      output += data.toString();
    });

    process.stderr.on('data', (data) => {
      console.error('Python script error:', data.toString());
    });

    process.on('close', (code) => {
      if (code === 0) {
        resolve(output);
      } else {
        reject(new Error(`Python script exited with code ${code}`));
      }
    });
  });
}