import cadquery as cq

# -- Parametric Dimensions --
length = 200.0      # Total length of the rail
width = 12.0        # Width (thickness)
height = 12.0       # Height
fillet_radius = 3.0 # Radius for the top edges
hole_diameter = 4.0 # Diameter of the side holes

# -- Geometry Generation --

# 1. Create the base rectangular profile aligned with the X-axis
# Centered at (0,0,0)
result = cq.Workplane("XY").box(length, width, height)

# 2. Create the rounded top profile
# Select the top face (>Z) and then filter for edges parallel to the X-axis (|X)
result = result.faces(">Z").edges("|X").fillet(fillet_radius)

# 3. Add the mounting holes
# Define positions relative to the center of the side face
# Pattern based on image: One hole at left, two holes clustered at right
hole_locations = [
    (-length/2 + 15, 0),         # Left end hole
    (length/2 - 45, 0),          # Right inner hole
    (length/2 - 15, 0)           # Right end hole
]

# Select the side face (>Y), create workplane, and cut holes through
result = (
    result.faces(">Y")
    .workplane()
    .pushPoints(hole_locations)
    .hole(hole_diameter)
)