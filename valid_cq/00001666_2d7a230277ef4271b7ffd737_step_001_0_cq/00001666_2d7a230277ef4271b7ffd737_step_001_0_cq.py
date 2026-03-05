import cadquery as cq

# Parametric dimensions
outer_diameter = 30.0
inner_diameter = 20.0
thickness = 5.0
chamfer_size = 1.0

# Create the main cylindrical body (the washer shape)
# We start with a solid cylinder for the outer diameter
# Then cut the inner diameter hole
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(thickness)
)

# Apply chamfers to the edges
# The image shows chamfers on both the inner and outer edges of the top face,
# and likely on the bottom face as well, although only the top is clearly visible.
# Standard washers often have chamfers or rounded edges. The image specifically
# shows a distinct angled cut (chamfer) on the top inner and outer edges.

# Select the top and bottom faces
# Then select the edges on those faces
# We will apply a chamfer to all circular edges
result = result.edges("%CIRCLE").chamfer(chamfer_size)

# If only the top edges were intended based on a stricter interpretation:
# result = result.faces(">Z").edges().chamfer(chamfer_size)
# But a symmetrical part is more likely for this generic shape. The code above applies to all edges.

# Alternative interpretation: The image looks like it might specifically have chamfers
# primarily on the top face's OD and ID. Let's stick to the symmetric chamfer 
# as it creates the most robust "finished" looking part matching the render style.