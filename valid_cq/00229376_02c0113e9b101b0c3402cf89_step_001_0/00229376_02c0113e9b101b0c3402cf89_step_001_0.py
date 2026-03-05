import cadquery as cq

# ==============================================================================
# 3D Model Parameters
# ==============================================================================
# Dimensions estimated from the image geometry
base_diameter = 40.0
base_height = 12.0
waist_diameter = 22.0     # Diameter at the narrowest point
waist_height = 36.0       # Height from bottom to the waist inflection point
top_diameter = 34.0
total_height = 60.0
inner_diameter = 12.0     # Central bore diameter
slot_width = 4.0          # Width of the gaps between fingers
num_fingers = 6           # Number of segments

# ==============================================================================
# Geometry Construction
# ==============================================================================

# 1. Define the Revolution Profile
# Working in the XZ plane where X is Radius and Y is Z-Height
r_base = base_diameter / 2.0
r_waist = waist_diameter / 2.0
r_top = top_diameter / 2.0
r_inner = inner_diameter / 2.0

# Define points counter-clockwise starting from bottom-inner
profile_points = [
    (r_inner, 0),                 # Bottom Inner Corner
    (r_base, 0),                  # Bottom Outer Corner
    (r_base, base_height),        # Top of Base Cylinder
    (r_waist, waist_height),      # Waist Point (narrowest)
    (r_top, total_height),        # Top Outer Corner
    (r_inner, total_height)       # Top Inner Corner
]

# 2. Create the Main Body
# Revolve the profile around the Z-axis to create the solid form
# The .close() method automatically connects the last point back to the first (creating the inner wall)
main_body = (
    cq.Workplane("XZ")
    .polyline(profile_points)
    .close()
    .revolve()
)

# 3. Create Slots
# Calculate slot dimensions
cut_height = total_height - base_height
cut_z_center = base_height + (cut_height / 2.0)

# Create a cutter object (a box) representing the empty space of a slot
# The box is centered vertically on the finger section
# Length is set large enough to cut through the entire diameter
cutter = (
    cq.Workplane("XY")
    .workplane(offset=cut_z_center)
    .box(base_diameter * 2.5, slot_width, cut_height)
)

# 4. Apply Cuts to Create Segments
result = main_body

# We perform boolean cuts. Since the cutter passes through the center,
# each operation cuts two opposite slots. We need num_fingers / 2 operations.
for i in range(num_fingers // 2):
    angle = i * (360.0 / num_fingers)
    # Rotate the cutter around the Z-axis
    rotated_cutter = cutter.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.cut(rotated_cutter)