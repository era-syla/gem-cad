import cadquery as cq

# Parametric dimensions
base_r = 16.0
base_h = 6.0

sphere_r = 17.0
barrel_r = 16.6
barrel_h = 16.0
cap_r = 17.0
cap_h = 8.0

nub_r = 2.5
nub_extrude = 3.0
rod_r = 1.0
rod_extrude = 150.0

# Create the base
base = cq.Workplane("XY").circle(base_r).extrude(base_h).edges(">Z").chamfer(1)

# Create the camera head components
sphere = cq.Workplane("XY").sphere(sphere_r)
barrel = cq.Workplane("XY").circle(barrel_r).extrude(barrel_h)

cap = cq.Workplane("XY").workplane(offset=barrel_h).circle(cap_r).extrude(cap_h)
cap = cap.edges(">Z").chamfer(1)
cap = cap.faces(">Z").workplane().circle(14).cutBlind(-1.5)

# Assemble and position the camera head
head = sphere.union(barrel).union(cap)
head = head.rotate((0, 0, 0), (0, 1, 0), -55)
head = head.translate((0, 0, base_h + sphere_r - 5))

# Create the side nub and rod
nub = cq.Workplane("YZ").workplane(offset=base_r).center(0, base_h / 2).circle(nub_r).extrude(nub_extrude)
rod = cq.Workplane("YZ").workplane(offset=base_r + nub_extrude).center(0, base_h / 2).circle(rod_r).extrude(rod_extrude)

# Combine all parts into the final result
result = base.union(nub).union(rod).union(head)