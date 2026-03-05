import cadquery as cq

# Parameters
length = 100
width = 10
height = 5
arm_offset = 30
arm_radius = 15
hole_radius = 3
peg_height = 10
peg_width = 5

# Create the main body
result = cq.Workplane("YZ").box(length, width, height)

# Create the circle arm
arm = cq.Workplane("YZ").center(arm_offset, 0).circle(arm_radius).extrude(width)

# Create the hole in the arm
arm = arm.faces(">X").workplane().hole(hole_radius * 2)

# Add the circle arm to the body
result = result.union(arm)

# Create the pegs
peg = cq.Workplane("YZ").center(-length/2 + peg_height/2, 0).box(peg_height, peg_width, peg_width)
peg = peg.union(peg.mirror(mirrorPlane="XY"))

# Add the pegs to the body
result = result.union(peg)