"use client";

import * as THREE from "three";
import { Canvas, useFrame } from "@react-three/fiber";
import { useRef, useMemo, useEffect, useState } from "react";

/** Petal color combos, matching <FloatingPetal> */
const petalColors = [
  {
    start: "#2e2066", // Deep purple
    mid: "#bf3abb", // Vibrant pink
    end: "#0c0c1c", // Midnight blue
  },
  {
    start: "#3b82f6", // Blue
    mid: "#6366f1", // Indigo
    end: "#2e2066", // Deep purple
  },
  {
    start: "#ec4899", // Pink
    mid: "#d946ef", // Fuschia
    end: "#6366f1", // Indigo
  },
  {
    start: "#bf3abb", // Vibrant pink
    mid: "#9333ea", // Purple
    end: "#2e2066", // Deep purple
  },
  {
    start: "#ffadc0", // Peach
    mid: "#ffc7d3", // Light peach
    end: "#ffeef2", // Ultralight peach
  },
];

/** Scene / physics parameters */
const SCENE_PARAMS = {
  FOV: 45,
  CAMERA_Z: 120, // Increased for more zoomed out view
  MAX_PETALS: 30, // maximum shader array size
  PETAL_COUNT: 20, // actual number of petals to simulate
  BOUNDS: 2.5, // increased bounding region for more space
  COLLISION_RADIUS: 0.7, // collision distance
  COLLISION_PUSH: 0.02, // how strongly they push off each other
  MIN_SPEED: 0.003,
  MAX_SPEED: 0.006,
  NOISE_STRENGTH: 0.0002, // random force each frame

  // Visual parameters
  PETAL_SIZE: {
    MIN: 0.08, // minimum petal size multiplier
    MAX: 0.5, // maximum petal size multiplier
  },
  GRAD_INNER: 0.35, // radial gradient stops
  GRAD_MID: 0.7,
};

interface PetalData {
  center: THREE.Vector3;
  velocity: THREE.Vector3;
  radius: number;
  size: number; // Added size property
  colorSet: {
    start: THREE.Color;
    mid: THREE.Color;
    end: THREE.Color;
  };
}

/** Root component */
export function NeuromosaicBlobs() {
  const [debugMode, setDebugMode] = useState(false);

  // Toggle debug with "d" key
  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === "d") setDebugMode((prev) => !prev);
    };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, []);

  return (
    <Canvas
      className="absolute inset-0 -z-10"
      style={{ width: "100vw", height: "100vh" }}
      camera={{
        position: [0, 0, SCENE_PARAMS.CAMERA_Z],
        fov: SCENE_PARAMS.FOV,
      }}
      gl={{ alpha: false, antialias: true }}
    >
      <MetaballScene debugMode={debugMode} />
    </Canvas>
  );
}

/**
 * The main scene: a single big plane that we raymarch with
 * a pseudo "petal" radial gradient approach
 */
function MetaballScene({ debugMode }: { debugMode: boolean }) {
  // match the plane to the camera's view size
  const fovRad = (SCENE_PARAMS.FOV * Math.PI) / 180;
  const viewHeight = 2 * Math.tan(fovRad / 2) * SCENE_PARAMS.CAMERA_Z;
  const viewWidth = viewHeight * (window.innerWidth / window.innerHeight);

  return (
    <mesh scale={[viewWidth, viewHeight, 1]}>
      <planeGeometry args={[1, 1]} />
      <PetalMetaballs debugMode={debugMode} />
    </mesh>
  );
}

/**
 * PetalMetaballs:
 * - Takes N petals, each with a center + velocity.
 * - Collisions keep them moving, random noise prevents them from halting.
 * - The fragment shader draws a radial gradient for each petal, blending them.
 */
function PetalMetaballs({ debugMode }: { debugMode: boolean }) {
  const matRef = useRef<THREE.ShaderMaterial>(null);

  // 1) Create random petals
  const petals = useMemo<PetalData[]>(() => {
    const arr: PetalData[] = [];
    for (let i = 0; i < SCENE_PARAMS.PETAL_COUNT; i++) {
      // random center in ±SCENE_PARAMS.BOUNDS
      const x = (Math.random() - 0.5) * 2 * SCENE_PARAMS.BOUNDS;
      const y = (Math.random() - 0.5) * 2 * SCENE_PARAMS.BOUNDS;
      const z = (Math.random() - 0.5) * 2 * SCENE_PARAMS.BOUNDS;

      // random velocity
      const vx = (Math.random() - 0.5) * 0.002;
      const vy = (Math.random() - 0.5) * 0.002;
      const vz = (Math.random() - 0.5) * 0.002;

      // random size within range
      const size =
        SCENE_PARAMS.PETAL_SIZE.MIN +
        Math.random() *
          (SCENE_PARAMS.PETAL_SIZE.MAX - SCENE_PARAMS.PETAL_SIZE.MIN);

      // random color set
      const c = petalColors[Math.floor(Math.random() * petalColors.length)];

      arr.push({
        center: new THREE.Vector3(x, y, z),
        velocity: new THREE.Vector3(vx, vy, vz),
        radius: SCENE_PARAMS.COLLISION_RADIUS * size, // scale collision radius with size
        size, // store size for shader
        colorSet: {
          start: new THREE.Color(c.start),
          mid: new THREE.Color(c.mid),
          end: new THREE.Color(c.end),
        },
      });
    }
    return arr;
  }, []);

  // 2) Build uniforms with fixed-size arrays
  const uniforms = useMemo(() => {
    const actualCount = petals.length;

    // Create fixed-size arrays with dummy values beyond actualCount
    const centerArray = new Array(SCENE_PARAMS.MAX_PETALS)
      .fill(null)
      .map((_, i) => {
        if (i < actualCount) return petals[i].center;
        return new THREE.Vector3(9999, 9999, 9999); // Far away
      });

    const sizeArray = new Array(SCENE_PARAMS.MAX_PETALS)
      .fill(null)
      .map((_, i) => {
        if (i < actualCount) return petals[i].size;
        return 0; // Zero size for unused slots
      });

    const startCols = new Array(SCENE_PARAMS.MAX_PETALS)
      .fill(null)
      .map((_, i) => {
        if (i < actualCount) return petals[i].colorSet.start;
        return new THREE.Color(0x000000);
      });

    const midCols = new Array(SCENE_PARAMS.MAX_PETALS)
      .fill(null)
      .map((_, i) => {
        if (i < actualCount) return petals[i].colorSet.mid;
        return new THREE.Color(0x000000);
      });

    const endCols = new Array(SCENE_PARAMS.MAX_PETALS)
      .fill(null)
      .map((_, i) => {
        if (i < actualCount) return petals[i].colorSet.end;
        return new THREE.Color(0x000000);
      });

    return {
      uTime: { value: 0 },
      uResolution: {
        value: new THREE.Vector2(window.innerWidth, window.innerHeight),
      },
      uDebug: { value: debugMode },
      uPetalCount: { value: actualCount },
      uPetalCenters: { value: centerArray },
      uPetalSizes: { value: sizeArray }, // Added sizes uniform
      uPetalStartCols: { value: startCols },
      uPetalMidCols: { value: midCols },
      uPetalEndCols: { value: endCols },
    };
  }, [petals, debugMode]);

  // 3) Animate (collisions, random noise, bounding)
  useFrame((state, delta) => {
    const dt = delta * 60; // ~ normalized for 60fps
    const t = state.clock.getElapsedTime();

    // keep them moving
    petals.forEach((petal) => {
      // collision check with others
      petals.forEach((other) => {
        if (other === petal) return;
        const diff = new THREE.Vector3().subVectors(petal.center, other.center);
        const dist = diff.length();
        if (dist < petal.radius + other.radius) {
          // push them apart
          const overlap = petal.radius + other.radius - dist;
          diff.normalize();
          petal.center.addScaledVector(
            diff,
            overlap * 0.5 * SCENE_PARAMS.COLLISION_PUSH
          );
          other.center.addScaledVector(
            diff,
            -overlap * 0.5 * SCENE_PARAMS.COLLISION_PUSH
          );

          // basic bounce
          const relVel = new THREE.Vector3().subVectors(
            petal.velocity,
            other.velocity
          );
          const speed = relVel.dot(diff);
          if (speed < 0) {
            const impulse = -1.2 * speed;
            diff.multiplyScalar(impulse * 0.5);
            petal.velocity.add(diff);
            other.velocity.sub(diff);
          }
        }
      });

      // random noise to ensure perpetual motion
      petal.velocity.x += (Math.random() - 0.5) * SCENE_PARAMS.NOISE_STRENGTH;
      petal.velocity.y += (Math.random() - 0.5) * SCENE_PARAMS.NOISE_STRENGTH;
      petal.velocity.z += (Math.random() - 0.5) * SCENE_PARAMS.NOISE_STRENGTH;

      // update position
      petal.center.addScaledVector(petal.velocity, dt);

      // bounds check => bounce
      (["x", "y", "z"] as const).forEach((axis) => {
        const val = petal.center[axis];
        if (Math.abs(val) > SCENE_PARAMS.BOUNDS) {
          petal.velocity[axis] *= -1;
          petal.center[axis] = Math.sign(val) * SCENE_PARAMS.BOUNDS;
        }
      });

      // clamp speed
      const speedLen = petal.velocity.length();
      if (speedLen < SCENE_PARAMS.MIN_SPEED) {
        petal.velocity.normalize().multiplyScalar(SCENE_PARAMS.MIN_SPEED);
      } else if (speedLen > SCENE_PARAMS.MAX_SPEED) {
        petal.velocity.normalize().multiplyScalar(SCENE_PARAMS.MAX_SPEED);
      }
    });

    // update uniforms - only need to update centers since colors don't change
    if (matRef.current) {
      matRef.current.uniforms.uTime.value = t;
      // Update centers array while preserving dummy values
      const centerArray = matRef.current.uniforms.uPetalCenters.value;
      petals.forEach((p, i) => {
        centerArray[i].copy(p.center);
      });
    }
  });

  // 4) The fragment shader to replicate FloatingPetal's radial gradient + transparency.
  return (
    <shaderMaterial
      ref={matRef}
      uniforms={uniforms}
      vertexShader={`
        varying vec2 vUv;
        void main() {
          vUv = uv;
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0);
        }
      `}
      fragmentShader={`
        precision highp float;

        uniform float uTime;
        uniform vec2 uResolution;
        uniform bool uDebug;
        uniform int uPetalCount;

        // arrays of centers and colors - fixed size
        uniform vec3 uPetalCenters[${SCENE_PARAMS.MAX_PETALS}];
        uniform float uPetalSizes[${SCENE_PARAMS.MAX_PETALS}];  // Added sizes
        uniform vec3 uPetalStartCols[${SCENE_PARAMS.MAX_PETALS}];
        uniform vec3 uPetalMidCols[${SCENE_PARAMS.MAX_PETALS}];
        uniform vec3 uPetalEndCols[${SCENE_PARAMS.MAX_PETALS}];

        const float GRAD_INNER = ${SCENE_PARAMS.GRAD_INNER.toFixed(2)}; 
        const float GRAD_MID = ${SCENE_PARAMS.GRAD_MID.toFixed(2)};

        varying vec2 vUv;

        void main(){
          vec2 uv = (vUv - 0.5) * 2.0;
          float aspect = uResolution.x / uResolution.y;
          uv.x *= aspect;

          vec3 finalColor = vec3(0.06, 0.06, 0.1);
          float accumulatedAlpha = 0.0;

          for(int i=0; i<${SCENE_PARAMS.MAX_PETALS}; i++){
            if(i >= uPetalCount) break;
            vec2 center = vec2(uPetalCenters[i].x, uPetalCenters[i].z);

            // Scale distances by petal size
            float size = uPetalSizes[i];
            float dx = (uv.x - center.x) / size;
            float dy = (uv.y - center.y) / size;
            float dist = sqrt(dx*dx + dy*dy);

            if(dist < 1.0){
              vec3 colStart = uPetalStartCols[i];
              vec3 colMid   = uPetalMidCols[i];
              vec3 colEnd   = uPetalEndCols[i];

              float alpha = 1.0;
              vec3 color;

              if(dist < GRAD_INNER){
                float t = dist / GRAD_INNER;
                color = mix(colStart, colStart, t);
                alpha = mix(0.85, 0.6, t);
              }
              else if(dist < GRAD_MID){
                float t = (dist - GRAD_INNER)/(GRAD_MID - GRAD_INNER);
                color = mix(colStart, colMid, t);
                alpha = mix(0.4, 0.25, t);
              }
              else{
                float t = (dist - GRAD_MID)/(1.0 - GRAD_MID);
                color = mix(colMid, colEnd, t);
                alpha = mix(0.25, 0.15, t);
              }

              float pulse = sin(uTime * 0.4) * 0.05 + 0.95;
              color *= pulse;

              float blend = alpha * (1.0 - accumulatedAlpha);
              finalColor = mix(finalColor, color, blend);
              accumulatedAlpha += blend;
            }
          }

          if(uDebug){
            finalColor = vec3(accumulatedAlpha);
          }

          gl_FragColor = vec4(finalColor, 1.0);
        }
      `}
    />
  );
}
