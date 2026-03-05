import cadquery as cq

# Parametric dimensions
length = 100.0
width = 40.0
height = 15.0

# Top features
center_dimple_diameter = 25.0
center_dimple_depth = 5.0  # Depth of the spherical cut
side_dimple_diameter = 15.0
side_dimple_depth = 3.0
side_dimple_spacing = 30.0  # Distance from center to side dimples

# Side features
side_hole_diameter = 6.0
side_hole_spacing = 30.0  # Distance from center to side holes
side_hole_depth = 10.0 # Depth of blind holes on the side

# Create the main block
base = cq.Workplane("XY").box(length, width, height)

# Create the top dimples (spherical cuts)
# We use a sphere to cut the dimple. To get the correct diameter at the surface,
# we need to calculate the sphere radius and vertical offset.
# For a spherical cap of radius 'a' (dimple radius) and height 'h' (depth):
# The radius of the sphere R is given by R = (a^2 + h^2) / (2h)
# We position the sphere center so that the bottom of the sphere is at (surface_z - h).
# Or simpler: center the sphere at z = surface_z - R + h.

def create_dimple(workplane, diameter, depth):
    radius = diameter / 2.0
    sphere_radius = (radius**2 + depth**2) / (2 * depth)
    z_offset = height / 2.0 - sphere_radius + depth
    
    # Create a sphere and cut it from the workplane
    # We need to position the sphere correctly relative to the current workplane location
    return workplane.cut(
        cq.Workplane("XY")
        .workplane(offset=z_offset)
        .sphere(sphere_radius)
    )

# Apply center dimple
result = base
# We need to manually locate the spheres because standard cut operations work relative to local origins
# Calculation for center dimple geometry
r_center = center_dimple_diameter / 2.0
R_center = (r_center**2 + center_dimple_depth**2) / (2 * center_dimple_depth)
z_center = height/2.0 + center_dimple_depth - R_center

# Calculation for side dimple geometry
r_side = side_dimple_diameter / 2.0
R_side = (r_side**2 + side_dimple_depth**2) / (2 * side_dimple_depth)
z_side = height/2.0 + side_dimple_depth - R_side

# Cut center dimple
result = result.cut(
    cq.Workplane("XY").center(0, 0).workplane(offset=z_center).sphere(R_center)
)

# Cut side dimples
result = result.cut(
    cq.Workplane("XY").center(-side_dimple_spacing, 0).workplane(offset=z_side).sphere(R_side)
)
result = result.cut(
    cq.Workplane("XY").center(side_dimple_spacing, 0).workplane(offset=z_side).sphere(R_side)
)

# Create side holes (blind holes)
# Select the front face (assuming Y is width, so Y-min face is "front")
# Or simpler: standard Workplane transformation
result = result.faces(">Y").workplane().center(0, 0) \
    .pushPoints([(-side_hole_spacing, 0), (side_hole_spacing, 0)]) \
    .hole(side_hole_diameter, side_hole_depth)

# Alternatively, if the image implies through holes or deeper cuts, adjust side_hole_depth.
# Based on the shading inside the side holes, they look like blind holes.