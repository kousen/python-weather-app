import pytest
import json
from unittest.mock import patch, Mock
from main import app


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHomePage:
    def test_home_page_renders(self, client):
        """Test that home page loads successfully"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Weather' in response.data
        assert b'Search for a city' in response.data
    
    def test_home_page_post_redirect(self, client):
        """Test that posting a city name redirects correctly"""
        response = client.post('/', data={'search': 'London'})
        assert response.status_code == 302
        assert response.location == '/London'
    
    def test_home_page_sanitizes_input(self, client):
        """Test that special characters are removed from input"""
        response = client.post('/', data={'search': 'New@#$York123'})
        assert response.status_code == 302
        assert response.location == '/NewYork'
    
    def test_empty_search_redirects_to_error(self, client):
        """Test that empty search redirects to error page"""
        response = client.post('/', data={'search': ''})
        assert response.status_code == 302
        assert response.location == '/error'


class TestCityWeather:
    @patch('main.get_weather_data')
    @patch('main.requests.get')  
    def test_single_city_result(self, mock_get, mock_weather_data, client):
        """Test weather display for single city result"""
        # Mock geocoding API response
        geocoding_response = Mock()
        geocoding_response.json.return_value = [{
            'name': 'London',
            'lat': 51.5074,
            'lon': -0.1278,
            'country': 'GB',
            'state': 'England'
        }]
        geocoding_response.raise_for_status = Mock()
        mock_get.return_value = geocoding_response
        
        # Mock weather data helper function
        mock_weather_data.return_value = {
            'metric': {
                'current': {
                    'main': {
                        'temp': 15.5,
                        'temp_min': 13.0,
                        'temp_max': 18.0,
                        'humidity': 65,
                        'feels_like': 16.2
                    },
                    'weather': [{'main': 'Clouds'}],
                    'wind': {'speed': 3.5},
                    'sys': {
                        'sunrise': 1609459200,
                        'sunset': 1609488000
                    }
                },
                'forecast': {
                    'list': [
                        {'dt_txt': '2024-01-01 12:00:00', 'main': {'temp': 16.0}, 'weather': [{'main': 'Clouds'}]},
                        {'dt_txt': '2024-01-02 12:00:00', 'main': {'temp': 17.0}, 'weather': [{'main': 'Rain'}]},
                        {'dt_txt': '2024-01-03 12:00:00', 'main': {'temp': 14.0}, 'weather': [{'main': 'Clear'}]},
                        {'dt_txt': '2024-01-04 12:00:00', 'main': {'temp': 15.0}, 'weather': [{'main': 'Clouds'}]},
                        {'dt_txt': '2024-01-05 12:00:00', 'main': {'temp': 16.0}, 'weather': [{'main': 'Rain'}]},
                    ]
                }
            },
            'imperial': {
                'current': {
                    'main': {
                        'temp': 59.9,
                        'temp_min': 55.4,
                        'temp_max': 64.4,
                        'humidity': 65,
                        'feels_like': 61.2
                    },
                    'weather': [{'main': 'Clouds'}],
                    'wind': {'speed': 3.5},
                    'sys': {
                        'sunrise': 1609459200,
                        'sunset': 1609488000
                    }
                },
                'forecast': {
                    'list': [
                        {'dt_txt': '2024-01-01 12:00:00', 'main': {'temp': 60.8}, 'weather': [{'main': 'Clouds'}]},
                        {'dt_txt': '2024-01-02 12:00:00', 'main': {'temp': 62.6}, 'weather': [{'main': 'Rain'}]},
                        {'dt_txt': '2024-01-03 12:00:00', 'main': {'temp': 57.2}, 'weather': [{'main': 'Clear'}]},
                        {'dt_txt': '2024-01-04 12:00:00', 'main': {'temp': 59.0}, 'weather': [{'main': 'Clouds'}]},
                        {'dt_txt': '2024-01-05 12:00:00', 'main': {'temp': 60.8}, 'weather': [{'main': 'Rain'}]},
                    ]
                }
            }
        }
        
        response = client.get('/London')
        assert response.status_code == 200
        assert b'London, England, GB' in response.data
        assert b'16' in response.data  # Temperature
        assert b'Clouds' in response.data
    
    @patch('main.requests.get')
    def test_multiple_city_results(self, mock_get, client):
        """Test city selection page for multiple results"""
        # Mock geocoding API response with multiple cities
        geocoding_response = Mock()
        geocoding_response.json.return_value = [
            {
                'name': 'Springfield',
                'lat': 39.7817,
                'lon': -89.6501,
                'country': 'US',
                'state': 'Illinois'
            },
            {
                'name': 'Springfield',
                'lat': 42.1015,
                'lon': -72.5898,
                'country': 'US',
                'state': 'Massachusetts'
            },
            {
                'name': 'Springfield',
                'lat': 37.2090,
                'lon': -93.2923,
                'country': 'US',
                'state': 'Missouri'
            }
        ]
        geocoding_response.raise_for_status = Mock()
        
        mock_get.return_value = geocoding_response
        
        response = client.get('/Springfield')
        assert response.status_code == 200
        assert b'Multiple cities found' in response.data
        assert b'Illinois' in response.data
        assert b'Massachusetts' in response.data
        assert b'Missouri' in response.data
    
    @patch('main.get_weather_data')
    def test_weather_by_coords(self, mock_weather_data, client):
        """Test weather display when selecting from multiple cities"""
        # Mock weather data helper function
        mock_weather_data.return_value = {
            'metric': {
                'current': {
                    'main': {
                        'temp': 20.5,
                        'temp_min': 18.0,
                        'temp_max': 23.0,
                        'humidity': 70,
                        'feels_like': 21.1
                    },
                    'weather': [{'main': 'Clear'}],
                    'wind': {'speed': 2.5},
                    'sys': {
                        'sunrise': 1609459200,
                        'sunset': 1609488000
                    }
                },
                'forecast': {
                    'list': [
                        {'dt_txt': '2024-01-01 12:00:00', 'main': {'temp': 21.0}, 'weather': [{'main': 'Clear'}]},
                        {'dt_txt': '2024-01-02 12:00:00', 'main': {'temp': 22.0}, 'weather': [{'main': 'Clear'}]},
                        {'dt_txt': '2024-01-03 12:00:00', 'main': {'temp': 19.0}, 'weather': [{'main': 'Clouds'}]},
                        {'dt_txt': '2024-01-04 12:00:00', 'main': {'temp': 20.0}, 'weather': [{'main': 'Clear'}]},
                        {'dt_txt': '2024-01-05 12:00:00', 'main': {'temp': 21.0}, 'weather': [{'main': 'Clear'}]},
                    ]
                }
            },
            'imperial': {
                'current': {
                    'main': {
                        'temp': 68.9,
                        'temp_min': 64.4,
                        'temp_max': 73.4,
                        'humidity': 70,
                        'feels_like': 70.0
                    },
                    'weather': [{'main': 'Clear'}],
                    'wind': {'speed': 2.5},
                    'sys': {
                        'sunrise': 1609459200,
                        'sunset': 1609488000
                    }
                },
                'forecast': {
                    'list': [
                        {'dt_txt': '2024-01-01 12:00:00', 'main': {'temp': 69.8}, 'weather': [{'main': 'Clear'}]},
                        {'dt_txt': '2024-01-02 12:00:00', 'main': {'temp': 71.6}, 'weather': [{'main': 'Clear'}]},
                        {'dt_txt': '2024-01-03 12:00:00', 'main': {'temp': 66.2}, 'weather': [{'main': 'Clouds'}]},
                        {'dt_txt': '2024-01-04 12:00:00', 'main': {'temp': 68.0}, 'weather': [{'main': 'Clear'}]},
                        {'dt_txt': '2024-01-05 12:00:00', 'main': {'temp': 69.8}, 'weather': [{'main': 'Clear'}]},
                    ]
                }
            }
        }
        
        response = client.post('/weather', data={
            'lat': '39.7817',
            'lon': '-89.6501',
            'display_name': 'Springfield, Illinois, US'
        })
        
        assert response.status_code == 200
        assert b'Springfield, Illinois, US' in response.data
        assert b'21' in response.data  # Temperature
        assert b'Clear' in response.data


class TestErrorHandling:
    @patch('main.requests.get')
    def test_city_not_found(self, mock_get, client):
        """Test error page when city is not found"""
        geocoding_response = Mock()
        geocoding_response.json.return_value = []
        geocoding_response.raise_for_status = Mock()
        
        mock_get.return_value = geocoding_response
        
        response = client.get('/InvalidCityName')
        assert response.status_code == 302
        assert response.location == '/error'
    
    @patch('main.requests.get')
    def test_api_error_handling(self, mock_get, client):
        """Test error handling when API fails"""
        import requests
        mock_get.side_effect = requests.exceptions.RequestException("API Error")
        
        response = client.get('/London')
        assert response.status_code == 302
        assert response.location == '/error'
    
    def test_error_page_renders(self, client):
        """Test that error page displays correctly"""
        response = client.get('/error')
        assert response.status_code == 200
        assert b'This city does not exist' in response.data
    
    def test_weather_coords_missing_data(self, client):
        """Test error when coordinates are missing"""
        response = client.post('/weather', data={
            'lat': '39.7817',
            # Missing lon and display_name
        })
        assert response.status_code == 302
        assert response.location == '/error'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])