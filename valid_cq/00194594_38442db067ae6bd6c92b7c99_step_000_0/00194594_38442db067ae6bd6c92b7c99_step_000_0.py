import cadquery as cq

# Parametric dimensions
width = 120.0             # Outer width of the square frame
total_height = 10.0       # Total height of the part
thickness = 2.5           # Thickness of the base plate and rim walls
center_hole_dia = 105.0   # Diameter of the large central cutout
mount_hole_dia = 4.5      # Diameter of the corner mounting holes
mount_hole_spacing = 105.0 # Center-to-center distance of mounting holes

# 1. Create the base plate
# Generate a solid box centered at the origin
result = cq.Workplane("XY").box(width, width, thickness)

# 2. Add the perimeter rim
# Select the top face of the base plate
# Sketch two rectangles: the outer boundary and the inner wall boundary
# Extrude the difference upwards to create the rim
result = (result.faces(">Z").workplane()
          .rect(width, width)                                         # Outer edge
          .rect(width - 2*thickness, width - 2*thickness)             # Inner edge
          .extrude(total_height - thickness))

# 3. Create the central cutout
# Select the face and cut the large circle through the geometry
result = (result.faces(">Z").workplane()
          .circle(center_hole_dia / 2.0)
          .cutThruAll())

# 4. Create mounting holes
# Use a construction rectangle to place points at the four corners
# Cut small circles at these points
result = (result.faces(">Z").workplane()
          .rect(mount_hole_spacing, mount_hole_spacing, forConstruction=True)
          .vertices()
          .circle(mount_hole_dia / 2.0)
          .cutThruAll())