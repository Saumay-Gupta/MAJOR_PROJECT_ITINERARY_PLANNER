import React from 'react'
import Weather from './Weather'
import {Outlet} from 'react-router-dom';
import HeaderRoute from './Routes/HeaderRoute';

function AfterLogIn() {
    // This Weather Data will be fetched through Pyhton API later on--
    const weatherData = {
    "destination": "Manali",
    "start_date": "2025-09-10",
    "end_date": "2025-09-15",
    "weather_forecast": [
        {
        "date": "2025-09-10",
        "temperature": {
            "min": 14,
            "max": 22
        },
        "condition": "Partly Cloudy",
        "humidity": 65,
        "wind_speed": 10
        },
        {
        "date": "2025-09-11",
        "temperature": {
            "min": 13,
            "max": 20
        },
        "condition": "Rain Showers",
        "humidity": 72,
        "wind_speed": 12
        },
        {
        "date": "2025-09-12",
        "temperature": {
            "min": 13,
            "max": 20
        },
        "condition": "Rain Showers",
        "humidity": 72,
        "wind_speed": 12
        }
    ]
    };

    return (
        <>
            <Weather forecast={weatherData.weather_forecast} />
            <HeaderRoute />
            <Outlet />
        </>
    )
}

export default AfterLogIn
