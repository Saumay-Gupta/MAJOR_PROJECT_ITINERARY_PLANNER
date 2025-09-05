import { useState } from 'react'
import BeforeLogIn from './components/BeforeLogIn'
import AfterLogIn from './components/AfterLogIn'
import Itinerary from './components/Itinerary';
import Hotels from './components/Hotels';
import { createBrowserRouter,RouterProvider, Navigate} from 'react-router-dom';
import CabServices from './components/CabServices';
import SuggestedPlaces from './components/SuggestedPlaces';

function App() {
    // This Planner Data will be recieved from Python file later-on:- 
    const planner = [
        { day: "Day 1 - Paris", activities: ["Visit Eiffel Tower", "Louvre Museum"] },
        { day: "Day 2 - Rome", activities: ["Colosseum tour", "Vatican City"] },
        { day: "Day 3 - London", activities: ["Big Ben", "London Eye"] },
    ];
    
    const [isLoggedIn, setIsLoggedIn] = useState(true);

    const router = createBrowserRouter([
    {
      path: "/",
      element: isLoggedIn ? <AfterLogIn /> : <BeforeLogIn />,
      children: isLoggedIn
        ? [
            {
              path: "/",
              element: <Itinerary planner={planner}/>,
            },
            {
              path: "Hotels",
              element: <Hotels planner={planner}/>,
            },
            {
              path: "CabServices",
              element: <CabServices/>,
            },
            {
              path: "SuggestedPlaces",
              element: <SuggestedPlaces/>,
            }
          ]
        : [],
    },
    ]);

    return (
      <RouterProvider router={router} />
    )
}

export default App
