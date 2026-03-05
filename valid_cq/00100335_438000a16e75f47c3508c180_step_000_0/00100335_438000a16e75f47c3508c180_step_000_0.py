import cadquery as cq

# Parametric dimensions based on image estimation
rear_shaft_diam = 12.0
rear_shaft_length = 30.0
rear_flat_offset = 4.5  # Distance from center to the flat face (D-shaft)

collar_diam = 18.0
collar_length = 10.0

front_shaft_diam = 8.0
front_shaft_length = 12.0

tip_chamfer_size = 1.5

# 1. Create the base rear shaft (Section 1)
# Oriented along Z-axis
result = cq.Workplane("XY").circle(rear_shaft_diam / 2.0).extrude(rear_shaft_length)

# 2. Create the collar (Section 2)
# Extruded from the top of the rear shaft
result = (
    result.faces(">Z")
    .workplane()
    .circle(collar_diam / 2.0)
    .extrude(collar_length)
)

# 3. Create the front shaft (Section 3)
# Extruded from the top of the collar
result = (
    result.faces(">Z")
    .workplane()
    .circle(front_shaft_diam / 2.0)
    .extrude(front_shaft_length)
)

# 4. Apply Chamfer to the tip (Section 4)
result = result.faces(">Z").edges().chamfer(tip_chamfer_size)

# 5. Cut the flat on the rear shaft (D-profile)
# Create a cutter box to remove material from the side of the rear shaft
cut_width = rear_shaft_diam * 2.0
cut_height = rear_shaft_diam  # Arbitrary large height to clear the material
cut_length = rear_shaft_length + 2.0  # Slightly longer to ensure clean cut at ends

# Calculate Y-center for the cutter box so its bottom face aligns with rear_flat_offset
# Box is centered, so center_y = limit + height/2
cutter_center_y = rear_flat_offset + (cut_height / 2.0)

cutter = (
    cq.Workplane("XY")
    .workplane(offset=rear_shaft_length / 2.0)  # Center Z relative to shaft
    .center(0, cutter_center_y)                 # Position Y to cut the flat
    .box(cut_width, cut_height, cut_length)
)

# Apply the cut
result = result.cut(cutter)