import cadquery as cq
import math

# --- Parameters ---
total_length = 220.0     # Total length of the bar
bar_height = 20.0        # Vertical height of the bar
thickness = 8.0          # Thickness of the bar
arch_radius = 8.0        # Radius of the semi-circular cutouts
arch_spacing = 120.0     # Distance between the centers of the two arches
hole_offset = 18.0       # Horizontal distance from arch center to hole center
hole_diameter = 4.5      # Diameter of the through holes
hex_across_flats = 8.0   # Width across flats for the hex recess
hex_depth = 3.0          # Depth of the hex recess

# --- Derived Values ---
# Calculate the circumscribed diameter for the hexagon (required by polygon method)
# Relation: Diameter = 2 * (AcrossFlats / sqrt(3))
hex_diameter = 2 * hex_across_flats / math.sqrt(3)

# X coordinates for arch centers
arch_x_left = -arch_spacing / 2.0
arch_x_right = arch_spacing / 2.0

# Coordinates for the 4 mounting holes (x, y)
# Y is centered vertically. X is relative to arch centers.
hole_y = bar_height / 2.0
hole_locations = [
    (arch_x_left - hole_offset, hole_y),
    (arch_x_left + hole_offset, hole_y),
    (arch_x_right - hole_offset, hole_y),
    (arch_x_right + hole_offset, hole_y)
]

# --- Modeling ---

# 1. Base Geometry: Rectangular Bar
# Created on XY plane, extruded in Z
# Translated so the bottom edge aligns with Y=0
result = (
    cq.Workplane("XY")
    .rect(total_length, bar_height)
    .extrude(thickness)
    .translate((0, bar_height / 2.0, 0))
)

# 2. Cutouts: Semi-circular Arches
# Create cylinders to use as cutting tools
# Tools are made slightly larger in Z to ensure clean cuts
cutter_left = (
    cq.Workplane("XY")
    .moveTo(arch_x_left, 0)
    .circle(arch_radius)
    .extrude(thickness * 2)
    .translate((0, 0, -thickness / 2.0))
)

cutter_right = (
    cq.Workplane("XY")
    .moveTo(arch_x_right, 0)
    .circle(arch_radius)
    .extrude(thickness * 2)
    .translate((0, 0, -thickness / 2.0))
)

# Subtract the arches from the main body
result = result.cut(cutter_left).cut(cutter_right)

# 3. Holes: Through Holes
# Select the top face (Z = thickness) to start drilling
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_locations)
    .hole(hole_diameter)
)

# 4. Holes: Hexagonal Recesses
# Select the top face again to cut the counterbores
# 'polygon' creates a regular polygon; 6 sides for a hex
# Default orientation has flats on top/bottom, matching the image
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_locations)
    .polygon(6, hex_diameter)
    .cutBlind(-hex_depth)
)