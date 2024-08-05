import fs from 'fs';
import path from 'path';
import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();

const outputDir = path.resolve(__dirname, '../../data/scraped_data');
const csvFilePath = path.join(outputDir, 'combined_data.csv');
const huggingfaceApiToken = process.env.HUGGINGFACE_API_TOKEN;
const autoTrainProjectId = process.env.AUTOTRAIN_PROJECT_ID;

async function uploadToAutoTrain() {
  const fileStream = fs.createReadStream(csvFilePath);
  
  try {
    const response = await axios.post(`https://api.autotrain.huggingface.co/projects/${autoTrainProjectId}/datasets/upload`, fileStream, {
      headers: {
        'Authorization': `Bearer ${huggingfaceApiToken}`,
        'Content-Type': 'multipart/form-data'
      }
    });
    console.log('File uploaded successfully:', response.data);
  } catch (error) {
    console.error('Error uploading file:', error);
  }
}

uploadToAutoTrain();