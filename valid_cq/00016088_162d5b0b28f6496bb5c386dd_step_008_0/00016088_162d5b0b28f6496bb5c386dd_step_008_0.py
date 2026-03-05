import cadquery as cq

# --- Parametric Dimensions ---
height = 80.0           # Overall height of the vertical leg
length = 80.0           # Overall length of the horizontal leg
width = 80.0            # Width of the bracket (extrusion depth)
thickness = 12.0        # Thickness of the plate ends
fillet_radius = 2.0     # Radius for the outer corner fillet
hole_diameter = 6.5     # Diameter of the through holes
csk_diameter = 12.0     # Diameter of the countersink
csk_angle = 90.0        # Angle of the countersink
hole_spacing_x = 50.0   # Horizontal spacing between holes (width direction)
hole_spacing_z = 50.0   # Vertical spacing between holes (height direction)

# --- Geometry Construction ---

# 1. Create the Base Profile
# sketch on the YZ plane (Side View)
# Y axis corresponds to the horizontal leg, Z axis to the vertical leg.
# The profile includes the outer 90-degree corner and the inner diagonal web.
result = (
    cq.Workplane("YZ")
    .polyline([
        (0, 0),                 # Outer corner (origin)
        (0, height),            # Top outer tip
        (thickness, height),    # Top inner tip
        (length, thickness),    # End inner tip (connecting diagonal)
        (length, 0),            # End outer tip
        (0, 0)                  # Close profile to origin
    ])
    .close()
    .extrude(width)             # Extrude along X axis
)

# 2. Fillet the Outer Corner
# Select the edge at the intersection of the minimum Y and minimum Z bounds (the spine)
result = result.edges("<Y and <Z").fillet(fillet_radius)

# 3. Add Countersunk Holes
# Select the vertical outer face (located at Y=0)
# Create a workplane on this face, define a grid of points, and cut holes
result = (
    result.faces("<Y")
    .workplane()
    .rarray(hole_spacing_x, hole_spacing_z, 2, 2, True)
    .cskHole(hole_diameter, csk_diameter, csk_angle)
)