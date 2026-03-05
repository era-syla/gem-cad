import cadquery as cq
import math

# --- Parameters ---
thickness = 2.0             # Thickness of the plate
outer_radius = 20.0         # Radius to the furthest corners
flat_width = 12.0           # Width of the flat sides (approximate)
notch_width = 4.0           # Width of the rectangular notches
notch_depth = 5.0           # Depth of the notches from the outer edge

# The shape is essentially an octagon with notches on the faces.
# Or, more simply, a disk/polygon with cuts.
# Let's model it as a base octagon and cut slots into it.

# Calculate parameters for a regular octagon
# If outer_radius is the circumradius (center to corner)
angle_step = 360.0 / 8.0

# --- Geometry Construction ---

# 1. Start with the base octagonal shape
# We create a polygon. We can use the circumscribed radius.
result = cq.Workplane("XY").polygon(8, outer_radius * 2).extrude(thickness)

# 2. Create the notches
# The notches appear to be rectangular cuts located at the center of each face.
# A regular octagon has 8 faces. We need to cut a rectangle into each face.

# We will iterate 8 times, rotating the workplane each time to cut the notch.
# Alternatively, we can define one cutting shape and polar array it.

# Define the cutting tool (a box)
# Dimensions: width = notch_width, depth = notch_depth, height = thickness (or more to be safe)
# The cutter needs to be positioned at the edge of the octagon.
# The apothem (distance from center to midpoint of a side) for an octagon is R * cos(22.5 deg)
apothem = outer_radius * math.cos(math.radians(22.5))

# Create the cutter profile
cutter = (
    cq.Workplane("XY")
    .rect(notch_width, notch_depth * 2) # Make it deep enough to cross the boundary
    .extrude(thickness * 2)             # Make it tall enough
    .translate((0, apothem, 0))         # Move to the edge
)

# Subtract the cutter from the base using a polar array approach
# We need to rotate the cutter 8 times around the Z axis
for i in range(8):
    angle = i * 45.0
    rotated_cutter = cutter.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.cut(rotated_cutter)

# Ideally, a cleaner CadQuery way without a loop variable assignment:
# We can use polarArray on a sketch, but since we are cutting from a solid, 
# let's try a 2D sketch approach which is often more robust.

# --- Alternative (cleaner) Approach: 2D Sketch ---

# Define the base octagon sketch
base_sketch = cq.Workplane("XY").polygon(8, outer_radius * 2)

# Define the notches sketch
# The notches are rectangles on the flats.
# We place a rectangle at the top (Y-positive) edge and polar array it.
# The center of the rectangle needs to be at y = apothem.
# However, to cut inward, the rectangle needs to overlap the edge.
# Center Y = apothem. Height = notch_depth * 2 (to ensure it cuts the edge).
notch_sketch = (
    cq.Workplane("XY")
    .center(0, apothem)
    .rect(notch_width, notch_depth * 2)
)

# Combine using polar array for the cuts
# We can't easily boolean 2D wires in basic CQ without forming faces first usually,
# but we can extrude the cut.

# Let's go with the solid operations approach as it's very readable.

result = (
    cq.Workplane("XY")
    .polygon(8, outer_radius * 2)
    .extrude(thickness)
)

# Define the single cut shape
# Position it so it cuts into the "top" face of the octagon
cut_shape = (
    cq.Workplane("XY")
    .translate((0, apothem))  # Move to the edge distance
    .rect(notch_width, notch_depth * 2) # Create rect centered at the edge
    .extrude(thickness)
)

# Apply cuts in a polar pattern
# We create 8 cuts rotated around the center
cuts = (
    cq.Workplane("XY")
    .polarArray(outer_radius, 0, 360, 8) # Radius doesn't matter much for location here if we translate manually, but let's stick to the rotate logic
    .eachpoint(lambda loc: cut_shape.val().located(loc)) # This isn't quite right for rotation logic combined with shape orientation
)

# Correct Logic for Rotated Cuts:
# 1. Create base
result = cq.Workplane("XY").polygon(8, outer_radius * 2).extrude(thickness)

# 2. Create a collection of cutting solids
for i in range(8):
    # Create a cutter at the origin
    # Move it to the perimeter (Y axis)
    # Rotate it around Z
    cutter = (
        cq.Workplane("XY")
        .rect(notch_width, notch_depth * 2)
        .extrude(thickness * 3) # generous thickness
        .translate((0, 0, -thickness)) # center Z slightly
        .translate((0, apothem, 0)) # move to edge
        .rotate((0,0,0), (0,0,1), i * 45) # rotate around center
    )
    result = result.cut(cutter)

# Ensure the result is returned
result = result