import cadquery as cq

# Parameters derived from visual estimation
length = 100.0
height = 25.0
thickness = 8.0
hole_diameter = 5.0
fillet_radius = 6.0
num_holes = 4

# Calculate spacing for evenly distributed holes with equal margins
# Distance between holes = Distance from end to hole center
hole_spacing = length / (num_holes + 1)

# Generate the CAD model
result = (
    cq.Workplane("XY")
    # Create the base rectangular block
    .box(length, height, thickness)
    # Select the vertical edges at the top (positive Y) side to apply fillets
    .edges("|Z and >Y")
    .fillet(fillet_radius)
    # Select the top face (positive Z) to drill the holes
    .faces(">Z")
    .workplane()
    # Create a linear array of points along the X axis
    .rarray(hole_spacing, 1, num_holes, 1)
    # Cut the holes through the entire part
    .hole(hole_diameter)
)