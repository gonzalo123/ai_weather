"""Unit tests for weather models"""
import pytest
from datetime import datetime
from pydantic import ValidationError

from modules.weather.models import (
    TemperatureReading,
    HumidityReading,
    ApparentTemperatureReading,
    PrecipitationReading,
    EvapotranspirationReading,
    SurfacePressureReading,
    MeteoData
)


class TestTemperatureReading:
    """Test cases for TemperatureReading model"""
    
    def test_valid_temperature_reading(self):
        """Test creating a valid temperature reading"""
        time = datetime(2025, 7, 12, 14, 30)
        reading = TemperatureReading(time=time, value=25.5)
        
        assert reading.time == time
        assert reading.value == 25.5
    
    def test_negative_temperature_allowed(self):
        """Test that negative temperatures are allowed"""
        time = datetime(2025, 1, 15, 6, 0)
        reading = TemperatureReading(time=time, value=-10.2)
        
        assert reading.value == -10.2
    
    def test_extreme_temperatures_allowed(self):
        """Test extreme temperature values are allowed"""
        time = datetime(2025, 7, 12, 14, 30)
        
        # Very hot temperature
        hot_reading = TemperatureReading(time=time, value=50.0)
        assert hot_reading.value == 50.0
        
        # Very cold temperature  
        cold_reading = TemperatureReading(time=time, value=-40.0)
        assert cold_reading.value == -40.0
    
    def test_invalid_time_type(self):
        """Test validation error for invalid time type"""
        with pytest.raises(ValidationError):
            TemperatureReading(time="invalid", value=25.0)
    
    def test_invalid_value_type(self):
        """Test validation error for invalid value type"""
        time = datetime(2025, 7, 12, 14, 30)
        with pytest.raises(ValidationError):
            TemperatureReading(time=time, value="invalid")


class TestHumidityReading:
    """Test cases for HumidityReading model"""
    
    def test_valid_humidity_reading(self):
        """Test creating a valid humidity reading"""
        time = datetime(2025, 7, 12, 14, 30)
        reading = HumidityReading(time=time, value=65)
        
        assert reading.time == time
        assert reading.value == 65
    
    def test_minimum_humidity_value(self):
        """Test minimum humidity value (0%)"""
        time = datetime(2025, 7, 12, 14, 30)
        reading = HumidityReading(time=time, value=0)
        
        assert reading.value == 0
    
    def test_maximum_humidity_value(self):
        """Test maximum humidity value (100%)"""
        time = datetime(2025, 7, 12, 14, 30)
        reading = HumidityReading(time=time, value=100)
        
        assert reading.value == 100
    
    def test_negative_humidity_invalid(self):
        """Test that negative humidity values are invalid"""
        time = datetime(2025, 7, 12, 14, 30)
        with pytest.raises(ValidationError):
            HumidityReading(time=time, value=-1)
    
    def test_humidity_above_100_invalid(self):
        """Test that humidity values above 100% are invalid"""
        time = datetime(2025, 7, 12, 14, 30)
        with pytest.raises(ValidationError):
            HumidityReading(time=time, value=101)
    
    def test_float_humidity_converted_to_int(self):
        """Test that float humidity values require explicit conversion"""
        time = datetime(2025, 7, 12, 14, 30)
        # Pydantic v2 is stricter - floats with fractional parts are not automatically converted
        # We test with a float that can be converted (no fractional part)
        reading = HumidityReading(time=time, value=65.0)
        
        assert reading.value == 65
        assert isinstance(reading.value, int)
        
        # Test that fractional floats raise validation error
        with pytest.raises(ValidationError):
            HumidityReading(time=time, value=65.7)


class TestApparentTemperatureReading:
    """Test cases for ApparentTemperatureReading model"""
    
    def test_valid_apparent_temperature_reading(self):
        """Test creating a valid apparent temperature reading"""
        time = datetime(2025, 7, 12, 14, 30)
        reading = ApparentTemperatureReading(time=time, value=28.3)
        
        assert reading.time == time
        assert reading.value == 28.3
    
    def test_negative_apparent_temperature_allowed(self):
        """Test that negative apparent temperatures are allowed"""
        time = datetime(2025, 1, 15, 6, 0)
        reading = ApparentTemperatureReading(time=time, value=-15.8)
        
        assert reading.value == -15.8


class TestPrecipitationReading:
    """Test cases for PrecipitationReading model"""
    
    def test_valid_precipitation_reading(self):
        """Test creating a valid precipitation reading"""
        time = datetime(2025, 7, 12, 14, 30)
        reading = PrecipitationReading(time=time, value=2.5)
        
        assert reading.time == time
        assert reading.value == 2.5
    
    def test_zero_precipitation_allowed(self):
        """Test that zero precipitation is allowed"""
        time = datetime(2025, 7, 12, 14, 30)
        reading = PrecipitationReading(time=time, value=0.0)
        
        assert reading.value == 0.0
    
    def test_negative_precipitation_invalid(self):
        """Test that negative precipitation values are invalid"""
        time = datetime(2025, 7, 12, 14, 30)
        with pytest.raises(ValidationError):
            PrecipitationReading(time=time, value=-1.0)


class TestEvapotranspirationReading:
    """Test cases for EvapotranspirationReading model"""
    
    def test_valid_evapotranspiration_reading(self):
        """Test creating a valid evapotranspiration reading"""
        time = datetime(2025, 7, 12, 14, 30)
        reading = EvapotranspirationReading(time=time, value=3.2)
        
        assert reading.time == time
        assert reading.value == 3.2
    
    def test_zero_evapotranspiration_allowed(self):
        """Test that zero evapotranspiration is allowed"""
        time = datetime(2025, 7, 12, 14, 30)
        reading = EvapotranspirationReading(time=time, value=0.0)
        
        assert reading.value == 0.0
    
    def test_negative_evapotranspiration_allowed(self):
        """Test that negative evapotranspiration values are allowed"""
        time = datetime(2025, 7, 12, 14, 30)
        reading = EvapotranspirationReading(time=time, value=-0.5)
        
        assert reading.value == -0.5


class TestSurfacePressureReading:
    """Test cases for SurfacePressureReading model"""
    
    def test_valid_surface_pressure_reading(self):
        """Test creating a valid surface pressure reading"""
        time = datetime(2025, 7, 12, 14, 30)
        reading = SurfacePressureReading(time=time, value=1013.25)
        
        assert reading.time == time
        assert reading.value == 1013.25
    
    def test_zero_pressure_invalid(self):
        """Test that zero pressure is invalid"""
        time = datetime(2025, 7, 12, 14, 30)
        with pytest.raises(ValidationError):
            SurfacePressureReading(time=time, value=0.0)
    
    def test_negative_pressure_invalid(self):
        """Test that negative pressure values are invalid"""
        time = datetime(2025, 7, 12, 14, 30)
        with pytest.raises(ValidationError):
            SurfacePressureReading(time=time, value=-10.0)
    
    def test_very_low_positive_pressure_valid(self):
        """Test that very low positive pressure values are valid"""
        time = datetime(2025, 7, 12, 14, 30)
        reading = SurfacePressureReading(time=time, value=0.1)
        
        assert reading.value == 0.1


class TestMeteoData:
    """Test cases for MeteoData model"""
    
    def test_valid_meteo_data(self):
        """Test creating a valid MeteoData object"""
        time = datetime(2025, 7, 12, 14, 30)
        
        meteo_data = MeteoData(
            temperature=[TemperatureReading(time=time, value=25.0)],
            humidity=[HumidityReading(time=time, value=60)],
            apparent_temperature=[ApparentTemperatureReading(time=time, value=27.0)],
            precipitation=[PrecipitationReading(time=time, value=0.0)],
            evapotranspiration=[EvapotranspirationReading(time=time, value=2.5)],
            surface_pressure=[SurfacePressureReading(time=time, value=1013.25)]
        )
        
        assert len(meteo_data.temperature) == 1
        assert len(meteo_data.humidity) == 1
        assert len(meteo_data.apparent_temperature) == 1
        assert len(meteo_data.precipitation) == 1
        assert len(meteo_data.evapotranspiration) == 1
        assert len(meteo_data.surface_pressure) == 1
    
    def test_empty_meteo_data(self):
        """Test creating MeteoData with empty lists"""
        meteo_data = MeteoData(
            temperature=[],
            humidity=[],
            apparent_temperature=[],
            precipitation=[],
            evapotranspiration=[],
            surface_pressure=[]
        )
        
        assert len(meteo_data.temperature) == 0
        assert len(meteo_data.humidity) == 0
        assert len(meteo_data.apparent_temperature) == 0
        assert len(meteo_data.precipitation) == 0
        assert len(meteo_data.evapotranspiration) == 0
        assert len(meteo_data.surface_pressure) == 0
    
    def test_multiple_readings_meteo_data(self):
        """Test MeteoData with multiple readings for each type"""
        time1 = datetime(2025, 7, 12, 14, 0)
        time2 = datetime(2025, 7, 12, 15, 0)
        
        meteo_data = MeteoData(
            temperature=[
                TemperatureReading(time=time1, value=25.0),
                TemperatureReading(time=time2, value=26.0)
            ],
            humidity=[
                HumidityReading(time=time1, value=60),
                HumidityReading(time=time2, value=58)
            ],
            apparent_temperature=[
                ApparentTemperatureReading(time=time1, value=27.0),
                ApparentTemperatureReading(time=time2, value=28.5)
            ],
            precipitation=[
                PrecipitationReading(time=time1, value=0.0),
                PrecipitationReading(time=time2, value=1.2)
            ],
            evapotranspiration=[
                EvapotranspirationReading(time=time1, value=2.5),
                EvapotranspirationReading(time=time2, value=3.1)
            ],
            surface_pressure=[
                SurfacePressureReading(time=time1, value=1013.25),
                SurfacePressureReading(time=time2, value=1012.8)
            ]
        )
        
        assert len(meteo_data.temperature) == 2
        assert len(meteo_data.humidity) == 2
        assert len(meteo_data.apparent_temperature) == 2
        assert len(meteo_data.precipitation) == 2
        assert len(meteo_data.evapotranspiration) == 2
        assert len(meteo_data.surface_pressure) == 2
        
        # Verify specific values
        assert meteo_data.temperature[0].value == 25.0
        assert meteo_data.temperature[1].value == 26.0
        assert meteo_data.humidity[0].value == 60
        assert meteo_data.humidity[1].value == 58
    
    def test_meteo_data_invalid_reading_types(self):
        """Test validation error when invalid reading types are provided"""
        with pytest.raises(ValidationError):
            MeteoData(
                temperature=["invalid"],
                humidity=[],
                apparent_temperature=[],
                precipitation=[],
                evapotranspiration=[],
                surface_pressure=[]
            )
