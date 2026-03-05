import cadquery as cq

# Parametric dimensions
head_mid_diameter = 50.0    # Diameter of the central cylindrical part
head_end_diameter = 30.0    # Diameter of the flat ends
head_mid_height = 30.0      # Height of the central cylindrical part
head_taper_height = 25.0    # Height of the tapered top/bottom sections
handle_diameter = 14.0      # Diameter of the handle
handle_length = 250.0       # Total length of the handle from the center of the head

# Derived radius values
r_mid = head_mid_diameter / 2.0
r_end = head_end_diameter / 2.0
r_handle = handle_diameter / 2.0

# Calculate vertical coordinates for the head profile (centered on origin)
z_mid_top = head_mid_height / 2.0
z_mid_bot = -head_mid_height / 2.0
z_top = z_mid_top + head_taper_height
z_bot = z_mid_bot - head_taper_height

# 1. Create the Head
# We define a profile in the XZ plane and revolve it around the Z axis.
# The profile consists of the central cylinder wall and the two tapered sections.
head = (
    cq.Workplane("XZ")
    .polyline([
        (0, z_top),         # Top point on axis
        (r_end, z_top),     # Top outer edge
        (r_mid, z_mid_top), # Transition to middle cylinder (top)
        (r_mid, z_mid_bot), # Transition to middle cylinder (bottom)
        (r_end, z_bot),     # Bottom outer edge
        (0, z_bot)          # Bottom point on axis
    ])
    .close()
    .revolve()              # Revolves around the Workplane's local Y axis (Global Z)
)

# 2. Create the Handle
# We create a circle on the YZ plane (facing X) and extrude it along the X axis.
# It starts at X=0 (center of head) to ensure a solid connection.
handle = (
    cq.Workplane("YZ")
    .circle(r_handle)
    .extrude(handle_length)
)

# 3. Combine parts
result = head.union(handle)