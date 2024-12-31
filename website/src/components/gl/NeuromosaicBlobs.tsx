"use client";

import * as THREE from "three";
import { Canvas, useFrame } from "@react-three/fiber";
import { useRef, useMemo, useEffect, useState } from "react";

declare global {
  namespace JSX {
    interface IntrinsicElements {
      mesh: any;
      planeGeometry: any;
      shaderMaterial: any;
    }
  }
}

interface PetalData {
  center: THREE.Vector3;
  scale: THREE.Vector3;
  twist: number;
  velocity: THREE.Vector3;
}

interface SdfUniforms {
  uTime: { value: number };
  uResolution: { value: THREE.Vector2 };

  // How many petals in the scene
  uPetalCount: { value: number };

  // For each petal: center, scale, twist
  uPetalCenters: { value: THREE.Vector3[] };
  uPetalScales: { value: THREE.Vector3[] };
  uPetalTwists: { value: number[] };

  // Color palette
  uColor1: { value: THREE.Color };
  uColor2: { value: THREE.Color };
  uColor3: { value: THREE.Color };

  // Debug mode
  uDebugMode: { value: boolean };
}

// Scene parameters
const SCENE_PARAMS = {
  // Camera settings
  FOV: 45,
  CAMERA_Z: 6,
  NEAR_PLANE: -2,
  FAR_PLANE: 2,

  // Petal settings
  PETAL_COUNT: 8,
  PETAL_SPAWN_RANGE: {
    X: 1.2,
    Y: 1.2,
    Z: 1.2,
  },
  PETAL_SCALE: {
    X: { MIN: 0.4, MAX: 0.8 },
    Y: { MIN: 0.8, MAX: 1.4 },
    Z: { MIN: 0.2, MAX: 0.5 },
  },
  PETAL_BOUNDS: {
    X: 1.2,
    Y: 1.2,
    Z: 1.2,
  },

  // Movement settings
  MIN_SPEED: 0.001, // Minimum speed to maintain
  MAX_SPEED: 0.004, // Maximum speed cap
  REPULSION_RADIUS: 0.3, // How close petals can get before repelling
  REPULSION_STRENGTH: 0.02, // How strongly petals repel
  EDGE_SOFTNESS: 0.2, // How far from bounds to start slowing
  DAMPING: 0.98, // Speed reduction factor
  NOISE_STRENGTH: 0.0001, // Random movement strength

  // Field rendering
  FIELD_RADIUS: 0.05,
  FIELD_SMOOTHING: 0.02,
};

export function NeuromosaicBlobs() {
  const [debugMode, setDebugMode] = useState(false);

  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      if (e.key === "d") {
        setDebugMode((prev) => !prev);
        console.log("Debug mode:", !debugMode);
      }
    };
    window.addEventListener("keydown", handleKeyPress);
    return () => window.removeEventListener("keydown", handleKeyPress);
  }, [debugMode]);

  let sceneBounding = (
    <>
      <Scene3D debugMode={debugMode} />
      {debugMode && <BoundingBoxes />}
    </>
  );

  return (
    <Canvas
      className="absolute inset-0 -z-10"
      style={{ width: "100vw", height: "100vh" }}
      camera={{
        position: [0, 0, SCENE_PARAMS.CAMERA_Z],
        fov: SCENE_PARAMS.FOV,
      }}
      gl={{ alpha: false, antialias: true }}
      children={sceneBounding}
    />
  );
}

function BoundingBoxes() {
  // Calculate box dimensions based on FOV and camera distance
  const fovRad = (SCENE_PARAMS.FOV * Math.PI) / 180;
  const viewHeight = 2 * Math.tan(fovRad / 2) * SCENE_PARAMS.CAMERA_Z;
  const viewWidth = viewHeight * (window.innerWidth / window.innerHeight);

  return (
    <>
      {/* Scene boundaries at z=0 plane */}
      <mesh position={[0, 0, 0]}>
        <boxGeometry args={[viewWidth, viewHeight, 0.02]} />
        <meshBasicMaterial color="green" wireframe={true} />
      </mesh>

      {/* Camera frustum near plane */}
      <mesh position={[0, 0, SCENE_PARAMS.NEAR_PLANE]}>
        <boxGeometry args={[viewWidth * 0.67, viewHeight * 0.67, 0.02]} />
        <meshBasicMaterial color="lime" wireframe={true} />
      </mesh>

      {/* Camera frustum far plane */}
      <mesh position={[0, 0, SCENE_PARAMS.FAR_PLANE]}>
        <boxGeometry args={[viewWidth * 1.33, viewHeight * 1.33, 0.02]} />
        <meshBasicMaterial color="lime" wireframe={true} />
      </mesh>
    </>
  );
}

function Scene3D({ debugMode }: { debugMode: boolean }) {
  // Calculate scale based on FOV and camera distance to match viewport exactly
  const fovRad = (SCENE_PARAMS.FOV * Math.PI) / 180;
  const viewHeight = 2 * Math.tan(fovRad / 2) * SCENE_PARAMS.CAMERA_Z;
  const viewWidth = viewHeight * (window.innerWidth / window.innerHeight);

  // Since our plane is 1x1, we need to scale it to match the view dimensions
  const scaleX = viewWidth;
  const scaleY = viewHeight;

  return (
    <mesh rotation={[0, 0, 0]} scale={[scaleX, scaleY, 1]}>
      <planeGeometry args={[1, 1]} />
      <RaymarchedPetals debugMode={debugMode} />
    </mesh>
  );
}

/**
 * RaymarchedPetals:
 * - Replaces sphere SDF with a "petal-like" ellipsoid + twist
 * - Unions multiple petals in the scene for an organic swirl
 */
function RaymarchedPetals({ debugMode }: { debugMode: boolean }) {
  const materialRef = useRef<THREE.ShaderMaterial>(null);
  const lastLogTime = useRef(0);

  // Adjust to taste
  const PETAL_COUNT = 8;
  const STEP_COUNT = 64;
  const SURF_DIST = 0.002;

  // 1) Random petal data
  const petalData = useMemo<PetalData[]>(() => {
    const petals: PetalData[] = [];
    for (let i = 0; i < SCENE_PARAMS.PETAL_COUNT; i++) {
      const cx = (Math.random() - 0.5) * SCENE_PARAMS.PETAL_SPAWN_RANGE.X * 2;
      const cy = (Math.random() - 0.5) * SCENE_PARAMS.PETAL_SPAWN_RANGE.Y * 2;
      const cz = (Math.random() - 0.5) * SCENE_PARAMS.PETAL_SPAWN_RANGE.Z * 2;

      const sx =
        SCENE_PARAMS.PETAL_SCALE.X.MIN +
        Math.random() *
          (SCENE_PARAMS.PETAL_SCALE.X.MAX - SCENE_PARAMS.PETAL_SCALE.X.MIN);
      const sy =
        SCENE_PARAMS.PETAL_SCALE.Y.MIN +
        Math.random() *
          (SCENE_PARAMS.PETAL_SCALE.Y.MAX - SCENE_PARAMS.PETAL_SCALE.Y.MIN);
      const sz =
        SCENE_PARAMS.PETAL_SCALE.Z.MIN +
        Math.random() *
          (SCENE_PARAMS.PETAL_SCALE.Z.MAX - SCENE_PARAMS.PETAL_SCALE.Z.MIN);

      const twist = Math.random() * 2.0;

      // Initialize with random velocity
      const velocity = new THREE.Vector3(
        (Math.random() - 0.5) * 0.002,
        (Math.random() - 0.5) * 0.002,
        (Math.random() - 0.5) * 0.002
      );

      petals.push({
        center: new THREE.Vector3(cx, cy, cz),
        scale: new THREE.Vector3(sx, sy, sz),
        twist,
        velocity,
      });
    }
    return petals;
  }, []);

  // Handle window resize and log viewport info
  useEffect(() => {
    const handleResize = () => {
      if (materialRef.current) {
        const width = window.innerWidth;
        const height = window.innerHeight;
        materialRef.current.uniforms.uResolution.value.set(width, height);

        // Log canvas dimensions and calculated scene boundaries
        console.log("\nCanvas/Scene Boundaries:");
        console.log(`Canvas dimensions: ${width}x${height} pixels`);
        console.log(`Aspect ratio: ${(width / height).toFixed(3)}`);

        // Calculate scene boundaries at z=0 plane
        // Using FOV=90° and camera at z=6:
        const fov = (90 * Math.PI) / 180; // to radians
        const distance = 6; // camera z position
        const viewHeight = 2 * Math.tan(fov / 2) * distance;
        const viewWidth = viewHeight * (width / height);

        console.log("\nScene boundaries at z=0 plane:");
        console.log(
          `Width: ${viewWidth.toFixed(2)} units (±${(viewWidth / 2).toFixed(
            2
          )})`
        );
        console.log(
          `Height: ${viewHeight.toFixed(2)} units (±${(viewHeight / 2).toFixed(
            2
          )})`
        );
      }
    };

    // Log initial dimensions
    handleResize();

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  // Log petal positions and scene occupation
  const logPetalStatus = (time: number) => {
    if (time - lastLogTime.current >= 10) {
      console.log("\n=== Petal Status at time", time.toFixed(2), "===");

      // Calculate scene occupation including petal scales
      const bounds = {
        minX: Math.min(...petalData.map((p) => p.center.x - p.scale.x)),
        maxX: Math.max(...petalData.map((p) => p.center.x + p.scale.x)),
        minY: Math.min(...petalData.map((p) => p.center.y - p.scale.y)),
        maxY: Math.max(...petalData.map((p) => p.center.y + p.scale.y)),
        minZ: Math.min(...petalData.map((p) => p.center.z - p.scale.z)),
        maxZ: Math.max(...petalData.map((p) => p.center.z + p.scale.z)),
      };

      console.log("Scene occupation (including petal scales):");
      console.log(
        `X range: ${bounds.minX.toFixed(2)} to ${bounds.maxX.toFixed(2)}`
      );
      console.log(
        `Y range: ${bounds.minY.toFixed(2)} to ${bounds.maxY.toFixed(2)}`
      );
      console.log(
        `Z range: ${bounds.minZ.toFixed(2)} to ${bounds.maxZ.toFixed(2)}`
      );

      console.log("\nIndividual petal data:");
      petalData.forEach((petal, i) => {
        console.log(
          `Petal ${i}: ` +
            `center(${petal.center.x.toFixed(2)}, ${petal.center.y.toFixed(
              2
            )}, ${petal.center.z.toFixed(2)}), ` +
            `scale(${petal.scale.x.toFixed(2)}, ${petal.scale.y.toFixed(
              2
            )}, ${petal.scale.z.toFixed(2)}), ` +
            `twist=${petal.twist.toFixed(3)}`
        );
      });

      lastLogTime.current = time;
    }
  };

  // 2) Uniforms
  const uniforms = useMemo<SdfUniforms>(() => {
    return {
      uTime: { value: 0 },
      uResolution: {
        value: new THREE.Vector2(window.innerWidth, window.innerHeight),
      },

      uPetalCount: { value: PETAL_COUNT },

      uPetalCenters: { value: petalData.map((p) => p.center) },
      uPetalScales: { value: petalData.map((p) => p.scale) },
      uPetalTwists: { value: petalData.map((p) => p.twist) },

      uColor1: { value: new THREE.Color("#2e2066") },
      uColor2: { value: new THREE.Color("#bf3abb") },
      uColor3: { value: new THREE.Color("#0c0c1c") },

      uDebugMode: { value: debugMode },
    };
  }, [petalData, debugMode]);

  // 3) Animation with improved physics
  useFrame((state) => {
    const mat = materialRef.current;
    if (!mat) return;
    const time = state.clock.getElapsedTime();

    mat.uniforms.uTime.value = time;
    logPetalStatus(time);

    // Update each petal's position based on physics
    petalData.forEach((petal, i) => {
      // Add some noise to movement
      petal.velocity.add(
        new THREE.Vector3(
          (Math.random() - 0.5) * SCENE_PARAMS.NOISE_STRENGTH,
          (Math.random() - 0.5) * SCENE_PARAMS.NOISE_STRENGTH,
          (Math.random() - 0.5) * SCENE_PARAMS.NOISE_STRENGTH
        )
      );

      // Apply repulsion from other petals
      petalData.forEach((other, j) => {
        if (i !== j) {
          const diff = new THREE.Vector3().subVectors(
            petal.center,
            other.center
          );
          const distance = diff.length();
          if (distance < SCENE_PARAMS.REPULSION_RADIUS) {
            diff
              .normalize()
              .multiplyScalar(
                SCENE_PARAMS.REPULSION_STRENGTH *
                  (1 - distance / SCENE_PARAMS.REPULSION_RADIUS)
              );
            petal.velocity.add(diff);
          }
        }
      });

      // Soft bounds checking - start slowing down near edges
      const bounds = 1.0;
      const softness = SCENE_PARAMS.EDGE_SOFTNESS;

      // Handle each axis
      const axes: Array<"x" | "y" | "z"> = ["x", "y", "z"];
      axes.forEach((axis) => {
        const pos = petal.center[axis];
        const vel = petal.velocity[axis];
        const absPos = Math.abs(pos);

        if (absPos > bounds - softness) {
          // Calculate repulsion from boundary
          const overlap = absPos - (bounds - softness);
          const repulsion = -(overlap / softness) * Math.abs(vel) * 2;
          petal.velocity[axis] += repulsion * Math.sign(pos);
        }
      });

      // Apply damping
      petal.velocity.multiplyScalar(SCENE_PARAMS.DAMPING);

      // Ensure minimum speed
      const speed = petal.velocity.length();
      if (speed < SCENE_PARAMS.MIN_SPEED) {
        petal.velocity.normalize().multiplyScalar(SCENE_PARAMS.MIN_SPEED);
      }
      // Cap maximum speed
      else if (speed > SCENE_PARAMS.MAX_SPEED) {
        petal.velocity.normalize().multiplyScalar(SCENE_PARAMS.MAX_SPEED);
      }

      // Update position
      petal.center.add(petal.velocity);
    });

    // Update uniform arrays
    mat.uniforms.uPetalCenters.value = petalData.map((p) => p.center);
  });

  // 4) Shader material
  return (
    <shaderMaterial
      ref={materialRef}
      uniforms={uniforms as any}
      vertexShader={`
        varying vec2 vUv;
        void main() {
          vUv = uv;
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
      `}
      fragmentShader={`
        uniform float uTime;
        uniform vec2 uResolution;
        uniform int uPetalCount;
        uniform vec3 uPetalCenters[${SCENE_PARAMS.PETAL_COUNT}];
        uniform vec3 uPetalScales[${SCENE_PARAMS.PETAL_COUNT}];
        uniform float uPetalTwists[${SCENE_PARAMS.PETAL_COUNT}];
        uniform vec3 uColor1;
        uniform vec3 uColor2;
        uniform vec3 uColor3;
        uniform bool uDebugMode;
        
        varying vec2 vUv;
        
        void main() {
          // Scale UV to [-1,1] range with aspect correction
          vec2 uv = (vUv - 0.5) * 2.0;
          float aspect = uResolution.x / uResolution.y;
          uv.x *= aspect;
          
          // Calculate scene color
          vec3 color = uColor3;  // Start with background color
          float totalField = 0.0;
          
          // Sum contribution from all petals
          for(int i = 0; i < ${SCENE_PARAMS.PETAL_COUNT}; i++) {
            vec3 center = uPetalCenters[i];
            vec2 petalPos = center.xz;
            
            // Calculate distance field
            float d = length(uv - petalPos);
            float field = smoothstep(
              ${SCENE_PARAMS.FIELD_SMOOTHING.toFixed(3)}, 
              0.0, 
              d - ${SCENE_PARAMS.FIELD_RADIUS.toFixed(3)}
            );
            
            // Accumulate field with soft max
            totalField = totalField + field * (1.0 - totalField);
          }
          
          if (uDebugMode) {
            // Debug mode: White petals on black background
            color = vec3(totalField);
          } else {
            // Normal mode: Smooth gradient between colors
            vec3 petalColor = mix(uColor1, uColor2, totalField);
            color = mix(uColor3, petalColor, smoothstep(0.0, 0.7, totalField));
          }
          
          gl_FragColor = vec4(color, 1.0);
        }
      `}
    />
  );
}
