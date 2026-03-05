import cadquery as cq

# Parameters
base_width = 100.0
base_height = 40.0
base_thickness = 10.0

block_width = 40.0
block_height = 20.0
block_thickness = 20.0

hole_width = 10.0
hole_height = 20.0
hole_dist = 35.0

pin_radius = 3.0
pin_height = 10.0
pin_dist = 10.0

# Create the base plate
base = cq.Workplane("XY").box(base_width, base_height, base_thickness)

# Add rectangular holes to the base plate
base = (base
        .faces(">Z").workplane()
        .pushPoints([(hole_dist, 0), (-hole_dist, 0)])
        .rect(hole_width, hole_height)
        .cutThruAll()
        )

# Add the block on top of the base plate
block = (cq.Workplane("XY")
         .workplane(offset=base_thickness/2)
         .box(block_width, block_height, block_thickness, centered=(True, False, False))
         )

result = base.union(block)

# Add pins on top of the block
result = (result
          .faces(">Z").workplane(centerOption="CenterOfBoundBox")
          .pushPoints([(pin_dist, 0), (-pin_dist, 0)])
          .circle(pin_radius)
          .extrude(pin_height)
          )