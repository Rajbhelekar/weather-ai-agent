import unittest
from unittest.mock import Mock, patch
import requests
from main import get_weather


class TestWeather(unittest.TestCase):

    @patch("main.requests.get")
    def test_city_not_found(self, mock_get):
        mock_get.return_value.json.return_value = {
            "results": []
        }

        result = get_weather("xyzabc123")

        self.assertEqual(
            result,
            {"error": "City not found: xyzabc123"}
        )

    @patch("main.requests.get")
    def test_geocoding_api_failure(self, mock_get):
        mock_get.return_value.raise_for_status.side_effect = (
            requests.exceptions.HTTPError("HTTP 500")
        )

        with self.assertRaises(requests.exceptions.HTTPError):
            get_weather("Mumbai")

    @patch("main.requests.get")
    def test_successful_weather(self, mock_get):
        geo_response = Mock()
        geo_response.json.return_value = {
            "results": [{
                "name": "Mumbai",
                "country": "India",
                "latitude": 19.07,
                "longitude": 72.87
            }]
        }

        weather_response = Mock()
        weather_response.json.return_value = {
            "current": {
                "temperature_2m": 32.0,
                "apparent_temperature": 36.0,
                "relative_humidity_2m": 65,
                "wind_speed_10m": 10.0,
                "precipitation": 0.0,
                "weather_code": 1
            }
        }

        mock_get.side_effect = [geo_response, weather_response]

        result = get_weather("Mumbai")

        self.assertEqual(result["city"], "Mumbai")
        self.assertEqual(result["country"], "India")
        self.assertEqual(result["temperature_°C"], 32.0)
        self.assertEqual(result["humidity_percentage_%"], 65)

    def test_empty_city(self):
        result = get_weather("")
        self.assertEqual(
            result,
            {"error": "Please provide a valid city name."}
        )


    def test_whitespace_city(self):
        result = get_weather("   ")
        self.assertEqual(
            result,
            {"error": "Please provide a valid city name."}
        )


if __name__ == "__main__":
    unittest.main()