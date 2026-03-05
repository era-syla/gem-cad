import cadquery as cq

# Parametric dimensions
shaft_radius = 3.5
shaft_height = 40.0
sphere_radius = 9.0
sphere_offset = 6.5       # Distance from central axis to sphere center
base_radius = 7.0
base_thick_cyl = 3.0      # Thickness of the cylindrical part of the base before filleting
base_fillet_radius = 2.9  # Slightly less than thickness for a full round over

# 1. Create the vertical shaft
# Centered at origin, extruded upwards along Z
shaft = cq.Workplane("XY").circle(shaft_radius).extrude(shaft_height)

# 2. Create the top spheres
# Sphere 1: Offset to the right, centered at the top of the shaft
sphere_right = (
    cq.Workplane("XY")
    .workplane(offset=shaft_height)
    .center(sphere_offset, 0)
    .sphere(sphere_radius)
)

# Sphere 2: Offset to the left, centered at the top of the shaft
sphere_left = (
    cq.Workplane("XY")
    .workplane(offset=shaft_height)
    .center(-sphere_offset, 0)
    .sphere(sphere_radius)
)

# 3. Create the base
# Modeled as a cylinder situated below Z=0, joining the shaft bottom
base = (
    cq.Workplane("XY")
    .workplane(offset=-base_thick_cyl)
    .circle(base_radius)
    .extrude(base_thick_cyl)
)

# Round off the bottom of the base to create the button-head shape
# Select the bottom-most edges (<Z) and apply fillet
base = base.edges("<Z").fillet(base_fillet_radius)

# 4. Combine all parts into the final result
result = shaft.union(sphere_right).union(sphere_left).union(base)