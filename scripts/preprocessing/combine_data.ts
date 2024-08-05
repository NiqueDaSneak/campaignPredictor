import fs from 'fs';
import csvParser from 'csv-parser';
import path from 'path';

const directoryPath = path.join(__dirname, '../../data/scraped_data');
const combinedData: any[] = [];

fs.readdir(directoryPath, (err, files) => {
    if (err) {
        return console.log('Unable to scan directory: ' + err);
    }

    files.forEach(file => {
        if (file.endsWith('.csv')) {
            const filePath = path.join(directoryPath, file);
            fs.createReadStream(filePath)
                .pipe(csvParser())
                .on('data', (data) => combinedData.push(data))
                .on('end', () => {
                    console.log('CSV file successfully processed');
                    // Save combined data
                    const combinedDataPath = path.join(directoryPath, 'combined_data.csv');
                    fs.writeFileSync(combinedDataPath, JSON.stringify(combinedData, null, 4));
                });
        }
    });
});