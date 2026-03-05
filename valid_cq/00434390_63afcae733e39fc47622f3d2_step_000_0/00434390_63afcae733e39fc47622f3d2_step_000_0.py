import cadquery as cq

# Parametric dimensions for the large disk (top right)
large_od = 50.0       # Outer Diameter
large_id = 10.0       # Inner Diameter (Hole)
large_thickness = 10.0

# Parametric dimensions for the small disk (bottom left)
small_od = 22.0
small_id = 7.0
small_thickness = 7.0

# Position offset for the small disk relative to the large one
offset_x = -50.0
offset_y = -40.0

# Create the large washer/disk
# Centered at (0,0) on the XY plane
large_disk = (
    cq.Workplane("XY")
    .circle(large_od / 2.0)
    .circle(large_id / 2.0)
    .extrude(large_thickness)
)

# Create the small washer/disk
# Positioned using the offset values
small_disk = (
    cq.Workplane("XY")
    .center(offset_x, offset_y)
    .circle(small_od / 2.0)
    .circle(small_id / 2.0)
    .extrude(small_thickness)
)

# Combine both solids into a single result object
result = large_disk.union(small_disk)