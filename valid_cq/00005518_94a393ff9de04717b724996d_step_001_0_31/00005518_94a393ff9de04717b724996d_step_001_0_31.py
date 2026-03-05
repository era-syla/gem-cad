import cadquery as cq

# Parametric dimensions based on visual proportions
width = 100.0            # Outer width of the frame
height = 60.0            # Outer height of the frame
frame_width = 10.0       # Width of the frame's border
depth = 5.0              # Extrusion depth (thickness) of the model
cylinder_radius = 7.0    # Radius of the corner cylinder

# Create the main rectangular frame
# This is done by drawing the outer rectangle, then the inner rectangle to create a profile, 
# and finally extruding it.
frame = (
    cq.Workplane("XY")
    .rect(width, height)
    .rect(width - 2 * frame_width, height - 2 * frame_width)
    .extrude(depth)
)

# Create the cylinder at the bottom-right corner
# The bottom-right outer vertex is located at (width/2, -height/2)
cylinder = (
    cq.Workplane("XY")
    .center(width / 2.0, -height / 2.0)
    .circle(cylinder_radius)
    .extrude(depth)
)

# Combine the frame and the cylinder into a single solid
result = frame.union(cylinder)