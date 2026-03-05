import cadquery as cq

# Define dimensions for the pipe/tube
length = 100.0   # Length of the tube
outer_diam = 10.0 # Outer diameter of the tube
thickness = 1.5  # Wall thickness of the tube
inner_diam = outer_diam - (2 * thickness)

# Create the tube
# We create a solid cylinder first
result = (
    cq.Workplane("XY")
    .circle(outer_diam / 2.0)
    .circle(inner_diam / 2.0)
    .extrude(length)
)

# Alternatively, using the tube operation for a potentially cleaner approach in some contexts:
# result = cq.Workplane("XY").circle(outer_diam / 2).extrude(length).faces(">Z").hole(inner_diam)

# Export the result (optional, but good practice for verification if running locally)
# cq.exporters.export(result, "tube.step")