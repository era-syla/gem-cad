import cadquery as cq

# Dimensions
shaft_diameter = 6
shaft_length = 80
collar_outer_diameter = 10
collar_inner_diameter = 7
collar_length = 12
small_tab_size = 2

# Create the main shaft (solid cylinder)
shaft = (
    cq.Workplane("XY")
    .cylinder(shaft_length, shaft_diameter / 2)
)

# Create the collar (hollow cylinder) at the top of the shaft
collar = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length / 2 - collar_length / 2)
    .circle(collar_outer_diameter / 2)
    .circle(collar_inner_diameter / 2)
    .extrude(collar_length)
)

# Create a small tab/notch on the side of the collar
tab = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length / 2 - collar_length / 2)
    .center(collar_outer_diameter / 2, 0)
    .rect(small_tab_size, small_tab_size)
    .extrude(small_tab_size)
)

# Combine shaft and collar
result = shaft.union(collar).union(tab)