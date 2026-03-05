import cadquery as cq

# --- Parametric Dimensions ---
# Vertical Mast dimensions
mast_radius = 8.0
mast_height = 140.0

# Horizontal Arm dimensions
arm_radius = 2.5
arm_length = 80.0       # Length extending from the mast surface
arm_z_pos = 90.0        # Vertical position of the arm on the mast

# Gusset (Reinforcement Rib) dimensions
gusset_height = 15.0    # Height along the mast
gusset_length = 15.0    # Length along the arm
gusset_thickness = 2.0  # Thickness of the rib

# --- Modeling ---

# 1. Create the main vertical mast (Cylinder aligned with Z-axis)
mast = cq.Workplane("XY").circle(mast_radius).extrude(mast_height)

# 2. Create the horizontal arm
# We create a workplane on YZ (normal to X) to draw the circle profile
# We offset it slightly inside the mast (-mast_radius) to ensure a solid intersection
arm = (
    cq.Workplane("YZ")
    .workplane(offset=-mast_radius * 0.5) 
    .center(0, arm_z_pos)
    .circle(arm_radius)
    .extrude(arm_length + mast_radius * 0.5)
)

# 3. Create the triangular gusset
# Defined on the XZ plane to slice through the center of both cylinders
# Points are calculated relative to the intersection corner
corner_x = mast_radius
corner_z = arm_z_pos + arm_radius
overlap = 0.5  # Small overlap value to ensure boolean union succeeds

# Define vertices of the triangle
v1 = (corner_x - overlap, corner_z - overlap)              # Intersection corner (embedded)
v2 = (corner_x - overlap, corner_z + gusset_height)        # Point up the mast
v3 = (corner_x + gusset_length, corner_z - overlap)        # Point along the arm

gusset = (
    cq.Workplane("XZ")
    .polyline([v1, v2, v3])
    .close()
    .extrude(gusset_thickness / 2.0, both=True)  # Symmetric extrusion
)

# --- Final Assembly ---
# Combine all parts into a single solid
result = mast.union(arm).union(gusset)