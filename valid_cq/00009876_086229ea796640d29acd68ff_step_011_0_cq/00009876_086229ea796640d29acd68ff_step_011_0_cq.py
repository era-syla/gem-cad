import cadquery as cq

# -- Parametric Dimensions --
# Adjust these values to change the size of the model
head_diameter = 16.0    # Diameter of the mushroom-like head
head_height = 8.0       # Height of the head portion
shaft_diameter = 8.0    # Diameter of the cylindrical shaft
shaft_length = 15.0     # Length of the shaft
chamfer_size = 0.5      # Size of the chamfer at the bottom of the shaft

# -- Modeling --

# 1. Create the Shaft
# We start with the cylindrical base
shaft = cq.Workplane("XY").circle(shaft_diameter / 2.0).extrude(shaft_length)

# 2. Create the Head
# The head is a spherical cap or dome shape. 
# We'll create a sphere and cut off the bottom to make a cap, 
# then position it on top of the shaft.
# Alternatively, we can revolve a profile. Let's use the sphere method for a nice dome.
# A simple way to get that specific shape is creating a sphere larger than the shaft
# and cutting it or intersecting it.
# Based on the image, the head looks like a section of a sphere.

# Let's create a sphere centered at the top of the shaft
# We need to calculate the radius of the sphere that satisfies the head_diameter at a certain cut.
# However, a simpler geometric approximation for this specific look (mushroom head) 
# is often just a sphere or ellipsoid cut.
# Let's try revolving an arc.

# Profile approach:
# We draw the cross-section on the XZ plane and revolve it around the Z axis.
# The profile consists of:
# - A vertical line for the shaft
# - A horizontal line for the bottom of the head overhang
# - An arc for the top of the head

head_radius = head_diameter / 2.0
shaft_radius = shaft_diameter / 2.0

# Let's build it top-down for easier positioning
# 1. The Head
# We create a sphere and cut the bottom off to get a "cap".
# Or simpler: Revolve an arc.
# The arc starts at (0, head_height) and ends at (head_radius, 0) - wait, that's an ellipse quadrant.
# The image shows a continuous dome. Let's assume a spherical cap.
# If diameter is 16 and height is 8, it's a perfect hemisphere.
# If diameter is 16 and height is < 8, it's a cap.
# The image looks roughly like a hemisphere, maybe slightly flattened. Let's assume hemisphere for simplicity or slightly flattened.
# Let's model it as a solid of revolution to get the exact "mushroom" shape.

final_assembly = (
    cq.Workplane("XY")
    # Draw the shaft circle
    .circle(shaft_radius)
    .extrude(shaft_length)
    # Move workplane to the top of the shaft
    .faces(">Z").workplane()
    # Create the head. 
    # We will use a revolve operation for the head to ensure a smooth transition if needed, 
    # but a simple sphere intersection or revolution of an arc is best.
    # Let's just create a solid for the head and union it.
)

# Creating the head separately to ensure control over shape
# Option A: A Sphere cut by a plane.
# Option B: Revolve an arc.
# Let's use a Sphere and cut it.
sphere_radius = head_radius # If it's a hemisphere
head = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length) # Position at top of shaft
    .sphere(sphere_radius)
    # Cut off the bottom half of the sphere (everything below the current workplane Z)
    # But wait, a sphere center is at the workplane. We want the bottom of the hemisphere at the workplane.
    # So we need to cut off Z < shaft_length
    .cut(
        cq.Workplane("XY").workplane(offset=shaft_length - sphere_radius).box(head_diameter*2, head_diameter*2, sphere_radius)
    )
)

# Actually, the CadQuery sphere is centered at the origin of the workplane.
# If we want a hemisphere sitting ON TOP of the shaft:
# 1. Center of sphere should be at Z = shaft_length.
# 2. We keep the top half (Z > shaft_length).
# By default .sphere() creates a full sphere.

# Let's try a cleaner Revolve approach for the whole object or just the head.
# It usually produces cleaner topology for these shapes.

# Define the profile for revolution
# Points: (0,0) -> (shaft_radius, 0) -> (shaft_radius, shaft_length) -> ... arc ... -> (0, shaft_length + head_height)
def create_profile(p):
    return (
        p.lineTo(shaft_radius, 0)
        .lineTo(shaft_radius, shaft_length)
        .lineTo(head_radius, shaft_length) # Underside of the head
        # Arc for the top. 
        # Three point arc: start(current), point_on_arc, end
        # Start: (head_radius, shaft_length)
        # End: (0, shaft_length + head_height)
        # Mid: roughly somewhere in between to define curvature. 
        # For a circular arc tangent to the top, we can use radiusArc.
        .radiusArc((0, shaft_length + head_height), head_radius) 
        .lineTo(0, 0)
        .close()
    )

# Note: radiusArc might be tricky if the geometry is strictly a hemisphere (radius = head_height). 
# If head_height == head_radius, simple fillet or sphere is easier.
# Let's assume it's a standard button head rivet/screw which is often a portion of a sphere.

# Revised Strategy: Two simple primitives unioned.
# 1. Cylinder for Shaft
# 2. Sphere for Head, cut to be a hemisphere (or cap).

# Create Shaft
pt_shaft = cq.Workplane("XY").circle(shaft_radius).extrude(shaft_length)

# Create Head (Hemisphere style)
# We position a sphere at the top of the shaft. 
# To get a hemisphere sitting flat, the center of the sphere is at Z = shaft_length.
# Then we cut away the bottom half.
pt_head = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length) # Move to top of shaft
    .sphere(head_radius)
    # Cut the bottom half. A large box positioned below the center.
    .cut(
        cq.Workplane("XY")
        .workplane(offset=shaft_length - head_radius) # Move down by radius
        .box(head_radius*3, head_radius*3, head_radius) # Cut box
    )
)

# Combine
result = pt_shaft.union(pt_head)

# Add Chamfer at the bottom of the shaft
result = result.faces("<Z").edges().chamfer(chamfer_size)

# Optional: Fillet at the neck (junction of head and shaft) for realism
# result = result.faces(cq.NearestToPointSelector((0, 0, shaft_length))).edges().fillet(0.5)
# Looking at the image, the junction is quite sharp, so I will omit the neck fillet to stay true to the visual.

# There is a small "dimple" or feature on the very top in the reference image, 
# possibly an injection molding gate mark or a stylistic line. 
# It looks like a small faint line. I will leave the geometry clean as per standard CAD practices for this part type.

# Final cleanup
result = result.val() # Convert to TopoDS_Shape if needed, but returning the Workplane object is standard.
result = cq.Workplane("XY").add(result) # Wrap back in Workplane for consistency