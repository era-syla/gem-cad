import cadquery as cq

# -- Parametric Dimensions --
sphere_radius = 30.0
neck_radius = 10.0
neck_height = 25.0       # Length of neck extending above the sphere
rim_tube_radius = 2.5    # Radius of the torus tube forming the lip
stopper_radius = 9.8     # Radius of the stopper cap
stopper_height = 2.5     # Thickness of the visible stopper cap

# -- Geometry Construction --

# 1. Main Body: Sphere
# Centered at the origin
body = cq.Workplane("XY").sphere(sphere_radius)

# 2. Neck: Cylinder
# Positioned to start slightly inside the sphere to ensure a robust boolean union.
# Top of sphere is at z = sphere_radius.
neck_overlap = 5.0
z_neck_start = sphere_radius - neck_overlap
z_neck_top = sphere_radius + neck_height

neck = (
    cq.Workplane("XY")
    .workplane(offset=z_neck_start)
    .circle(neck_radius)
    .extrude(z_neck_top - z_neck_start)
)

# 3. Rim: Revolved Torus
# Modeled by revolving a circular profile around the Z axis.
# Positioned at the top of the neck.
rim = (
    cq.Workplane("XZ")
    .moveTo(neck_radius, z_neck_top - rim_tube_radius)
    .circle(rim_tube_radius)
    .revolve()
)

# 4. Stopper: Cylinder
# Sits at the top, effectively capping the flask.
stopper = (
    cq.Workplane("XY")
    .workplane(offset=z_neck_top - rim_tube_radius)
    .circle(stopper_radius)
    .extrude(stopper_height + rim_tube_radius * 0.5)
)

# -- Assembly and Finishing --

# Union the body and neck first to create a single solid for filleting
result = body.union(neck)

# Fillet the transition between the spherical body and the cylindrical neck.
# We identify the edge near the geometric intersection of the sphere and cylinder.
intersection_z = (sphere_radius**2 - neck_radius**2)**0.5
result = result.edges(cq.NearestToPointSelector((neck_radius, 0, intersection_z))).fillet(4.0)

# Add the rim and the stopper to the final geometry
result = result.union(rim).union(stopper)