import cadquery as cq

plate_thk = 5
plate_length = 120
plate_width = 80
inner_len = 100
inner_wid = 60
side_plate_height = 50

# Top plate with central cutout and mounting holes
top = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thk)
    .faces(">Z")
    .workplane()
    .rect(inner_len, inner_wid)
    .cutThruAll()
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .center(0, plate_width / 2 - 10)
    .rarray(3, 1, 30, 1)
    .hole(5)
)

# Front side plate with hole pattern
front = (
    cq.Workplane("YZ", origin=(plate_length/2, 0, 0))
    .rect(plate_width, side_plate_height)
    .extrude(plate_thk)
    .faces(">X")
    .workplane(centerOption="CenterOfMass")
    .rarray(4, 2, 20, 20)
    .hole(5)
)

# Back side plate (blank)
back = (
    cq.Workplane("YZ", origin=(-plate_length/2, 0, 0))
    .rect(plate_width, side_plate_height)
    .extrude(plate_thk)
)

# Gusset profile parameters
gx = -plate_length/2 + 5
d = 30
gusset_pts = [(0, 0), (0, side_plate_height), (d, side_plate_height)]

# Left gusset (extruded toward negative Y)
gusset1 = (
    cq.Workplane("XZ", origin=(gx, 0, 0))
    .polyline(gusset_pts)
    .close()
    .extrude(-plate_thk)
    .translate((0, plate_width/2 - plate_thk/2, 0))
)

# Right gusset (extruded toward positive Y)
gusset2 = (
    cq.Workplane("XZ", origin=(gx, 0, 0))
    .polyline(gusset_pts)
    .close()
    .extrude(plate_thk)
    .translate((0, -plate_width/2 + plate_thk/2, 0))
)

result = top.union(front).union(back).union(gusset1).union(gusset2)