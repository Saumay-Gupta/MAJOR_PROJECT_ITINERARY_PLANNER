import React from "react";
import { NavLink } from "react-router-dom";

function HeaderRoute() {
  return (
    <div className="w-full flex justify-center mt-5">
      <ul className="flex gap-20 font-medium text-xl">
        <li>
          <NavLink
            to="/"
            className={({ isActive }) =>
              isActive ? "text-orange-500" : ""
            }
          >
            Planner
          </NavLink>
        </li>
        <li>
          <NavLink
            to="Hotels"
            className={({ isActive }) =>
              isActive ? "text-orange-500" : ""
            }
          >
            Hotels
          </NavLink>
        </li>
        <li>
          <NavLink
            to="CabServices"
            className={({ isActive }) =>
              isActive ? "text-orange-500" : ""
            }
          >
            Cab-Services
          </NavLink>
        </li>
        <li>
          <NavLink
            to="SuggestedPlaces"
            className={({ isActive }) =>
              isActive ? "text-orange-500" : ""
            }
          >
            Suggested Places
          </NavLink>
        </li>
      </ul>
    </div>
  );
}

export default HeaderRoute;
