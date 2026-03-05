import cadquery as cq
import math

# --- Parameters ---
outer_radius = 50.0       # Radius of the entire wheel
rim_thickness = 5.0       # Width of the outer rim ring
hub_outer_radius = 10.0   # Radius of the central hub cylinder
hub_inner_radius = 6.0    # Radius of the through-hole in the center
thickness = 4.0           # Thickness of the main plate pattern
hub_height = 8.0          # Height of the central hub (stands taller than spokes)

# --- Design Logic ---

# 1. Create the base outer rim
# We'll create a ring by subtracting a smaller circle from a larger one
rim = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(outer_radius - rim_thickness)
    .extrude(thickness)
)

# 2. Create the central hub
# This is a cylinder in the center, slightly taller than the rest
hub = (
    cq.Workplane("XY")
    .circle(hub_outer_radius)
    .circle(hub_inner_radius)
    .extrude(hub_height)
    # Center the hub vertically relative to the rim/spokes if desired, 
    # but usually hubs stick out. Let's make it symmetric or stick up.
    # Here we stick it up from z=0 like the rim.
)

# 3. Design one spoke "sector"
# The complex curved shape is best defined by a 2D sketch.
# Looking at the image, there are 4 repeating sectors.
# The shape is like a curved scythe or tribal flame.
# We will define points for splines/arcs to create one of these void shapes,
# or conversely, define the solid spoke shape.
# Let's try to define the solid spoke shape connecting hub to rim.

# It's easier to think about this as a subtraction of "voids" from a solid disk,
# or adding "spokes" to the hub/rim. 
# Looking at the negative space (the holes), they are roughly comma-shaped.
# There are two main layers of cutouts per quadrant.
# Let's model the *solid* spoke shape instead, it looks like a swirling arm.

def create_spoke_shape():
    """
    Creates a single curved spoke arm using spline points.
    This shape connects the hub to the rim.
    """
    s = cq.Workplane("XY")
    
    # Points approximate the curvature seen in the image.
    # The shape starts near the hub and spirals out to the rim.
    # Inner curve of the spoke
    pts_inner = [
        (hub_outer_radius - 1, 2),
        (15, 10),
        (25, 25),
        (20, 40),
        (outer_radius - rim_thickness + 1, 20)
    ]
    
    # Outer curve of the spoke (defining the thickness of the arm)
    pts_outer = [
        (hub_outer_radius - 1, -5), 
        (20, 0),
        (35, 15),
        (42, 30),
        (outer_radius - rim_thickness + 1, 10)
    ]

    # This is tricky with splines alone. Let's use a subtractive approach.
    # It's much easier to cut the specific "tribal" holes out of a solid disk.
    return None

# Switching strategy: Subtractive.
# Create a full disk, then cut the specific patterns out.

# Base Disk
base_disk = cq.Workplane("XY").circle(outer_radius).extrude(thickness)

# Define the "Void" shape. 
# There is a large outer kidney/comma shape and a smaller inner detail.
# Let's define one quadrant of cutouts.

def create_cutout_wires():
    """Returns the wires for one sector of cutouts"""
    
    # The large outer curved slot
    # We define a shape that looks like the gap between spokes
    
    # Outer Cutout (the big swoosh)
    outer_cutout_pts = [
        (15, 15),
        (25, 10),
        (35, 10),
        (42, 20),
        (35, 35), 
        (20, 35),
        (10, 25)
    ]
    
    # Because geometric constraints from an image are hard to guess perfectly,
    # we construct a shape using polyline and splines that mimics the visual flow.
    
    # Let's try a different approach: Construct the solid spoke arm using InterpSpline
    # It seems to be a 4-arm swirl.
    
    spoke_wire = (
        cq.Workplane("XY")
        .moveTo(10, 0) # Start at hub
        # Curve out towards rim (concave side)
        .spline([(18, 5), (28, 20), (30, 42)], includeCurrent=True) 
        # Follow rim
        .lineTo(44, 15) 
        # Curve back in (convex side)
        .spline([(35, 15), (25, 5), (10, -3)], includeCurrent=True)
        .close()
    )
    return spoke_wire

# Refined Strategy: 
# The image shows a very specific "tribal" cutout style. 
# It creates a distinct "hook" or "claw" shape.
# Let's build the solid spoke arm that looks like a wave.

# Points for the "upper" curve of a spoke
p1_start = (hub_outer_radius * math.cos(math.radians(-10)), hub_outer_radius * math.sin(math.radians(-10)))
p1_mid1 = (20, 5)
p1_mid2 = (30, 25)
p1_end = (38, 30) # Touches rim inner edge roughly

# Points for the "lower" curve of a spoke
p2_start = (hub_outer_radius * math.cos(math.radians(-50)), hub_outer_radius * math.sin(math.radians(-50)))
p2_mid1 = (25, -5)
p2_mid2 = (38, 10)
p2_end = (43, 15)

# Since exact spline reconstruction is trial-and-error without vectors,
# I will create a parametric approximation of the 4-spoke design.

spoke_sector = (
    cq.Workplane("XY")
    # Start at hub
    .moveTo(hub_outer_radius, 0)
    # Draw the leading edge of the spoke (curving forward)
    .spline([(20, 5), (35, 25), (40, 42)], tangents=[(0, 10), (-10, 0)], includeCurrent=True)
    # Trace along the rim inner radius for a bit
    .radiusArc((38, 28), -45) # Small arc to connect
    # Draw the trailing edge (the hook part)
    .spline([(32, 20), (22, 10), (hub_outer_radius, -4)], tangents=[(-5, -5), (-10, 5)], includeCurrent=True)
    .close()
    .extrude(thickness)
)

# That shape was too complex to guess. Let's do a simple Boolean approach.
# 1. Full Disk
# 2. Cut Central Hole
# 3. Cut "Commas" to form spokes.

# The cutouts.
# There are 4 major cutouts that define the spokes.
# Each cutout looks like a curved teardrop that wraps around.

cutout_shape = (
    cq.Workplane("XY")
    .moveTo(14, 5)
    .spline([(25, 8), (38, 20), (43, 40), (25, 35), (15, 20)], includeCurrent=True)
    .close()
    .extrude(thickness)
)
# This is still guessing. Let's use a proven method for swirl wheels:
# Create a solid disk, cut concentric slots, then rotate/mask them.

# Final Approach: Construct the distinct "Claw" spoke profile 
# seen in the image by unioning curves.

# 1. Hub and Rim (The easy parts)
main_body = cq.Workplane("XY").circle(outer_radius).circle(outer_radius - rim_thickness).extrude(thickness)
hub_body = cq.Workplane("XY").circle(hub_outer_radius).circle(hub_inner_radius).extrude(hub_height)
# Center the hub Z-wise
hub_body = hub_body.translate((0, 0, (thickness - hub_height) / 2)) # Actually, let's just leave it aligned at bottom

# 2. The Spokes
# We will define one spoke and array it 4 times.
# The spoke has a unique shape with a "cutout" bite taken out of it near the hub.

def make_spoke():
    # Define points for a shape that connects hub to rim
    # We work in a single sector
    pts = [
        (9, -2),   # Start at hub
        (20, -5),  # Lower curve start
        (35, 5),   # Lower curve sweep
        (43, 25),  # Tip near rim
        (38, 30),  # Top edge
        (25, 15),  # Inner curve sweep
        (15, 8),   # Back towards hub
        (9, 4)     # Connect to hub
    ]
    
    # Refined Spline for a smoother bio-look
    s = (
        cq.Workplane("XY")
        .moveTo(hub_outer_radius - 1, -2)
        .spline([(25, -5), (44, 20)], tangents=[(1, -0.2), (0, 1)], includeCurrent=True) # Lower Edge
        .lineTo(40, 28) # Rim Connection width
        .spline([(30, 15), (hub_outer_radius - 1, 4)], tangents=[(-1, -1), (-1, 0)], includeCurrent=True) # Upper Edge
        .close()
        .extrude(thickness)
    )
    
    # The image has a secondary small "bite" or hook detail on the spoke.
    # We subtract a small circle/shape to create that "thorn" look.
    bite = (
        cq.Workplane("XY")
        .moveTo(20, 5)
        .circle(3.5)
        .extrude(thickness)
    )
    
    return s.cut(bite)

# Generate one spoke
one_spoke = make_spoke()

# Create the assembly
# 1. Base Rim
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(outer_radius - rim_thickness)
    .extrude(thickness)
)

# 2. Add Hub
result = result.union(
    cq.Workplane("XY")
    .circle(hub_outer_radius)
    .circle(hub_inner_radius)
    .extrude(hub_height)
    .translate((0,0, (thickness-hub_height)/2)) # Center hub vertically on spoke plane
)

# 3. Add Spokes (Arrayed)
for i in range(4):
    angle = i * 90
    rotated_spoke = one_spoke.rotate((0,0,0), (0,0,1), angle)
    result = result.union(rotated_spoke)

# 4. Filleting
# The image shows very smooth, rounded edges on the top face.
try:
    result = result.edges("|Z").fillet(0.5) # Fillet vertical edges slightly
    result = result.faces(">Z").edges().fillet(0.4) # Fillet top face edges
except:
    # Fallback if geometry is too complex for fillet kernel
    pass

# Ensure the hub hole is clear (union might have closed it)
result = result.cut(
    cq.Workplane("XY").circle(hub_inner_radius).extrude(20).translate((0,0,-5))
)