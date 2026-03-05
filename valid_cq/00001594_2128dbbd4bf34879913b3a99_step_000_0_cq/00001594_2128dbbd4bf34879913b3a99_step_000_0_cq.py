import cadquery as cq

# Define parametric dimensions
diameter = 50.0       # Diameter of the base
radius = diameter / 2.0
base_height = 2.0     # Height of the cylindrical base part
dome_height = 15.0    # Height of the domed section

# Create the base cylinder
base = cq.Workplane("XY").circle(radius).extrude(base_height)

# Create the dome (half-sphere or spherical cap)
# We can create a sphere and cut it, or revolve a profile.
# A revolution is robust. We need an arc.
# The arc starts at (radius, base_height) and goes to (0, base_height + dome_height).
# However, looking at the image, it looks like a standard hemisphere on a cylinder, 
# or a shallower spherical cap. Let's assume a spherical cap on top of the cylinder.

# Using a sphere and intersecting it is a clean way to get a dome, but positioning is key.
# Alternatively, a revolution of an arc.

# Let's model it as a cylinder + a sphere on top, carefully placed.
# Or simply a revolution of a profile that includes the straight edge and the curve.

# Method: Revolve a profile
# Points for profile: (0,0) -> (radius, 0) -> (radius, base_height) -> arc -> (0, total_height) -> close
total_height = base_height + dome_height

# Calculate radius of curvature for the dome if it's a spherical cap
# R^2 = (R-h)^2 + r^2  => R^2 = R^2 - 2Rh + h^2 + r^2 => 2Rh = h^2 + r^2 => R = (h^2 + r^2) / 2h
# where h is dome_height, r is radius (of the base)
# If dome_height = radius, it's a perfect hemisphere.
# In the image, the dome looks somewhat hemispherical but maybe slightly flatter. 
# Let's assume a standard hemisphere where dome_height approx equals radius for a "full" look, 
# or calculate the specific radius for a cap. 
# Visually, it looks like a hemisphere. Let's assume dome_height = radius.

# Let's try a simpler approach: A cylinder combined with a sphere.
sphere_radius = radius
dome = cq.Workplane("XY").workplane(offset=base_height).sphere(sphere_radius)

# We only want the top half of the sphere sitting on the cylinder. 
# The sphere command creates a full sphere centered at the workplane origin.
# We need to cut off the bottom half of the sphere.
dome_hemisphere = dome.cut(
    cq.Workplane("XY").workplane(offset=base_height).rect(diameter*2, diameter*2).extrude(-sphere_radius*2)
)

# Combine base and dome
# Actually, constructing it as a revolution is often cleaner for single-body topology.

result = (
    cq.Workplane("XZ")
    .lineTo(radius, 0)
    .lineTo(radius, base_height)
    .threePointArc((0, base_height + radius), ( -radius, base_height)) # This creates a full 180 arc
    .close() # This creates a profile, but the arc went too far.
)

# Let's stick to the boolean operation approach for clarity and robustness with standard primitives.
# 1. Create Cylinder
base_cyl = cq.Workplane("XY").circle(radius).extrude(base_height)

# 2. Create Hemisphere on top
# We create a sphere centered at z = base_height.
# Then we intersect it with a box or cylinder defined above that plane to keep only the top part?
# Or simpler: Create a sphere, cut off the bottom, then fuse.

sphere_center_z = base_height
sphere = (
    cq.Workplane("XY")
    .workplane(offset=sphere_center_z)
    .sphere(radius)
)

# To get a perfect hemisphere on top of the cylinder:
# We need to remove the part of the sphere below z=base_height.
cut_tool = (
    cq.Workplane("XY")
    .workplane(offset=sphere_center_z)
    .rect(radius * 3, radius * 3)
    .extrude(-radius * 1.5) # Extrude downwards to cut the bottom half
)

top_dome = sphere.cut(cut_tool)
result = base_cyl.union(top_dome)

# Optional: If the image implies a "lens" shape or a specific curvature that isn't a full hemisphere,
# the code below is easily adjustable by changing 'dome_height'.
# For this specific image, it looks like a cylindrical base with a hemispherical top.

# Refined parameters to match visual proportions
diameter = 20.0
radius = diameter / 2.0
base_thickness = 2.0
dome_radius = radius # Looks like a full hemisphere

# Re-creating with clean logic
c1 = cq.Workplane("XY").circle(radius).extrude(base_thickness)
s1 = cq.Workplane("XY").workplane(offset=base_thickness).sphere(radius)
# Cut the bottom of the sphere
cut_box = cq.Workplane("XY").workplane(offset=base_thickness).rect(radius*4, radius*4).extrude(-radius*2)
hemisphere = s1.cut(cut_box)

result = c1.union(hemisphere)