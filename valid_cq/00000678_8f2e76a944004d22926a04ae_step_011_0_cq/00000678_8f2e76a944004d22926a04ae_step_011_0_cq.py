import cadquery as cq

# Parametric dimensions
width = 100.0   # Width of the plate
height = 50.0   # Height of the plate
thickness = 2.0 # Thickness of the plate

# Create the rectangular plate
# We center it on the X and Z axes for symmetry, but extrude along Y for thickness
result = (
    cq.Workplane("XY")
    .box(width, thickness, height)
)

# Alternatively, if we want to sketch on a plane and extrude:
# result = (
#     cq.Workplane("Front")
#     .rect(width, height)
#     .extrude(thickness)
# )