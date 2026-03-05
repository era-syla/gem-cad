import cadquery as cq
import math

# --- Parameters ---
# Dimensions based on the visual proportions of the hexagonal standoff
height = 40.0                # Total length of the standoff
width_across_flats = 12.0    # Hexagon width (flat to flat)
hole_diameter = 6.0          # Diameter of the central through-hole
chamfer_size = 0.5           # Size of the chamfer on the hole openings

# --- Geometric Calculations ---
# CadQuery's polygon method uses the circumscribed diameter (vertex to vertex).
# Relationship: Circumscribed Diameter = (2 * Width Across Flats) / sqrt(3)
circum_diameter = 2 * width_across_flats / math.sqrt(3)

# --- Modeling ---
result = (
    cq.Workplane("XY")
    # 1. Create the base hexagon profile
    .polygon(nSides=6, diameter=circum_diameter)
    # 2. Extrude to create the prism body
    .extrude(height)
    # 3. Select the top face to define the hole location
    .faces(">Z")
    .workplane()
    # 4. Cut the through-hole
    .hole(hole_diameter)
    # 5. Select top and bottom faces to find hole edges
    .faces(">Z or <Z")
    # 6. Select only the circular edges (the hole boundaries)
    .edges("%Circle")
    # 7. Apply chamfer
    .chamfer(chamfer_size)
)