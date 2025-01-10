```jsx
import React, { useState, useEffect, useRef } from "react";
import { motion, useInView } from "framer-motion";

function About({ data }) {
    const ref = useRef(null); // Reference to track the section
    const isInView = useInView(ref, {
        once: true,
        margin: "0px 0px -100px 0px",
    }); // Trigger only once when 100px above the viewport

    return (
        <div className="md:w-1/2 text-center md:text-start" ref={ref}>
            <motion.div
                initial={{ opacity: 0, y: 50 }}
                animate={isInView ? { opacity: 1, y: 0 } : {}}
                transition={{ duration: 0.8, ease: "easeOut" }}
            ></motion.div>
        </div>
    );
}

export default About;
```
