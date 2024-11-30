import { useMemo, useState, useEffect } from "react";
import { onWatchNumAtom } from "./Avatar";
import { useAtom } from "jotai";


const InfoboxLeft = ({
  characters,
  selectedAvatar
}) => {
  const [showHungerChange, setShowHungerChange] = useState(false);
  const [showEnergeChange, setShowEnergeChange] = useState(false);

  const [onWatchNum] = useAtom(onWatchNumAtom);

  const currentCharacter = characters?.find(character => character.id === selectedAvatar);

  const hungerPercentage = useMemo(() => {
    if (!currentCharacter) return 0;
    return currentCharacter?.current_hunger / currentCharacter.max_hunger * 100;
  }, [currentCharacter?.current_hunger]);

  const hungerChangePercentage = useMemo(() => {
    if (!currentCharacter) return 0;
    return currentCharacter?.hunger_change / currentCharacter.max_hunger * 100;
  }, [currentCharacter?.hunger_change]);

  const energerePercentage = useMemo(() => {
    if (!currentCharacter) return 0;
    return currentCharacter.current_energe / currentCharacter.max_energe * 100;
  }, [currentCharacter?.current_energe]);

  const energereChangePercentage = useMemo(() => {
    if (!currentCharacter) return 0;
    return currentCharacter.energe_change / currentCharacter.max_energe * 100;
  }, [currentCharacter?.energe_change]);

  useEffect(() => {
    if (currentCharacter?.hunger_change) {
      setShowHungerChange(true);
      const timer = setTimeout(() => {
        setShowHungerChange(false);
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [currentCharacter?.hunger_change]);

  useEffect(() => {
    if (currentCharacter?.energe_change) {
      setShowEnergeChange(true);
      const timer = setTimeout(() => {
        setShowEnergeChange(false);
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [currentCharacter?.energe_change]);

  return (
    <>{currentCharacter && (
        <div className="flex flex-col space-y-4">

          <div className="flex items-center space-x-2 text-slate-600 text-xs">
            <div>
              <svg 
              xmlns="http://www.w3.org/2000/svg" 
              fill="none" 
              viewBox="0 0 24 24" 
              strokeWidth={1.5} 
              stroke="currentColor" 
              className="w-4 h-4"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" 
                />
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
                />
              </svg>
            </div>
            <div>
              {onWatchNum} 人
            </div>
          </div>
        
          <div className="flex space-x-2 items-center">
            <div className="text-slate-600 text-xs">
              饥饿
            </div>  
            <div className="w-40 h-2 rounded-lg backdrop-blur-sm bg-slate-800/20 flex relative">
              <div
                className="h-full bg-slate-500 rounded-l-lg"
                style={{ width: `${hungerPercentage}%` }}
              ></div>
              <div
                className={`h-full ${hungerChangePercentage > 0 ? 'bg-green-500/40' : 'bg-red-500/40'} rounded-r-lg`}
                style={{ width: `${Math.abs(hungerChangePercentage)}%` }}
              ></div>
            </div>
            {showHungerChange && (
              <div
                className={`text-xs duration-500 transition-opacity ${currentCharacter.hunger_change > 0 ? 'text-green-500' : 'text-red-500'}`}
              >
                {currentCharacter.hunger_change}
              </div>
            )}
          </div>
          
          <div className="flex space-x-2 items-center">
            <div className="text-slate-600 text-xs">
              精力
            </div>  
            <div className="w-40 h-2 rounded-lg backdrop-blur-sm bg-slate-800/20 flex relative">
              <div
                className="h-full bg-slate-500 rounded-l-lg"
                style={{ width: `${energerePercentage}%` }}
              ></div>
              <div
                className={`h-full ${energereChangePercentage > 0 ? 'bg-green-500/40' : 'bg-red-500/40'} rounded-r-lg`}
                style={{ width: `${Math.abs(energereChangePercentage)}%` }}
              ></div>
            </div>
            {showEnergeChange && (
              <div
                className={`text-xs duration-500 transition-opacity ${currentCharacter.energe_change > 0 ? 'text-green-500' : 'text-red-500'}`}
              >
                {currentCharacter.energe_change}
              </div>
            )}
          </div>
        </div>
      )}
    </>
  );
};

export default InfoboxLeft;