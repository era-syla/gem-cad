import cadquery as cq

# --- Parametric Dimensions ---
# Main Motor Body
body_dia = 36.0         # Diameter of the main housing
body_len = 57.0         # Length of the main housing
crimp_pos = 5.0         # Distance of the crimp groove from the rear face
crimp_width = 1.0       # Width of the crimp groove
crimp_depth = 0.5       # Depth of the crimp groove

# Rear Features (Connection side)
rear_boss_dia = 15.0    # Diameter of the central rear boss
rear_boss_h = 3.5       # Height of the rear boss
term_dia = 2.5          # Diameter of the electrical terminals
term_h = 4.0            # Height of the terminals
term_spacing = 7.0      # Horizontal spacing between terminals
term_offset_y = -9.0    # Vertical offset of terminals from center

# Front Features (Shaft side)
front_boss_dia = 13.0   # Diameter of the front bearing boss
front_boss_h = 2.0      # Height of the front boss
shaft_dia = 3.175       # Shaft diameter (standard 1/8")
shaft_len = 15.0        # Shaft length protruding from front boss
d_cut_depth = 0.5       # Depth of the D-cut flat
d_cut_len = 13.0        # Length of the D-cut section

# --- Modeling ---

# 1. Main Housing
# Create the main cylinder along the X-axis
housing = cq.Workplane("YZ").circle(body_dia / 2.0).extrude(body_len)

# Create the crimp groove near the rear
crimp_cutter = (
    cq.Workplane("YZ")
    .workplane(offset=crimp_pos)
    .circle(body_dia / 2.0 + 1.0)          # Outer boundary
    .circle(body_dia / 2.0 - crimp_depth)  # Inner cutting boundary
    .extrude(crimp_width)
)
housing = housing.cut(crimp_cutter)

# Chamfer the ends of the main housing
try:
    housing = housing.edges(cq.NearestToPointSelector((0, body_dia/2.0, 0))).chamfer(0.5)
    housing = housing.edges(cq.NearestToPointSelector((body_len, body_dia/2.0, 0))).chamfer(0.5)
except:
    pass

# 2. Rear Components (Extruding in negative X direction)
# Rear Boss
rear_boss = (
    cq.Workplane("YZ")
    .workplane(offset=0)
    .circle(rear_boss_dia / 2.0)
    .extrude(-rear_boss_h)
)

# Terminals
terminals = (
    cq.Workplane("YZ")
    .workplane(offset=0)
    .moveTo(term_spacing / 2.0, term_offset_y)
    .circle(term_dia / 2.0)
    .moveTo(-term_spacing / 2.0, term_offset_y)
    .circle(term_dia / 2.0)
    .extrude(-term_h)
)
# Add rounded tips to terminals
try:
    terminals = terminals.edges("<X").fillet(term_dia / 3.0)
except:
    pass

# 3. Front Components (At X = body_len)
# Front Boss
front_boss = (
    cq.Workplane("YZ")
    .workplane(offset=body_len)
    .circle(front_boss_dia / 2.0)
    .extrude(front_boss_h)
)

# Shaft
shaft_start_x = body_len + front_boss_h
shaft = (
    cq.Workplane("YZ")
    .workplane(offset=shaft_start_x)
    .circle(shaft_dia / 2.0)
    .extrude(shaft_len)
)

# D-Cut on Shaft
# Create a tool to cut the flat section
shaft_radius = shaft_dia / 2.0
cut_plane_y = shaft_radius - d_cut_depth

d_cut_tool = (
    cq.Workplane("YZ")
    .workplane(offset=shaft_start_x + shaft_len) # Start at shaft tip
    # Position a rectangle above the cut plane
    .moveTo(0, cut_plane_y + shaft_radius) 
    .rect(shaft_dia * 2.0, shaft_dia * 2.0) # Large enough to encompass the top
    .extrude(-d_cut_len) # Cut backwards along the shaft
)
shaft = shaft.cut(d_cut_tool)

# --- Assembly ---
# Combine all parts into the final result
result = (
    housing
    .union(rear_boss)
    .union(terminals)
    .union(front_boss)
    .union(shaft)
)