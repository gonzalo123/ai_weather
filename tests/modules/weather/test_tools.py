"""Unit tests for weather tools"""
import pytest
from datetime import datetime, date
from unittest.mock import Mock, patch

from modules.weather.tools import Tools
from modules.weather.models import MeteoData


class TestTools:
    """Test cases for Tools class"""
    
    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.latitude = 40.7128
        self.longitude = -74.0060
        self.tools_instance = Tools(latitude=self.latitude, longitude=self.longitude)
    
    def test_tools_initialization(self):
        """Test Tools class initialization"""
        assert self.tools_instance.latitude == self.latitude
        assert self.tools_instance.longitude == self.longitude
    
    def test_get_tools_returns_list(self):
        """Test that get_tools returns a list"""
        tools = self.tools_instance.get_tools()
        assert isinstance(tools, list)
        assert len(tools) == 1
    
    def test_get_tools_function_name(self):
        """Test that the returned tool has the correct function name"""
        tools = self.tools_instance.get_tools()
        tool_function = tools[0]
        assert tool_function.__name__ == "get_hourly_weather_data"
    
    @patch('modules.weather.tools.requests.get')
    def test_get_hourly_weather_data_success(self, mock_get):
        """Test successful API call and data processing"""
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            'hourly': {
                'time': [
                    '2025-07-12T14:00',
                    '2025-07-12T15:00'
                ],
                'temperature_2m': [25.5, 26.0],
                'relative_humidity_2m': [60, 58],
                'apparent_temperature': [27.0, 28.5],
                'precipitation': [0.0, 1.2],
                'evapotranspiration': [2.5, 3.1],
                'surface_pressure': [1013.25, 1012.8]
            }
        }
        mock_get.return_value = mock_response
        
        # Get the tool function
        tools = self.tools_instance.get_tools()
        get_hourly_weather_data = tools[0]
        
        # Test the function
        from_date = date(2025, 7, 12)
        to_date = date(2025, 7, 12)
        
        result = get_hourly_weather_data(from_date=from_date, to_date=to_date)
        
        # Verify API call
        expected_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={self.latitude}&"
            f"longitude={self.longitude}&"
            f"hourly=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,evapotranspiration,surface_pressure&"
            f"start_date=2025-07-12&"
            f"end_date=2025-07-12"
        )
        mock_get.assert_called_once_with(expected_url)
        
        # Verify result type and structure
        assert isinstance(result, MeteoData)
        assert len(result.temperature) == 2
        assert len(result.humidity) == 2
        assert len(result.apparent_temperature) == 2
        assert len(result.precipitation) == 2
        assert len(result.evapotranspiration) == 2
        assert len(result.surface_pressure) == 2
        
        # Verify specific values
        assert result.temperature[0].value == 25.5
        assert result.temperature[1].value == 26.0
        assert result.humidity[0].value == 60
        assert result.humidity[1].value == 58
        assert result.apparent_temperature[0].value == 27.0
        assert result.apparent_temperature[1].value == 28.5
        assert result.precipitation[0].value == 0.0
        assert result.precipitation[1].value == 1.2
        assert result.evapotranspiration[0].value == 2.5
        assert result.evapotranspiration[1].value == 3.1
        assert result.surface_pressure[0].value == 1013.25
        assert result.surface_pressure[1].value == 1012.8
        
        # Verify timestamps
        expected_time1 = datetime(2025, 7, 12, 14, 0)
        expected_time2 = datetime(2025, 7, 12, 15, 0)
        
        assert result.temperature[0].time == expected_time1
        assert result.temperature[1].time == expected_time2
    
    @patch('modules.weather.tools.requests.get')
    def test_get_hourly_weather_data_empty_response(self, mock_get):
        """Test handling of empty API response"""
        # Setup mock response with empty data
        mock_response = Mock()
        mock_response.json.return_value = {
            'hourly': {
                'time': [],
                'temperature_2m': [],
                'relative_humidity_2m': [],
                'apparent_temperature': [],
                'precipitation': [],
                'evapotranspiration': [],
                'surface_pressure': []
            }
        }
        mock_get.return_value = mock_response
        
        # Get the tool function
        tools = self.tools_instance.get_tools()
        get_hourly_weather_data = tools[0]
        
        # Test the function
        from_date = date(2025, 7, 12)
        to_date = date(2025, 7, 12)
        
        result = get_hourly_weather_data(from_date=from_date, to_date=to_date)
        
        # Verify result is empty but valid MeteoData
        assert isinstance(result, MeteoData)
        assert len(result.temperature) == 0
        assert len(result.humidity) == 0
        assert len(result.apparent_temperature) == 0
        assert len(result.precipitation) == 0
        assert len(result.evapotranspiration) == 0
        assert len(result.surface_pressure) == 0
    
    @patch('modules.weather.tools.requests.get')
    def test_get_hourly_weather_data_single_reading(self, mock_get):
        """Test processing of single weather reading"""
        # Setup mock response with single reading
        mock_response = Mock()
        mock_response.json.return_value = {
            'hourly': {
                'time': ['2025-07-12T14:00'],
                'temperature_2m': [25.5],
                'relative_humidity_2m': [60],
                'apparent_temperature': [27.0],
                'precipitation': [0.0],
                'evapotranspiration': [2.5],
                'surface_pressure': [1013.25]
            }
        }
        mock_get.return_value = mock_response
        
        # Get the tool function
        tools = self.tools_instance.get_tools()
        get_hourly_weather_data = tools[0]
        
        # Test the function
        from_date = date(2025, 7, 12)
        to_date = date(2025, 7, 12)
        
        result = get_hourly_weather_data(from_date=from_date, to_date=to_date)
        
        # Verify result has exactly one reading for each metric
        assert len(result.temperature) == 1
        assert len(result.humidity) == 1
        assert len(result.apparent_temperature) == 1
        assert len(result.precipitation) == 1
        assert len(result.evapotranspiration) == 1
        assert len(result.surface_pressure) == 1
        
        # Verify values
        assert result.temperature[0].value == 25.5
        assert result.humidity[0].value == 60
        assert result.apparent_temperature[0].value == 27.0
        assert result.precipitation[0].value == 0.0
        assert result.evapotranspiration[0].value == 2.5
        assert result.surface_pressure[0].value == 1013.25
        
        # Verify timestamp
        expected_time = datetime(2025, 7, 12, 14, 0)
        assert result.temperature[0].time == expected_time
    
    @patch('modules.weather.tools.requests.get')
    def test_get_hourly_weather_data_different_coordinates(self, mock_get):
        """Test API call with different coordinates"""
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            'hourly': {
                'time': ['2025-07-12T14:00'],
                'temperature_2m': [20.0],
                'relative_humidity_2m': [70],
                'apparent_temperature': [22.0],
                'precipitation': [5.0],
                'evapotranspiration': [1.8],
                'surface_pressure': [1020.0]
            }
        }
        mock_get.return_value = mock_response
        
        # Create tools instance with different coordinates
        different_lat = 51.5074
        different_lon = -0.1278
        tools_instance = Tools(latitude=different_lat, longitude=different_lon)
        
        # Get the tool function
        tools = tools_instance.get_tools()
        get_hourly_weather_data = tools[0]
        
        # Test the function
        from_date = date(2025, 7, 12)
        to_date = date(2025, 7, 12)
        
        result = get_hourly_weather_data(from_date=from_date, to_date=to_date)
        
        # Verify API call with correct coordinates
        expected_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={different_lat}&"
            f"longitude={different_lon}&"
            f"hourly=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,evapotranspiration,surface_pressure&"
            f"start_date=2025-07-12&"
            f"end_date=2025-07-12"
        )
        mock_get.assert_called_once_with(expected_url)
        
        # Verify result
        assert isinstance(result, MeteoData)
        assert result.temperature[0].value == 20.0
    
    @patch('modules.weather.tools.requests.get')
    def test_get_hourly_weather_data_date_range(self, mock_get):
        """Test API call with different date range"""
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            'hourly': {
                'time': ['2025-07-10T14:00'],
                'temperature_2m': [23.0],
                'relative_humidity_2m': [65],
                'apparent_temperature': [25.0],
                'precipitation': [2.5],
                'evapotranspiration': [2.0],
                'surface_pressure': [1015.0]
            }
        }
        mock_get.return_value = mock_response
        
        # Get the tool function
        tools = self.tools_instance.get_tools()
        get_hourly_weather_data = tools[0]
        
        # Test with different date range
        from_date = date(2025, 7, 10)
        to_date = date(2025, 7, 15)
        
        result = get_hourly_weather_data(from_date=from_date, to_date=to_date)
        
        # Verify API call with correct date range
        expected_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={self.latitude}&"
            f"longitude={self.longitude}&"
            f"hourly=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,evapotranspiration,surface_pressure&"
            f"start_date=2025-07-10&"
            f"end_date=2025-07-15"
        )
        mock_get.assert_called_once_with(expected_url)
        
        # Verify result
        assert isinstance(result, MeteoData)
    
    @patch('modules.weather.tools.requests.get')
    @patch('modules.weather.tools.logger')
    def test_get_hourly_weather_data_logging(self, mock_logger, mock_get):
        """Test that logging is called correctly"""
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            'hourly': {
                'time': ['2025-07-12T14:00', '2025-07-12T15:00'],
                'temperature_2m': [25.5, 26.0],
                'relative_humidity_2m': [60, 58],
                'apparent_temperature': [27.0, 28.5],
                'precipitation': [0.0, 1.2],
                'evapotranspiration': [2.5, 3.1],
                'surface_pressure': [1013.25, 1012.8]
            }
        }
        mock_get.return_value = mock_response
        
        # Get the tool function
        tools = self.tools_instance.get_tools()
        get_hourly_weather_data = tools[0]
        
        # Test the function
        from_date = date(2025, 7, 12)
        to_date = date(2025, 7, 12)
        
        get_hourly_weather_data(from_date=from_date, to_date=to_date)
        
        # Verify logging was called
        mock_logger.info.assert_called_once()
        log_call_args = mock_logger.info.call_args[0][0]
        assert "[get_hourly_weather_data]" in log_call_args
        assert "2025-07-12" in log_call_args
        assert "2 records found" in log_call_args
    
    @patch('modules.weather.tools.requests.get')
    def test_get_hourly_weather_data_extreme_values(self, mock_get):
        """Test handling of extreme weather values"""
        # Setup mock response with extreme values
        mock_response = Mock()
        mock_response.json.return_value = {
            'hourly': {
                'time': ['2025-07-12T14:00'],
                'temperature_2m': [-40.0],  # Extreme cold
                'relative_humidity_2m': [100],  # Maximum humidity
                'apparent_temperature': [-45.0],  # Extreme apparent cold
                'precipitation': [100.0],  # Heavy precipitation
                'evapotranspiration': [0.0],  # No evapotranspiration
                'surface_pressure': [950.0]  # Low pressure
            }
        }
        mock_get.return_value = mock_response
        
        # Get the tool function
        tools = self.tools_instance.get_tools()
        get_hourly_weather_data = tools[0]
        
        # Test the function
        from_date = date(2025, 7, 12)
        to_date = date(2025, 7, 12)
        
        result = get_hourly_weather_data(from_date=from_date, to_date=to_date)
        
        # Verify extreme values are handled correctly
        assert result.temperature[0].value == -40.0
        assert result.humidity[0].value == 100
        assert result.apparent_temperature[0].value == -45.0
        assert result.precipitation[0].value == 100.0
        assert result.evapotranspiration[0].value == 0.0
        assert result.surface_pressure[0].value == 950.0
    
    def test_tools_with_negative_coordinates(self):
        """Test Tools initialization with negative coordinates"""
        negative_lat = -34.6037
        negative_lon = -58.3816
        tools_instance = Tools(latitude=negative_lat, longitude=negative_lon)
        
        assert tools_instance.latitude == negative_lat
        assert tools_instance.longitude == negative_lon
    
    def test_tools_with_zero_coordinates(self):
        """Test Tools initialization with zero coordinates"""
        tools_instance = Tools(latitude=0.0, longitude=0.0)
        
        assert tools_instance.latitude == 0.0
        assert tools_instance.longitude == 0.0
