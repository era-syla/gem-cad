import cadquery as cq

# Parametric dimensions
length = 100.0   # Length of the block
height = 80.0    # Height of the block
thickness = 15.0 # Thickness of the block
fillet_radius = 5.0 # Radius of the rounded corners

# Create the base rectangular block
# We extrude a rectangle to create the initial box shape
result = (
    cq.Workplane("XY")
    .box(length, height, thickness)
    .edges("|Z")  # Select vertical edges (parallel to Z axis)
    .fillet(fillet_radius) # Apply fillet to all four vertical corners
)

# Alternatively, if only specific corners need filleting based on a strict interpretation 
# of just the visible silhouette (though typically these shapes are symmetric):
# The image shows a block with rounded corners on its profile. 
# A common way to make this is drawing a rectangle with rounded corners and extruding.

result = (
    cq.Workplane("XY")
    .rect(length, height)
    .extrude(thickness)
    .edges("|Z") # Select edges along the extrusion direction
    .fillet(fillet_radius)
)