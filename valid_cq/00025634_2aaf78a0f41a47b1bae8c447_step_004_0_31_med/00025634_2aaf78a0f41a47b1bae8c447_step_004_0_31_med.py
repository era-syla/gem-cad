import cadquery as cq

# Parameters for standard 2020 T-slot extrusion
L = 400.0       # Extrusion length
W = 20.0        # Width/Height of the profile
w1 = 3.1        # Half-width of the outer slot opening (6.2mm total)
w2 = 5.75       # Half-width of the inner slot cavity (11.5mm total)
d1 = 1.8        # Depth of the outer slot opening
d2 = 6.0        # Total depth of the slot cavity
center_r = 2.1  # Radius of the center hole (4.2mm total for M5 tap)
corner_r = 1.5  # Fillet radius for the outer corners

# 1. Create the solid square base
result = cq.Workplane("XY").rect(W, W).extrude(L)

# 2. Fillet the outer edges (parallel to Z)
result = result.edges("|Z").fillet(corner_r)

# 3. Create the center hole
result = result.faces(">Z").workplane().circle(center_r).cutThruAll()

# 4. Define a single T-slot cutter shape on the top edge
cutter_wp = (
    cq.Workplane("XY")
    .moveTo(w1, W/2 + 1.0)
    .lineTo(w1, W/2 - d1)
    .lineTo(w2, W/2 - d1 - 1.0)
    .lineTo(w2, W/2 - d2)
    .lineTo(-w2, W/2 - d2)
    .lineTo(-w2, W/2 - d1 - 1.0)
    .lineTo(-w1, W/2 - d1)
    .lineTo(-w1, W/2 + 1.0)
    .close()
    .extrude(L)
)

# Extract the solid cutter and create rotated copies for the other sides
c_top = cutter_wp.val()
c_right = c_top.rotate((0, 0, 0), (0, 0, 1), 90)
c_bottom = c_top.rotate((0, 0, 0), (0, 0, 1), 180)
c_left = c_top.rotate((0, 0, 0), (0, 0, 1), 270)

# 5. Perform the boolean cuts for all 4 slots
result = (
    result
    .cut(c_top)
    .cut(c_right)
    .cut(c_bottom)
    .cut(c_left)
)