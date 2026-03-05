import cadquery as cq

# Parametric dimensions
radius = 25.0
cylinder_height = 60.0

# Create the cylindrical base extruded along the Z axis
cylinder = cq.Workplane("XY").circle(radius).extrude(cylinder_height)

# Create the spherical dome centered at the top of the cylinder
dome = cq.Workplane("XY").workplane(offset=cylinder_height).sphere(radius)

# Combine the shapes into the final geometry
result = cylinder.union(dome)