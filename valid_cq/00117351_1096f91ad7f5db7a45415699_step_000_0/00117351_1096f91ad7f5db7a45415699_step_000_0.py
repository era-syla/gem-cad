import cadquery as cq

# -- Parametric Dimensions --
width = 100.0          # Overall width of the shape at the top corners
height = 80.0          # Vertical distance from bottom tip to top corners
thickness = 15.0       # Thickness of the solid
chamfer_size = 3.0     # Size of the bevel on the top edge

# Curve control parameters
top_bulge = 15.0       # How much the top arc curves outward
side_concavity = 8.0   # How much the side arcs curve inward

# -- Geometry Calculation --

# Key Vertices
p_bottom = (0, 0)
p_top_right = (width / 2, height)
p_top_left = (-width / 2, height)

# Arc Intermediate Points (Control Points)
# 1. Right Side (Concave): Midpoint of vector shifted inwards
p_mid_right = (width / 4 - side_concavity, height / 2)

# 2. Top Edge (Convex): Center X, above the corner height
p_mid_top = (0, height + top_bulge)

# 3. Left Side (Concave): Symmetric to right side
p_mid_left = (-width / 4 + side_concavity, height / 2)

# -- Model Generation --

# Create 2D Profile and Extrude
result = (
    cq.Workplane("XY")
    .moveTo(*p_bottom)
    .threePointArc(p_mid_right, p_top_right)  # Draw right concave edge
    .threePointArc(p_mid_top, p_top_left)     # Draw top convex edge
    .threePointArc(p_mid_left, p_bottom)      # Draw left concave edge
    .close()
    .extrude(thickness)
)

# Apply Chamfer to Top Edges
# Select the top face (positive Z), then select its perimeter edges
result = result.faces(">Z").edges().chamfer(chamfer_size)