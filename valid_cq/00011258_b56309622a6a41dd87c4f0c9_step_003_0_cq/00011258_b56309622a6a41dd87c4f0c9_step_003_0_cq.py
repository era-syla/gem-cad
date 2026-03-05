import cadquery as cq

# Define parametric dimensions
# Based on visual inspection, this is a thin rectangular plate
length = 100.0  # Dimension along one horizontal axis
width = 80.0    # Dimension along the other horizontal axis
thickness = 2.0 # Thickness of the plate

# Create the solid geometry
# We create a box centered on the XY plane for symmetry, though center=False is also valid
result = cq.Workplane("XY").box(length, width, thickness)

# Alternatively, if a specific origin point is desired (e.g., bottom-left corner), 
# one could use:
# result = cq.Workplane("XY").box(length, width, thickness, centered=(False, False, False))

# The variable 'result' now contains the 3D model