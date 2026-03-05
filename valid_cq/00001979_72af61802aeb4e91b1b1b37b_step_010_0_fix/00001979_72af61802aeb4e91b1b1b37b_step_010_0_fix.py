import cadquery as cq

# Parameters
r_small = 6    # radius of small end
r_big = 20     # radius of big end
thk = 5        # thickness of part
handle_len = 50  # length of the straight handle between circle tangents
hole_dia = 4   # diameter of hole in small end

# Create small end cylinder and cut hole
small = (
    cq.Workplane("XY")
    .circle(r_small)
    .extrude(thk)
    .faces(">Z")
    .workplane()
    .hole(hole_dia)
)

# Create big end cylinder
big_center_x = r_small + handle_len + r_big
big = (
    cq.Workplane("XY")
    .center(big_center_x, 0)
    .circle(r_big)
    .extrude(thk)
)

# Create rectangular handle between the two circles
rect_center_x = r_small + handle_len/2
rect = (
    cq.Workplane("XY")
    .center(rect_center_x, 0)
    .rect(handle_len, 2*r_small)
    .extrude(thk)
)

# Union all features
result = small.union(rect).union(big)