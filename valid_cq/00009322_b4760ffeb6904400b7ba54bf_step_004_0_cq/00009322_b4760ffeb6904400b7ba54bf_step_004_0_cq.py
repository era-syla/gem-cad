import cadquery as cq

# Define parameters for the three plates
# Dimensions appear to be roughly small square, rectangle, large square.
# Let's create a reusable function to make the base shape.

def create_plate(length, width, thickness, corner_radius, hole_diameter, csk_diameter, csk_angle):
    """
    Creates a rectangular plate with rounded corners and a central countersunk hole.
    """
    
    # 1. Create the base box
    plate = cq.Workplane("XY").box(length, width, thickness)
    
    # 2. Fillet the vertical edges
    plate = plate.edges("|Z").fillet(corner_radius)
    
    # 3. Create the countersunk hole in the center
    # cskHole creates a countersunk hole. 
    # The depth logic in CadQuery's cskHole usually requires the hole to go through.
    plate = plate.faces(">Z").workplane().cskHole(hole_diameter, csk_diameter, csk_angle)
    
    return plate

# --- Parameters ---

# Common parameters
thickness = 5.0
corner_radius = 2.0
hole_dia = 6.0      # Clearance hole for screw
csk_dia = 12.0      # Diameter of the countersink top
csk_ang = 90.0      # Standard countersink angle

# Specific dimensions for the three variations seen in the image
# 1. Large Square
large_sq_dim = 60.0

# 2. Rectangle
rect_length = 60.0
rect_width = 30.0

# 3. Small Square
small_sq_dim = 30.0

# --- Geometry Generation ---

# Create the individual parts
large_plate = create_plate(large_sq_dim, large_sq_dim, thickness, corner_radius, hole_dia, csk_dia, csk_ang)
rect_plate = create_plate(rect_length, rect_width, thickness, corner_radius, hole_dia, csk_dia, csk_ang)
small_plate = create_plate(small_sq_dim, small_sq_dim, thickness, corner_radius, hole_dia, csk_dia, csk_ang)

# --- Assembly ---
# Position them to match the image (roughly diagonal layout)

# Large plate at origin (or slightly offset)
p1 = large_plate.translate((-50, -30, 0))

# Rectangle in the middle
p2 = rect_plate.translate((20, 20, 0))

# Small square at the top right
p3 = small_plate.translate((70, 50, 0))

# Combine into a single result object for visualization
result = p1.union(p2).union(p3)