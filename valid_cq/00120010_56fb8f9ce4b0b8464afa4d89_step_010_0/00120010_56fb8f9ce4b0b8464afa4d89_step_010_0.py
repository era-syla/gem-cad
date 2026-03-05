import cadquery as cq

# Parametric dimensions based on visual estimation
head_radius = 13.0    # Radius of the larger spherical end
body_radius = 10.0    # Radius of the cylindrical body and tail cap
cyl_length = 30.0     # Length of the cylindrical section (center to end center)

# 1. Create the larger spherical head
# We center this at the origin
head = cq.Workplane("XY").sphere(head_radius)

# 2. Create the cylindrical body
# Drawn on the YZ plane (x=0) and extruded along the positive X axis
# This cylinder starts inside the head sphere and extends outwards
body = cq.Workplane("YZ").circle(body_radius).extrude(cyl_length)

# 3. Create the rounded tail cap
# This is a sphere positioned at the end of the cylinder
# It creates a hemispherical cap that merges tangentially with the cylinder
tail = cq.Workplane("YZ").workplane(offset=cyl_length).sphere(body_radius)

# Combine all parts using boolean union
# The union handles the intersection between the larger head and the cylinder,
# creating the "neck" transition seen in the image.
result = head.union(body).union(tail)