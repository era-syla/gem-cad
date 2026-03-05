import cadquery as cq

# Parametric dimensions
inner_radius = 15.0     # Radius of the central hole
wall_thickness = 3.0    # Thickness of the walls
cylinder_height = 20.0  # Height of the straight cylindrical part
base_radius_add = 10.0  # How much wider the base is compared to the cylinder
base_height = 10.0      # Height of the flared base section
fillet_radius = 8.0     # Radius for the smooth transition

# Derived dimensions
outer_radius = inner_radius + wall_thickness
base_outer_radius = outer_radius + base_radius_add

# 1. Create the base profile to revolve
# We will draw half of the cross-section and revolve it.
# Points for the outer profile
p0 = (inner_radius, 0)
p1 = (base_outer_radius, 0)
p2 = (base_outer_radius, 1.0) # Small vertical lip at the bottom
p3 = (outer_radius, base_height)
p4 = (outer_radius, base_height + cylinder_height)
p5 = (inner_radius, base_height + cylinder_height)

# Create the solid by revolving a profile
# We use a spline or tangent arc for the smooth flare, but a large fillet is often easier and more robust in CAD.
# Strategy: Create a stepped cylinder first, then fillet the junction.

# Step 1: Create the main cylindrical body
main_body = cq.Workplane("XY").circle(outer_radius).extrude(base_height + cylinder_height)

# Step 2: Create the base flange
# We'll make a larger disk at the bottom and loft or fillet, but looking at the image, 
# it looks like a specific flared shape. Let's try a revolution of a specific profile for better control.

# Re-evaluating strategy: The image shows a very smooth, organic flare. 
# A revolution of a sketch with a tangent arc or spline is best.

result = (
    cq.Workplane("XZ")
    # Draw the cross-section
    .moveTo(inner_radius, 0)
    .lineTo(base_outer_radius, 0)
    .lineTo(base_outer_radius, 1.5) # Small vertical edge at the very bottom
    # Create a smooth curve (fillet-like) connecting the wide base to the narrower cylinder
    .tangentArcPoint((outer_radius, base_height), relative=False) 
    .lineTo(outer_radius, base_height + cylinder_height)
    .lineTo(inner_radius, base_height + cylinder_height)
    .close()
    # Revolve 360 degrees around the Z-axis
    .revolve(360)
)

# Alternative strategy (Constructive Solid Geometry) if the sketch is tricky:
# 1. Cylinder
# 2. Base Cone/Cylinder
# 3. Fillet
# Let's verify the visual against the image. The image has a very smooth transition, 
# almost like a fillet operation between a base plate and a cylinder.
# Let's try the CSG approach as it's often more parametric friendly for standard parts.

# CSG Approach Implementation:
# 1. Base Disk
base_disk = cq.Workplane("XY").circle(base_outer_radius).extrude(2.0)
# 2. Cylinder
cylinder = cq.Workplane("XY").workplane(offset=2.0).circle(outer_radius).extrude(base_height + cylinder_height - 2.0)
# 3. Union
part = base_disk.union(cylinder)
# 4. Fillet the interface
# We need a large fillet to create that slope.
try:
    part = part.faces("Z>0").edges(f"%circle and >radius {outer_radius - 0.1}").fillet(base_height - 1.0)
except:
    # Fallback to revolve if fillet fails or is geometrically impossible
    pass

# Re-evaluating the image: The transition starts almost immediately from the bottom edge.
# The revolve method is safer and produces cleaner geometry for this specific shape.

final_geometry = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(base_outer_radius, 0)
    .lineTo(base_outer_radius, 1.0) # Small vertical section at bottom
    # Use a 3-point arc or spline for the flare. 
    # A spline from the base lip to the cylinder wall is flexible.
    .spline([(outer_radius + (base_outer_radius-outer_radius)*0.3, base_height*0.4), 
             (outer_radius, base_height)], includeCurrent=True)
    .lineTo(outer_radius, base_height + cylinder_height)
    .lineTo(inner_radius, base_height + cylinder_height)
    .close()
    .revolve()
)

result = final_geometry