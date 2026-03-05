import cadquery as cq

# Parameters for the stepped pyramid
num_layers = 4
base_width = 100.0  # Width of the bottom-most square
base_height = 20.0  # Height of each individual layer
step_inset = 10.0   # How much each layer shrinks from the one below it
fillet_radius = 5.0 # Radius for the rounded corners

# Create the base object
result = cq.Workplane("XY")

# Loop to create each layer
current_width = base_width
current_height_offset = 0.0

for i in range(num_layers):
    # Create a square centered at the origin
    layer = (
        cq.Workplane("XY")
        .workplane(offset=current_height_offset)
        .rect(current_width, current_width)
        .extrude(base_height)
    )
    
    # Fillet the vertical edges of the current layer
    # We select edges that are parallel to the Z axis
    layer = layer.edges("|Z").fillet(fillet_radius)
    
    # Union the new layer with the previous result
    # For the first iteration, result is just the first layer
    if i == 0:
        result = layer
    else:
        result = result.union(layer)
    
    # Update parameters for the next layer
    current_width -= (2 * step_inset)
    current_height_offset += base_height

# The 'result' variable now contains the final geometry