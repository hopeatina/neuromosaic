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

// Petal color combos (matching FloatingPetal.tsx)
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
];

interface PetalData {
  center: THREE.Vector3;
  scale: THREE.Vector3;
  twist: number;
  velocity: THREE.Vector3;
  colors: {
    start: THREE.Color;
    mid: THREE.Color;
    end: THREE.Color;
  };
  size: number; // Overall size multiplier
  rotation: number; // Base rotation
  shape: number; // Shape variation factor
}

interface SdfUniforms {
  uTime: { value: number };
  uResolution: { value: THREE.Vector2 };
  uPetalCount: { value: number };
  uPetalCenters: { value: THREE.Vector3[] };
  uPetalScales: { value: THREE.Vector3[] };
  uPetalTwists: { value: number[] };
  uPetalColorsStart: { value: THREE.Color[] };
  uPetalColorsMid: { value: THREE.Color[] };
  uPetalColorsEnd: { value: THREE.Color[] };
  uPetalSizes: { value: number[] };
  uPetalRotations: { value: number[] };
  uPetalShapes: { value: number[] };
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
  PETAL_COUNT: 30,
  PETAL_SPAWN_RANGE: {
    X: 1.2,
    Y: 1.2,
    Z: 1.2,
  },
  PETAL_SCALE: {
    X: { MIN: 3, MAX: 9 }, // More variation
    Y: { MIN: 6, MAX: 16 }, // More variation
    Z: { MIN: 1.5, MAX: 4.5 }, // More variation
  },
  SIZE: {
    MIN: 2,
    MAX: 12,
  },
  SHAPE: {
    MIN: 1, // More circular
    MAX: 1, // More elongated
  },
  PETAL_BOUNDS: {
    X: 1.2,
    Y: 1.2,
    Z: 1.2,
  },

  // Movement settings
  MIN_SPEED: 0.003, // Minimum speed to maintain
  MAX_SPEED: 0.006, // Maximum speed cap
  REPULSION_RADIUS: 0.8, // How close petals can get before repelling
  REPULSION_STRENGTH: 0.02, // How strongly petals repel
  EDGE_SOFTNESS: 0.2, // How far from bounds to start slowing
  DAMPING: 0.98, // Speed reduction factor
  NOISE_STRENGTH: 0.0001, // Random movement strength

  // Field rendering
  FIELD_RADIUS: 0.005,
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
      // Random position
      const cx = (Math.random() - 0.5) * SCENE_PARAMS.PETAL_SPAWN_RANGE.X * 2;
      const cy = (Math.random() - 0.5) * SCENE_PARAMS.PETAL_SPAWN_RANGE.Y * 2;
      const cz = (Math.random() - 0.5) * SCENE_PARAMS.PETAL_SPAWN_RANGE.Z * 2;

      // Random scale
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

      // Random color scheme
      const colorScheme =
        petalColors[Math.floor(Math.random() * petalColors.length)];

      petals.push({
        center: new THREE.Vector3(cx, cy, cz),
        scale: new THREE.Vector3(sx, sy, sz),
        twist: Math.random() * 2.0,
        velocity: new THREE.Vector3(
          (Math.random() - 0.5) * 0.002,
          (Math.random() - 0.5) * 0.002,
          (Math.random() - 0.5) * 0.002
        ),
        colors: {
          start: new THREE.Color(colorScheme.start),
          mid: new THREE.Color(colorScheme.mid),
          end: new THREE.Color(colorScheme.end),
        },
        size:
          SCENE_PARAMS.SIZE.MIN +
          Math.random() * (SCENE_PARAMS.SIZE.MAX - SCENE_PARAMS.SIZE.MIN),
        rotation: Math.random() * Math.PI * 2,
        shape:
          SCENE_PARAMS.SHAPE.MIN +
          Math.random() * (SCENE_PARAMS.SHAPE.MAX - SCENE_PARAMS.SHAPE.MIN),
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
      uPetalColorsStart: { value: petalData.map((p) => p.colors.start) },
      uPetalColorsMid: { value: petalData.map((p) => p.colors.mid) },
      uPetalColorsEnd: { value: petalData.map((p) => p.colors.end) },
      uPetalSizes: { value: petalData.map((p) => p.size) },
      uPetalRotations: { value: petalData.map((p) => p.rotation) },
      uPetalShapes: { value: petalData.map((p) => p.shape) },
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
        uniform vec3 uPetalColorsStart[${SCENE_PARAMS.PETAL_COUNT}];
        uniform vec3 uPetalColorsMid[${SCENE_PARAMS.PETAL_COUNT}];
        uniform vec3 uPetalColorsEnd[${SCENE_PARAMS.PETAL_COUNT}];
        uniform float uPetalSizes[${SCENE_PARAMS.PETAL_COUNT}];
        uniform float uPetalRotations[${SCENE_PARAMS.PETAL_COUNT}];
        uniform float uPetalShapes[${SCENE_PARAMS.PETAL_COUNT}];
        uniform bool uDebugMode;
        
        varying vec2 vUv;

        // Rotation matrix function
        mat2 rotate2D(float angle) {
          float s = sin(angle);
          float c = cos(angle);
          return mat2(c, -s, s, c);
        }
        
        // Noise function for organic movement
        float noise(vec2 p) {
          vec2 ip = floor(p);
          vec2 fp = fract(p);
          fp = fp * fp * (3.0 - 2.0 * fp);
          
          float n = mix(
            mix(sin(dot(ip, vec2(12.9898, 78.233))),
                sin(dot(ip + vec2(1.0, 0.0), vec2(12.9898, 78.233))), fp.x),
            mix(sin(dot(ip + vec2(0.0, 1.0), vec2(12.9898, 78.233))),
                sin(dot(ip + vec2(1.0, 1.0), vec2(12.9898, 78.233))), fp.x),
            fp.y
          );
          return n * 0.5 + 0.5;
        }
        
        // Improved blob shape function with internal morphing
        float blobShape(vec2 uv, vec2 center, float size, float rotation, float shape, float time) {
          // Apply rotation
          vec2 p = uv - center;
          p = rotate2D(rotation) * p;
          
          // Scale by size
          p /= size;
          
          // Base shape
          float r = length(p);
          float angle = atan(p.y, p.x);
          
          // Add multiple layers of noise-based deformation
          float deform = 0.0;
          
          // Layer 1: Slow, large deformation
          deform += noise(vec2(angle * 2.0 + time * 0.1, time * 0.05)) * 0.3;
          
          // Layer 2: Medium frequency wobble
          deform += noise(vec2(angle * 4.0 + time * 0.2, time * 0.1)) * 0.2;
          
          // Layer 3: Fast, small details
          deform += noise(vec2(angle * 8.0 + time * 0.4, time * 0.2)) * 0.1;
          
          // Combine deformations with base radius
          float modifiedRadius = r * (1.0 + deform * shape);
          
          return modifiedRadius;
        }
        
        // Get layered color based on radius, matching FloatingPetal's radial gradient
        vec4 getLayeredColor(float radius, vec3 startColor, vec3 midColor, vec3 endColor) {
          // Match FloatingPetal's gradient stops: 0%, 35%, 70%, 100%
          float opacity = 1.0;
          vec3 color;
          
          if (radius < 0.35) {
            // Inner core: start color with high opacity
            color = startColor;
            opacity = mix(0.85, 0.6, radius / 0.35);
          } 
          else if (radius < 0.7) {
            // Middle layer: transition to mid color with medium opacity
            float t = (radius - 0.35) / 0.35;
            color = mix(startColor, midColor, t);
            opacity = mix(0.4, 0.25, t);
          }
          else {
            // Outer edge: transition to end color with low opacity
            float t = (radius - 0.7) / 0.3;
            color = mix(midColor, endColor, t);
            opacity = mix(0.25, 0.15, t);
          }
          
          return vec4(color, opacity);
        }
        
        void main() {
          // Scale UV to [-1,1] range with aspect correction
          vec2 uv = (vUv - 0.5) * 2.0;
          float aspect = uResolution.x / uResolution.y;
          uv.x *= aspect;
          
          // Calculate scene color
          vec3 color = vec3(0.047, 0.047, 0.11);  // Dark background
          float totalOpacity = 0.0;
          
          // Sum contribution from all petals
          for(int i = 0; i < ${SCENE_PARAMS.PETAL_COUNT}; i++) {
            vec3 center = uPetalCenters[i];
            vec2 petalPos = center.xz;
            
            // Calculate blob shape
            float radius = blobShape(
              uv, 
              petalPos, 
              uPetalSizes[i] * ${SCENE_PARAMS.FIELD_RADIUS.toFixed(3)},
              uPetalRotations[i] + uTime * 0.1,
              uPetalShapes[i],
              uTime
            );
            
            // Only process if within maximum radius
            if (radius < 1.0) {
              // Get layered colors and opacity
              vec4 layerColor = getLayeredColor(
                radius,
                uPetalColorsStart[i],
                uPetalColorsMid[i],
                uPetalColorsEnd[i]
              );
              
              // Add subtle pulse effect
              float pulse = sin(uTime * 0.5) * 0.1 + 0.9;
              layerColor.rgb *= pulse;
              
              // Blend with accumulated color using opacity
              float alpha = layerColor.a * (1.0 - totalOpacity);
              color = mix(color, layerColor.rgb, alpha);
              totalOpacity = totalOpacity + alpha;
            }
          }
          
          if (uDebugMode) {
            // Debug mode: Show opacity values in grayscale
            color = vec3(totalOpacity);
          }
          
          gl_FragColor = vec4(color, 1.0);
        }
      `}
    />
  );
}