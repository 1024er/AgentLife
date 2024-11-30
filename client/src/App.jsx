import { Canvas } from "@react-three/fiber";
import { ScrollControls, useProgress } from "@react-three/drei";
import { useAtom } from "jotai";
import { useEffect, useState } from "react";
import { Experience } from "./components/Experience";
import { Loader } from "./components/Loader";
import {
  SocketManager,
  itemsAtom,
  roomIDAtom,
} from "./components/SocketManager";
import { UI, shopModeAtom } from "./components/UI";

function App() {
  const [roomID] = useAtom(roomIDAtom);
  const [shopMode, setShopMode] = useAtom(shopModeAtom);

  const { progress } = useProgress();
  const [loaded, setLoaded] = useState(false);
  const [items] = useAtom(itemsAtom);

  useEffect(() => {
    if (progress === 100 && items) {
      setLoaded(true); // As progress can go back to 0 when new resources are loaded, we need to make sure we don't fade out the UI when that happens
    }
  }, [progress]);

  return (
    <>
      <SocketManager />
      <Canvas
        shadows
        camera={{
          position: [0, 8, 2],
          fov: 30,
        }}
      >
        <color attach="background" args={["#ffffff"]} />
        <ScrollControls pages={shopMode ? 4 : 0}>
          <Experience loaded={loaded} />
        </ScrollControls>
      </Canvas>
      <Loader loaded={loaded} />
      {loaded && <UI />}
    </>
  );
}

export default App;
