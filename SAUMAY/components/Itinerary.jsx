import React from 'react'
import { motion } from "motion/react"
import DayActivity from '../components/DayActivity.jsx'

function Ininerary({planner}) {

  const container = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 1,
      },
    },
  };

  const card = {
    hidden: { opacity: 0, x: 0 },
    visible: {
      opacity: 1,
      x: 10,
      transition: { duration: 1, ease: "easeOut"},
    },
  };

  return (
      <motion.div
        className="flex flex-wrap"
        variants={container}
        initial="hidden"
        animate="visible"
      >
        {planner.map((plan, i) => (
          <motion.div key={i} variants={card}>
            <DayActivity day={plan.day} activities={plan.activities} />
          </motion.div>
        ))}
      </motion.div>
  )
}

export default Ininerary
