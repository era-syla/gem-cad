import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
height = 100.0          # Total height of the cylinder
outer_diameter = 40.0   # Outer diameter of the tube
wall_thickness = 5.0    # Thickness of the tube wall
hole_diameter = 10.0    # Diameter of the radial holes
hole_height = height / 2.0  # Height of the holes from the bottom

# Calculated derived parameters
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness
hole_radius = hole_diameter / 2.0

# 1. Create the main hollow cylinder
# Drawn on the XY plane with two concentric circles to form the wall
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(height)
)

# 2. Create the radial holes
# We define cutters (cylinders) oriented perpendicular to the Z-axis
# to subtract material from the main body.

# Cutter 1: Oriented along the X-axis (Creates holes at 0 and 180 degrees)
# We draw on the YZ plane (normal to X) and extrude along X
cutter_x = (
    cq.Workplane("YZ")
    .center(0, hole_height)  # Move local center to hole height (Global Y=0, Z=hole_height)
    .circle(hole_radius)
    .extrude(outer_diameter * 2, both=True)  # Extrude through the object
)

# Cutter 2: Oriented along the Y-axis (Creates holes at 90 and 270 degrees)
# We draw on the XZ plane (normal to Y) and extrude along Y
cutter_y = (
    cq.Workplane("XZ")
    .center(0, hole_height)  # Move local center to hole height (Global X=0, Z=hole_height)
    .circle(hole_radius)
    .extrude(outer_diameter * 2, both=True)
)

# 3. Apply the cuts to the main body
result = result.cut(cutter_x).cut(cutter_y)