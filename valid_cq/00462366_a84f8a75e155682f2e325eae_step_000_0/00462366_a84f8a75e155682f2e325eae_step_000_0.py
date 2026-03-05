import cadquery as cq

# --- Parameters ---
length = 1000.0         # Total length of the tube
width = 40.0            # Outer width of the square profile
height = 40.0           # Outer height of the square profile
wall_thickness = 3.0    # Thickness of the tube walls
hole_diameter = 8.0     # Diameter of the mounting holes
hole_spacing = 300.0    # Distance of holes from the center of the beam

# --- Geometry Generation ---

# 1. Create the main hollow tube body
# We sketch on the YZ plane to orient the tube along the X axis.
# By drawing two rectangles (outer and inner) in the same sketch, 
# the area between them is extruded, creating a hollow tube.
result = (
    cq.Workplane("YZ")
    .rect(width, height)
    .rect(width - 2 * wall_thickness, height - 2 * wall_thickness)
    .extrude(length)
)

# 2. Cut mounting holes
# Select the top face (+Z direction), establish a workplane centered on that face,
# and cut holes through the tube.
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-hole_spacing, 0),  # Hole towards one end
        (hole_spacing, 0)    # Hole towards the other end
    ])
    .hole(hole_diameter)
)

# The 'result' variable now contains the final valid 3D solid.