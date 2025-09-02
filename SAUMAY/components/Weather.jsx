import React, { useEffect, useState } from 'react'

function Weather({forecast}) {
  return (
    <>
      <div className='flex flex-col items-center justify-center mt-10'>
        <h1 className='text-3xl font-medium'>Weather</h1>
        <div className='flex bg-blue-100 justify-center rounded p-2'>

            <div className={`grid grid-cols-${forecast.length} gap-4`}>
              {forecast.map((day, index) => (
                <div key={index} className="border rounded p-4 shadow">
                  <p>{day.condition}</p>
                  <img 
                    src={`utilities/${day.condition}.png`} 
                    alt={day.condition} className='w-20 h-20'/>
                  <h2 className="font-medium">{day.date}</h2>
                  <p>🌡 {day.temperature.min}°C - {day.temperature.max}°C</p>
                  <p>💧 Humidity: {day.humidity}%</p>
                  <p>🌬 Wind: {day.wind_speed} km/h</p>
                </div>
              ))}
            </div>

        </div>
      </div>
    </>
  )
}

export default Weather
