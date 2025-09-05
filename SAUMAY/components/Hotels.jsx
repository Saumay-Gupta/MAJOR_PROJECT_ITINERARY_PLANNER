import React from 'react'
import { motion } from "motion/react"
import DayActivity from '../components/DayActivity.jsx'

// Hotel Data will be shown later on --

function Hotels({planner}) {
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
      x: 50,
      transition: { duration: 1, ease: "easeOut"},
    },
  };

  return (
      <div className='mt-10'>
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
      </div>
  )
}

export default Hotels
