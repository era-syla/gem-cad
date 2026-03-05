import cadquery as cq

# Parameters for the block
plate_size = 60
plate_thk = 5
wall_th = 3
wall_h = 30
hole_dia = 20

# Create top plate
plate = cq.Workplane("XY").box(plate_size, plate_size, plate_thk)

# Create side walls
wp = cq.Workplane("XY").workplane(offset=plate_thk)
w1 = wp.center(0,  plate_size/2 - wall_th/2).rect(plate_size, wall_th).extrude(wall_h)
w2 = wp.center(0, -plate_size/2 + wall_th/2).rect(plate_size, wall_th).extrude(wall_h)
w3 = wp.center( plate_size/2 - wall_th/2, 0).rect(wall_th, plate_size - 2*wall_th).extrude(wall_h)
w4 = wp.center(-plate_size/2 + wall_th/2, 0).rect(wall_th, plate_size - 2*wall_th).extrude(wall_h)

block = plate.union(w1).union(w2).union(w3).union(w4)

# Cut central hole through the top plate
block = block.faces(">Z").workplane().hole(hole_dia)

# Create an elbow-shaped tube
# Define an arc path in the XZ plane
path = (
    cq.Workplane("XZ")
      .moveTo(0, 0)
      .threePointArc((20, 20), (40, 0))
      .wire()
)

# Sweep a circle along the path to make the tube
tube_profile = cq.Workplane("XY").circle(10)
tube = tube_profile.sweep(path, isFrenet=True)

# Position the tube next to the block
tube = tube.translate((80, 0, 0))

# Combine both parts into the final result
result = block.union(tube)