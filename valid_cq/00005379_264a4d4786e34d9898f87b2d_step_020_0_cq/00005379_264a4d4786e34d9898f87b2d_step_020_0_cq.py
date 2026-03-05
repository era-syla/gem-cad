import cadquery as cq

# Define parametric dimensions
length = 50.0  # Length of the box
width = 30.0   # Width of the box
height = 10.0  # Height of the box
fillet_radius = 2.0 # Radius for the rounded edges

# Create the base box
box = cq.Workplane("XY").box(length, width, height)

# Apply fillet to all edges
# Selecting all edges and applying the fillet
result = box.edges().fillet(fillet_radius)