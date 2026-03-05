import cadquery as cq

# Parameters
length = 80.0       # Total length of the part
width = 30.0        # Total width of the part
base_height = 3.0   # Height of the rectangular base section
gap_width = 8.0     # Width of the flat gap between the two raised features
fillet_radius = 2.5 # Radius of the fillet on the end caps

# Derived dimensions
hump_width = (width - gap_width) / 2.0
hump_radius = hump_width / 2.0

# Define coordinates for the profile sketch on the YZ plane
# Right Hump Points
r_inner_start = (gap_width / 2.0, base_height)
r_arc_mid = (gap_width / 2.0 + hump_radius, base_height + hump_radius)
r_outer_end = (width / 2.0, base_height)

# Left Hump Points
l_outer_start = (-width / 2.0, base_height)
l_arc_mid = (-(gap_width / 2.0 + hump_radius), base_height + hump_radius)
l_inner_end = (-gap_width / 2.0, base_height)

# Generate the 3D model
result = (
    cq.Workplane("YZ")
    .moveTo(*r_inner_start)
    .threePointArc(r_arc_mid, r_outer_end)  # Right semi-circle
    .lineTo(width / 2.0, 0)                 # Right vertical wall
    .lineTo(-width / 2.0, 0)                # Bottom flat base
    .lineTo(*l_outer_start)                 # Left vertical wall
    .threePointArc(l_arc_mid, l_inner_end)  # Left semi-circle
    .close()                                # Connects l_inner_end to r_inner_start (flat gap)
    .extrude(length)
)

# Apply fillets to the curved edges at the ends of the extrusion
# Selects edges on the start/end faces (>X, <X) that are at the top (>Z)
result = result.edges("(>X or <X) and >Z").fillet(fillet_radius)