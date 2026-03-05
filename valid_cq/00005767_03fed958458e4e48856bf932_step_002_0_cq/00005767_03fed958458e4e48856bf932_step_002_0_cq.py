import cadquery as cq

# Define parametric dimensions
length = 200.0   # Length of the tube
outer_diam = 10.0 # Outer diameter of the tube
thickness = 1.0  # Wall thickness of the tube
inner_diam = outer_diam - (2 * thickness)

# Create the tube
# We create a solid cylinder first
result = cq.Workplane("XY").circle(outer_diam / 2).extrude(length)

# Then we create a hole to make it a tube
# Alternatively, we could just sketch two concentric circles and extrude
result = (
    cq.Workplane("XY")
    .circle(outer_diam / 2)
    .circle(inner_diam / 2)
    .extrude(length)
)

# If the image represents a solid rod instead of a tube, uncomment the line below
# result = cq.Workplane("XY").circle(outer_diam / 2).extrude(length)