import cadquery as cq

# --- Parameters ---
sphere_radius = 25.0
wall_thickness = 2.0
groove_height = 2.5  # Total height of the equatorial gap/groove
groove_depth = 1.5   # How deep the groove is inset

# Hinge parameters
hinge_radius = 2.5
hinge_width = 18.0   # Total width of the hinge assembly
hinge_offset = 1.0   # How much the hinge sticks out from the surface
knuckle_count = 3    # Number of hinge knuckles
pin_radius = 0.8     # Radius of the hole in the hinge

# --- Geometry Construction ---

# 1. Base Sphere
# We start with a full sphere
base_sphere = cq.Workplane("XY").sphere(sphere_radius)

# 2. Hollow out the sphere
# Create a smaller sphere to subtract, creating the wall thickness
inner_radius = sphere_radius - wall_thickness
hollow_sphere = base_sphere.cut(cq.Workplane("XY").sphere(inner_radius))

# 3. Create the Equatorial Groove/Split
# We need to cut away a band around the middle to separate top and bottom
# or at least create the visual groove.
# The image shows a recessed lip. Let's model it as two hemispheres with a stepped cut.

# Define the cutting tool for the main separation
split_plane_thickness = 0.2 # Small gap between halves if physical separation is needed
                            # For visual similarity to image, we create a groove.

# Let's create the Top and Bottom shells separately based on the sphere.

# Create a cylinder to cut the groove
groove_cutter = (
    cq.Workplane("XY")
    .cylinder(groove_height, sphere_radius + 1) # height, radius
)

# Create a cylinder that represents the inner connecting lip (recessed area)
# This sits inside the groove
lip_cylinder = (
    cq.Workplane("XY")
    .cylinder(groove_height, sphere_radius - groove_depth)
)

# To make it look like the image, we take the hollow sphere, cut the groove band out of the outer surface,
# but leave the material for the inner lip.

# Actually, a simpler approach for a solid model representation:
# 1. Sphere
# 2. Cut a groove ring out of the equator
# 3. Hollow it out
# 4. Add the hinge

# Let's refine the "Groove" logic based on the image.
# The groove looks like a simple inset band.
groove_outer_radius = sphere_radius + 0.1 # slightly larger to ensure cut
groove_inner_radius = sphere_radius - groove_depth

# Create the ring to subtract for the groove
groove_cut_ring = (
    cq.Workplane("XY")
    .cylinder(groove_height, groove_outer_radius)
    .cut(cq.Workplane("XY").cylinder(groove_height, groove_inner_radius))
)

body_with_groove = base_sphere.cut(groove_cut_ring)

# Now hollow it out
final_body_shell = body_with_groove.cut(cq.Workplane("XY").sphere(inner_radius))

# 4. Create the Hinge
# The hinge needs to be positioned on the equator at the surface.
# We'll calculate the position on the circumference. Let's put it at X positive.

# Calculate hinge position
# It sits tangent to the sphere surface at the equator.
hinge_center_radius = sphere_radius + hinge_radius - groove_depth # Approximate positioning
# To match image, hinge axis is tangent to the groove surface.

hinge_knuckle_length = hinge_width / knuckle_count

# Create the main cylinder for the hinge
hinge_solid = (
    cq.Workplane("YZ")
    .center(0, sphere_radius - groove_depth/2) # Position relative to origin
    .circle(hinge_radius)
    .extrude(hinge_width)
    .translate((-hinge_width/2, 0, 0)) # Center it on X axis
)

# Create cuts to separate knuckles
knuckle_gap = 0.5
cuts = cq.Workplane("YZ")

# We need two cuts to make 3 segments
cut1 = (
    cq.Workplane("YZ")
    .center(0, sphere_radius - groove_depth/2)
    .rect(hinge_radius*3, hinge_radius*3) # Big enough to cut
    .extrude(knuckle_gap)
    .translate((-hinge_width/6 - knuckle_gap/2, 0, 0))
)

cut2 = (
    cq.Workplane("YZ")
    .center(0, sphere_radius - groove_depth/2)
    .rect(hinge_radius*3, hinge_radius*3)
    .extrude(knuckle_gap)
    .translate((hinge_width/6 - knuckle_gap/2, 0, 0))
)

hinge_segmented = hinge_solid.cut(cut1).cut(cut2)

# Create the pin hole
pin_hole = (
    cq.Workplane("YZ")
    .center(0, sphere_radius - groove_depth/2)
    .circle(pin_radius)
    .extrude(hinge_width + 5) # Extra long to ensure cut
    .translate((- (hinge_width + 5)/2, 0, 0))
)

final_hinge = hinge_segmented.cut(pin_hole)

# Rotate hinge to align with the X-axis properly (currently extruded along X in YZ plane geometry context)
# The extrusion was along X (normal to YZ).
# The 'center' move pushed it up in Z.
# We want the hinge axis to be horizontal (along Y or similar tangent).
# Let's adjust orientation.

# Re-doing Hinge for easier placement:
# Construct along Y axis, centered at X = sphere_radius
hinge_geo = (
    cq.Workplane("XZ")
    .workplane(offset=sphere_radius - groove_depth*0.5) # Move plane to surface
    .center(0, 0) # Center at equator
    .circle(hinge_radius)
    .extrude(hinge_width/2, both=True) # Extrude along Y
)

# Cut the gaps for knuckles
# Knuckles at: -width/2 to -width/6, -width/6 to width/6, width/6 to width/2
# Gaps need to be at -width/6 and width/6
gap_box = (
    cq.Workplane("XY")
    .box(hinge_radius*3, knuckle_gap, hinge_radius*3)
    .translate((sphere_radius, -hinge_width/6, 0))
)
gap_box2 = (
    cq.Workplane("XY")
    .box(hinge_radius*3, knuckle_gap, hinge_radius*3)
    .translate((sphere_radius, hinge_width/6, 0))
)

hinge_geo = hinge_geo.cut(gap_box).cut(gap_box2)

# Pin hole
pin = (
    cq.Workplane("XZ")
    .workplane(offset=sphere_radius - groove_depth*0.5)
    .circle(pin_radius)
    .extrude(hinge_width/2 + 1, both=True)
)

final_hinge = hinge_geo.cut(pin)

# 5. Combine Sphere and Hinge
result = final_body_shell.union(final_hinge)

# Optional: Add the split line (tiny gap) horizontally through the hinge to show it opens
# Since we modeled it as one solid, a split is visual.
# The image shows the hinge connected to top and bottom.
# Usually center knuckle is one part, outer two are the other.
# We will leave it fused as requested for a single solid model representation, 
# but ensuring the geometry looks correct.
