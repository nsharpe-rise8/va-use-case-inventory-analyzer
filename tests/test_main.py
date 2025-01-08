import unittest
import os
import json
from unittest.mock import patch, mock_open
from main import (
    list_csv_files,
    save_analysis_result,
    get_processed_records,
    update_processed_records
)

class TestMainFunctions(unittest.TestCase):
    def setUp(self):
        # This runs before each test
        self.test_dir = "test_results"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

    def tearDown(self):
        # This runs after each test
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)

    def test_list_csv_files(self):
        with patch('os.listdir') as mock_listdir:
            # Test with CSV files
            mock_listdir.return_value = ['file1.csv', 'file2.csv', 'file3.txt']
            result = list_csv_files()
            self.assertEqual(result, ['file1.csv', 'file2.csv'])

            # Test with no CSV files
            mock_listdir.return_value = ['file1.txt', 'file2.pdf']
            result = list_csv_files()
            self.assertEqual(result, [])

    def test_save_analysis_result(self):
        test_id = "test123"
        test_data = {"result": "test_analysis"}
        
        m = mock_open()
        with patch('builtins.open', m), patch('json.dump') as mock_dump:
            save_analysis_result(test_id, test_data)
            
            # Assert file was opened with correct path
            m.assert_called_once_with(
                os.path.join("results", "test123.json"), 
                "w"
            )
            
            # Assert json.dump was called with correct data
            mock_dump.assert_called_once_with(
                test_data,
                m(),
                indent=4
            )

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_processed_records_existing_file(self, mock_file, mock_exists):
        # Mock file existence check
        mock_exists.return_value = True
        # Mock JSON file with existing records
        mock_file.return_value.__enter__().read.return_value = '["id1", "id2"]'
        result = get_processed_records()
        self.assertEqual(result, {"id1", "id2"})

    def test_get_processed_records_no_file(self):
        # Test when file doesn't exist
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = False
            result = get_processed_records()
            self.assertEqual(result, set())

    def test_update_processed_records(self):
        test_id = "test123"
        mock_data = '["existing_id"]'
        
        with patch('builtins.open', new_callable=mock_open, read_data=mock_data) as m:
            update_processed_records(test_id)
            # Check if file was written to
            m.assert_called_with('processed_records.json', 'w')

if __name__ == '__main__':
    unittest.main() 