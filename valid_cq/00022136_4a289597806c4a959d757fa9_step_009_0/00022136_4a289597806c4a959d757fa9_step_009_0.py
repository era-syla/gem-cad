import cadquery as cq

# --- Dimensions & Parameters ---
base_diameter = 36.0
base_height = 12.0
base_fillet = 1.0

head_diameter = 44.0
head_radius = head_diameter / 2.0
head_cyl_length = 34.0
bezel_offset = 8.0     # Distance of groove from front face
groove_width = 0.5
groove_depth = 0.5

tilt_angle = 50.0      # Angle of the head
pivot_height = 24.0    # Z height of the sphere center

cord_diameter = 2.5
cord_length = 150.0
strain_relief_dia = 4.0
strain_relief_len = 2.0

# --- 1. Create the Base ---
# Cylindrical base with a filleted top edge
base = (
    cq.Workplane("XY")
    .circle(base_diameter / 2.0)
    .extrude(base_height)
    .edges(">Z")
    .fillet(base_fillet)
)

# --- 2. Create the Head Assembly ---
# We construct the head aligned with the Z-axis first, then rotate/move it.

# Part A: The Spherical Back
sphere = cq.Workplane("XY").sphere(head_radius)

# Part B: The Cylindrical Body
cylinder = (
    cq.Workplane("XY")
    .circle(head_radius)
    .extrude(head_cyl_length)
)

# Combine Sphere and Cylinder
head_solid = sphere.union(cylinder)

# Add Chamfer to the front face
head_solid = head_solid.edges(">Z").chamfer(1.5)

# Create the Groove (Parting line)
# We create a disk cutter to remove material around the circumference
groove_z_pos = head_cyl_length - bezel_offset
cutter = (
    cq.Workplane("XY")
    .workplane(offset=groove_z_pos)
    .circle(head_radius + 5)             # Outer radius (large enough to clear)
    .circle(head_radius - groove_depth)  # Inner radius (defines groove depth)
    .extrude(groove_width)
)
head_solid = head_solid.cut(cutter)

# Position the Head
# Rotate around Y axis to tilt, then translate up to pivot position
head_positioned = (
    head_solid
    .rotate((0, 0, 0), (0, 1, 0), -tilt_angle)
    .translate((0, 0, pivot_height))
)

# --- 3. Create the Cord ---
# Cord exiting from the side of the base (along +X axis)
cord_z_pos = base_height / 3.0

# Strain relief (thickened part at exit)
strain_relief = (
    cq.Workplane("YZ")
    .workplane(offset=base_diameter/2.0 - 0.5) # Start slightly inside base surface
    .circle(strain_relief_dia / 2.0)
    .extrude(strain_relief_len)
    .translate((0, 0, cord_z_pos))
)

# The wire itself
wire = (
    cq.Workplane("YZ")
    .workplane(offset=-5.0) # Start deep inside base to ensure connection
    .circle(cord_diameter / 2.0)
    .extrude(cord_length + 5.0)
    .translate((0, 0, cord_z_pos))
)

# --- 4. Final Assembly ---
result = base.union(head_positioned).union(strain_relief).union(wire)