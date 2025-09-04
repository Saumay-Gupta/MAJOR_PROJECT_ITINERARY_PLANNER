import { motion } from 'motion/react';

const container = {
  hidden: { opacity: 1 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 1.4
    },
  },
};

const sentence = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.03,
    },
  },
};

const letter = {
  hidden: { opacity: 0, x:0 },
  visible: { opacity: 1, x: 5, transition: { duration: 0.9 } },
};

function DayActivity({day,activities}) {
  return (
    <>
      <div className='w-200 ml-10 mt-10 bg-white rounded'>
        <motion.h1 
        className='text-black font medium ml-5'
        variants={letter}
        initial="hidden"
        animate="visible"
        >{day}</motion.h1>
        <motion.div
          className="p-4"
          variants={container}
          initial="hidden"
          animate="visible"
        >
          {activities.map((activity,index) => (
            <motion.p key={index} className="mb-2 mt-2 ml-2 break-words" 
            variants={sentence}
            >
              {activity.split("").map((char,index2)=>(
                <motion.span key={index2} variants={letter}>
                  {char === " " ? "\u00A0" : char}
                </motion.span>
              )
              )}
            </motion.p>
          )
          )}
        </motion.div>
      </div>
    </>
  );
}

export default DayActivity;
