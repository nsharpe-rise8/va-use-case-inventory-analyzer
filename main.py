import json
import logging
import os

from src.utils.utils import read_csv
from src.analysis.analysis import analyze_use_case
from src.analysis.analysis_results import AnalysisResult

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Update directory constants
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")

def list_csv_files(directory=RAW_DATA_DIR):
    """Log and list all CSV files in the specified directory."""
    logging.info(f"Listing CSV files in directory: {directory}")
    try:
        files = [f for f in os.listdir(directory) if f.endswith('.csv')]
        if not files:
            logging.warning("No CSV files found in the directory.")
        else:
            logging.info(f"CSV files found: {files}")
        return files
    except Exception as e:
        logging.error(f"Error listing files in directory {directory}: {e}")
        return []

def save_analysis_result(row_id, result: AnalysisResult):
    """Save analysis result to a JSON file in the 'data/processed' folder using the Use Case ID."""
    try:
        os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
        file_path = os.path.join(PROCESSED_DATA_DIR, f"{row_id}.json")
        with open(file_path, "w") as file:
            file.write(result.to_json())
        logging.info(f"Saved analysis result for Use Case ID {row_id} to {file_path}.")
    except Exception as e:
        logging.error(f"Error saving analysis result for Use Case ID {row_id}: {e}")

def get_processed_records():
    """Get list of already processed Use Case IDs from tracking file."""
    processed_records_path = os.path.join(PROCESSED_DATA_DIR, 'processed_records.json')
    try:
        if os.path.exists(processed_records_path):
            with open(processed_records_path, 'r') as f:
                return set(json.load(f))
        return set()
    except Exception as e:
        logging.error(f"Error reading processed records: {e}")
        return set()

def update_processed_records(use_case_id):
    """Add newly processed Use Case ID to tracking file."""
    processed_records_path = os.path.join(PROCESSED_DATA_DIR, 'processed_records.json')
    try:
        processed = get_processed_records()
        processed.add(use_case_id)
        with open(processed_records_path, 'w') as f:
            json.dump(list(processed), f)
    except Exception as e:
        logging.error(f"Error updating processed records: {e}")

def process_csv(file_path):
    logging.info(f"Starting to process CSV file: {file_path}")
    try:
        rows = read_csv(file_path)
        processed_records = get_processed_records()
        
        if not rows:
            logging.warning("No rows found in the CSV file.")
            return

        logging.info(f"Found {len(rows)} rows. {len(processed_records)} already processed.")
        new_records = 0
        
        for index, row in enumerate(rows):
            try:
                use_case_id = row.get('Use Case ID')
                if not use_case_id:
                    logging.warning(f"Row {index + 1} missing Use Case ID. Skipping.")
                    continue
                    
                if use_case_id in processed_records:
                    logging.debug(f"Skipping already processed Use Case ID: {use_case_id}")
                    continue

                logging.info(f"Processing new record: {use_case_id}")
                
                if not ('Purpose and Benefits' in row and 'AI System Outputs' in row):
                    logging.warning(f"Row {index + 1} missing required fields. Skipping.")
                    continue

                description = row['Purpose and Benefits'] + ' ' + row['AI System Outputs']
                analysis_result = analyze_use_case(description)
                save_analysis_result(use_case_id, analysis_result)
                update_processed_records(use_case_id)
                new_records += 1
                
            except Exception as e:
                logging.error(f"Error processing row {index + 1}: {e}")
                
        logging.info(f"Processed {new_records} new records.")
        
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")

if __name__ == "__main__":
    # List available CSV files
    list_csv_files()

    # Update the CSV file path to use the constants
    process_csv(os.path.join(RAW_DATA_DIR, 'use-case-inventory.csv'))
