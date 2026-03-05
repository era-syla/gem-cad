import cadquery as cq

# Parametric dimensions
length = 100.0   # Total length of the tube
outer_diam = 10.0 # Outer diameter of the tube
inner_diam = 8.0  # Inner diameter of the tube (must be less than outer_diam)

# Create the tube
# We start with a workplane (usually XY)
# Draw the outer circle
# Draw the inner circle to create the hollow profile
# Extrude it to the desired length
result = (
    cq.Workplane("XY")
    .circle(outer_diam / 2)
    .circle(inner_diam / 2)
    .extrude(length)
)

# Alternative method using cylinder and hole/cut
# result = cq.Workplane("XY").cylinder(length, outer_diam/2).faces(">Z").hole(inner_diam, length)

# Export or display is handled by the calling environment, 
# but 'result' variable holds the final geometry.