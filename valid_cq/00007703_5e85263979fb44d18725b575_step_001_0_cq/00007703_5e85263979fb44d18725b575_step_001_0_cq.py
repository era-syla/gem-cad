import cadquery as cq

# --- Parameter Definitions ---

# Plate Parameters
plate_size = 200.0
plate_thickness = 2.0
center_hole_radius = 40.0 # Approximate radius for the central triangular-ish void
truss_width = 3.0 # Width of the beams in the truss pattern

# Corner Detail Component Parameters
corner_block_size = 30.0
corner_height = 15.0
shelf_thickness = 2.0
shelf_spacing = 4.0

# --- Geometry Construction ---

# 1. Main Truss Plate Generation
# The plate has a complex truss pattern. We will approximate this with a procedural approach
# creating a triangular symmetry.

def create_truss_sketch():
    # Create the base square
    base_sq = cq.Sketch().rect(plate_size, plate_size)
    
    # Create the inner cutout shape (approximated as a rounded triangle/hexagon)
    # We will subtract a pattern of triangles/quads to leave the "truss" behind.
    
    # Let's define the outer boundary of the truss area (a slightly smaller square)
    margin = 15.0
    
    # We will build the cutouts using a polar array logic but applied to the sketch
    # This is a simplification of the complex Voronoi-like pattern in the image
    
    cutouts = cq.Sketch()
    
    # Generate the triangular sectors pattern
    for i in range(4): # 4 sides
        with cq.Location(cq.Vector(0,0,0), cq.Vector(0,0,1), i*90):
            # Outer triangular cutouts
            pts_outer = [
                (10, 10),
                (plate_size/2 - margin, 10),
                (plate_size/2 - margin, plate_size/2 - margin)
            ]
            
            # Inner details - rows of smaller cutouts
            # To mimic the image, we create a grid of holes and subtract the "beams"
            # Instead, let's make a solid plate and cut out specific shapes.
            pass

    # Alternative Strategy: Create the solid plate and cut the pattern.
    # The pattern looks like a large central void surrounded by a truss.
    
    return base_sq

# Since the truss pattern is very specific and hard to parametrically replicate exactly
# without vector data, we will create a stylized representation that captures the
# design intent: A square frame, a central void, and connecting ribs.

# Start with a solid plate
plate = cq.Workplane("XY").box(plate_size, plate_size, plate_thickness)

# Create the large central triangular-ish cutout
# Using a polygon for the central void
central_void_pts = [
    (0, 50),
    (45, -35),
    (-45, -35)
]
# Smooth the corners of the void
central_void = (
    cq.Workplane("XY")
    .polyline(central_void_pts).close()
    .extrude(plate_thickness*2)
    .edges("|Z").fillet(10)
    .translate((0,0,-plate_thickness))
)

plate = plate.cut(central_void)

# Create the lattice/truss cutouts.
# We'll create one sector and rotate it 4 times (since it's a square, though the center is triangular,
# the outer pattern has 4-fold symmetry in the corners).
# Actually, looking closer, the pattern seems to have a 3-fold symmetry in the center 
# but adapts to a 4-sided square. Let's make a series of cuts.

cutters = cq.Workplane("XY")

# Define a cutter shape for the "webs"
def make_web_cutter(length, width, angle, x_pos, y_pos):
    return (
        cq.Workplane("XY")
        .box(length, width, plate_thickness * 3)
        .rotate((0,0,1), (0,0,0), angle)
        .translate((x_pos, y_pos, 0))
    )

# Instead of complex math, we'll punch out a series of triangular holes to mimic the truss.
# Inner ring of holes
r1 = 60
for i in range(12):
    angle = i * (360/12)
    cutters = cutters.union(
        cq.Workplane("XY")
        .polarArray(r1, i * (360/12), 360, 1)
        .box(15, 15, plate_thickness*3)
        .rotate((0,0,1), (0,0,0), angle)
    )

# Use a sketch for a cleaner pattern approximation
s = cq.Sketch()
s = s.rect(plate_size - 10, plate_size - 10) # Outer border

# Subtract the material to create the frame
plate_frame = cq.Workplane("XY").rect(plate_size, plate_size).extrude(plate_thickness)
inner_cut = cq.Workplane("XY").rect(plate_size-20, plate_size-20).extrude(plate_thickness)

# Let's rebuild the plate with a more direct geometric construction of the pattern shown.
# It looks like a triangulated mesh.

# 1. Base Plate
base_plate = cq.Workplane("XY").box(plate_size, plate_size, plate_thickness)

# 2. Pattern Cutter
# We will create a collection of solids to subtract from the base plate.
cutter_ops = cq.Workplane("XY")

# Define the regions
# Central region is empty (already cut above in concept, doing it properly now)
center_tri = (
    cq.Workplane("XY")
    .polygon(3, 100) # Triangle approx radius 50
    .extrude(10)
    .translate((0, -10, -5)) # Shift to center visual weight
    .edges("|Z").fillet(15)
)

# Radial Cuts
# Create a pattern of triangular cuts radiating from center
for angle in range(0, 360, 20):
    # Skip angles that interfere with corners for strength
    if angle % 90 == 0: continue 
    
    radial_cut = (
        cq.Workplane("XY")
        .center(0,0)
        .transformed(rotate=(0,0,angle))
        .moveTo(60, 0)
        .lineTo(90, 10)
        .lineTo(90, -10)
        .close()
        .extrude(10)
        .translate((0,0,-5))
    )
    cutter_ops = cutter_ops.union(radial_cut)

# Corner Cuts (Triangle patterns in the corners)
corner_cut = (
    cq.Workplane("XY")
    .moveTo(0,0)
    .lineTo(30, 0)
    .lineTo(0, 30)
    .close()
    .extrude(10)
)

# Apply corner cuts to 4 corners
for x, y in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
    pos_x = x * (plate_size/2 - 40)
    pos_y = y * (plate_size/2 - 40)
    rot = 0
    if x==1 and y==-1: rot = 90
    if x==1 and y==1: rot = 180
    if x==-1 and y==1: rot = 270
    
    c = corner_cut.rotate((0,0,1), (0,0,0), rot).translate((pos_x, pos_y, -5))
    cutter_ops = cutter_ops.union(c)

# Add perforations along the "arms" seen in the image (rows of small holes)
perf_row = cq.Workplane("XY")
for i in range(3):
    sq = cq.Workplane("XY").rect(5, 5).extrude(10).translate((60 + i*8, 0, -5))
    perf_row = perf_row.union(sq)

for angle in [30, 150, 270]: # Approximate arms of the triangle
     r_row = perf_row.rotate((0,0,1), (0,0,0), angle)
     cutter_ops = cutter_ops.union(r_row)

# Execute Cuts on Plate
final_plate = base_plate.cut(center_tri).cut(cutter_ops)


# 2. Detailed Corner Component (The "Block")
# This component looks like a manifold or a heat exchanger block.
# It has a stepped profile and internal curved channels.

block_l = 60.0
block_w = 60.0
block_h = 20.0

# Base block
block = cq.Workplane("XY").box(block_l, block_w, block_h).translate((-plate_size/2 - 50, 0, block_h/2 - plate_thickness/2))

# Create the L-shaped cutout on the block (corner removed)
cutout_l = block.faces(">Z").workplane().rect(block_l/2, block_w/2).extrude(-block_h, combine=False)
# Shift cutout to corner
cutout_l = cutout_l.translate((block_l/4, -block_w/4, 0))
block = block.cut(cutout_l)

# Create the internal channels/fins
# These look like semicircular grooves cut into the block.

groove_r = 4.0
groove_spacing = 12.0
grooves = cq.Workplane("YZ")

# Create a series of cylinders to cut
for x_off in [-15, 0, 15]: # Rows
    for z_off in [5, 15]: # Levels
        # Creating horizontal channels
        cyl = (
            cq.Workplane("YZ")
            .circle(groove_r)
            .extrude(block_l) # Length of the channel
            .translate((-block_l/2, x_off, z_off)) # Position
        )
        # Rotate to align correctly with the block orientation in world space
        # The extrusion was along X, so we need to position it relative to the block
        # Our block is centered at (-150, 0, 10) roughly.
        
        # Re-orienting for simpler boolean
        cyl_tool = (
            cq.Workplane("XY")
            .workplane(offset=z_off + (block_h/2 - plate_thickness/2) - block_h/2) # Height adjustment
            .moveTo(-plate_size/2 - 50 - block_l/2, x_off) # Start point
            .lineTo(-plate_size/2 - 50 + block_l/2, x_off) # End point
        )
        
        # We need a solid cylinder along X
        cyl_solid = (
            cq.Workplane("YZ")
            .workplane(offset=-plate_size/2 - 50 - block_l/2)
            .center(x_off, z_off + (block_h/2 - plate_thickness/2) - block_h/2)
            .circle(groove_r)
            .extrude(block_l)
        )
        
        block = block.cut(cyl_solid)

# Add the vertical slots/fins visible on the front face of the L-shape
slot_w = 2.0
slot_d = 10.0
for i in range(3):
    z_lev = 5 + i * 5
    slot = (
        cq.Workplane("XY")
        .box(10, 15, slot_w)
        .translate((-plate_size/2 - 50 - 15, 15, z_lev + (block_h/2 - plate_thickness/2) - block_h/2))
    )
    block = block.cut(slot)

# Add the rounded cutouts on the top surface
top_dimples = (
    cq.Workplane("XY")
    .workplane(offset=block_h + (block_h/2 - plate_thickness/2) - block_h/2)
    .rarray(15, 15, 3, 3) # Grid of dimples
    .sphere(3)
)
# We only want to cut, so intersect sphere with a box to make a hemisphere tool or just cut
# Using sphere directly for cut usually works if positioned right.
# Adjust position to block location
top_dimples = top_dimples.translate((-plate_size/2 - 50, 15, 0)) # Shift to the non-cutout part
block = block.cut(top_dimples)

# Combine elements
result = final_plate.union(block)