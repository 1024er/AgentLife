import { useCursor, useGLTF, useScroll } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import { useAtom } from "jotai";
import { useMemo, useRef, useState, useEffect } from "react";
import { SkeletonUtils } from "three-stdlib";
import { useGrid } from "../hooks/useGrid";
import { itemsAtom, mapAtom } from "./SocketManager";

const ShopItem = ({ item, ...props }) => {
  const { name, size, rotation } = item;
  const { scene } = useGLTF(`/models/items/${name}.glb`);
  // Skinned meshes cannot be re-used in threejs without cloning them
  const clone = useMemo(() => SkeletonUtils.clone(scene), [scene]);
  const { gridToVector3 } = useGrid();
  const [hover, setHover] = useState(false);
  useCursor(hover);
  return (
    <group {...props}>
      <group
        position={gridToVector3([0, 0], size[0], size[1])}
        rotation-y={((rotation || 0) * Math.PI) / 2}
        onPointerEnter={() => setHover(true)}
        onPointerLeave={() => setHover(false)}
      >
        <primitive object={clone} />
      </group>
    </group>
  );
};

export const Shop = ({ onItemSelected }) => {
  const [items] = useAtom(itemsAtom);
  const [map] = useAtom(mapAtom);

  const maxX = useRef(0);

  const shopItems = useMemo(() => {
    let x = 0;
    return Object.values(items).map((item, index) => {
      const xPos = x;
      x += item.size[0] / map.gridDivision + 1;
      maxX.current = x;
      return (
        <ShopItem
          key={index}
          position-x={xPos}
          item={item}
          onClick={(e) => {
            e.stopPropagation(); // Prevents the onPlaneClicked from firing just after we pick up an item
            onItemSelected(item);
          }}
        />
      );
    });
  }, [items]);

  const shopContainer = useRef();
  const scrollData = useScroll();
  const scale = 0.42;

  // 添加滚轮事件监听器
  // useEffect(() => {
  //   const handleWheel = (event) => {
  //     scrollData.offset += event.deltaY * 0.001; // 调整滚动速度
  //     scrollData.offset = Math.max(0, Math.min(1, scrollData.offset)); // 限制 offset 在 0 到 1 之间
  //   };

  //   window.addEventListener("wheel", handleWheel);
  //   return () => {
  //     window.removeEventListener("wheel", handleWheel);
  //   };
  // }, [scrollData]);

  useFrame(() => {
    shopContainer.current.position.x =
      -scrollData.offset * maxX.current * scale;
  });

  return (
    <group ref={shopContainer} scale={scale}>
      {shopItems}
    </group>
  );
};