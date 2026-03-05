import cadquery as cq

# --- Parametric Dimensions ---
shaft_length = 150.0
shaft_diameter = 3.5
shaft_bore = 1.2  # Diameter of the hole at the top

float_diameter = 12.0
float_height = 15.0
float_bottom_fillet = 3.0  # Rounding at the bottom of the float

collar_diameter = 8.0
collar_thickness = 2.0
collar_elevation = 25.0  # Distance from the bottom of the model to the collar

# --- Geometry Construction ---

# 1. Create the Main Shaft
# A long vertical cylinder centered at the origin
shaft = cq.Workplane("XY").circle(shaft_diameter / 2.0).extrude(shaft_length)

# 2. Create the Float (Bottom Cylinder)
# Centered at the origin, encompassing the bottom of the shaft
float_body = (
    cq.Workplane("XY")
    .circle(float_diameter / 2.0)
    .extrude(float_height)
    # Select the bottom-most edge and apply a fillet for the rounded look
    .edges("<Z")
    .fillet(float_bottom_fillet)
)

# 3. Create the Collar (Stop Ring)
# Positioned at a specific height offset from the bottom
collar = (
    cq.Workplane("XY")
    .workplane(offset=collar_elevation)
    .circle(collar_diameter / 2.0)
    .extrude(collar_thickness)
)

# 4. Combine Parts into a Single Solid
# Union the shaft, float, and collar
result = shaft.union(float_body).union(collar)

# 5. Add the Central Hole
# Select the top face of the shaft and cut a hole through the entire depth
result = result.faces(">Z").workplane().hole(shaft_bore)