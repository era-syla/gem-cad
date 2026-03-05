import cadquery as cq

# Parameters for the parametric model
length = 100.0        # Total length of the top plate
width = 50.0          # Total width of the top plate
top_thickness = 3.0   # Thickness of the upper wider section
base_thickness = 5.0  # Thickness of the lower narrower section
inset = 3.0           # Distance the lower section is indented from the edge

# Generate the 3D model
result = (
    cq.Workplane("XY")
    # Create the top plate
    # centered=(True, True, False) places the box centered in X/Y, 
    # but starting at Z=0 and extruding upwards to Z=top_thickness.
    .box(length, width, top_thickness, centered=(True, True, False))
    
    # Select the bottom face (at Z=0)
    .faces("<Z")
    .workplane()
    
    # Sketch the smaller rectangle for the base
    .rect(length - 2 * inset, width - 2 * inset)
    
    # Extrude downwards to form the base block
    .extrude(base_thickness)
)