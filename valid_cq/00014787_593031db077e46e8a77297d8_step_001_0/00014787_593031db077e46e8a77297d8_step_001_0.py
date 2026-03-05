import cadquery as cq

# --- Parametric Dimensions ---
# Beam dimensions
beam_length = 120.0
beam_width = 20.0
beam_height = 8.0
web_thickness = 2.0
flange_thickness = 1.5

# Nut dimensions
nut_distance = 20.0   # Distance from the end of the beam
nut_diameter = 9.0    # Circumscribed diameter (size across corners)
nut_thickness = 4.0
hole_diameter = 4.0

# --- Geometry Construction ---

# 1. Create the I-Beam Profile
# We define the profile on the YZ plane (X is the extrusion axis)
# Coordinates are (Y, Z)
w, h, tw, tf = beam_width, beam_height, web_thickness, flange_thickness

# Define points for the I-profile starting from top-right corner and going clockwise
profile_pts = [
    (w/2, h/2),             # Top-Right Outer
    (w/2, h/2 - tf),        # Top-Right Inner
    (tw/2, h/2 - tf),       # Web Top-Right
    (tw/2, -h/2 + tf),      # Web Bottom-Right
    (w/2, -h/2 + tf),       # Bottom-Right Inner
    (w/2, -h/2),            # Bottom-Right Outer
    (-w/2, -h/2),           # Bottom-Left Outer
    (-w/2, -h/2 + tf),      # Bottom-Left Inner
    (-tw/2, -h/2 + tf),     # Web Bottom-Left
    (-tw/2, h/2 - tf),      # Web Top-Left
    (-w/2, h/2 - tf),       # Top-Left Inner
    (-w/2, h/2)             # Top-Left Outer
]

# Generate the beam by extruding the profile
beam = (
    cq.Workplane("YZ")
    .polyline(profile_pts)
    .close()
    .extrude(beam_length)
)

# 2. Create the Hex Nut
# Determine position along X axis
nut_pos_x = beam_length + nut_distance

# Generate the nut geometry
nut = (
    cq.Workplane("YZ")
    .workplane(offset=nut_pos_x)  # Offset plane along X axis
    .polygon(6, nut_diameter)     # Hexagon
    .circle(hole_diameter / 2)    # Central hole
    .extrude(nut_thickness)
)

# 3. Combine parts into final result
result = beam.union(nut)