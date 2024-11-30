import { atom, useAtom } from "jotai";
import { useEffect, useRef, useState } from "react";

import { motion } from "framer-motion";
import { roomItemsAtom } from "./Room";
import { roomIDAtom, socket, charactersAtom, selectedAvatarAtom } from "./SocketManager";
import { conversationHistoryAtom } from "./Avatar";
import InfoBox from "./InfoBox";
import EventBox from "./EventBox";
import TimeBox from "./TimeBox";
import ThoughtBox from "./ThoughtBox";
import ConversationHistory from "./ConversationHistory";
import SelectAvatarButton from "./SelectAvatarButton";
import InfoboxLeft from "./InfoboxLeft";
import BottomButtons from "./BottomButtons";
import PasswordInput from "./PasswordInput";

export const buildModeAtom = atom(false);
export const shopModeAtom = atom(false);
export const draggedItemAtom = atom(null);
export const draggedItemRotationAtom = atom(0);

export const UI = () => {
  const [buildMode, setBuildMode] = useAtom(buildModeAtom);
  const [shopMode, setShopMode] = useAtom(shopModeAtom);
  const [draggedItem, setDraggedItem] = useAtom(draggedItemAtom);
  const [draggedItemRotation, setDraggedItemRotation] = useAtom(
    draggedItemRotationAtom
  );
  const [_roomItems, setRoomItems] = useAtom(roomItemsAtom);
  const [passwordMode, setPasswordMode] = useState(false);
  const [roomID, setRoomID] = useAtom(roomIDAtom);
  const [passwordCorrectForRoom, setPasswordCorrectForRoom] = useState(false);
  const [selectedAvatar, setSelectedAvatar] = useAtom(selectedAvatarAtom);
  const [conversationHistory, setConversationHistory] = useAtom(conversationHistoryAtom);

  useEffect(() => {
    setPasswordCorrectForRoom(false); // PS: this is an ugly shortcut
  }, [roomID]);

  const ref = useRef();
  const [chatMessage, setChatMessage] = useState("");
  const sendChatMessage = () => {
    if (chatMessage.length > 0) {
      socket.emit("chatMessage", chatMessage);
      setChatMessage("");
    }
  };

  const [characters, setCharacters] = useAtom(charactersAtom);

  return (
    <div style={{ position: 'relative', zIndex: 9999 }}>
      <motion.div
        ref={ref}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5, delay: 0.5 }}
      >
        {passwordMode && (
          <PasswordInput
            onClose={() => setPasswordMode(false)}
            onSuccess={() => {
              setBuildMode(true);
              setPasswordCorrectForRoom(true);
            }}
          />
        )}
        
        <BottomButtons 
          roomID={roomID} 
          shopMode={shopMode} 
          buildMode={buildMode} 
          draggedItem={draggedItem} 
          draggedItemRotation={draggedItemRotation} 
          setShopMode={setShopMode} 
          setBuildMode={setBuildMode} 
          setDraggedItem={setDraggedItem} 
          setDraggedItemRotation={setDraggedItemRotation} 
          setRoomItems={setRoomItems} 
          passwordCorrectForRoom={passwordCorrectForRoom} 
          setPasswordMode={setPasswordMode} 
          chatMessage={chatMessage} 
          setChatMessage={setChatMessage} 
          sendChatMessage={sendChatMessage} 
        />
        
        <div className="fixed top-0 left-0 flex flex-col space-y-8 p-5">
            <SelectAvatarButton characters={characters} selectedAvatar={selectedAvatar} setSelectedAvatar={setSelectedAvatar} />
            <InfoboxLeft characters={characters} selectedAvatar={selectedAvatar} />
        </div>

        {selectedAvatar && (
          <>
            <InfoBox characters={characters} selectedAvatar={selectedAvatar} />
            <EventBox characters={characters} selectedAvatar={selectedAvatar} />
            <ThoughtBox characters={characters} selectedAvatar={selectedAvatar} />
          </>
        )}

        <TimeBox />
        <ConversationHistory conversationHistory={conversationHistory}/>

      </motion.div>
    </div>
  );
};
