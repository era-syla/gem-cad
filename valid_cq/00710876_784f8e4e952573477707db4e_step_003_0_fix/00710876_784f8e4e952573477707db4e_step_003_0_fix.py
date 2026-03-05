import cadquery as cq

# Base plate with prongs profile
profile = cq.Workplane("XY").polyline([
    (-40, -30), (20, -30), (20, -20),
    (60, -20), (60, 20), (20, 20),
    (20, 30), (-40, 30), (-40, -30)
]).close().extrude(5)

# Fillet all vertical edges
result = profile.edges("|Z").fillet(2)

# Drill mounting holes in base plate corners
mount_pts = [(-35, -25), (35, -25), (35, 25), (-35, 25)]
result = result.faces(">Z").workplane().pushPoints(mount_pts).hole(5)

# Drill hinge holes in prongs
hinge_pts = [(40, 25), (40, -25)]
result = result.faces(">Z").workplane().pushPoints(hinge_pts).hole(6)

# Add cam body (half cylinder) on top of plate
cam = (
    cq.Workplane("XY")
    .workplane(offset=5)
    .center(0, 0)
    .circle(20)
    .extrude(10)
    # Cut the back half to make a flat face
    .faces(">Z").workplane()
    .transformed(offset=(0, 0, 5), rotate=(0, 90, 0))
    .rect(40, 40, forConstruction=True)
    .split(keepTop=True)
)

result = result.union(cam)

# Cut slot in cam body
slot = (
    cq.Workplane("XY")
    .workplane(offset=5 + 5)  # mid-height of cam
    .center(0, 0)
    .box(30, 10, 5)
)

result = result.cut(slot)