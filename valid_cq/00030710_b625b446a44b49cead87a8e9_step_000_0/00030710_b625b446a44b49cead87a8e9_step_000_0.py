import cadquery as cq

# --- Parametric Dimensions ---
# Main body dimensions
body_diameter = 16.0
body_radius = body_diameter / 2.0

# Segment lengths (from Rear/Bottom to Front/Top)
len_rear = 12.0
len_mid = 14.0
len_front = 12.0

# Groove definition
groove_width = 0.5
groove_depth = 0.4

# Shaft dimensions
shaft_diameter = 3.0
shaft_length = 9.0
shaft_flat_cut = 0.5  # Depth of the D-cut

# Front notch dimensions
notch_width = 2.5
notch_depth = 1.5
notch_height = 2.0

# --- Geometry Construction ---

# 1. Create Main Body Cylinder
# Calculate groove positions and total length
z_groove1 = len_rear
z_groove2 = len_rear + groove_width + len_mid
total_length = len_rear + groove_width + len_mid + groove_width + len_front

# Start with a solid cylinder
body = cq.Workplane("XY").circle(body_radius).extrude(total_length)

# 2. Create Grooves
# Helper function to create a ring cutter for the grooves
def create_groove_cutter(z_pos):
    return (cq.Workplane("XY")
            .workplane(offset=z_pos)
            .circle(body_radius + 1.0)  # Outer boundary (larger than body)
            .circle(body_radius - groove_depth)  # Inner groove floor
            .extrude(groove_width))

# Apply groove cuts
body = body.cut(create_groove_cutter(z_groove1))
body = body.cut(create_groove_cutter(z_groove2))

# 3. Add Details to Ends
# Rear chamfer (Bottom)
body = body.edges("<Z").chamfer(0.8)

# Front chamfer (Top)
body = body.edges(">Z").chamfer(0.5)

# 4. Create Front Notch
# Positioned on the rim of the front face
notch_cutter = (cq.Workplane("XY")
                .workplane(offset=total_length - notch_height)
                .center(body_radius, 0)  # Move center to the edge
                .box(notch_depth * 2, notch_width, notch_height * 2))

body = body.cut(notch_cutter)

# 5. Create Output Shaft with D-profile
shaft_radius = shaft_diameter / 2.0

# Base shaft cylinder
shaft = (cq.Workplane("XY")
         .workplane(offset=total_length)
         .circle(shaft_radius)
         .extrude(shaft_length))

# Create the D-cut (flat section)
# Calculate position for the flat cut
flat_distance_from_center = shaft_radius - shaft_flat_cut
cutter_size = 10.0

# Create a cutting box offset from the center
d_cut_tool = (cq.Workplane("XY")
              .workplane(offset=total_length)
              .center(0, flat_distance_from_center + cutter_size / 2.0)
              .box(shaft_diameter * 2, cutter_size, shaft_length * 2))

shaft = shaft.cut(d_cut_tool)

# 6. Final Assembly
# Union the body and the shaft
result = body.union(shaft)

# Optional: Rotate for better view matching (uncomment if needed)
# result = result.rotate((0,0,0), (1,-1,0), 60)