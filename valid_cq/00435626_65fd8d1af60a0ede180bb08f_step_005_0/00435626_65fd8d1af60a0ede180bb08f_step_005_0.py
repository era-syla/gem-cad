import cadquery as cq

# --- Model Parameters ---
length = 300.0        # Total length of the beam
height = 60.0         # Vertical height of the beam
width_base = 40.0     # Width at the bottom base
width_top = 20.0      # Width at the top surface
hole_diam = 5.0       # Diameter of the mounting holes
hole_spacing_x = 35.0 # Horizontal distance between hole centers
hole_spacing_y = 20.0 # Vertical distance between hole centers (along the slanted face)

# --- Geometry Construction ---

# Define the trapezoidal profile points on the YZ plane
# The profile is centered around the Z-axis for symmetry
pts = [
    (width_base / 2.0, 0),
    (width_top / 2.0, height),
    (-width_top / 2.0, height),
    (-width_base / 2.0, 0)
]

# Create the main body by extruding the profile along the X-axis
# both=True ensures the origin remains at the center of the beam's length
result = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(length / 2.0, both=True)
)

# Create the 4-hole pattern on one of the slanted faces
# We select the face with the negative Y normal (front/side face)
result = (
    result
    .faces("<Y")
    .workplane()
    .rarray(hole_spacing_x, hole_spacing_y, 2, 2)
    .hole(hole_diam)
)