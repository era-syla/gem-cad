import cadquery as cq

# Define parametric dimensions
# Main axis is aligned with Z for easier construction
# Moving from left to right in the image (which I will treat as bottom to top or negative to positive Z)

# Segment 1: Small tip cylinder
seg1_diam = 6.0
seg1_len = 12.0
seg1_chamfer = 1.0  # Chamfer at the very end

# Segment 2: Small flange/collar
seg2_diam = 10.0
seg2_len = 2.0

# Segment 3: Conical transition
seg3_base_diam = 10.0
seg3_top_diam = 6.0
seg3_len = 6.0

# Segment 4: Shaft section connecting cone to ball
seg4_diam = 6.0
seg4_len = 12.0

# Segment 5: The "Ball" or spherical bulge
# It looks like a sphere intersecting the shaft, or a barrel.
# Let's model it as a sphere.
seg5_sphere_diam = 14.0
# The effective length depends on where the adjacent cylinders intersect the sphere.
# We will position the sphere center relative to the stack.

# Segment 6: Large end cylinder
seg6_diam = 10.0
seg6_len = 20.0

# Construction
# We will build this as a single revolved profile or a stack of primitives.
# Stacking primitives is often more readable and easier to parameterize in CadQuery.

# 1. Start with the leftmost small cylinder
part = cq.Workplane("XY").circle(seg1_diam / 2).extrude(seg1_len)

# Chamfer the starting edge
part = part.edges("<Z").chamfer(seg1_chamfer)

# 2. Add the small flange
# We create a new workplane on the top face of the previous extrusion
part = part.faces(">Z").workplane().circle(seg2_diam / 2).extrude(seg2_len)

# 3. Add the conical transition
# CadQuery creates cones by lofting or simple extrude with taper, 
# but simply extruding a circle to a different circle is done via lofting 
# or creating a cone primitive. Let's use lofting for clarity on the workplane stack.
part = (
    part.faces(">Z")
    .workplane()
    .circle(seg3_base_diam / 2)
    .workplane(offset=seg3_len)
    .circle(seg3_top_diam / 2)
    .loft(combine=True)
)

# 4. Add the middle shaft section
part = part.faces(">Z").workplane().circle(seg4_diam / 2).extrude(seg4_len)

# 5. Add the Sphere
# To ensure the sphere is centered correctly, we need to know the current Z height.
# It's easier to union a sphere positioned absolutely.
# Calculate current Z height:
current_z = seg1_len + seg2_len + seg3_len + seg4_len

# The sphere center should probably be slightly "up" from the current face 
# so the shaft flows into it, but looking at the image, the shaft seems to tangent 
# into the sphere or intersect it. A simple intersection is robust.
# Let's assume the sphere center is exactly at the end of seg4 + radius, 
# or simply attached.
# Actually, usually such parts have the sphere centered on the axis.
# Let's append the sphere.
# We need to position the sphere. The previous face is at Z = current_z.
# If we want the sphere to look like the image, the cylinder seg4 goes *into* it.
# Let's determine the center of the sphere.
sphere_center_z = current_z + (seg5_sphere_diam / 2.0) - 2.0 # Overlap slightly for robustness
# Alternatively, just add a sphere at a specific point.

# Let's create the sphere object
ball = cq.Workplane("XY").workplane(offset=sphere_center_z).sphere(seg5_sphere_diam / 2)

# Union the sphere to the main body
part = part.union(ball)

# 6. Add the final large cylinder
# This cylinder exits the sphere.
# We need to start it from the sphere's geometric boundary or just overlap it from the center.
# Starting from the center of the sphere is safest to ensure boolean continuity.
last_cyl = (
    cq.Workplane("XY")
    .workplane(offset=sphere_center_z)
    .circle(seg6_diam / 2)
    .extrude(seg6_len + (seg5_sphere_diam/2)) # Extrude enough to stick out, length relative to center
)

# Calculate where the actual cylinder should visually start to look like the image.
# The image shows the cylinder extending to the right.
# Let's refine the last cylinder position.
# We want the total length of the extension to be seg6_len *from the edge of the sphere*.
# But simplistic modeling: just extrude from sphere center.
part = part.union(last_cyl)

# 7. Rotate to match image orientation (approximately isometric view)
# The image shows the part lying roughly horizontal.
result = part.rotate((0,0,0), (0,1,0), -90)

# Export or Render
if "show_object" in locals():
    show_object(result)