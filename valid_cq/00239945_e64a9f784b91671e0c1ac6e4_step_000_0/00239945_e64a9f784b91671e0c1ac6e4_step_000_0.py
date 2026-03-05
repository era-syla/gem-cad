import cadquery as cq

# Parametric dimensions
length = 120.0       # Total length of the plate
width = 25.0         # Width of the plate
thickness = 4.0      # Thickness of the plate
fillet_radius = 2.0  # Radius of the corner fillets
hole_diameter = 5.0  # Diameter of the through-holes
num_holes = 5        # Number of holes
# Calculate spacing to evenly distribute holes with margins
# Assuming a standard margin roughly equal to half the width at ends
hole_spacing = (length - width) / (num_holes - 1) 
# Alternatively, fixed spacing: hole_spacing = 20.0

# Generate the 3D model
result = (
    cq.Workplane("XY")
    # 1. Create the main rectangular body
    .box(length, width, thickness)
    
    # 2. Add fillets to the four vertical edges
    .edges("|Z")
    .fillet(fillet_radius)
    
    # 3. Create the pattern of holes on the top face
    .faces(">Z")
    .workplane()
    .rarray(hole_spacing, 1, num_holes, 1) # Linear array along X-axis
    .hole(hole_diameter)
)