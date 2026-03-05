import cadquery as cq

# Parameters for dimensions
od = 50.0          # Outer Diameter
id_val = 38.0      # Inner Diameter
thickness = 1.5    # Thickness of the washer

# Feature Dimensions
tab_inner_w = 8.0  # Width of the flat inner tab
tab_inner_l = 5.0  # Length of the flat inner tab
tab_outer_w = 6.0  # Base width of the outer triangular tab
tab_outer_l = 4.0  # Height of the outer triangular tab
tab_bent_w = 10.0  # Width of the bent tab
tab_bent_l = 9.0   # Length of the bent tab
bend_angle = 35.0  # Angle of the bend in degrees
overlap = 1.0      # Material overlap to ensure solid union

# 1. Base Ring
# Create the main circular body
base_ring = cq.Workplane("XY").circle(od / 2.0).circle(id_val / 2.0).extrude(thickness)

# 2. Inner Flat Tab (Bottom-Left)
# Located approx 220 degrees. Rectangular, extends inwards.
angle_inner = 220.0
r_inner = (id_val / 2.0) - (tab_inner_l / 2.0) + overlap

inner_tab = (
    cq.Workplane("XY")
    .polarArray(r_inner, angle_inner, 360, 1)
    .rect(tab_inner_l, tab_inner_w) # X is radial, Y is tangential
    .extrude(thickness)
)

# 3. Outer Flat Tab (Bottom-Right)
# Located approx 320 degrees. Triangular, extends outwards.
angle_outer = 320.0
r_outer_start = (od / 2.0) - overlap

outer_tab = (
    cq.Workplane("XY")
    .transformed(rotate=cq.Vector(0, 0, angle_outer))
    .center(r_outer_start, 0)
    .polyline([(0, tab_outer_w / 2.0), (tab_outer_l, 0), (0, -tab_outer_w / 2.0)])
    .close()
    .extrude(thickness)
)

# 4. Bent Tab (Top-Left)
# Located approx 130 degrees. Extends inwards and bends up.
angle_bent = 130.0

bent_tab = (
    cq.Workplane("XY")
    # Rotate workplane to the tab's angular position
    .transformed(rotate=cq.Vector(0, 0, angle_bent))
    # Move origin to the inner diameter (the hinge point)
    .center(id_val / 2.0, 0)
    # Rotate the plane around the local tangent (Y-axis) to create the bend
    # Negative angle lifts the inward-pointing vector (-X) upwards
    .transformed(rotate=cq.Vector(0, -bend_angle, 0))
    # Position the rectangle. 
    # It extends from the hinge (0) inwards (-X).
    # We shift center by -length/2 + overlap to position it correctly relative to hinge.
    .center(-tab_bent_l / 2.0 + overlap, 0)
    .rect(tab_bent_l, tab_bent_w)
    .extrude(thickness)
)

# Combine all components into the final result
result = base_ring.union(inner_tab).union(outer_tab).union(bent_tab)