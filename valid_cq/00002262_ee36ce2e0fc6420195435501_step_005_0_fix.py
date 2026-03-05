import cadquery as cq

# Parameters
disk_radius = 50
disk_thickness = 3
hub_outer_radius = 12
hub_inner_radius = 7
hub_height = 10
flange_radius = 16
flange_height = 2

# Create the main flat disk
disk = (
    cq.Workplane("XY")
    .circle(disk_radius)
    .extrude(disk_thickness)
)

# Add a fillet to the top edge of the disk
disk = (
    disk
    .faces(">Z")
    .edges()
    .chamfer(0.5)
)

# Create the flange (wider base of hub)
flange = (
    cq.Workplane("XY")
    .workplane(offset=disk_thickness)
    .circle(flange_radius)
    .extrude(flange_height)
)

# Create the hub cylinder
hub = (
    cq.Workplane("XY")
    .workplane(offset=disk_thickness + flange_height)
    .circle(hub_outer_radius)
    .extrude(hub_height - flange_height)
)

# Combine disk, flange, and hub
result = disk.union(flange).union(hub)

# Create the center hole through everything
result = (
    result
    .faces(">Z")
    .workplane()
    .circle(hub_inner_radius)
    .cutThruAll()
)

# Add a small groove/ring detail on the hub (the visible ring line)
groove_depth = 0.5
groove_z = disk_thickness + flange_height + 1

groove = (
    cq.Workplane("XY")
    .workplane(offset=groove_z)
    .circle(hub_outer_radius + 0.1)
    .circle(hub_outer_radius - groove_depth)
    .extrude(1.0)
)

result = result.cut(groove)