import cadquery as cq

# --- Model Parameters ---
num_segments = 4
sphere_radius = 8.0
shaft_radius = 3.5
pitch = 18.0           # Distance between sphere centers
end_extension = 3.0    # Shaft length extending past the top/bottom spheres

# Feature details
groove_width = 0.6     # Width of the horizontal equatorial cut
groove_depth = 0.8     # Depth of the groove
slot_width = 5.0       # Width of vertical slots (Y-axis)
slot_height = 10.0     # Height of vertical slots (Z-axis)
slot_offset = 4.5      # Distance from center to the flat face of the slot (X-axis)

# --- Geometry Construction ---

# 1. Create the central connecting shaft
# The shaft runs through the entire length.
# Calculate limits based on sphere positions and extensions.
# First sphere is at z=0, last at z=(n-1)*pitch.
shaft_start_z = -(sphere_radius + end_extension)
shaft_length = (num_segments - 1) * pitch + 2 * (sphere_radius + end_extension)

shaft = (
    cq.Workplane("XY")
    .workplane(offset=shaft_start_z)
    .circle(shaft_radius)
    .extrude(shaft_length)
)

# 2. Define a function to generate a single bead segment
def make_bead(z_center):
    # Base Sphere
    bead = cq.Workplane("XY").workplane(offset=z_center).sphere(sphere_radius)

    # Equatorial Groove Cut
    # Create a ring (tube) to subtract from the sphere surface
    groove_outer_r = sphere_radius + 1.0
    groove_inner_r = sphere_radius - groove_depth
    
    groove_cutter = (
        cq.Workplane("XY")
        .workplane(offset=z_center - groove_width / 2.0)
        .circle(groove_outer_r)
        .circle(groove_inner_r)
        .extrude(groove_width)
    )
    
    bead = bead.cut(groove_cutter)

    # Vertical Side Slots
    # Rectangular cuts on the left and right sides (X-axis)
    # We define a box large enough to cut from the outside in
    cutter_depth = sphere_radius * 2  # Arbitrary large size
    
    # Calculate center position for the cutter box so its inner face is at 'slot_offset'
    # Right cutter (+X)
    x_pos_right = slot_offset + (cutter_depth / 2.0)
    # Left cutter (-X)
    x_pos_left = -(slot_offset + (cutter_depth / 2.0))

    cutter_right = (
        cq.Workplane("XY")
        .workplane(offset=z_center)
        .center(x_pos_right, 0)
        .box(cutter_depth, slot_width, slot_height)
    )

    cutter_left = (
        cq.Workplane("XY")
        .workplane(offset=z_center)
        .center(x_pos_left, 0)
        .box(cutter_depth, slot_width, slot_height)
    )

    bead = bead.cut(cutter_right).cut(cutter_left)
    return bead

# 3. Assemble the segments
result = shaft

for i in range(num_segments):
    z_pos = i * pitch
    segment = make_bead(z_pos)
    result = result.union(segment)

# The 'result' variable now contains the final geometry