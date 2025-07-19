from datetime import date

from fastmcp import FastMCP
from modules.weather.tools import get_hourly_weather_data_tool
from modules.weather.models import MeteoData
from settings import MY_LATITUDE, MY_LONGITUDE

mcp = FastMCP("FastMCP Weather Agent", version="1.0.0")


@mcp.tool(description="Get hourly weather data for a given date range.")
def get_hourly_weather_data(from_date: date, to_date: date) -> MeteoData:
    return get_hourly_weather_data_tool(
        latitude=MY_LATITUDE,
        longitude=MY_LONGITUDE,
        from_date=from_date,
        to_date=to_date)


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8888, path="/mcp")
