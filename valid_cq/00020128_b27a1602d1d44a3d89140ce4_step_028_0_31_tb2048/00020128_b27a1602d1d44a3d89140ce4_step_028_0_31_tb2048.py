import cadquery as cq

# Parameters
H = 120.0
R_out = 20.0
R_in = 18.0
Flange_R = 25.0
Lip_R = 24.0

# Main cylindrical body
body = cq.Workplane("XY").circle(R_out).circle(R_in).extrude(H)

# Middle flange
flange = cq.Workplane("XY").workplane(offset=25).circle(Flange_R).circle(R_in).extrude(2)
body = body.union(flange)

# Bottom lip
bottom_lip = cq.Workplane("XY").circle(Lip_R).circle(R_in).extrude(2)
body = body.union(bottom_lip)

# Bottom cutouts
bottom_cut = cq.Workplane("XZ").center(0, 5).box(16, 20, 60)
body = body.cut(bottom_cut)

# Large side cutouts with filleted corners
cut_box = cq.Workplane("XZ").center(0, 72.5).box(26, 85, 60).edges("|Y").fillet(4)
body = body.cut(cut_box)

# Top flat bridge
bridge = cq.Workplane("XY").workplane(offset=118).rect(40, 12).extrude(2)
body = body.union(bridge)

# Top side tabs
tabs = cq.Workplane("XY").workplane(offset=114).rect(44, 8).extrude(4)
body = body.union(tabs)

# Top groove along the bridge
groove = cq.Workplane("XY").workplane(offset=118).rect(40, 2).extrude(5)
body = body.cut(groove)

# Optional: Add small grooves to the bottom lip to match the image details
lip_grooves = cq.Workplane("XY").center(0, 0).rect(6, 60).extrude(2)
body = body.cut(lip_grooves)

result = body