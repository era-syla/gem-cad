import cadquery as cq

# --- Parameter Definitions ---
# Rod dimensions
rod_length = 180.0
rod_radius = 3.0

# Collar dimensions (the flange between rod and neck)
collar_radius = 5.5
collar_width = 3.5

# Neck dimensions (conical section connecting head to collar)
neck_end_x = 22.0  # Position along X where neck ends and collar starts
neck_radius_start = 5.0 # Inside the head
neck_radius_end = 4.0   # At the collar

# Head (Banjo fitting) dimensions
head_sphere_radius = 9.0
head_cylinder_radius = 6.5
head_height_bottom = 15.0 # Extension below center
head_height_top = 7.0     # Extension above center (before screw)

# Screw/Bolt dimensions
screw_radius = 7.5
screw_height = 2.5
slot_width = 2.0
slot_depth = 1.5

# --- Geometry Construction ---

# 1. Create the Vertical Head Assembly
# Center of the spherical part is at (0,0,0)

# The central spherical bulge
sphere = cq.Workplane("XY").sphere(head_sphere_radius)

# The vertical cylinder housing (main body axis)
vertical_cyl = (
    cq.Workplane("XY")
    .workplane(offset=-head_height_bottom)
    .circle(head_cylinder_radius)
    .extrude(head_height_bottom + head_height_top)
)

# The screw head on top
screw_head = (
    cq.Workplane("XY")
    .workplane(offset=head_height_top)
    .circle(screw_radius)
    .extrude(screw_height)
)

# The screwdriver slot cut into the screw head
# We rotate it 45 degrees for visual style
slot_cut = (
    cq.Workplane("XY")
    .workplane(offset=head_height_top + screw_height)
    .rect(screw_radius * 2.5, slot_width)
    .rotate((0,0,1), (0,0,0), 45)
    .extrude(-slot_depth)
)

# Combine head components
head_assembly = sphere.union(vertical_cyl).union(screw_head).cut(slot_cut)

# 2. Create the Lateral Arm (Neck + Collar + Rod)
# All aligned along the positive X axis

# Neck: A loft connecting the head interior to the collar
# Starting at X=0 ensures the loft merges cleanly with the sphere
neck = (
    cq.Workplane("YZ")
    .workplane(offset=0)
    .circle(neck_radius_start)
    .workplane(offset=neck_end_x)
    .circle(neck_radius_end)
    .loft()
)

# Collar: A cylinder at the end of the neck
collar = (
    cq.Workplane("YZ")
    .workplane(offset=neck_end_x)
    .circle(collar_radius)
    .extrude(collar_width)
)

# Rod: The long shaft extending from the collar
rod = (
    cq.Workplane("YZ")
    .workplane(offset=neck_end_x + collar_width)
    .circle(rod_radius)
    .extrude(rod_length)
)

# End Cap: A small detail at the very end of the rod
end_cap = (
    cq.Workplane("YZ")
    .workplane(offset=neck_end_x + collar_width + rod_length)
    .circle(rod_radius + 0.3)
    .extrude(1.5)
)

# 3. Final Assembly
# Union all parts together
result = head_assembly.union(neck).union(collar).union(rod).union(end_cap)

# Optional: Add small fillets at the collar transitions for realism
try:
    # Fillet between neck and collar
    result = result.edges(cq.NearestToPointSelector((neck_end_x, 0, collar_radius))).fillet(0.5)
    # Fillet between collar and rod
    result = result.edges(cq.NearestToPointSelector((neck_end_x + collar_width, 0, collar_radius))).fillet(0.5)
except Exception:
    # Skip fillets if topology makes selection difficult
    pass