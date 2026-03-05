import cadquery as cq

# Parametric dimensions
height = 100.0       # Height of the cylinder
outer_diameter = 40.0 # Outer diameter of the cylinder
wall_thickness = 2.0  # Thickness of the cylinder wall

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create the hollow cylinder
# 1. Start on the XY plane
# 2. Draw the outer circle
# 3. Draw the inner circle to create the hollow profile
# 4. Extrude to the specified height
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(height)
)

# Optional: Add a slight vertical seam line to match the visual detail in the image
# This creates a very thin slit or scribed line to represent a manufacturing seam
# For a pure geometric solid, this might be omitted, but here is a simple implementation:
# We create a thin box and cut it, or just leave it as a perfect tube. 
# Given the prompt asks for the 3D model based on the image, a simple tube is the standard interpretation.
# If a physical "split" was needed, we would cut a slot. 
# The code below produces the clean, standard pipe geometry.