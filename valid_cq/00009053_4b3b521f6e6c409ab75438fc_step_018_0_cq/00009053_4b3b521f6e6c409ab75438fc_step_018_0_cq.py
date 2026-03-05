import cadquery as cq

# Parametric dimensions
width = 100.0   # Overall width of the box
height = 100.0  # Overall height of the box
depth = 40.0    # Depth (thickness) of the box
wall_thickness = 10.0 # Thickness of the walls

# Create the main outer box
# Using Workplane centered on X and Y, and extruding in Z
result = (
    cq.Workplane("XY")
    .rect(width, height)
    .extrude(depth)
)

# Create the inner cutout
# Select the front face, draw a smaller rectangle, and cut through
result = (
    result.faces(">Z")
    .workplane()
    .rect(width - 2 * wall_thickness, height - 2 * wall_thickness)
    .cutThruAll()
)

# Alternatively, using the 'shell' operation which is often cleaner for hollow objects
# result = cq.Workplane("XY").box(width, height, depth).faces(">Z").shell(-wall_thickness)