import cadquery as cq
import math

# --- Parameters ---
# Overall dimensions
L_total = 200.0         # Total length of the part
W_tube = 50.0           # Width/Height of the square tube
L_tube = 40.0           # Length of the square tube section
t_wall = 5.0            # Wall thickness of the tube
t_base = 8.0            # Thickness of the base plate
t_rib = 4.0             # Thickness of the support ribs

# Rib geometry
rib_runout_len = 100.0  # Distance from tube face to end of ribs
x_rib_end = L_tube + rib_runout_len

# Side Tab (Mounting Plate Extension)
W_tab = 40.0            # Width of the extension tab
L_tab = 65.0            # Length of the extension tab
x_tab_start = L_total - L_tab
fillet_rad = 10.0       # Corner radius for the tab

# Holes
d_hole = 8.0            # Diameter of mounting holes

# --- Geometry Construction ---

# 1. Square Tube Section
# Create solid block
tube_block = cq.Workplane("XY").box(L_tube, W_tube, W_tube, centered=(False, True, False))

# Cut the hollow interior
# Select the face at X=0 (normal points -X), cut inwards (negative depth relative to workplane normal implies cutting into the solid)
tube = tube_block.faces("<X").workplane().rect(W_tube - 2*t_wall, W_tube - 2*t_wall).cutBlind(-L_tube)

# 2. Base Plate
# Main strip running the full length
base_main = cq.Workplane("XY").box(L_total, W_tube, t_base, centered=(False, True, False))

# Side Tab Extension (L-shape configuration)
# Extending in -Y direction relative to the main strip
tab_center_x = x_tab_start + L_tab / 2.0
tab_center_y = -W_tube / 2.0 - W_tab / 2.0

base_tab = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .center(tab_center_x, tab_center_y)
    .box(L_tab, W_tab, t_base, centered=(True, True, False))
    .edges("|Z").fillet(fillet_rad)
)

# Combine base parts
base = base_main.union(base_tab)

# 3. Support Ribs
# Central Rib (Vertical, aligned with X-axis)
center_rib = (
    cq.Workplane("XZ")
    .moveTo(L_tube, W_tube)       # Start at top edge of tube
    .lineTo(x_rib_end, t_base)    # Slope down to base plate
    .lineTo(L_tube, t_base)       # Return to bottom of tube
    .close()
    .extrude(t_rib / 2.0, both=True) # Symmetric extrusion
)

# Side Ribs (Angled/Fanned out)
# Calculate geometry for the rib on the +Y side
# Start point: Upper corner of tube face
# End point: Base plate, converging towards the center line
y_start = W_tube / 2.0 - t_rib
y_end = 2.0  # Converges close to center line
dx = x_rib_end - L_tube
dy = y_start - y_end
angle_deg = math.degrees(math.atan2(dy, dx))
length_hyp = math.sqrt(dx**2 + dy**2)

# Create +Y Side Rib
side_rib_pos = (
    cq.Workplane("XY")
    .center(L_tube, y_start)
    .transformed(rotate=(0, 0, -angle_deg)) # Rotate to align with rib path
    .transformed(rotate=(90, 0, 0))         # Rotate up to vertical plane
    .moveTo(0, W_tube)                      # Start height matches tube
    .lineTo(length_hyp, t_base)             # Slope down
    .lineTo(0, t_base)                      # Bottom edge
    .close()
    .extrude(t_rib / 2.0, both=True)
)

# Create -Y Side Rib (Mirror of +Y)
side_rib_neg = side_rib_pos.mirror("XZ")

# 4. Holes
# Holes on the main strip (end section)
h_spacing_main = 25.0
h_start_main = x_rib_end + 20.0

holes_main_tool = (
    cq.Workplane("XY")
    .workplane(offset=t_base)
    .moveTo(h_start_main, 0)
    .circle(d_hole / 2.0)
    .moveTo(h_start_main + h_spacing_main, 0)
    .circle(d_hole / 2.0)
    .extrude(-t_base * 2) # Create cutting tool
)

# Holes on the Tab (Rectangular pattern)
h_spacing_tab = 20.0 # Spacing between holes in the grid
holes_tab_tool = (
    cq.Workplane("XY")
    .workplane(offset=t_base)
    .center(tab_center_x, tab_center_y)
    .rect(h_spacing_tab, h_spacing_tab, forConstruction=True)
    .vertices()
    .circle(d_hole / 2.0)
    .extrude(-t_base * 2) # Create cutting tool
)

# --- Final Assembly ---
# Union all structural parts
structure = tube.union(base).union(center_rib).union(side_rib_pos).union(side_rib_neg)

# Cut holes
result = structure.cut(holes_main_tool).cut(holes_tab_tool)