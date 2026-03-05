import cadquery as cq

# Parametric dimensions inferred from the image
shaft_length = 80.0       # Length of the cylindrical rod
shaft_diameter = 4.0      # Diameter of the rod
head_diameter = 10.0      # Diameter of the spherical end
head_thickness = 6.0      # Thickness of the flattened head (distance between flats)
hole_diameter = 4.0       # Diameter of the through-hole

# 1. Create the Shaft
# We align the shaft along the X-axis. 
# "YZ" plane is used to draw the circle, then extruded along X.
shaft = cq.Workplane("YZ").circle(shaft_diameter / 2.0).extrude(shaft_length)

# 2. Create the Head (Rod End)
# The head is positioned at the end of the shaft (X = shaft_length).
head_center = (shaft_length, 0, 0)

# Step A: Create the base sphere
head_sphere = cq.Workplane("XY", origin=head_center).sphere(head_diameter / 2.0)

# Step B: Create a slab to flatten the top and bottom of the sphere
# We create a large rectangle and extrude it to the desired head_thickness centered on Z=0.
# Intersecting this with the sphere leaves only the middle slice of the sphere.
slab = (
    cq.Workplane("XY", origin=head_center)
    .rect(head_diameter * 2.0, head_diameter * 2.0)
    .extrude(head_thickness / 2.0, both=True)
)

# Step C: Create the cutting tool for the hole
hole_cutter = (
    cq.Workplane("XY", origin=head_center)
    .circle(hole_diameter / 2.0)
    .extrude(head_diameter, both=True)
)

# Step D: Apply Boolean operations to form the final head shape
# Sphere INTERSECT Slab -> Flattened Sphere
# Flattened Sphere CUT Hole -> Final Head
head_final = head_sphere.intersect(slab).cut(hole_cutter)

# 3. Union the Shaft and the Head
result = shaft.union(head_final)