import cadquery as cq

# --- Parameters ---
# Ball Joint Head (Housing)
head_radius = 5.5
head_center = (0, 0, 0)

# Vertical Shank (Bottom Stud)
shank_radius = 3.5
shank_length = 10.0
shank_offset_overlap = 1.0

# Top Cap (Screw Head Simulation)
cap_radius = 4.2
cap_height = 1.5
cap_offset_overlap = 1.0

# Screwdriver Slot
slot_width = 1.2
slot_depth = 1.0
slot_length = 10.0

# Neck (Transition from Head to Rod)
neck_length = 5.0
neck_start_radius = 4.5  # Slightly smaller than head radius
neck_end_radius = 3.0    # Matches collar/rod transition

# Collar (Stop Nut / Flange)
collar_radius = 4.0
collar_thickness = 1.5

# Main Rod
rod_radius = 2.2
rod_length = 120.0

# --- Modeling ---

# 1. Create the Main Head Assembly (Vertical Orientation)
# Central Sphere
head = cq.Workplane("XY").sphere(head_radius)

# Bottom Shank (Cylinder extending downwards)
shank = (
    cq.Workplane("XY")
    .workplane(offset=-head_radius + shank_offset_overlap)
    .circle(shank_radius)
    .extrude(-shank_length)
)

# Top Cap (Cylinder extending upwards)
cap = (
    cq.Workplane("XY")
    .workplane(offset=head_radius - cap_offset_overlap)
    .circle(cap_radius)
    .extrude(cap_height + cap_offset_overlap)
)

# Slot Cut (for the screw head look)
# Positioned at the top of the cap
slot_plane_z = head_radius + cap_height
slot = (
    cq.Workplane("XY")
    .workplane(offset=slot_plane_z)
    .rect(slot_length, slot_width)
    .extrude(-slot_depth)
)

# Union vertical parts and cut the slot
head_assembly = head.union(shank).union(cap).cut(slot)

# 2. Create the Lateral Linkage (Horizontal Orientation along X-axis)

# Calculate positions along X axis
# Start neck inside the sphere to ensure a clean boolean union
neck_start_x = 0.0
neck_end_x = head_radius + 2.0  # Where neck meets collar
collar_start_x = neck_end_x
rod_start_x = collar_start_x + collar_thickness

# Neck: A lofted cone from inside the sphere to the collar
# Using YZ plane for cross-sections along X axis
neck = (
    cq.Workplane("YZ")
    .workplane(offset=neck_start_x)
    .circle(neck_start_radius)
    .workplane(offset=neck_end_x - neck_start_x)
    .circle(neck_end_radius)
    .loft(combine=False)
)

# Collar: A short cylinder
collar = (
    cq.Workplane("YZ")
    .workplane(offset=collar_start_x)
    .circle(collar_radius)
    .extrude(collar_thickness)
)

# Rod: The main long shaft
rod = (
    cq.Workplane("YZ")
    .workplane(offset=rod_start_x)
    .circle(rod_radius)
    .extrude(rod_length)
)

# 3. Combine All Parts
# Union head assembly with the lateral chain
result = head_assembly.union(neck).union(collar).union(rod)

# 4. Refinements (Fillets)
# Smooth the transition between collar and rod, and neck and collar
try:
    # Select edges at the collar-rod interface
    result = result.edges(cq.selectors.NearestToPointSelector((rod_start_x, 0, 0))).fillet(0.4)
    # Select edges at the neck-collar interface
    result = result.edges(cq.selectors.NearestToPointSelector((collar_start_x, 0, 0))).fillet(0.4)
except Exception:
    # Fallback if fillet selection fails due to geometry specificities
    pass