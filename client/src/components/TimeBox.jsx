import React, { useState, useEffect } from 'react'

const TimeBox = () => {
    const [time, setTime] = useState(new Date().toLocaleTimeString())

    useEffect(() => {
        const interval = setInterval(() => {
            setTime(new Date().toLocaleTimeString())
        }, 1000)

        return () => clearInterval(interval)
    }, [])

    return (
        <div className="fixed right-5 top-1/2 w-80 transform -translate-y-1/2 justify-center items-center flex duration-50 text-gray-700/50 text-6xl" style={{ userSelect: 'none' }}>
            {time}
        </div>
    )
}

export default TimeBox