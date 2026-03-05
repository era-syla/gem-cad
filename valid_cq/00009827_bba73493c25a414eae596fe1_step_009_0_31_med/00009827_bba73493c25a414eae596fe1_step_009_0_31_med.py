import cadquery as cq

# Parameters
L = 100.0             # Overall length
W = 30.0              # Overall width
T = 4.0               # Thickness

chamfer_size = 5.0    # Corner chamfer size

notch_len = 15.0      # Length of the side cutouts
notch_depth = 5.0     # Depth of the side cutouts
notch_center_x = 22.5 # X position of the notch centers
notch_center_y = W / 2 # Y position of the notch centers

hole_dist = 20.0      # Distance between the two holes
hole_dia = 6.0        # Diameter of the holes

# Create the base plate and chamfer the 4 outer vertical corners
result = (
    cq.Workplane("XY")
    .box(L, W, T)
    .edges("|Z")
    .chamfer(chamfer_size)
)

# Create the tool bodies for the rectangular side notches
notches = (
    cq.Workplane("XY")
    .pushPoints([
        (notch_center_x, notch_center_y),
        (notch_center_x, -notch_center_y),
        (-notch_center_x, notch_center_y),
        (-notch_center_x, -notch_center_y)
    ])
    .box(notch_len, notch_depth * 2, T * 2)
)

# Subtract the notches from the base plate
result = result.cut(notches)

# Add the two central holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([
        (-hole_dist / 2, 0),
        (hole_dist / 2, 0)
    ])
    .hole(hole_dia)
)