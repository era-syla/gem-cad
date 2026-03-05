import cadquery as cq

# Parameters
L, W, H = 80, 30, 20       # block dimensions: length, width, height
r_shallow, d_shallow = 15, 3  # shallow pocket radius and depth
R_sphere = 12                # spherical pocket radius

# 1. Create the rectangular block
block = cq.Workplane("XY").box(L, W, H)

# 2. Cut a shallow cylindrical pocket on the top face
block = block.faces(">Z").workplane().circle(r_shallow).cutBlind(-d_shallow)

# 3. Create a spherical cutter positioned so it cuts into the shallow pocket
#    Offset of sphere center from the block center in Z:
#    block top is at +H/2, shallow pocket is d_shallow deep, then sphere center sits R_sphere below that
z_offset = H/2 - d_shallow - R_sphere
sphere_cutter = cq.Workplane("XY").transformed(offset=(0, 0, z_offset)).sphere(R_sphere)

# 4. Subtract the sphere to form the deep spherical pocket
result = block.cut(sphere_cutter)