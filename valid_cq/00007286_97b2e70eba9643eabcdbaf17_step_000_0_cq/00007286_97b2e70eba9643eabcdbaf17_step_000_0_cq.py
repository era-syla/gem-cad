import cadquery as cq

# --- Parametric Variables ---
# Base Plate
base_width = 300.0
base_depth = 250.0
base_thickness = 10.0

# Arch/Frame
arch_width = 120.0
arch_height = 100.0
arch_depth = 50.0
arch_thickness = 15.0
arch_fillet = 5.0
arch_foot_width = 20.0  # Extra width for mounting feet
arch_foot_depth = 10.0

# Main Angled Support Block
support_width = 80.0
support_base_height = 60.0 # Vertical part before slope
support_total_height = 140.0
support_depth = 80.0
support_angle_offset = 30.0 # How far back the top face is from the front face

# Top Clamp Mechanism (approximated)
clamp_block_h = 30.0
clamp_block_w = 40.0
clamp_block_d = 40.0

# --- Geometry Construction ---

# 1. Base Plate
base = (
    cq.Workplane("XY")
    .box(base_width, base_depth, base_thickness)
    .edges("|Z").fillet(2.0)
)

# Mounting holes on corners
base_holes = (
    base.faces(">Z").workplane()
    .rect(base_width - 30, base_depth - 30, forConstruction=True)
    .vertices()
    .hole(8.0)
)
# Additional mounting holes pattern near center
base = (
    base_holes.faces(">Z").workplane()
    .pushPoints([(50, -20), (50, -50), (80, -20), (80, -50)])
    .hole(8.0)
)

# 2. Arch/Bridge Structure
# Sketching the profile on the XZ plane (front view style)
arch_outer_width = arch_width + 2*arch_thickness
arch_inner_width = arch_width

arch_sketch = (
    cq.Workplane("XZ")
    .rect(arch_outer_width + 2*arch_foot_width, arch_thickness) # Feet base
    .extrude(arch_depth) # Extrude feet first for base
)

# Create the U-shape
arch_u = (
    cq.Workplane("XZ")
    .transformed(offset=(0, arch_thickness/2.0, 0)) # Start above the foot base
    .moveTo(-arch_outer_width/2.0, 0)
    .lineTo(-arch_outer_width/2.0, arch_height)
    .lineTo(arch_outer_width/2.0, arch_height)
    .lineTo(arch_outer_width/2.0, 0)
    .lineTo(arch_inner_width/2.0, 0)
    .lineTo(arch_inner_width/2.0, arch_height - arch_thickness)
    .lineTo(-arch_inner_width/2.0, arch_height - arch_thickness)
    .lineTo(-arch_inner_width/2.0, 0)
    .close()
    .extrude(arch_depth)
)

# Combine feet and U-shape
arch_solid = arch_sketch.union(arch_u)

# Add fillets to the arch
arch_solid = (
    arch_solid
    .edges("|Y and >Z") # Top outer edges
    .fillet(10.0)
    .edges("|Y and <Z") # Bottom inner corners
    .fillet(5.0)
)

# Hole on top of arch
arch_solid = (
    arch_solid.faces(">Y").workplane() # Top face (Y is up in extrusion, but let's reorient)
    .center(0, 0)
    .hole(20.0, depth=arch_thickness + 5)
)

# Mounting holes in arch feet
arch_solid = (
    arch_solid.faces("<Y").workplane(invert=True)
    .pushPoints([
        (-(arch_outer_width/2.0 + arch_foot_width/2.0), arch_depth/3.0),
        (-(arch_outer_width/2.0 + arch_foot_width/2.0), -arch_depth/3.0),
        ((arch_outer_width/2.0 + arch_foot_width/2.0), arch_depth/3.0),
        ((arch_outer_width/2.0 + arch_foot_width/2.0), -arch_depth/3.0),
    ])
    .hole(6.0)
)

# Move arch to position
arch_solid = arch_solid.rotate((0,0,0), (1,0,0), -90).translate((-60, 0, base_thickness/2.0))


# 3. Central Angled Support
# Create a wedge/sloped shape
pts = [
    (0, 0),
    (support_depth, 0),
    (support_depth, support_base_height),
    (support_depth - 30, support_total_height),
    (0, support_total_height),
]

support_shape = (
    cq.Workplane("YZ")
    .polyline(pts).close()
    .extrude(support_width)
    .translate((-support_width/2.0, -support_depth/2.0, 0)) # Centering
)

# Side holes on the support
support_shape = (
    support_shape.faces(">X").workplane()
    .pushPoints([(20, 40), (20, 70), (20, 100)])
    .hole(6.0)
)

# 4. Top Fixture Mechanism
# A block on top of the support
top_block = (
    cq.Workplane("XY")
    .box(50, 60, 20)
    .translate((0, 20, support_total_height + 10))
)

# Vertical Clamp Block (split block style)
clamp_vertical = (
    cq.Workplane("XY")
    .box(30, 30, 40)
    .translate((0, 10, support_total_height + 20 + 20))
)
# Hole through vertical clamp
clamp_vertical = (
    clamp_vertical.faces(">Z").workplane()
    .hole(12.0)
)
# Split slot
clamp_vertical = (
    clamp_vertical.faces(">Y").workplane()
    .rect(2, 40)
    .cutThruAll()
)

# Horizontal Bearing/Clamp mount on the front
front_mount = (
    cq.Workplane("XY")
    .box(60, 40, 20)
    .translate((0, 50, support_total_height + 10))
)
# Bearing housing cutout
front_mount = (
    front_mount.faces(">Y").workplane()
    .hole(25.0)
)
# Split slot horizontal
front_mount = (
    front_mount.faces(">Z").workplane()
    .rect(60, 2)
    .cutThruAll()
)
# Bolt holes for clamp
front_mount = (
    front_mount.faces(">Z").workplane()
    .pushPoints([(-20, 0), (20, 0)])
    .hole(5.0)
)

# Combine support components
support_assembly = support_shape.union(top_block).union(clamp_vertical).union(front_mount)
support_assembly = support_assembly.translate((40, 0, base_thickness/2.0))


# 5. Linkage / Crank Mechanism (inside arch)
crank_arm = (
    cq.Workplane("YZ")
    .rect(10, 30)
    .extrude(5)
    .edges("|X").fillet(2.5)
    .translate((-60, 0, 30))
)
crank_pin = (
    cq.Workplane("YZ")
    .circle(4)
    .extrude(15)
    .translate((-60 - 5, 0, 30 - 10))
)
shaft = (
    cq.Workplane("YZ")
    .circle(6)
    .extrude(60)
    .translate((-60, 0, 30 + 10))
)

linkage = crank_arm.union(crank_pin).union(shaft)

# 6. Rear Shaft (sticking out back)
rear_shaft = (
    cq.Workplane("YZ")
    .circle(8)
    .extrude(40)
    .translate((40, 50, 40)) # Position relative to support block
)

# --- Final Assembly ---
result = (
    base
    .union(arch_solid)
    .union(support_assembly)
    .union(linkage)
    .union(rear_shaft)
)

# Reinforce arch with ribs
rib_points = [
    (0, 0), (20, 0), (0, 20)
]
rib_l = (
    cq.Workplane("YZ")
    .polyline(rib_points).close()
    .extrude(5)
    .translate((-60 - arch_width/2.0 - 5, -arch_depth/2.0, base_thickness/2.0))
)
rib_r = (
    cq.Workplane("YZ")
    .polyline(rib_points).close()
    .extrude(5)
    .translate((-60 + arch_width/2.0, -arch_depth/2.0, base_thickness/2.0))
)

result = result.union(rib_l).union(rib_r)

# Final Translation to sit on Z=0 plane properly (optional, usually base is centered on Z=0)
# The base construction was centered on Z, then extruded up/down effectively. 
# Let's verify result is a single compound.
pass