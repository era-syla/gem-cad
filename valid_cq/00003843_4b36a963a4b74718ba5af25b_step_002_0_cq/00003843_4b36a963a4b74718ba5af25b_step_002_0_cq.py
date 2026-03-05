import cadquery as cq

# Define parameters for the tube
length = 100.0   # Length of the tube
outer_diam = 10.0 # Outer diameter of the tube
wall_thickness = 1.5 # Thickness of the tube wall

# Calculate inner diameter
inner_diam = outer_diam - (2 * wall_thickness)

# Create the tube geometry
# We start by drawing the outer circle and extruding it
# Then we cut the inner hole
result = (
    cq.Workplane("XY")
    .circle(outer_diam / 2.0)
    .extrude(length)
    .faces(">Z")
    .workplane()
    .hole(inner_diam)
)

# Alternatively, a more direct way to create a tube in one go:
# result = cq.Workplane("XY").circle(outer_diam / 2.0).circle(inner_diam / 2.0).extrude(length)