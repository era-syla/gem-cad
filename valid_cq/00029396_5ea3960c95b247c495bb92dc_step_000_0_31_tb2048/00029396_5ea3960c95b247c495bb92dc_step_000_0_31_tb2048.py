import cadquery as cq

# Parameters
d_shaft = 12
l_shaft = 25

d_flange = 36
w_flange = 22
t_flange = 5

d_neck = 10
l_neck = 3

d_sphere = 26
overlap = 2
sphere_center_x = t_flange + l_neck + (d_sphere / 2) - overlap
flat_cut_depth = 4.5

# Create Shaft
shaft = cq.Workplane("YZ").circle(d_shaft / 2).extrude(-l_shaft)

# Create Flange with two parallel flats
flange_sketch = (
    cq.Sketch()
    .circle(d_flange / 2)
    .rect(w_flange, d_flange * 2, mode='i')
)
flange = cq.Workplane("YZ").placeSketch(flange_sketch).extrude(t_flange)

# Create Neck
neck = cq.Workplane("YZ").workplane(offset=t_flange).circle(d_neck / 2).extrude(l_neck)

# Create Sphere
sphere = cq.Workplane("YZ").workplane(offset=sphere_center_x).sphere(d_sphere / 2)

# Combine all bodies
result = shaft.union(flange).union(neck).union(sphere)

# Create a cutting box to truncate the sphere (flat face on the right)
cut_x = sphere_center_x + (d_sphere / 2) - flat_cut_depth
cut_box = cq.Workplane("YZ").workplane(offset=cut_x).rect(d_sphere * 2, d_sphere * 2).extrude(d_sphere)

# Perform the cut
result = result.cut(cut_box)