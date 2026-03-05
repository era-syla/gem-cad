import cadquery as cq

# Parametric dimensions
shaft_rad = 5.0
shaft_len = 20.0

flange_rad = 15.0
flange_thick = 4.0
flange_flat_dist = 20.0

neck_rad = 4.5
neck_len = 2.0

sphere_rad = 12.0
sphere_embed = 3.5
sphere_cut_dist = 7.5

# 1. Base Shaft
result = cq.Workplane("XY").circle(shaft_rad).extrude(shaft_len)

# 2. Flange with parallel flat sides
result = (result.faces(">Z").workplane()
    .sketch()
    .circle(flange_rad)
    .rect(flange_rad * 3, flange_flat_dist, mode='i')
    .finalize()
    .extrude(flange_thick)
)

# 3. Neck connecting to the sphere
result = (result.faces(">Z").workplane()
    .circle(neck_rad)
    .extrude(neck_len)
)

# 4. Spherical knob
z_sphere = shaft_len + flange_thick + neck_len + sphere_rad - sphere_embed
head = cq.Workplane("XY").workplane(offset=z_sphere).sphere(sphere_rad)
result = result.union(head)

# 5. Flat face cut on the front of the sphere
z_cut = z_sphere + sphere_cut_dist
cutter = (cq.Workplane("XY").workplane(offset=z_cut)
    .rect(sphere_rad * 3, sphere_rad * 3)
    .extrude(sphere_rad * 2)
)
result = result.cut(cutter)