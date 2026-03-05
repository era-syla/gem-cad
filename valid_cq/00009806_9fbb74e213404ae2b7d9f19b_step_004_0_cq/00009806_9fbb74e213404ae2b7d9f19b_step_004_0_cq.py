import cadquery as cq

# Parametric dimensions
# Large washer dimensions
large_washer_outer_diam = 40.0
large_washer_inner_diam = 15.0
large_washer_thickness = 3.0

# Small washer dimensions
small_washer_outer_diam = 10.0
small_washer_inner_diam = 3.0
small_washer_thickness = 3.0

# Positioning
# Position the small washer relative to the large one
# Based on the image, the small one is offset in X and Y
offset_x = 35.0
offset_y = 20.0
offset_z = 0.0 # They appear to be on the same plane

# Create the large washer
# Start a sketch on the XY plane
large_washer = (
    cq.Workplane("XY")
    .circle(large_washer_outer_diam / 2)
    .circle(large_washer_inner_diam / 2)
    .extrude(large_washer_thickness)
)

# Create the small washer
small_washer = (
    cq.Workplane("XY")
    .center(offset_x, offset_y) # Move the center for the new object
    .circle(small_washer_outer_diam / 2)
    .circle(small_washer_inner_diam / 2)
    .extrude(small_washer_thickness)
)

# Combine the two solids into a single result
result = large_washer.union(small_washer)