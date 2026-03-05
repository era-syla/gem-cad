import cadquery as cq

# Parametric dimensions for the model
length = 120.0       # Length of the main extrusion
chord = 50.0         # Height of the airfoil section (leading to trailing edge)
thickness = 15.0     # Maximum thickness of the airfoil
hole_diameter = 9.0  # Diameter of the large hole
pin_diameter = 3.0   # Diameter of the small pin
pin_length = 18.0    # Length of the protruding pin

# Define coordinates for the airfoil profile
# The profile is sketched on the YZ plane: 
# Local Y axis corresponds to global Z (Height/Chord)
# Local X axis corresponds to global Y (Thickness)
p_nose = (0, chord / 2)
p_tail = (0, -chord / 2)

# Control points for the spline defining the right half (Tail -> Nose)
# Points define the curvature of the flank
pts_right = [
    (thickness / 2 * 0.5, -chord / 2 * 0.6),
    (thickness / 2, 0),
    (thickness / 2 * 0.8, chord / 2 * 0.6),
    p_nose
]

# Control points for the spline defining the left half (Nose -> Tail)
pts_left = [
    (-thickness / 2 * 0.8, chord / 2 * 0.6),
    (-thickness / 2, 0),
    (-thickness / 2 * 0.5, -chord / 2 * 0.6),
    p_tail
]

# 1. Generate the main body
# We draw the profile on the YZ plane and extrude along the X axis
result = (
    cq.Workplane("YZ")
    .moveTo(*p_tail)
    # Create right side curve with specific tangents for smoothness
    # Tangent at tail points slightly outwards, tangent at nose is horizontal
    .spline(pts_right, includeCurrent=True, tangents=[(0.3, 1.0), (-1.0, 0.0)])
    # Create left side curve to close the loop
    .spline(pts_left, includeCurrent=True, tangents=[(-1.0, 0.0), (-0.3, -1.0)])
    .close()
    .extrude(length)
)

# 2. Create the hole feature
# Select the end face (positive X direction)
end_face = result.faces(">X")

result = (
    end_face
    .workplane()
    # Position near the "nose" (top rounded part)
    .moveTo(0, chord / 2 * 0.6)
    .circle(hole_diameter / 2)
    .cutThruAll()
)

# 3. Create the pin feature
# Re-select the face on the modified body
result = (
    result.faces(">X")
    .workplane()
    # Position near the "tail" (bottom sharp part)
    .moveTo(0, -chord / 2 * 0.65)
    .circle(pin_diameter / 2)
    .extrude(pin_length)
)