import unittest
from unittest.mock import patch, mock_open
from utils import read_csv

class TestUtils(unittest.TestCase):
    def test_read_csv(self):
        # Mock CSV content
        csv_content = (
            "Use Case ID,Purpose and Benefits,AI System Outputs\n"
            "1,Test purpose,Test output\n"
            "2,Another purpose,Another output"
        )
        
        # Create mock file with our test content
        with patch('builtins.open', mock_open(read_data=csv_content)):
            result = read_csv('dummy.csv')
            
            # Verify the results
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]['Use Case ID'], '1')
            self.assertEqual(result[0]['Purpose and Benefits'], 'Test purpose')
            self.assertEqual(result[0]['AI System Outputs'], 'Test output')

if __name__ == '__main__':
    unittest.main() 