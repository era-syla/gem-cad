import cadquery as cq

# --- Model Parameters ---
total_length = 200.0
width = 20.0
base_height = 10.0       # Thickness of the ends (shelf height)
center_raise = 6.0       # Additional height of the central section
shelf_length = 30.0      # Length of the stepped-down area at each end
hole_diameter = 6.0
tab_size = 3.0           # Length/Width of the small corner tabs
tab_height = 2.0         # Height of the tabs above the shelf

# --- Construction ---

# 1. Base Geometry
# Create the full-length underlying rectangular bar.
# We position Z=0 at the bottom.
result = cq.Workplane("XY").box(total_length, width, base_height, centered=(True, True, False))

# 2. Central Raised Section
# Calculate the length of the central raised area based on shelf length
center_length = total_length - (2 * shelf_length)

# Create the center block on top of the base and unite it
center_block = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .rect(center_length, width)
    .extrude(center_raise)
)
result = result.union(center_block)

# 3. Corner Tabs
# There are 4 small tabs located at the very corners of the shelf surfaces.
# We calculate the center coordinates for these tabs.
x_tab_pos = (total_length / 2) - (tab_size / 2)
y_tab_pos = (width / 2) - (tab_size / 2)

tab_points = [
    (x_tab_pos, y_tab_pos),
    (x_tab_pos, -y_tab_pos),
    (-x_tab_pos, y_tab_pos),
    (-x_tab_pos, -y_tab_pos)
]

# Extrude the tabs from the shelf level
tabs = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .pushPoints(tab_points)
    .rect(tab_size, tab_size)
    .extrude(tab_height)
)
result = result.union(tabs)

# 4. Mounting Holes
# The holes are centered in the shelf area.
x_hole_pos = (total_length / 2) - (shelf_length / 2)
hole_points = [(x_hole_pos, 0), (-x_hole_pos, 0)]

# Cut the holes through the entire assembly from the bottom face
result = (
    result.faces("<Z")
    .workplane()
    .pushPoints(hole_points)
    .hole(hole_diameter)
)