import fs from 'fs';
import path from 'path';

// Variables to store the root folder and its cache
let root_folder = null;
let root_folder_cache = null;

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const { folderPath } = req.body;

    if (!folderPath) {
      return res.status(400).json({ message: 'Folder path is required' });
    }

    // Check if root_folder is null or different from the folderPath
    if (!root_folder || root_folder !== folderPath) {
      root_folder = folderPath; // Update the root_folder
      root_folder_cache = folderPath; // Update the cache
      
      try {
        // Process the files (placeholder function for now)
        const files = processFiles(folderPath);

        return res.status(200).json({
          message: `Files in the folder '${folderPath}' processed successfully.`,
          files,
        });
      } catch (error) {
        return res.status(500).json({
          message: 'Error processing files',
          error: error.message,
        });
      }
    } else {
      return res.status(200).json({
        message: 'Folder has already been processed. No action taken.',
      });
    }
  } else {
    return res.status(405).json({ message: 'Method not allowed' });
  }
}

// Function to process files (placeholder logic)
function processFiles(folderPath) {
  try {
    const absolutePath = path.resolve(folderPath);
    const files = fs.readdirSync(absolutePath); // Read all files in the directory
    return files;
  } catch (error) {
    throw new Error(`Failed to read files in the directory: ${error.message}`);
  }
}
