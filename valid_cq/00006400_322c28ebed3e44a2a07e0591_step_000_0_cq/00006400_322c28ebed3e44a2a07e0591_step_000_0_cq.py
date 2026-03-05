import cadquery as cq

# Parametric dimensions
plate_length = 200.0
plate_height = 60.0
plate_thickness = 5.0

# Hinge/Knuckle dimensions
knuckle_radius = 8.0
knuckle_length = 30.0  # Height of the cylindrical hinge part
knuckle_wall_thickness = 3.0
pin_hole_radius = knuckle_radius - knuckle_wall_thickness

# Hole configuration
num_holes = 4
hole_radius = 2.5  # M5 screw clearance roughly
# Position holes near the top edge
hole_y_offset = (plate_height / 2.0) - 10.0 
# Calculate hole spacing
hole_spacing = (plate_length - 40.0) / (num_holes - 1)

# Create the main rectangular plate
# We center it first for easier hole positioning later
plate = cq.Workplane("XY").box(plate_length, plate_height, plate_thickness)

# Create the hinge knuckle
# It's a hollow cylinder attached to the left side (-X)
# We position it relative to the left face of the plate
knuckle = (
    cq.Workplane("XY")
    .workplane(offset=-knuckle_length / 2.0) # Move to start of cylinder
    .moveTo(-plate_length / 2.0 - knuckle_radius + plate_thickness/2.0, -plate_height/2.0 + knuckle_length/2.0) # Position: flush with left edge
    # Actually, looking at image, it's on the left vertical edge.
    # Let's adjust coordinate system: 
    # Let plate center be (0,0,0). Left edge is at x = -plate_length/2
    # The knuckle is a vertical cylinder attached to the left edge.
    # The image shows the knuckle height is less than the plate height, aligned with the bottom corner.
)

# Let's rebuild more systematically.

# 1. Main Plate
main_plate = cq.Workplane("XY").box(plate_length, plate_height, plate_thickness)

# 2. Hinge Knuckle
# Located at the bottom-left corner.
# Cylinder axis is Z-aligned in local coordinates if we extrude, but the plate is XY.
# Let's make the cylinder along the Y axis relative to the plate face, or just add a cylinder object.
knuckle_center_x = -plate_length/2.0 - knuckle_radius
knuckle_center_y = -plate_height/2.0 + knuckle_length/2.0
# The image shows the knuckle offset slightly or flush. Let's assume the tangent of the knuckle touches the plate face.
# Actually, standard hinges usually have the pin center aligned or offset. 
# Looking at the image, the knuckle is on the *end* of the plate.
# Let's place the cylinder center at x = -plate_length/2.
knuckle_center_x = -plate_length/2.0

# The knuckle seems to be shorter than the plate height, aligned with the bottom.
knuckle_z_start = -plate_thickness/2.0 # flush with back? No, usually centered or on one side.
# Let's assume the plate is tangential to the cylinder for a weld-on hinge or bent leaf.
# Based on the shading, it looks like a bent leaf (piano hinge style) or a welded tube.
# Let's model it as a tube fused to the side edge.

hinge_knuckle = (
    cq.Workplane("XY")
    .workplane(offset=-plate_thickness/2.0) # Start plane
    .moveTo(-plate_length/2.0, -plate_height/2.0 + knuckle_length/2.0)
    # This orientation is tricky. Let's use basic shapes and union.
)

# Alternative approach: Build parts and union.
# Plate center at (0,0,0)
plate_part = cq.Workplane("XY").box(plate_length, plate_height, plate_thickness)

# Knuckle: Cylinder along Y axis (vertical in the image's perspective of the plate standing up, 
# but in XY plane 'height' is Y). 
# The image shows the knuckle on the left edge (min X), bottom corner (min Y).
knuckle_part = (
    cq.Workplane("ZX") # Plane perpendicular to Y
    .workplane(offset=plate_height/2.0 - knuckle_length/2.0) # Move down to bottom area (Coordinate system flip logic needed)
)

# Let's stick to world coordinates for clarity.
# Plate: Center (0,0,0). Extent X: +/- 100, Y: +/- 30, Z: +/- 2.5
# Left edge at X = -100.
# Bottom edge at Y = -30.

# The knuckle is a cylinder with Axis along Y.
# Position: X = -100 - radius (tangent) or X = -100 (center). 
# Image looks like a "weld-on" bullet hinge or similar where the barrel is offset.
# Let's put the cylinder center at X = -plate_length/2 - knuckle_radius + 1 (overlap).
knuckle_x = -plate_length/2.0 - knuckle_radius + 2.0 # Slight overlap for union
knuckle_y_bottom = -plate_height/2.0
knuckle_center = cq.Vector(knuckle_x, knuckle_y_bottom + knuckle_length/2.0, 0)

knuckle_solid = (
    cq.Workplane("XZ") # Draw on XZ plane to extrude along Y
    .workplane(offset=knuckle_y_bottom) # Start at bottom of plate
    .center(knuckle_x, 0) # Center of circle
    .circle(knuckle_radius)
    .extrude(knuckle_length)
)

# Inner hole for pin
knuckle_hole = (
    cq.Workplane("XZ")
    .workplane(offset=knuckle_y_bottom)
    .center(knuckle_x, 0)
    .circle(pin_hole_radius)
    .extrude(knuckle_length)
)

# Create the union
result = plate_part.union(knuckle_solid).cut(knuckle_hole)

# 3. Add Holes
# The holes are arrayed along the top edge.
# We will select the front face and add points.

hole_points = []
start_x = -plate_length/2.0 + 30.0 # Start offset from left
# Generate points
for i in range(num_holes):
    hole_points.append((start_x + i * hole_spacing, hole_y_offset))

result = (
    result.faces(">Z") # Select the top face (Z-axis is thickness)
    .workplane()
    .pushPoints(hole_points)
    .cskHole(hole_radius * 2, hole_radius * 4, 82) # Countersunk holes
)

# Export or display
# show_object(result)