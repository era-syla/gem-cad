import cadquery as cq

# --- Parametric Dimensions ---
# Base Block Dimensions
length = 100.0
width = 40.0
thickness = 20.0

# Top Face Holes
# Large central hole
center_hole_diam = 20.0
# Two side holes on top face
top_side_hole_diam = 10.0
top_side_hole_spacing = 60.0  # Distance between the two side holes (30 from center each way)

# Front Face Holes
# Two smaller holes on the front face
front_hole_diam = 6.0
front_hole_spacing = 50.0 # Distance between the two front holes
front_hole_height_ratio = 0.5 # Positioned at mid-height

# --- Geometry Construction ---

# 1. Create the base block
# We center it on X and Y for easier symmetric hole placement, but keep Z>0
result = cq.Workplane("XY").box(length, width, thickness)

# 2. Create the holes on the Top Face (Z-axis direction)
# Central hole
result = result.faces(">Z").workplane().hole(center_hole_diam)

# Side holes on top face
# We create points at (-30, 0) and (30, 0) relative to the center
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([
        (-top_side_hole_spacing / 2, 0), 
        (top_side_hole_spacing / 2, 0)
    ])
    .hole(top_side_hole_diam)
)

# 3. Create the holes on the Front Face (Y-axis direction)
# We select the front face (>Y or <Y depending on orientation, usually <Y is front in standard CAD views, 
# but let's stick to the visible face in the image which looks like a long side).
# Let's assume the long side facing us is -Y.
result = (
    result.faces("<Y")
    .workplane()
    .pushPoints([
        (-front_hole_spacing / 2, 0),
        (front_hole_spacing / 2, 0)
    ])
    .hole(front_hole_diam)
)

# If the front face is >Y, simply change faces("<Y") to faces(">Y")
# Based on the isometric view, if Z is up, X is right-left, Y is front-back.