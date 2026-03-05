import cadquery as cq

# Parametric dimensions
length = 100.0   # Total length of the plate
width = 30.0     # Total width of the plate
thickness = 2.0  # Thickness of the plate
hole_diameter = 15.0 # Diameter of the center hole

# Create the main rectangular body centered at the origin
# box(length, width, thickness) creates a box centered at (0,0,0) by default in some contexts,
# but Workplane.box() centers it in x and y, and extends z.
# To keep it simple and symmetric, we center it.

result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .faces(">Z")
    .workplane()
    .hole(hole_diameter)
)

# Alternatively, using sketching/extruding which is often cleaner for flat parts:
# result = (
#     cq.Workplane("XY")
#     .rect(length, width)
#     .circle(hole_diameter / 2)
#     .extrude(thickness)
# )