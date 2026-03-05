import cadquery as cq

# Parameters
width = 20.0           # outer diameter of end cylinders
thickness = 6.0        # thickness of the part (Z height)
center_dist = 60.0     # distance between the centers of the end cylinders
radius = width / 2.0
cut_depth = radius     # depth of the jaw cut into each end

# Build the main bar
bar = cq.Workplane("XY").rect(center_dist, width).extrude(thickness)

# Build the end cylinders
end1 = cq.Workplane("XY").circle(radius).extrude(thickness).translate(( center_dist/2, 0, 0))
end2 = cq.Workplane("XY").circle(radius).extrude(thickness).translate((-center_dist/2, 0, 0))

# Fuse bar and ends
result = bar.union(end1).union(end2)

# Create a cutting box for the jaws
# We offset the workplane to mid-thickness so box spans fully in Z
cut_box = (
    cq.Workplane("XY")
    .workplane(offset=thickness/2)
    .box(cut_depth, width * 2.0, thickness + 2.0)
)

# Position cutting boxes at each end and subtract
cut1 = cut_box.translate(( center_dist/2 - cut_depth/2, 0, 0))
cut2 = cut_box.translate((-center_dist/2 + cut_depth/2, 0, 0))
result = result.cut(cut1).cut(cut2)