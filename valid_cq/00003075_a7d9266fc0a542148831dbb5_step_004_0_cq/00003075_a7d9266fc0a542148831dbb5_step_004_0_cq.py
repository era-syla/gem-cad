import cadquery as cq

# --- Parametric Dimensions ---
# Base Flange Dimensions
base_diameter = 100.0
base_thickness = 10.0

# Central Cylinder Dimensions
cylinder_height = 80.0     # Total height from the bottom of the base
cylinder_outer_diam = 40.0
cylinder_inner_diam = 30.0 # Creates the central bore

# Bolt Hole Pattern
bolt_circle_diam = 75.0
num_holes = 8
hole_diameter = 10.0

# --- Geometry Construction ---

# 1. Create the Base Flange
# We start by drawing a circle on the XY plane and extruding it.
base = (
    cq.Workplane("XY")
    .circle(base_diameter / 2.0)
    .extrude(base_thickness)
)

# 2. Create the Vertical Cylinder
# We select the top face of the base and extrude the cylinder upwards.
# Note: To get total height, we extrude by (cylinder_height - base_thickness)
vertical_post = (
    base.faces(">Z")
    .workplane()
    .circle(cylinder_outer_diam / 2.0)
    .extrude(cylinder_height - base_thickness)
)

# 3. Create the Central Bore
# Cut a hole through the entire assembly along the Z-axis.
part_with_bore = (
    vertical_post.faces(">Z")
    .workplane()
    .hole(cylinder_inner_diam)
)

# 4. Create the Bolt Holes
# Create a pattern of holes on the base flange.
result = (
    part_with_bore.faces("<Z") # Select the bottom face to drill upwards (or select top of flange)
    .workplane()
    .polarArray(bolt_circle_diam / 2.0, 0, 360, num_holes)
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)

# Alternative method for selecting face for bolt holes if preferred:
# result = part_with_bore.faces(">Z[1]").workplane()... (selecting the flange top face)
# But selecting the bottom face and cutting through all is robust.

# Export or visualization
if 'show_object' in globals():
    show_object(result)