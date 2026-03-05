import cadquery as cq

# Define parametric dimensions
height = 100.0    # Total height of the object
width = 30.0      # Width of the face
thickness = 6.0   # Thickness of the material
chamfer_size = 2.0 # Size of the 45-degree chamfer

# Create the base geometry
# We create a box centered on the origin. 
# Height is aligned with the Z-axis.
result = cq.Workplane("XY").box(width, thickness, height)

# Select the specific vertical edge to chamfer
# |Z selects edges parallel to the Z axis (vertical)
# <X selects the edge at the minimum X coordinate (left side)
# >Y selects the edge at the maximum Y coordinate (front side)
edge_to_chamfer = result.edges("|Z and <X and >Y")

# Apply the chamfer operation
result = edge_to_chamfer.chamfer(chamfer_size)