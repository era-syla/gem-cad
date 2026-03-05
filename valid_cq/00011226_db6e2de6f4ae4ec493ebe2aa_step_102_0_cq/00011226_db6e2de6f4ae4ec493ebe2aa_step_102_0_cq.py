import cadquery as cq

# Parametric dimensions
# Main shaft (left side)
shaft_length = 30.0
shaft_radius = 10.0

# Middle flange
flange_length = 15.0
flange_radius = 18.0

# Connector end (right side)
connector_length = 15.0
connector_outer_radius = 12.0
connector_inner_radius = 9.0  # Creating the hollow part
chamfer_size = 0.5            # Chamfer at the tip

# Internal features (assumed based on visual)
internal_bore_radius = 5.0    # Through hole or deep bore
internal_step_depth = 5.0     # Depth of the wider opening before narrowing

# Create the main assembly using a Workplane
result = (
    cq.Workplane("XY")
    
    # 1. Create the main shaft (the long cylinder on the left)
    .circle(shaft_radius)
    .extrude(shaft_length)
    
    # 2. Create the flange (the wide middle section)
    .faces(">Z")
    .workplane()
    .circle(flange_radius)
    .extrude(flange_length)
    
    # 3. Create the connector part (the cylinder on the right)
    .faces(">Z")
    .workplane()
    .circle(connector_outer_radius)
    .extrude(connector_length)
    
    # 4. Create the hollow opening (cup-like feature on the right)
    .faces(">Z")
    .workplane()
    .circle(connector_inner_radius)
    .cutBlind(-connector_length + internal_step_depth) # Cut most of the way down the connector
    
    # 5. Create the through-hole or deeper bore (visible at the bottom of the cup)
    .faces("<Z[1]") # Select the face at the bottom of the previous cut
    .workplane()
    .circle(internal_bore_radius)
    .cutBlind(-shaft_length - flange_length - internal_step_depth) # Cut through the rest
    
    # 6. Add chamfer to the opening edge for the refined look
    .faces(">Z")
    .edges()
    .chamfer(chamfer_size)
)