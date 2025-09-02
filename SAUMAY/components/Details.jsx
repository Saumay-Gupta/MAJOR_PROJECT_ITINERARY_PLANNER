import { useState } from "react";

function Details() {
  let [destination, setDestination] = useState("");
  
  let [to, setTo] = useState("");
  let [from,setFrom] = useState("");

  let [budget, setBudget] = useState("");
  let [group, setGroup] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = { destination, days, budget, group };

    try {
      const res = await fetch("http://localhost:5000/api/details", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      const result = await res.json();
      console.log("Server Response:", result);
    } catch (err) {
      console.error("Error:", err);
    }
  };

  return (
    <div className="h-full w-full flex flex-col items-center pt-10">
      <div className="h-full w-200">
        <h1 className="text-2xl font-medium">Tell us your travel preferences !!</h1>
        <p className="pt-1">
          Just provide some basic information, and our trip planner will generate
          a customized itinerary based on your preferences.
        </p>

        <form onSubmit={handleSubmit}>
          <h1 className="font-medium pt-8">What is your destination of choice?</h1>
          <input
            type="text"
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
            placeholder="Ex. Manali"
            className="border border-black w-full pl-2 rounded"
          />

          <h1 className="font-medium pt-8">When you are planning?</h1>
          <div className="flex">
            <div className="flex flex-col">
              <span className="mt-2 mb-1">Start Date</span>
              <input
                type="date"
                value={to}
                onChange={(e) => setTo(e.target.value)}
                className="border border-black w-50 pl-2 rounded"
              />
            </div>
            <div className="flex flex-col">
              <span className="mt-2 mb-1 mx-8">End Date</span>
              <input
                type="date"
                value={from}
                onChange={(e) => setFrom(e.target.value)}
                className="border border-black w-50 pl-2 rounded mx-8"
              />
            </div>
          </div>

          <h1 className="font-medium pt-10">What is your budget?</h1>
          <div className="flex flex-row mt-1">
            <div
              className={`border p-5 mt-3 mb-3 rounded cursor-pointer ${
                budget === "cheap" ? "border-amber-400" : "border-gray-300"
              }`}
              onClick={() => setBudget("cheap")}
            >
              <p className="font-medium">Cheap</p>
              <p>Stay conscious of costs</p>
            </div>
            <div
              className={`border p-5 mx-4 mt-3 mb-3 rounded cursor-pointer ${
                budget === "moderate" ? "border-amber-400" : "border-gray-300"
              }`}
              onClick={() => setBudget("moderate")}
            >
              <p className="font-medium">Medium</p>
              <p>Keep cost on the average side</p>
            </div>
            <div
              className={`border p-5 mt-3 mb-3 rounded cursor-pointer ${
                budget === "luxury" ? "border-amber-400" : "border-gray-300"
              }`}
              onClick={() => setBudget("luxury")}
            >
              <p className="font-medium">Luxury</p>
              <p>Don't worry about cost</p>
            </div>
          </div>

          <h1 className="font-medium pt-5">
            Who do you plan on travelling with?
          </h1>
          <div className="flex flex-row pt-1">
            <div
              className={`border p-5 mt-3 mb-3 rounded cursor-pointer ${
                group === "justMe" ? "border-amber-400" : "border-gray-300"
              }`}
              onClick={() => setGroup("justMe")}
            >
              <p className="font-medium">Just Me</p>
            </div>
            <div
              className={`border p-5 mt-3 mb-3 mx-4 rounded cursor-pointer ${
                group === "couple" ? "border-amber-400" : "border-gray-300"
              }`}
              onClick={() => setGroup("couple")}
            >
              <p className="font-medium">Couple</p>
            </div>
            <div
              className={`border p-5 mt-3 mb-3 rounded cursor-pointer ${
                group === "family" ? "border-amber-400" : "border-gray-300"
              }`}
              onClick={() => setGroup("family")}
            >
              <p className="font-medium">Family</p>
            </div>
            <div
              className={`border p-5 mt-3 mb-3 mx-4 rounded cursor-pointer ${
                group === "friends" ? "border-amber-400" : "border-gray-300"
              }`}
              onClick={() => setGroup("friends")}
            >
              <p className="font-medium">Friends</p>
            </div>
          </div>


          <div className="flex items-center justify-center">
            <button
              type="submit"
              className="text-white bg-black text-medium w-40 mt-5 p-2 border"
            >
              Submit Details
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Details;
