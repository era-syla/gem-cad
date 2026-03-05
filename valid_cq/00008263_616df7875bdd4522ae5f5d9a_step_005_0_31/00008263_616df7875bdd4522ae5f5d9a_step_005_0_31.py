import cadquery as cq

# Parameters for the parametric model
D_base = 150.0       # Outer diameter of the base pentagon
D_top = 20.0         # Outer diameter of the top pentagon (used for lofting, will be cut away)
H_top = 35.0         # Height of the loft
thickness = -2.0     # Shell thickness (negative value for inward shelling)
D_hole = 42.0        # Diameter of the central circular hole
notch_l = 8.0        # Extension length of the notch from the hole edge
notch_w = 6.0        # Width of the notch
notch_angle = -126.0 # Orientation angle of the notch (points to the midpoint of the bottom-left face)

# 1. Create the base and top profiles for the truncated pyramid
# The base workplane is rotated by -90 degrees to ensure a flat horizontal top edge 
base_wp = cq.Workplane("XY").transformed(rotate=(0, 0, -90))
top_wp = base_wp.workplane(offset=H_top)

# Loft the solid pentagonal pyramid
pyramid = (
    base_wp.polygon(5, D_base)
    .add(top_wp.polygon(5, D_top))
    .loft()
)

# 2. Create a thin shell from the solid by removing the top and bottom faces
shelled = pyramid.faces("<Z or >Z").shell(thickness)

# 3. Prepare cutters for the central hole and the notch
# Start above the geometry to ensure a clean cut completely through the part
cut_wp = cq.Workplane("XY").workplane(offset=H_top + 10)

# Main circular hole cutter
hole_cutter = cut_wp.circle(D_hole / 2).extrude(-H_top * 3)

# Rectangular channel cutter for the notch
box_len = D_hole / 2 + notch_l
notch_box = (
    cq.Workplane("XY").transformed(rotate=(0, 0, notch_angle))
    .workplane(offset=H_top + 10)
    .center(box_len / 2, 0)
    .box(box_len, notch_w, H_top * 3)
)

# Cylindrical cutter for the rounded end of the notch
notch_cyl = (
    cq.Workplane("XY").transformed(rotate=(0, 0, notch_angle))
    .workplane(offset=H_top + 10)
    .center(D_hole / 2 + notch_l, 0)
    .circle(notch_w / 2)
    .extrude(-H_top * 3)
)

# 4. Perform the boolean cuts to finalize the geometry
result = (
    shelled
    .cut(hole_cutter)
    .cut(notch_box)
    .cut(notch_cyl)
)