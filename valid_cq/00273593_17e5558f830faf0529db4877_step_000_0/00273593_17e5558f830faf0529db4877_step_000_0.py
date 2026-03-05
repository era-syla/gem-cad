import cadquery as cq

# Define parametric dimensions based on the visual proportions
length = 100.0  # Length of the rectangular plate
width = 30.0    # Width of the plate
thickness = 4.0 # Thickness of the plate

# Create the 3D model
# We start with a workplane on the XY plane
# Then create a box (cuboid) centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)