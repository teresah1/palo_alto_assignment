import io
import unittest
from unittest.mock import patch, MagicMock

import requests

from sol import get_domain_details, format_date_iso, create_output_table

class TestSol(unittest.TestCase):

    @patch('sol.requests.get')
    def test_get_domain_details_success(self, mock_get):
        # Mock successful response
        mock_get.return_value = MagicMock(json=lambda: {
            "WhoisRecord": {
                "domainName": "example.com",
                "registrarName": "Example Registrar",
                "createdDate": "2000-01-01T00:00:00Z",
                "expiresDate": "2030-01-01T00:00:00Z",
                "estimatedDomainAge": "24",
                "nameServers": {"hostNames": ["ns1.example.com"]},
                "registrant": {"name": "John Doe", "email": "john.doe@example.com"}
            }
        })

        result = get_domain_details("example.com", "mock_api_key")
        self.assertEqual(result["WhoisRecord"]["domainName"], "example.com")

    @patch('sol.requests.get')
    def test_get_domain_details_failure(self, mock_get):
        # Mock API failure
        mock_get.side_effect = requests.exceptions.RequestException("Failed to fetch data")
        result = get_domain_details("example.com", "mock_api_key")
        self.assertIsNone(result)

    def test_format_date_iso(self):
        # Test valid and invalid dates
        self.assertEqual(format_date_iso("2000-01-01T00:00:00+00:00"), "2000-01-01T00:00:00+00:00")
        self.assertEqual(format_date_iso("invalid-date"), "N/A")

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_create_output_table(self, mock_stdout):
        # Mock WHOIS data
        whois_data = {
            "domainName": "example.com",
            "registrarName": "Example Registrar",
            "createdDate": "2000-01-01T00:00:00Z",
            "expiresDate": "2030-01-01T00:00:00Z",
            "estimatedDomainAge": "24",
            "nameServers": {"hostNames": ["ns1.example.com"]},
            "registrant": {"name": "John Doe", "email": "john.doe@example.com"}
        }

        create_output_table(whois_data)
        output = mock_stdout.getvalue()

        self.assertIn("**Domain Name**", output)
        self.assertIn("example.com", output)

if __name__ == '__main__':
    unittest.main()
