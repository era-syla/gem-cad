import cadquery as cq

# Parameters
base_length = 80
base_width = 80
base_thickness = 3
mount_length = 80
mount_width = 20
mount_thickness = 10
hole_diameter = 5
circular_cutout_diameter = 60
fillet_radius = 3

# Base
base = (cq.Workplane("XY")
        .box(base_length, base_width, base_thickness))

# Mount
mount = (cq.Workplane("XY")
         .workplane(offset=base_thickness)
         .box(mount_length, mount_width, mount_thickness))

# Combine base and mount
result = base.union(mount)

# Circular cutout
result = (result.faces("<Z")
          .workplane()
          .center(0, 0)
          .circle(circular_cutout_diameter / 2)
          .cutThruAll())

# Holes in the mount
result = (result.faces(">Z").workplane()
          .pushPoints([(-30, 0), (30, 0)])
          .circle(hole_diameter / 2)
          .cutThruAll())

# Fillet the corners of the base
result = result.edges("|Z and (>Y or <Y)").fillet(fillet_radius)