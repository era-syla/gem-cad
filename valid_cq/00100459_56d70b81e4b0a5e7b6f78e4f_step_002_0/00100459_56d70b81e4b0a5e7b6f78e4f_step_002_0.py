import cadquery as cq

# --- Parameters ---
# Dimensions based on visual analysis (standard Technic beam geometry)
num_holes = 15
pitch = 8.0          # Distance between hole centers
width = 8.0          # Beam width (square profile)
length = num_holes * pitch
hole_diameter = 4.8  # Standard axle clearance
cbore_diameter = 6.2 # Counterbore diameter for aesthetic/functional rim
cbore_depth = 0.8    # Shallow counterbore
fillet_radius = 0.3  # Small radius on edges for realism

# --- Geometry Construction ---

# 1. Create the base rectangular prism (Beam)
# Oriented vertically along the Z-axis
result = cq.Workplane("XY").box(width, width, length)

# 2. Calculate hole positions
# Holes are distributed evenly along the Z-axis
# Z-coordinates range from -length/2 to +length/2
z_positions = [
    (i * pitch) - (length / 2) + (pitch / 2) 
    for i in range(num_holes)
]
# Points for the 2D workplanes on the faces (local_x=0, local_y=z)
hole_centers = [(0, z) for z in z_positions]

# 3. Create Holes along the X-axis (Front and Back faces)
# Cut through-hole with counterbore on the front face (>X)
result = (
    result.faces(">X")
    .workplane()
    .pushPoints(hole_centers)
    .cboreHole(hole_diameter, cbore_diameter, cbore_depth, depth=None) # Depth=None cuts through entire part
)

# Add counterbore detail to the back face (<X) 
# (Through-hole already exists from previous operation)
result = (
    result.faces("<X")
    .workplane()
    .pushPoints(hole_centers)
    .hole(cbore_diameter, cbore_depth)
)

# 4. Create Holes along the Y-axis (Left and Right faces)
# Cut through-hole with counterbore on the right face (>Y)
# These will intersect with the X-axis holes
result = (
    result.faces(">Y")
    .workplane()
    .pushPoints(hole_centers)
    .cboreHole(hole_diameter, cbore_diameter, cbore_depth, depth=None)
)

# Add counterbore detail to the left face (<Y)
result = (
    result.faces("<Y")
    .workplane()
    .pushPoints(hole_centers)
    .hole(cbore_diameter, cbore_depth)
)

# 5. Apply fillets to the long vertical edges
result = result.edges("|Z").fillet(fillet_radius)