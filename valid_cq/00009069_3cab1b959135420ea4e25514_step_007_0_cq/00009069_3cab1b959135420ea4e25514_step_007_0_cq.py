import cadquery as cq
import math

# --- Parameters ---
# Horn dimensions
horn_mouth_dia = 60.0
horn_throat_dia = 20.0
horn_length = 50.0
horn_wall_thickness = 1.5

# Y-Split/Mounting Structure dimensions
arm_length = 40.0
arm_width_start = 12.0  # Width where it meets the horn throat
arm_width_end = 6.0    # Width at the tips
arm_spread = 35.0      # Distance between tips at the end
arm_thickness = 5.0    # Thickness of the arms

# Mounting Slot/Clip feature
clip_length = 20.0
clip_width = 8.0
clip_thickness = 3.0
slot_depth = 1.5

# --- Geometry Construction ---

# 1. Create the Horn Body using a Revolve operation
# We define a profile in the XZ plane and revolve it around the X axis.
# The profile is an exponential or parabolic curve for the flare.

def exponential_flare(t):
    """Calculates radius at position t (0 to 1) along length."""
    r_start = horn_throat_dia / 2.0
    r_end = horn_mouth_dia / 2.0
    # Equation: r(x) = r_start * e^(k*x)
    # k = ln(r_end/r_start)
    k = math.log(r_end / r_start)
    return r_start * math.exp(k * t)

# Generate points for the outer shell
points_outer = []
steps = 20
for i in range(steps + 1):
    t = i / steps
    x = t * horn_length
    y = exponential_flare(t)
    points_outer.append((x, y))

# Generate points for the inner shell (offset by wall thickness)
points_inner = []
for i in range(steps, -1, -1):
    t = i / steps
    x = t * horn_length
    # Approximate normal offset by subtracting from Y
    # For a true offset, vector math is needed, but this is sufficient for this shape
    y = exponential_flare(t) - horn_wall_thickness
    # Ensure inner radius doesn't invert
    if y < 0.1: y = 0.1 
    points_inner.append((x, y))

# Close the polygon
horn_profile_pts = points_outer + points_inner + [points_outer[0]]

# Create the Horn Solid
horn = (
    cq.Workplane("XY")
    .polyline(points_outer + points_inner)
    .close()
    .revolve(360, (0,0,0), (1,0,0))
)

# 2. Create the Y-shaped mounting arms
# This structure attaches to the throat (smaller end) of the horn.
# We'll build this starting from the back of the horn (X=0) and extending backwards (-X).

# Define the shape of one arm
arm_path = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(-arm_length, arm_spread/2)
)

# Create a loft for the arm to transition smoothly
# Profile at the horn throat connection
throat_connect = (
    cq.Workplane("YZ")
    .workplane(offset=0) # At X=0
    .rect(horn_throat_dia, horn_throat_dia/1.5) # Approximate rectangular connection
    .extrude(-5) # Slight overlap into horn for boolean union
)

# We will model the "fork" shape using a sketch and extrusion approach for simplicity
# relative to the complex organic blending seen in the image.

# Create the main body of the fork using a loft or hull
# Start section (Circle at throat)
s1 = cq.Workplane("YZ").workplane(offset=horn_length * 0.1).circle(horn_throat_dia/2 + 1)

# End section (Two rectangles at the tips)
s2 = (
    cq.Workplane("YZ")
    .workplane(offset=-arm_length)
    .pushPoints([(0, arm_spread/2), (0, -arm_spread/2)])
    .rect(arm_thickness, arm_width_end)
)

# Middle control section for smooth transition
s_mid = (
    cq.Workplane("YZ")
    .workplane(offset=-arm_length/3)
    .rect(horn_throat_dia, arm_spread/1.5)
)

# Constructing the organic "Y" shape using a hull/loft operation is tricky directly.
# Let's approximate the Y-shape seen in the image: a central block that splits.
# We will use a solid block and cut away the middle.

fork_block = (
    cq.Workplane("XY")
    .moveTo(2, 0) # Start slightly inside the horn
    .lineTo(-arm_length, arm_spread/2 + arm_width_end/2)
    .lineTo(-arm_length, -(arm_spread/2 + arm_width_end/2))
    .lineTo(2, 0)
    .close()
    .extrude(arm_thickness)
    .translate((0, 0, -arm_thickness/2)) # Center vertically
)

# Cutout the middle to make it a fork
cutout = (
    cq.Workplane("XY")
    .moveTo(-5, 0)
    .lineTo(-arm_length-1, (arm_spread/2 - arm_width_end/2))
    .lineTo(-arm_length-1, -(arm_spread/2 - arm_width_end/2))
    .close()
    .extrude(arm_thickness*2)
    .translate((0, 0, -arm_thickness))
)

# Refine the fork shape with fillets
fork = fork_block.cut(cutout)
fork = fork.edges("|Z").fillet(2.0)
fork = fork.edges("|Y").fillet(1.0)


# 3. Create the Top Clip/Rail feature
# This is the rectangular feature on top of the fork junction.

clip = (
    cq.Workplane("XZ")
    .workplane(offset=0)
    .moveTo(0, horn_throat_dia/2) 
    .rect(clip_length, clip_thickness, centered=False)
    .extrude(clip_width) # Extrude in Y
    .translate((-clip_length, -clip_width/2, 0)) # Position it
)

# Add the slot inside the clip
slot_cutter = (
    cq.Workplane("XZ")
    .workplane(offset=0)
    .moveTo(-clip_length/2, horn_throat_dia/2 + clip_thickness/2)
    .rect(clip_length + 2, slot_depth)
    .extrude(clip_width - 2)
    .translate((-clip_length/2, -(clip_width-2)/2, 0))
)
clip = clip.cut(slot_cutter)


# 4. Combine parts
# Position the Horn correctly relative to the fork.
# The horn was revolved around X, starting at X=0 and going positive.
# The fork starts at X=2 and goes negative.

# Combine
structure = fork.union(clip)

# Smooth the transition between the horn and the structure
# Since fillets can be fragile in CAD kernels between complex disjoint surfaces,
# we ensure overlap and union.
result = horn.union(structure)

# Apply final fillets to smooth the junction where the flat fork meets the round horn
try:
    result = result.edges(cq.NearestToPointSelector((0, 0, horn_throat_dia/2))).fillet(2.0)
except:
    pass # If fillet fails due to geometry complexity, return unfilleted

# Rotate for better view alignment with the prompt image
result = result.rotate((0,0,0), (0,0,1), 135).rotate((0,0,0), (1,0,0), -20)