import { useState } from 'react'
import Details from './components/Details.jsx'
import Weather from './components/Weather.jsx'
import Ininerary from './components/Itinerary.jsx';

function App() {

  // This weatherData will be fetched through Pyhton API later on--
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

  // This weatherData will be fetched through Pyhton API later on--
  const planner = [
    { day: "Day 1 - Paris", activities: ["Visit Eiffel Tower", "Louvre Museum"] },
    { day: "Day 2 - Rome", activities: ["Colosseum tour", "Vatican City"] },
    { day: "Day 3 - London", activities: ["Big Ben", "London Eye"] },
  ];

  return (
    <>
      {/* <Header /> */}
      {/* <Details /> */}
      <Weather forecast={weatherData.weather_forecast} />
      <Ininerary planner={planner}/>
    </>
  )
}

export default App
