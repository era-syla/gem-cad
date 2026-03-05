import cadquery as cq

# --- Parameter Definitions ---
# Plate dimensions
plate_width = 80.0   # Total width along the hinge axis (X-axis)
plate_length = 40.0  # Depth of the plate (Y-axis)
plate_thickness = 4.0

# Hinge knuckle dimensions
knuckle_outer_radius = 6.0
knuckle_inner_radius = 3.0
knuckle_length = 15.0 # Length of each cylindrical segment
knuckle_gap = 20.0    # Gap between the two knuckles (centered)

# Hole dimensions
hole_diameter = 5.0
csk_diameter = 9.0    # Countersink diameter
csk_angle = 90.0      # Countersink angle
hole_spacing_x = 50.0 # Distance between the two outer holes
hole_offset_y = 15.0  # Distance from the back edge (opposite hinge) to holes

# --- Derived Parameters ---
knuckle_offset_z = -plate_thickness / 2.0  # Align knuckles with bottom of plate or center? 
# Looking at image, knuckles seem tangent to the top surface or centered on thickness.
# Let's align the top of the knuckle with the top of the plate for a flush look, 
# or center them. The image suggests the knuckle centerline is below the plate surface.
# A common hinge design puts the pin axis slightly offset.
# Let's place the pin axis at Z = -knuckle_outer_radius + plate_thickness/2 (tangent bottom)
# Or simply center the knuckle axis relative to the plate edge. 
# Looking closely at the intersection, the cylinder centerline is likely aligned with the bottom face or slightly below.
# Let's assume the top of the cylinder is tangent to the top face of the plate.
knuckle_center_z = -knuckle_outer_radius + plate_thickness 

# --- Geometry Construction ---

# 1. Create the main base plate
# Centered on X and Y to make symmetry easier
base_plate = cq.Workplane("XY").box(plate_width, plate_length, plate_thickness)

# 2. Create the Hinge Knuckles
# The knuckles are cylinders located at the front edge (Y = -plate_length/2)
knuckle_y_pos = -plate_length / 2.0

# We need two knuckles. We can create one large cylinder and cut the middle, 
# or create two separate cylinders.
# Let's Create two separate cylinders.

# Left Knuckle
k1 = (cq.Workplane("YZ")
      .workplane(offset=-knuckle_gap/2 - knuckle_length)
      .center(knuckle_y_pos, knuckle_center_z)
      .circle(knuckle_outer_radius)
      .extrude(knuckle_length)
      )

# Right Knuckle
k2 = (cq.Workplane("YZ")
      .workplane(offset=knuckle_gap/2)
      .center(knuckle_y_pos, knuckle_center_z)
      .circle(knuckle_outer_radius)
      .extrude(knuckle_length)
      )

# Combine plate and knuckles
result = base_plate.union(k1).union(k2)

# 3. Create the pin hole through the knuckles
# This cuts through the entire width to ensure alignment
result = (result.faces("<X").workplane()
          .center(knuckle_y_pos, knuckle_center_z)
          .circle(knuckle_inner_radius)
          .cutThruAll()
          )

# 4. Create the mounting holes on the plate
# The image shows 3 holes. Two aligned, one offset in the middle.
# Let's approximate the pattern based on the visual.
# Two holes near the "back" (away from hinge), one hole near the hinge center.

# Hole coordinates relative to center
h1_x = -hole_spacing_x / 2.0
h2_x = hole_spacing_x / 2.0
back_row_y = (plate_length / 2.0) - 10.0 # 10mm from back edge
front_hole_y = -5.0 # Slightly towards the hinge

# Create points for the holes
# It looks like there are two holes near the outer edges and one in the center 
# but closer to the hinge. Or maybe two near the hinge and one back?
# Re-examining image:
# There are two holes towards the back (away from hinge) and one hole in the middle closer to the hinge?
# Actually, it looks like:
# - Left hole (back)
# - Right hole (back)
# - Middle hole (front)
# Let's assume a triangular pattern.

holes_pts = [
    (h1_x, back_row_y),
    (h2_x, back_row_y),
    (0, front_hole_y)
]

# Apply holes with countersink
result = (result.faces(">Z").workplane()
          .pushPoints(holes_pts)
          .cskHole(hole_diameter, csk_diameter, csk_angle)
          )

# Fillet the connection between plate and knuckles for a cleaner mesh/look (optional but good for realism)
# Identifying the edges where the plate meets the cylinder can be tricky automatically.
# We will skip the fillet to ensure robust execution without specific edge selectors failing.

# Final Result
part = result