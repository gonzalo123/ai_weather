import logging
from datetime import datetime, date
from typing import List

import requests
from strands import tool

from modules.weather.models import (
    TemperatureReading, HumidityReading, ApparentTemperatureReading,
    PrecipitationReading, EvapotranspirationReading, SurfacePressureReading, MeteoData)

logger = logging.getLogger(__name__)


def get_hourly_weather_data_tool(latitude: float, longitude: float, from_date: date, to_date: date) -> MeteoData:
    """
    Get hourly weather data for a specific date range.
    Notes:
        - The response is a MeteoData object containing lists of readings for temperature, humidity,
          apparent temperature, precipitation, evapotranspiration, and surface pressure.
        - Each reading has a timestamp and a value.

    Returns:
        MeteoData: Object containing weather readings for the specified date range
    """

    start_date = from_date.strftime('%Y-%m-%d')
    end_date = to_date.strftime('%Y-%m-%d')
    url = (f"https://api.open-meteo.com/v1/forecast?"
           f"latitude={latitude}&"
           f"longitude={longitude}&"
           f"hourly=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,evapotranspiration,surface_pressure&"
           f"start_date={start_date}&"
           f"end_date={end_date}")
    response = requests.get(url)

    meteo = MeteoData(
        temperature=[],
        humidity=[],
        apparent_temperature=[],
        precipitation=[],
        evapotranspiration=[],
        surface_pressure=[]
    )
    data = response.json()

    weather_data_time = data['hourly']['time']

    logger.info(f"[get_hourly_weather_data] Fetched weather data from {start_date} to {end_date}. {len(weather_data_time)} records found.")
    for iso in weather_data_time:
        time = datetime.fromisoformat(iso)
        meteo.temperature.append(TemperatureReading(
            time=time,
            value=data['hourly']['temperature_2m'][data['hourly']['time'].index(iso)]))
        meteo.humidity.append(HumidityReading(
            time=time,
            value=data['hourly']['relative_humidity_2m'][data['hourly']['time'].index(iso)]))
        meteo.apparent_temperature.append(ApparentTemperatureReading(
            time=time,
            value=data['hourly']['apparent_temperature'][data['hourly']['time'].index(iso)]))
        meteo.precipitation.append(PrecipitationReading(
            time=time,
            value=data['hourly']['precipitation'][data['hourly']['time'].index(iso)]))
        meteo.evapotranspiration.append(EvapotranspirationReading(
            time=time,
            value=data['hourly']['evapotranspiration'][data['hourly']['time'].index(iso)]))
        meteo.surface_pressure.append(SurfacePressureReading(
            time=time,
            value=data['hourly']['surface_pressure'][data['hourly']['time'].index(iso)]))
    return meteo

class Tools:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    def get_tools(self) -> List[tool]:
        @tool
        def get_hourly_weather_data(from_date: date, to_date: date) -> MeteoData:
            return get_hourly_weather_data_tool(
                latitude=self.latitude,
                longitude=self.longitude,
                from_date=from_date,
                to_date=to_date
            )

        return [get_hourly_weather_data, ]
