---
name: blender-render-automation
description: Procedural icosphere modeling guidelines and structural Solidify-after-Shrinkwrap 3D projection techniques inside Blender.
---

# Blender Automation and Procedural Modeling

## Overview

Blender headless automation allows developers to procedurally build 3D assets, apply structural modifiers, and render high-resolution assets using command-line scripts. This document details the math and workflow for generating procedural icospheres and utilizing the Solidify-after-Shrinkwrap 3D projection technique.

## Procedural Icosphere Modeling

An icosphere is a geodesic dome constructed by recursively subdividing a regular icosahedron. Unlike standard UV spheres, icospheres distribute vertices evenly across the surface, making them ideal for physics simulations, terrain generation, and clean geometric modeling.

### Core Mathematical Steps
1. **Initial Icosahedron**: Begin with 12 vertices defined by coordinates using the golden ratio `phi = (1 + sqrt(5)) / 2`.
2. **Subdivision**: For each subdivision level, split every triangular face into 4 smaller triangles by creating new vertices at the midpoint of each edge.
3. **Projection**: Project the new midpoint vertices outward to the target sphere radius using vector normalization: `v_new = (v / |v|) * Radius`.

## Solidify-after-Shrinkwrap Projection

The Solidify-after-Shrinkwrap technique is a high-fidelity modeling pipeline used to wrap procedural details or panels tightly onto a complex base mesh while maintaining clean, uniform shell thickness.

### Modifier Pipeline Order

To prevent intersection errors and uneven surfaces, you must apply modifiers in this exact sequence:

```
[Target Base Mesh] <--- (Projections Target)
                               |
[Source Panel Mesh] ---> [Shrinkwrap Modifier] ---> [Solidify Modifier] ---> [Bevel Modifier]
```

1. **Shrinkwrap Modifier**: Projects the vertices of the Source Panel Mesh onto the surface of the Target Base Mesh.
   - *Wrap Method*: Project
   - *Snap Mode*: On Surface
   - *Offset*: A small positive value (e.g., `0.002` meters) to prevent Z-fighting.
2. **Solidify Modifier**: Extrudes the wrapped panel outward, giving it physical depth.
   - *Thickness*: Set your target shell thickness (e.g., `0.02` meters).
   - *Offset*: `1.0` (extrudes outward) or `-1.0` (extrudes inward).
   - *Boundary Check*: Ensure "Even Thickness" is enabled to prevent corner pinch.
3. **Bevel Modifier**: Adds a subtle roundness to the sharp extruded edges to catch rendering lights.
   - *Segments*: `2` or `3`
   - *Amount*: Keep it small (e.g., `0.005` meters).

## Execution and Automation

Using headless Blender execution, these steps are fully scriptable. The companion automation template (`optix_cycles_render.py`) implements this pipeline, loading Blender headless, configuring OptiX hardware acceleration, and outputting clean procedural render frames.
