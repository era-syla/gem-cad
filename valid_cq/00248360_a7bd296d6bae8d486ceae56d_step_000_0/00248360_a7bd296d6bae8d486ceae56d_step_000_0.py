import cadquery as cq

# --- Parametric Dimensions ---
total_length = 60.0       # Total length of the pin
diameter = 12.0           # Main diameter of the cylindrical body
flat_thickness = 8.0      # Distance between the two flat parallel surfaces
groove_width = 0.5        # Width of the central seam/groove
groove_depth = 0.4        # Depth of the central groove
hole_diameter = 2.0       # Diameter of the hole at the tip
hole_depth = 4.0          # Depth of the hole

# Derived parameters
radius = diameter / 2.0
cyl_length = total_length - diameter  # Length of the straight cylindrical section

# --- Modeling ---

# 1. Create the Base Capsule (Cylinder + 2 Spheres)
# Create a cylinder aligned with the X-axis, centered at the origin
cylinder = cq.Workplane("YZ").circle(radius).extrude(cyl_length, both=True)

# Create spheres for the rounded ends
# The cylinder ends are at +/- cyl_length/2
sphere_left = cq.Workplane("YZ").sphere(radius).translate((-cyl_length / 2.0, 0, 0))
sphere_right = cq.Workplane("YZ").sphere(radius).translate((cyl_length / 2.0, 0, 0))

# Combine them into a single capsule solid
capsule = cylinder.union(sphere_left).union(sphere_right)

# 2. Cut the Flat Sides
# We cut material along the Y-axis to flatten the sides
# Create a large box to represent the volume to remove
cut_box_size = total_length * 2.0
y_cut_offset = (flat_thickness / 2.0) + (cut_box_size / 2.0)

# Create cutters for positive and negative Y sides
cutter_top = cq.Workplane("XY").box(cut_box_size, cut_box_size, cut_box_size).translate((0, y_cut_offset, 0))
cutter_bottom = cq.Workplane("XY").box(cut_box_size, cut_box_size, cut_box_size).translate((0, -y_cut_offset, 0))

# Apply the cuts
flattened_body = capsule.cut(cutter_top).cut(cutter_bottom)

# 3. Create the Central Groove
# Create a tube shape to subtract from the center to create the groove
groove_cutter = (
    cq.Workplane("YZ")
    .circle(radius + 2.0)            # Outer boundary (larger than body)
    .circle(radius - groove_depth)   # Inner boundary (defines groove floor)
    .extrude(groove_width, both=True)
)

grooved_body = flattened_body.cut(groove_cutter)

# 4. Create the End Hole
# Create a cylinder to cut the hole at the left tip (-X end)
# The tip of the sphere is at x = -total_length / 2
hole_cutter = (
    cq.Workplane("YZ")
    .circle(hole_diameter / 2.0)
    .extrude(hole_depth)
    .translate((-total_length / 2.0, 0, 0))
)

# Final Boolean Cut
result = grooved_body.cut(hole_cutter)