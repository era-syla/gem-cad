import cadquery as cq

# Parametric dimensions based on visual estimation of the provided image
height = 60.0         # Height of the cylinder
outer_diameter = 20.0 # Outer diameter
inner_diameter = 10.0 # Inner diameter (through hole)
chamfer_size = 0.8    # Size of the chamfer on the outer edges

# Generate the 3D model
# 1. Create a solid cylinder on the XY plane
# 2. Select all edges (top and bottom circular rims) and apply a chamfer
# 3. Select the top face and cut a hole through the entire part
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(height)
    .edges()
    .chamfer(chamfer_size)
    .faces(">Z")
    .workplane()
    .hole(inner_diameter)
)