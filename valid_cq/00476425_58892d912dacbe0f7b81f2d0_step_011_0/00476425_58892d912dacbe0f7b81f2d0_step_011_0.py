import cadquery as cq

# --- Dimensions & Parameters ---
pipe_radius = 6.0
inlet_spacing = 50.0       # Distance between inlet pipes
inlet_straight_len = 80.0  # Length of parallel inlet section
merge_len = 100.0          # Length of the merging Y-curve
initial_straight = 30.0    # Straight section after merge
rise_x = 180.0             # Horizontal distance of the first bend
rise_z = 60.0              # Vertical height of the first bend
top_straight = 220.0       # Length of the straight top section
drop_x = 140.0             # Horizontal distance of the drop bend
drop_z = -80.0             # Vertical drop relative to top height
tip_len = 25.0             # Length of vertical tip
muffler_radius = 22.0
muffler_length = 90.0

# --- 1. Inlet Pipes (Y-Section) ---
# We create two paths in the XY plane that merge at (0,0,0) with tangent continuity

# Calculate start positions
x_start = -inlet_straight_len - merge_len

# Left Inlet Path (Positive Y)
path_inlet_L = (
    cq.Workplane("XY")
    .moveTo(x_start, inlet_spacing/2)
    .lineTo(-merge_len, inlet_spacing/2) # Straight segment
    # Spline to (0,0) with horizontal tangents at both ends for smooth merge
    .spline([(0, 0, 0)], tangents=[(1, 0, 0), (1, 0, 0)], includeCurrent=True)
)

# Right Inlet Path (Negative Y)
path_inlet_R = (
    cq.Workplane("XY")
    .moveTo(x_start, -inlet_spacing/2)
    .lineTo(-merge_len, -inlet_spacing/2)
    .spline([(0, 0, 0)], tangents=[(1, 0, 0), (1, 0, 0)], includeCurrent=True)
)

# Sweep to create solids
# Profiles are defined in YZ plane at the start of the paths
inlet_L = (
    cq.Workplane("YZ")
    .workplane(offset=x_start)
    .moveTo(inlet_spacing/2, 0)
    .circle(pipe_radius)
    .sweep(path_inlet_L)
)

inlet_R = (
    cq.Workplane("YZ")
    .workplane(offset=x_start)
    .moveTo(-inlet_spacing/2, 0)
    .circle(pipe_radius)
    .sweep(path_inlet_R)
)

# --- 2. Main Pipe Run ---
# Defined in XZ plane to handle the vertical bends ("over the axle" shape)

# Track current coordinate
cur_x = 0
cur_z = 0

path_main = cq.Workplane("XZ").moveTo(cur_x, cur_z)

# Short straight after merge
cur_x += initial_straight
path_main = path_main.lineTo(cur_x, cur_z)

# Rise (S-curve up)
x_rise_end = cur_x + rise_x
z_rise_end = cur_z + rise_z
# Using spline for smooth transition
path_main = path_main.spline(
    [(x_rise_end, z_rise_end)], 
    tangents=[(1, 0, 0), (1, 0, 0)], 
    includeCurrent=True
)
cur_x = x_rise_end
cur_z = z_rise_end

# Top Straight Section (where Muffler sits)
x_top_end = cur_x + top_straight
path_main = path_main.lineTo(x_top_end, cur_z)
cur_x = x_top_end

# Drop (Curve down to vertical)
x_drop_end = cur_x + drop_x
z_drop_end = cur_z + drop_z
# Tangent starts horizontal (1,0) and ends vertical down (0,-1)
path_main = path_main.spline(
    [(x_drop_end, z_drop_end)], 
    tangents=[(1, 0, 0), (0, -1, 0)], 
    includeCurrent=True
)
cur_x = x_drop_end
cur_z = z_drop_end

# Final Vertical Tip
z_tip_end = cur_z - tip_len
path_main = path_main.lineTo(cur_x, z_tip_end)

# Sweep Main Pipe
main_pipe = (
    cq.Workplane("YZ")
    .circle(pipe_radius)
    .sweep(path_main)
)

# --- 3. Muffler Component ---
# Cylinder placed on the straight top section
muffler_x_center = x_rise_end + top_straight / 2
muffler_z_center = z_rise_end

muffler = (
    cq.Workplane("YZ")
    .workplane(offset=muffler_x_center)
    .center(0, muffler_z_center)
    .circle(muffler_radius)
    .extrude(muffler_length/2, both=True) # Extrude symmetrically
    .edges().fillet(5) # Round the edges
)

# --- 4. End Flange ---
# Rectangular block at the tip of the pipe
flange = (
    cq.Workplane("XY")
    .workplane(offset=z_tip_end)
    .center(cur_x, 0)
    .rect(35, 15)
    .extrude(5)
)

# --- 5. Final Assembly ---
result = (
    inlet_L
    .union(inlet_R)
    .union(main_pipe)
    .union(muffler)
    .union(flange)
)