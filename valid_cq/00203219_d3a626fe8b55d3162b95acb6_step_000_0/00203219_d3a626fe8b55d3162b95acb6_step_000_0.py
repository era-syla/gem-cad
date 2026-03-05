import cadquery as cq

# Parameters for the U-channel geometry
length = 200.0
width = 40.0
height = 30.0
thickness = 4.0
hole_diameter = 6.0

# Define the U-profile points on the YZ plane
# The profile corresponds to the cross-section of the channel
# Coordinates are (y, z) relative to the sketch plane
pts = [
    (0, height),                    # Top-left outer
    (0, 0),                         # Bottom-left outer
    (width, 0),                     # Bottom-right outer
    (width, height),                # Top-right outer
    (width - thickness, height),    # Top-right inner
    (width - thickness, thickness), # Bottom-right inner
    (thickness, thickness),         # Bottom-left inner
    (thickness, height)             # Top-left inner
]

# Create the base extrusion
# We draw the profile on the YZ plane and extrude along the X axis
base = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(length)
)

# Add the mounting holes
# We select one of the side faces (at y=0)
# We use CenterOfMass to position the holes relative to the face center
result = (
    base
    .faces("<Y")
    .workplane(centerOption="CenterOfMass")
    .pushPoints([
        (-length * 0.25, 0),
        (0, 0),
        (length * 0.25, 0)
    ])
    # Cut holes slightly deeper than thickness to ensure a clean cut, 
    # but not deep enough to hit the opposite flange.
    .hole(hole_diameter, depth=thickness * 2.0)
)