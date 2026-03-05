import cadquery as cq

# Parameters defining the dimensions of the handle
handle_width = 120.0   # Total width from outer leg to outer leg
handle_height = 50.0   # Total height of the handle
handle_depth = 20.0    # Depth (width of the metal strip)
thickness = 8.0        # Thickness of the material
tab_length = 20.0      # Length of the mounting tabs extending outwards
hole_diameter = 6.5    # Diameter of the mounting holes

# Calculate coordinate landmarks for the profile sketching
x_outer_leg = handle_width / 2.0
x_inner_leg = x_outer_leg - thickness
x_tab_tip = x_outer_leg + tab_length

y_base = 0.0
y_tab_top = thickness
y_handle_top = handle_height
y_inner_ceiling = handle_height - thickness

# Define points for the single closed wire profile on the XZ plane.
# Tracing counter-clockwise from the bottom-left tab.
points = [
    (-x_tab_tip, y_base),          # Bottom-left tab tip
    (-x_inner_leg, y_base),        # Bottom inner corner left (base of U-void)
    (-x_inner_leg, y_inner_ceiling), # Top inner corner left
    (x_inner_leg, y_inner_ceiling),  # Top inner corner right
    (x_inner_leg, y_base),         # Bottom inner corner right
    (x_tab_tip, y_base),           # Bottom-right tab tip
    (x_tab_tip, y_tab_top),        # Top-right tab tip
    (x_outer_leg, y_tab_top),      # Right leg/tab junction
    (x_outer_leg, y_handle_top),   # Top-right outer corner
    (-x_outer_leg, y_handle_top),  # Top-left outer corner
    (-x_outer_leg, y_tab_top),     # Left leg/tab junction
    (-x_tab_tip, y_tab_top)        # Top-left tab tip
]

# Create the solid geometry
result = (
    cq.Workplane("XZ")
    .polyline(points)
    .close()
    .extrude(handle_depth)
)

# Drill mounting holes centered on the tabs
# We select the top faces of the tabs by filtering for faces pointing up (+Z)
# that are located at the bottom section of the part (z < height/2).
result = (
    result
    .faces(">Z")
    .filter(lambda f: f.Center().z < handle_height / 2.0)
    .workplane()
    .hole(hole_diameter)
)