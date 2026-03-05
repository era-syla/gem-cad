import cadquery as cq

# Parameters
length = 150.0       # Total length
width = 120.0        # Total width including flanges
base_thickness = 5.0 # Thickness of the side flanges
boss_thickness = 10.0 # Total thickness of the central raised area
corner_radius = 10.0 # Radius for the corners of the main body
flange_width = 15.0  # Width of the side flanges containing holes
hole_diameter = 5.0  # Diameter of the through holes
counterbore_diam = 9.0 # Diameter of the counterbore
counterbore_depth = 3.0 # Depth of the counterbore
num_holes_per_side = 5 # Number of holes along each flange

# Derived dimensions
central_width = width - (2 * flange_width)

# Create the base shape (flanges + central area bottom)
# We start with the full footprint
base = (cq.Workplane("XY")
        .box(length, width, base_thickness)
        .edges("|Z")
        .fillet(corner_radius)
       )

# Create the raised central boss
# It sits on top of the base, centered
boss = (cq.Workplane("XY")
        .workplane(offset=base_thickness) # Start on top of the base
        .box(length, central_width, boss_thickness - base_thickness)
        .edges("|Z")
        .fillet(corner_radius)
       )

# Combine base and boss
part = base.union(boss)

# Create hole positions
# We need two lines of holes on the flanges
# Calculate Y positions for the hole lines
y_pos = (width / 2) - (flange_width / 2)
# Calculate X spacing
x_spacing = (length - (2 * corner_radius)) / (num_holes_per_side - 1)
# Create a list of points
hole_points = []

# Generate points for both sides
for side_sign in [-1, 1]:
    for i in range(num_holes_per_side):
        # Center the holes along the length, respecting the corner radius offset usually
        # But looking at image, they span most of the length. 
        # Let's space them evenly along the straight section + corners
        
        # Simpler approach: Distribute evenly along the total length minus some margin
        margin = 10.0
        x_start = -(length / 2) + margin
        x_step = (length - 2*margin) / (num_holes_per_side - 1)
        
        x_pos = x_start + (i * x_step)
        y_loc = side_sign * y_pos
        hole_points.append((x_pos, y_loc))

# Drill counterbored holes
result = (part
          .faces(">Z") # Select the top most face (technically the boss top)
          .workplane() # New workplane
          .pushPoints(hole_points) # Place points
          .cboreHole(hole_diameter, counterbore_diam, counterbore_depth)
         )

# Final clean up/filleting if needed (The image shows very slight fillets on the step)
# This selects the edges at the bottom of the raised boss
result = result.edges(cq.selectors.NearestToPointSelector((0, central_width/2, base_thickness))).fillet(1.0)

# Export or display
if 'show_object' in globals():
    show_object(result)