import cadquery as cq

# --- Parameter Definitions ---
egg_height = 80.0
egg_radius = 28.0       # Maximum radius of the egg
widest_z_factor = 0.35  # Height ratio where the egg is widest

feature_z = 35.0        # Z height of the circular feature center
feature_r = 12.0        # Radius of the circular feature
groove_width = 0.6      # Width of the groove cuts

seam_thickness = 0.3    # Thickness of the parting lines
bottom_seam_z = 14.0    # Z height of the bottom cap seam

# --- 1. Create Main Egg Body ---
# We define a spline profile on the XZ plane and revolve it around the vertical axis.
# Profile points: Bottom (0,0), Widest Point, Top (0, height)
p_start = (0, 0)
p_mid = (egg_radius, egg_height * widest_z_factor)
p_end = (0, egg_height)

# Tangents control the shape:
# (1, 0): Horizontal tangent at bottom pole
# (0, 1): Vertical tangent at widest point
# (-1, 0): Horizontal tangent at top pole
tangents = [(1, 0), (0, 1), (-1, 0)]

egg = (
    cq.Workplane("XZ")
    .moveTo(*p_start)
    .spline([p_mid, p_end], tangents=tangents, includeCurrent=True)
    .close()  # Close the wire back to origin along the axis
    .revolve(360, (0, 0, 0), (0, 1, 0)) # Revolve around Local Y (Global Z)
)

# --- 2. Create Seam Cutters ---

# Vertical Seam: A thin slice along the YZ plane (splitting X axis)
v_seam_cutter = (
    cq.Workplane("YZ")
    .rect(egg_radius * 3, egg_height * 1.5)
    .extrude(seam_thickness)
    .translate((-seam_thickness / 2, 0, egg_height / 2))
)

# Horizontal Seam: A thin slice along the XY plane near the bottom
h_seam_cutter = (
    cq.Workplane("XY")
    .rect(egg_radius * 3, egg_radius * 3)
    .extrude(seam_thickness)
    .translate((0, 0, bottom_seam_z - seam_thickness / 2))
)

# --- 3. Create Circular Feature Cutter ---
# A circular groove projected from the side (+X direction)
circle_cutter = (
    cq.Workplane("YZ")
    .workplane(offset=egg_radius * 1.5) # Start outside the egg on +X side
    .circle(feature_r)
    .circle(feature_r - groove_width)   # Create a ring profile
    .extrude(-egg_radius * 2)           # Extrude inwards to cut the groove
    .translate((0, 0, feature_z))       # Move to correct height
)

# --- 4. Combine Geometry ---
result = egg.cut(v_seam_cutter).cut(h_seam_cutter).cut(circle_cutter)