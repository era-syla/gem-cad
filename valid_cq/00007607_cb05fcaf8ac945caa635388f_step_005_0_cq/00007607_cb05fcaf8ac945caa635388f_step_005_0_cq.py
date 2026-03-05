import cadquery as cq

# --- Parameters ---
width = 10.0      # Width of the rectangular base
depth = 5.0       # Thickness of the part
height_rect = 30.0 # Height of the rectangular section
radius = width / 2 # Radius of the top circular arc (matches width/2 for tangent fit)
hole_radius = 1.0 # Radius of the small hole near the top
hole_offset = 2.0 # Distance from the center of the arc to the hole center

# Array parameters
num_instances = 4
spacing = 15.0    # Distance between centers of instances

# --- Geometry Construction ---

# 1. Create a single instance sketch
# We start with a rectangle and then add the arc on top.
# The sketch is drawn on the XY plane.
path = (
    cq.Workplane("XY")
    .lineTo(width, 0)         # Bottom edge
    .lineTo(width, height_rect) # Right vertical edge
    .threePointArc((width/2, height_rect + radius), (0, height_rect)) # Top semi-circle
    .lineTo(0, 0)             # Left vertical edge
    .close()
)

# 2. Extrude to create the 3D solid
single_part = path.extrude(depth)

# 3. Add the hole
# The arc center is at (width/2, height_rect).
# Looking at the image, the hole seems concentric or slightly offset from the arc center. 
# It looks centered horizontally (at width/2).
hole_center_y = height_rect  # Center of the arc
single_part = (
    single_part.faces(">Z") # Select the front face
    .workplane()
    .pushPoints([(width/2, hole_center_y)])
    .hole(hole_radius * 2) # .hole takes diameter
)

# 4. Create the linear array
# We will create a list of locations and place the single_part at each one.
result = (
    cq.Workplane("XY")
    .rarray(spacing, 1, num_instances, 1) # Linear array along X
    .eachpoint(lambda loc: single_part.val().moved(loc))
)

# Note: rarray centers the array around the origin. 
# If we want the first item at the origin, we would approach it differently,
# but rarray is the most efficient way to get the visual result.