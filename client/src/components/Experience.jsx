import { CameraControls, Environment, Sky } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import { useAtom } from "jotai";
import { useEffect, useRef } from "react";
import { Room } from "./Room";
import { mapAtom, roomIDAtom, userAtom, socket, selectedAvatarAtom } from "./SocketManager";
import { buildModeAtom, shopModeAtom } from "./UI";


export const Experience = ({ loaded }) => {
  const [buildMode] = useAtom(buildModeAtom);
  const [shopMode] = useAtom(shopModeAtom);
  const controls = useRef();
  const [roomID, setRoomID] = useAtom(roomIDAtom);
  const [map, setMap] = useAtom(mapAtom);
  const [user] = useAtom(userAtom);
  const [selectedAvatar] = useAtom(selectedAvatarAtom);

  const fixedRoomID = 1;

  useEffect(() => {
    console.log("emit joinRoom");
    socket.emit("joinRoom", fixedRoomID, {});
    setMap(null);
    setRoomID(fixedRoomID);
  }, []);

  useEffect(() => {
    // INITIAL POSITION
    if (!loaded) {
      controls.current.setPosition(0, 8, 2);
      controls.current.setTarget(0, 8, 0);
      return;
    }
    
    // DIRECTLY LOAD ROOM
    if (shopMode) {
      controls.current.setPosition(0, 1, 6, true);
      controls.current.setTarget(0, 0, 0, true);
      return;
    }

    if (buildMode) {
      controls.current.setPosition(14, 10, 14, true);
      controls.current.setTarget(3.5, 0, 3.5, true);
      return;
    }

    // No Avatar Selected
    if (!selectedAvatar) {
      controls.current.setPosition(
        map.size[0] * 2,
        map.size[0] * 1.5, 
        map.size[1] * 2,
        true
      );
      controls.current.setTarget(
        map.size[0] / 2, 
        0, 
        map.size[1] / 2, 
        true
      );
      return;
    }
  }, [buildMode, shopMode, loaded, selectedAvatar]);

  useFrame(({ scene }) => {

    if (!selectedAvatar) {
      return;
    }

    const character = scene.getObjectByName(`character-${selectedAvatar}`);
    if (!character) {
      return;
    }
    controls.current.setTarget(
      character.position.x,
      0,
      character.position.z,
      true
    );
    controls.current.setPosition(
      character.position.x + 8,
      character.position.y + 8,
      character.position.z + 8,
      true
    );
  });

  return (
    <>
      <Sky
        distance={450000}
        sunPosition={[5, 8, 20]}
        inclination={0}
        azimuth={0.25}
        rayleigh={0.1}
      />
      <Environment files={"/textures/venice_sunset_1k.hdr"} />

      <ambientLight intensity={0.1} />
      <directionalLight
        position={[
            map?.size[0] / map?.gridDivision / 2, 
            4, 
            -map?.size[1] / map?.gridDivision / 2
        ]}
        castShadow
        intensity={0.3}
        shadow-mapSize={[1024, 1024]}
        // color="pink"
      >
        <orthographicCamera
          attach={"shadow-camera"}
          args={[
            -40, 
            40, 
            40, 
            -40
        ]}
          far={1000}
        />
      </directionalLight>
      <CameraControls
        ref={controls}
        // disable all mouse buttons
        mouseButtons={{
          left: (buildMode || !selectedAvatar) ? 2 : 0,
          middle: (buildMode || !selectedAvatar) ? 1 : 0,
          right: 0,
          wheel: 0,
        }}
        // disable all touch gestures
        touches={{
          one: 0,
          two: 0,
          three: 0,
        }}
      />
      {roomID && map && <Room />}
    </>
  );
};