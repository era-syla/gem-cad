import cadquery as cq

# -- Parametric Dimensions --
num_holes = 30
pitch = 12.7            # Hole spacing (approx 0.5 inch, standard for VEX/Meccano)
width = 12.7            # Width of the angle legs
thickness = 1.6         # Thickness of the material (approx 1/16 inch)
hole_diameter = 4.2     # Hole diameter
fillet_radius = 3.0     # Radius for rounding the end corners

# Derived dimensions
length = num_holes * pitch
flange_center = width / 2

# -- Geometry Construction --

# 1. Create the base L-shaped profile
# Drawn on the YZ plane, extruded along the X axis
# Profile logic: Legs extend in +Y and +Z directions from origin (0,0)
result = (
    cq.Workplane("YZ")
    .polyline([
        (0, 0),                 # Corner
        (width, 0),             # End of horizontal leg
        (width, thickness),     # Top tip of horizontal leg
        (thickness, thickness), # Inner corner
        (thickness, width),     # Top tip of vertical leg
        (0, width),             # Back of vertical leg
        (0, 0)                  # Close profile
    ])
    .close()
    .extrude(length)
)

# 2. Define Hole Locations
# Calculate X positions for holes (centered on pitch)
x_locs = [pitch/2 + i * pitch for i in range(num_holes)]

# Create point lists for both flanges
# Horizontal flange (Flat on XY): Points are (x, y)
horizontal_pts = [(x, flange_center) for x in x_locs]

# Vertical flange (Flat on XZ): Points are (x, z) 
# Note: When mapping a workplane to the vertical face, Local Y typically maps to Global Z
vertical_pts = [(x, flange_center) for x in x_locs]

# 3. Cut Holes
# Select the top face of the horizontal leg (approx Z = thickness)
result = (
    result
    .faces(cq.NearestToPointSelector((length/2, flange_center, thickness)))
    .workplane()
    .pushPoints(horizontal_pts)
    .hole(hole_diameter)
)

# Select the side face of the vertical leg (approx Y = thickness)
result = (
    result
    .faces(cq.NearestToPointSelector((length/2, thickness, flange_center)))
    .workplane()
    .pushPoints(vertical_pts)
    .hole(hole_diameter)
)

# 4. Apply Fillets to Ends
# Fillet the corners of the horizontal flange (Edges parallel to Z at Y=width)
result = (
    result
    .edges("|Z")
    .filter(lambda e: abs(e.Center().y - width) < 0.1)
    .fillet(fillet_radius)
)

# Fillet the corners of the vertical flange (Edges parallel to Y at Z=width)
result = (
    result
    .edges("|Y")
    .filter(lambda e: abs(e.Center().z - width) < 0.1)
    .fillet(fillet_radius)
)