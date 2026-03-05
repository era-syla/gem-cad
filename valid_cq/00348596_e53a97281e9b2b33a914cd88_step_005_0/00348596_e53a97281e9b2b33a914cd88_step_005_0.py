import cadquery as cq

# Parametric Dimensions
length = 300.0         # Total length of the strip
width = 30.0           # Total width
height = 4.0           # Total height
flat_top_width = 10.0  # Width of the flat top surface
side_wall_height = 1.0 # Height of the vertical side walls
hole_diameter = 3.5    # Diameter of mounting holes
csk_diameter = 6.5     # Countersink diameter
hole_offset = 20.0     # Distance of holes from ends

# Define the cross-section profile
# Drawn on the YZ plane to extrude along the X axis
# Profile is centered on the Y axis
pts = [
    (-width / 2, 0),                 # Bottom-left corner
    (width / 2, 0),                  # Bottom-right corner
    (width / 2, side_wall_height),   # Vertical side right
    (flat_top_width / 2, height),    # Slope up to top right
    (-flat_top_width / 2, height),   # Top left
    (-width / 2, side_wall_height)   # Slope down to side left
]

# Create the base extrusion
# Extrude symmetrically along X axis
base = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(length, both=True)
)

# Add countersunk holes at both ends
result = (
    base
    .faces(">Z") # Select the top face
    .workplane()
    .pushPoints([
        (-length / 2 + hole_offset, 0), 
        (length / 2 - hole_offset, 0)
    ])
    .cskHole(hole_diameter, csk_diameter, 90.0)
)