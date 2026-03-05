import cadquery as cq

# Parameters
L = 60               # distance between the centers of the end discs
R = 10               # radius of the end discs
width = 2 * R        # overall width of the link
thickness = 5        # thickness in Z
bar_thickness = 3    # thickness of the rails
R_inner = R - bar_thickness
slot_width = width - 2 * bar_thickness

# Build the outer shape: central bar + two end cylinders
outer_bar = cq.Workplane('XY').box(L, width, thickness)
outer_cyl1 = cq.Workplane('XY').transformed(offset=( L/2, 0, 0)).circle(R).extrude(thickness)
outer_cyl2 = cq.Workplane('XY').transformed(offset=(-L/2, 0, 0)).circle(R).extrude(thickness)
outer = outer_bar.union(outer_cyl1).union(outer_cyl2)

# Build the cutter: smaller bar + smaller end cylinders
# Extrude cutter slightly more than thickness to ensure a through cut
cut_bar = cq.Workplane('XY').box(L, slot_width, thickness + 2)
cut_cyl1 = cq.Workplane('XY').transformed(offset=( L/2, 0, 0)).circle(R_inner).extrude(thickness + 2)
cut_cyl2 = cq.Workplane('XY').transformed(offset=(-L/2, 0, 0)).circle(R_inner).extrude(thickness + 2)
cut_shape = cut_bar.union(cut_cyl1).union(cut_cyl2)

# Subtract the slot from the outer shape
result = outer.cut(cut_shape)