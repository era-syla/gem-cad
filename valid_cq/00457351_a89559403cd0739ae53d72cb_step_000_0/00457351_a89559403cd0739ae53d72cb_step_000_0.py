import cadquery as cq

# Parametric dimensions based on visual aspect ratio
height = 100.0  # Total height of the plate
width = 60.0    # Width of the plate
thickness = 10.0 # Thickness of the plate

# Create the rectangular prism (box)
# box() creates a box centered at the origin
result = cq.Workplane("XY").box(width, thickness, height)