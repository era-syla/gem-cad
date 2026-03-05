import cadquery as cq

# Parametric dimensions
radius = 10.0      # Radius of the base cylinder and the hemisphere
base_height = 5.0  # Height of the cylindrical base section

# Create the base cylinder
# We start by drawing a circle on the XY plane and extruding it
base = cq.Workplane("XY").circle(radius).extrude(base_height)

# Create the hemisphere on top
# There are multiple ways to do this. A simple way is to create a sphere and cut it,
# or revolve an arc. However, CadQuery has primitive shapes which are often easier.
# We can create a sphere and translate it so its center aligns with the top of the cylinder,
# then intersect or union it.

# Another approach: Revolve a profile.
# Profile: A rectangle for the base + a quarter circle for the top.
# Let's stick to the boolean constructive solid geometry (CSG) approach for clarity.

# 1. Create a full sphere centered at the origin
sphere = cq.Workplane("XY").sphere(radius)

# 2. We need a hemisphere. A simple way in CQ using primitives is to intersect a sphere with a box,
# or cut a sphere with a box.
# Let's cut the bottom half off the sphere.
# We create a large box below the XY plane to cut away the bottom half.
cutting_box = cq.Workplane("XY").box(radius * 4, radius * 4, radius * 2).translate((0, 0, -radius))
hemisphere = sphere.cut(cutting_box)

# 3. Move the hemisphere to the top of the base cylinder
hemisphere = hemisphere.translate((0, 0, base_height))

# Combine the base and the hemisphere
result = base.union(hemisphere)

# Alternative, cleaner single-chain approach using a revolution:
# 1. Draw the profile on XZ plane:
#    - Start at origin (0,0)
#    - Line to (radius, 0)
#    - Line up to (radius, base_height)
#    - Arc to (0, base_height + radius) centered at (0, base_height)? No, center would be (0, base_height)
#      Let's trace: (radius, base_height) -> arc to (0, base_height + radius)
#    - Line down to origin.
# 2. Revolve around Z axis.

def create_dome_profile(height, r):
    return (
        cq.Workplane("XZ")
        .lineTo(r, 0)                  # Bottom radius line
        .lineTo(r, height)             # Cylinder side wall
        .threePointArc((r * 0.707, height + r * 0.293), (0, height + r)) # Arc to top
        .lineTo(0, 0)                  # Return to origin
        .close()
        .revolve()
    )

# Let's use the boolean approach as it's very robust for simple primitives.
# Re-implementing the boolean approach in a more concise "fluent" way if possible,
# but separate variables is often more readable for these specific shapes.

# Final Code Structure
# 1. Cylinder
# 2. Sphere (cut to hemisphere)
# 3. Union

# Let's refine the hemisphere creation to be simpler.
# Just creating a sphere and cutting it is fine.
# But actually, `sphere` creates a solid. If we want a perfect dome on a cylinder:

result = (
    cq.Workplane("XY")
    .circle(radius)
    .extrude(base_height)
    .faces(">Z")
    .workplane()
    .sphere(radius) # This creates a sphere centered on the current workplane (top of cylinder)
    # The sphere primitive in Workplane context usually unions by default or replaces? 
    # Actually .sphere() inside a chain creates a sphere and combines it.
    # However, it creates a full sphere. We need to intersect it with a half-space or cut the bottom.
    # The bottom half of the sphere will be "inside" the cylinder if we center it at the top face.
    # A sphere of radius R centered at Z=base_height will stick down to Z=base_height-R.
    # If base_height < R, it sticks out the bottom.
    # If base_height >= R, the bottom half is hidden inside.
    # The image shows a smooth transition, implying the sphere's equator matches the cylinder's rim.
    # This means the sphere center is exactly at the top of the cylinder.
)

# Since unioning a sphere centered at the top face will result in the bottom half of the sphere
# being inside the cylinder, this is geometrically valid and results in the correct outer appearance,
# provided we don't care about internal geometry (which we don't for a BRep).
# However, to be cleaner (no internal overlapping faces), let's construct it properly.

# Let's go with the Revolve approach. It creates a single, clean topological surface without internal seams.
result = (
    cq.Workplane("XZ")
    .lineTo(radius, 0)
    .lineTo(radius, base_height)
    # Create the arc for the dome.
    # Start point is current (radius, base_height)
    # End point is (0, base_height + radius)
    # Center of arc is (0, base_height)
    # We use radiusArc endpoint, radius
    .radiusArc((0, base_height + radius), radius)
    .lineTo(0, 0)
    .close()
    .revolve()
)