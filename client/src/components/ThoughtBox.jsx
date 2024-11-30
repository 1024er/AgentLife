import React, { useState, useEffect } from 'react'

const ThoughtBox = ({
    characters,
    selectedAvatar
}) => {
    const [currentCharacter, setCurrentCharacter] = useState(null)
    const [isAnimating, setIsAnimating] = useState(false)
    const [currentThought, setCurrentThought] = useState('')
    

    useEffect(() => {
        const newCharacter = characters?.find(character => character.id === selectedAvatar)
        if (newCharacter && newCharacter !== currentCharacter) {
            setIsAnimating(true)
            setTimeout(() => {
                setCurrentCharacter(newCharacter)
                setIsAnimating(false)
            }, 100) // 动画持续时间
        }
    }, [characters, selectedAvatar])

    useEffect(() => {
        if (currentCharacter) {
            setIsAnimating(true)
            setTimeout(() => {
                setIsAnimating(false)
            }, 100) // 动画持续时间
        }
    }, [currentCharacter?.current_thought])

    return (
        <>
            <div className={`fixed top-5 left-1/4 w-1/2 h-12 backdrop-blur-sm shadow-lg rounded-3xl flex items-center justify-center text-slate-700 align-baseline p-4 font-normal text-xs overflow-auto transition-transform ${isAnimating ? 'animate-slide-out' : 'animate-slide-in'}`} style={{ userSelect: 'none' }}>
                {currentCharacter ? `【${currentCharacter.name}的当前内心】${currentCharacter.current_thought}` : ''}
            </div>
        </>
    )
}

export default ThoughtBox