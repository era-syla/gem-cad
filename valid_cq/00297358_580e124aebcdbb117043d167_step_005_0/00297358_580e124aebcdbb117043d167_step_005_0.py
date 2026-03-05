import cadquery as cq

# -- Parameters --

# Top Rod (Rod 1) dimensions and position
rod1_diam = 10.0
rod1_len = 200.0
rod1_z = 15.0

# Middle Rod (Rod 2) dimensions and position
rod2_diam = 8.0
rod2_len = 180.0
rod2_z = 0.0  # Centered at Z=0

# Bottom Rod (Rod 3) dimensions and position
rod3_diam = 3.0
rod3_len = 80.0
rod3_z = -10.0
rod3_start_offset = 60.0  # Starting offset along the length (X-axis)

# -- Modeling --

# Create Rod 1: Extruded along X-axis, positioned high in Z
rod1 = (
    cq.Workplane("YZ")
    .center(0, rod1_z)
    .circle(rod1_diam / 2.0)
    .extrude(rod1_len)
)

# Create Rod 2: Extruded along X-axis, positioned in the middle
rod2 = (
    cq.Workplane("YZ")
    .center(0, rod2_z)
    .circle(rod2_diam / 2.0)
    .extrude(rod2_len)
)

# Create Rod 3: Extruded along X-axis, positioned low in Z, with X-offset
# We use .workplane(offset=...) to shift the sketch plane along the normal (X-axis)
rod3 = (
    cq.Workplane("YZ")
    .workplane(offset=rod3_start_offset)
    .center(0, rod3_z)
    .circle(rod3_diam / 2.0)
    .extrude(rod3_len)
)

# Combine all solids into the final result
result = rod1.union(rod2).union(rod3)