import cadquery as cq

# --- Parametric Dimensions ---
length = 600.0          # Total length of the tube
width = 30.0            # Width of the square profile
height = 30.0           # Height of the square profile
wall_thickness = 2.5    # Thickness of the tube walls
hole_offset = 100.0     # Distance of the holes from the end
side_hole_dia = 8.0     # Diameter of the larger hole on the side
top_hole_dia = 4.0      # Diameter of the smaller hole on the top

# --- 3D Geometry Generation ---

# 1. Create the base hollow rectangular tube
# We sketch two concentric rectangles on the YZ plane and extrude along the X axis.
result = (
    cq.Workplane("YZ")
    .rect(width, height)
    .rect(width - 2*wall_thickness, height - 2*wall_thickness)
    .extrude(length)
)

# 2. Cut the hole in the side face
# Select the face in the +Y direction (side face)
# Shift the workplane center from the face center (length/2) to the desired offset location
result = (
    result
    .faces(">Y")
    .workplane()
    .center(length/2 - hole_offset, 0)
    .hole(side_hole_dia)
)

# 3. Cut the hole in the top face
# Select the face in the +Z direction (top face)
# Align it with the side hole along the length
result = (
    result
    .faces(">Z")
    .workplane()
    .center(length/2 - hole_offset, 0)
    .hole(top_hole_dia)
)