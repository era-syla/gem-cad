import cadquery as cq

# -- Parametric Dimensions --
# Main body dimensions
height = 110.0
width = 60.0
thickness = 16.0
corner_radius = 8.0   # Vertical corner radius
face_radius = 5.0     # Edge rounding for the domed/pillow look

# Connector dimensions
conn_width = 14.0
conn_thickness = 8.0
conn_length = 12.0
conn_fillet = 2.0

# Cable dimensions
cable_diam = 3.5

# -- Modeling --

# 1. Main Enclosure
# Modeled as a box with rounded corners and rounded edges to simulate the "pillowed" clamshell shape
main_body = (
    cq.Workplane("XY")
    .box(width, height, thickness)
    .edges("|Z").fillet(corner_radius)  # Round the four vertical corners
    .edges("#Z").fillet(face_radius)    # Round the top and bottom face edges
)

# 2. USB Connector / Strain Relief
# Located at the bottom center of the device
connector = (
    cq.Workplane("XZ")
    .workplane(offset=-height/2)
    .rect(conn_width, conn_thickness)
    .extrude(-conn_length)
    .edges("|Y").fillet(conn_fillet)    # Round the connector profile
)

# 3. Cable
# Defined by a spline path starting from the connector
start_y = -height/2 - conn_length

# Points for the spline path (curving downwards and to the side)
path_points = [
    (0, start_y),             # Start point
    (0, start_y - 15),        # Go straight down a bit
    (10, start_y - 35),       # Start curving
    (25, start_y - 50)        # End point
]

# Create the path object
path = (
    cq.Workplane("XY")
    .moveTo(*path_points[0])
    .spline(path_points[1:])
)

# Create the cable solid by sweeping a circle along the path
cable = (
    cq.Workplane("XZ")
    .workplane(offset=start_y)
    .circle(cable_diam / 2.0)
    .sweep(path)
)

# -- Final Assembly --
result = main_body.union(connector).union(cable)