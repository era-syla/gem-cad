import cadquery as cq

# --- Parametric Dimensions ---
height = 100.0        # Total height of the case
width = 60.0          # Total width of the case
depth = 12.0          # Thickness/Depth of the case
corner_radius = 6.0   # Radius of the main corners
wall_thickness = 1.5  # Thickness of the shell walls

# Feature dimensions
front_hole_dia = 12.0
front_hole_offset = 25.0  # Distance from center to hole center
top_hole_dia = 3.0
side_slot_length = 85.0
side_slot_width = 4.0

# --- 3D Modeling ---

# 1. Create the base block
# We start with a solid box centered on the XY plane
result = cq.Workplane("XY").box(width, height, depth)

# 2. Round the corners
# Select vertical edges (parallel to Z axis) and apply fillet
result = result.edges("|Z").fillet(corner_radius)

# 3. Shell the object
# Select the back face (at -Z) to remove, creating a hollow case
result = result.faces("<Z").shell(wall_thickness)

# 4. Cut the Front Hole (Camera/Logo hole)
# Select the front face (+Z), create a workplane, move center, and cut
result = (
    result.faces(">Z")
    .workplane()
    .center(0, front_hole_offset)
    .circle(front_hole_dia / 2.0)
    .cutThruAll()
)

# 5. Cut the Top Hole (Port/Microphone hole)
# Select the top face (+Y), create workplane, and cut
result = (
    result.faces(">Y")
    .workplane()
    .center(0, 0)
    .circle(top_hole_dia / 2.0)
    .cutThruAll()
)

# 6. Cut the Side Slot
# Select the left face (-X). 
# Note: On this face, the local X-axis typically aligns with the global Y-axis (Height).
# We use cutBlind with a negative value to cut inwards through the wall only.
result = (
    result.faces("<X")
    .workplane()
    .rect(side_slot_length, side_slot_width)
    .cutBlind(-wall_thickness * 3) # Cut distance sufficient to pierce the wall
)