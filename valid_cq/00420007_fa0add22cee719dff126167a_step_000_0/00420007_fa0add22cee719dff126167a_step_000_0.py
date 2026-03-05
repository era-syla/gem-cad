import cadquery as cq

# Parameters for dimensions
thickness = 5.0
fillet_radius = 5.0

# Hole diameters
d_small = 3.5  # M3 clearance
d_med = 6.0    # Mounting holes
d_large = 24.0 # Bearing/Pass-through hole
d_corner = 5.0 

# Define the outer profile of the plate using key vertices
# Coordinates approximated based on visual estimation (Unit: mm)
p_top_left = (0, 150)
p_top_right = (260, 150)
p_btm_right = (300, 60)
p_curve_start = (60, 45) # Where the bottom curve meets the left chamfer
p_curve_mid = (180, 80)  # Midpoint to define the concave arc
p_btm_left = (0, 70)     # Start of the bottom-left chamfer on the vertical edge

# Create the base solid
plate = (cq.Workplane("XY")
    .moveTo(*p_top_left)
    .lineTo(*p_top_right)
    .lineTo(*p_btm_right)
    .threePointArc(p_curve_mid, p_curve_start)
    .lineTo(*p_btm_left)
    .close()
    .extrude(thickness)
)

# Apply fillets to vertical edges
plate = plate.edges("|Z").fillet(fillet_radius)

# Define hole patterns
# 1. Grid of small holes on the left and top
small_holes_pts = []
# Top row
for x in range(20, 250, 20):
    small_holes_pts.append((x, 135))
# Second row (interrupted by large hole)
for x in range(20, 110, 20):
    small_holes_pts.append((x, 115))
# Grid block on left
for y in [95, 75]:
    for x in range(20, 90, 20):
        small_holes_pts.append((x, y))
# Scattered small holes
small_holes_pts.extend([
    (40, 55), (100, 95), (120, 75), 
    (240, 115), (255, 100), (270, 85), (285, 70) # Following right edge
])

# 2. Specific larger holes
large_hole_pt = (160, 115)
med_hole_1 = (90, 75)
med_hole_2 = (210, 80)
corner_hole = (290, 50)

# Perform cuts
result = (plate
    .faces(">Z")
    .workplane()
    # Cut small holes
    .pushPoints(small_holes_pts)
    .hole(d_small)
    # Cut large hole
    .pushPoints([large_hole_pt])
    .hole(d_large)
    # Cut medium holes
    .pushPoints([med_hole_1, med_hole_2])
    .hole(d_med)
    # Cut corner hole
    .pushPoints([corner_hole])
    .hole(d_corner)
)