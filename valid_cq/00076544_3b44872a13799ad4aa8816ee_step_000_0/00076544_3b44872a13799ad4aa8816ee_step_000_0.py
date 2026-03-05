import cadquery as cq

# --- Parametric Dimensions ---
total_length = 150.0       # Total length of the part
diameter = 30.0            # Outer diameter of caps and center
radius = diameter / 2.0

cap_length = 10.0          # Length of the cylindrical end caps
neck_length = 20.0         # Length of the curved transition
neck_min_radius = 18.0 / 2.0 # Minimum radius at the narrowest part of the neck

center_length = total_length - 2 * (cap_length + neck_length)

# Groove parameters
groove_count = 4
groove_margin = 5.0        # Distance from neck transition to groove start
groove_length = center_length - 2 * groove_margin
groove_width = 6.0
groove_depth = 3.0

fillet_radius = 2.0        # Fillet on the end caps

# --- 1. Create Main Revolved Body ---

# Define profile points on XY plane (Y is radial axis, X is longitudinal axis)
p0 = (0, 0)
p1 = (0, radius)
p2 = (cap_length, radius)

# First Neck Arc Points
p3_mid = (cap_length + neck_length / 2.0, neck_min_radius)
p3 = (cap_length + neck_length, radius)

# Center Section End
p4 = (cap_length + neck_length + center_length, radius)

# Second Neck Arc Points
p5_mid = (total_length - cap_length - neck_length / 2.0, neck_min_radius)
p5 = (total_length - cap_length, radius)

# End Cap Points
p6 = (total_length, radius)
p7 = (total_length, 0)

# Draw profile and revolve around X-axis
result = (
    cq.Workplane("XY")
    .moveTo(*p0)
    .lineTo(*p1)
    .lineTo(*p2)
    .threePointArc(p3_mid, p3)  # Concave transition
    .lineTo(*p4)                # Center cylinder
    .threePointArc(p5_mid, p5)  # Concave transition
    .lineTo(*p6)
    .lineTo(*p7)
    .close()
    .revolve(360, (0, 0, 0), (1, 0, 0))
)

# --- 2. Create and Subtract Grooves ---

# Create a single groove cutter
# Positioned on the top surface (XZ plane offset by radius), centered in length
cutter = (
    cq.Workplane("XY")
    .workplane(offset=radius)
    .center(total_length / 2.0, 0)
    .slot2D(groove_length, groove_width)
    .extrude(-groove_depth)
)

# Pattern the cutter radially
cutters = cutter
for i in range(1, groove_count):
    angle = i * (360.0 / groove_count)
    # Rotate the cutter geometry around the X-axis
    cutters = cutters.union(cutter.rotate((0, 0, 0), (1, 0, 0), angle))

# Subtract the cutters from the main body
result = result.cut(cutters)

# --- 3. Apply Fillets ---

# Fillet the outer circular edges of the end caps
# Select edges on the faces with minimum and maximum X coordinates
result = result.edges("<X").fillet(fillet_radius)
result = result.edges(">X").fillet(fillet_radius)