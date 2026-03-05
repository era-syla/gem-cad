import cadquery as cq

# Parametric dimensions
key_thickness = 2.0
total_length = 50.0
blade_width = 10.0
blade_length = 30.0
head_radius = 12.0
tip_chamfer_length = 5.0

# Cutout parameters (the D-shape with hole)
cutout_hole_radius = 3.5
cutout_outer_radius = 5.5
cutout_offset_x = 10.0  # Distance from the center of the head

# Create the main body
# 1. Start with the circular head
head = cq.Workplane("XY").circle(head_radius).extrude(key_thickness)

# 2. Create the blade profile
# Calculate points for the blade
# It connects tangentially to the head usually, but for simplicity in this stylized model:
blade_center_y = 0
blade_start_x = -blade_length

# Draw the blade shape
blade_sketch = (
    cq.Workplane("XY")
    .moveTo(0, blade_width / 2)
    .lineTo(blade_start_x + tip_chamfer_length, blade_width / 2)
    .lineTo(blade_start_x, 0) # Tip point
    .lineTo(blade_start_x + tip_chamfer_length, -blade_width / 2)
    .lineTo(0, -blade_width / 2)
    .close()
    .extrude(key_thickness)
)

# Combine head and blade
key_body = head.union(blade_sketch)

# Create the D-shaped cutout detail in the head
# This looks like a circular cutout with a vertical bar/chord missing on the left side
# Located on the right side of the head

# Create the larger outer cutout shape (D-shape)
d_cutout = (
    cq.Workplane("XY")
    .center(cutout_offset_x, 0)
    .circle(cutout_outer_radius)
    .extrude(key_thickness)
)

# Create a box to chop off the left side of the circle to make the "D"
chopper = (
    cq.Workplane("XY")
    .center(cutout_offset_x - cutout_outer_radius, 0)
    .box(cutout_outer_radius, cutout_outer_radius * 3, key_thickness * 2)
)

# Form the D-shape solid (though we need negative space, we build the positive first)
d_shape_solid = d_cutout.cut(chopper)

# Create the inner hole
inner_hole = (
    cq.Workplane("XY")
    .center(cutout_offset_x, 0)
    .circle(cutout_hole_radius)
    .extrude(key_thickness)
)

# The final cutout feature seems to be an annulus (ring) cut by a chord
# Looking closely at the image:
# It's a D-shaped hole, with a circular post inside? No, it looks like a D-shaped hole.
# Let's re-examine the image.
# It looks like a 'D' shaped void. Inside that void, on the straight edge, there is a thin sliver of material remaining?
# Actually, it looks like a standard key ring hole but stylized.
# It looks like a circular hole, but with a flat vertical edge on the left side (a D-hole).
# AND there is a larger D-shaped recess or just a through-cut?
# Let's assume the simplest interpretation of the visual style:
# It is a D-shaped through-hole. 
# But wait, looking closer at the render, there's a ring. 
# It looks like a C-shape or a circular hole with a vertical bar to the left.
# Let's model it as:
# 1. A circular hole.
# 2. A vertical slot to the left of it, intersecting.
# Actually, looking at the shadow/AO, it looks like a "D" shaped hole where the straight part is a bridge.
# Let's try this interpretation: A circular hole, and a D-shaped perimeter cut.
# Let's go with a specific shape profile based on standard key ring loops sometimes seen in icons.
# It looks like a circle with a straight vertical line cutting off the left side (D-hole).

# Let's refine based on the specific artifact in the image:
# There is a circular hole.
# Surrounding the hole is a "D" shaped outline.
# The space between the hole and the D-outline is cut away.
# This leaves a "D" shaped hole with a floating circle? No, that would fall out.
# It looks like the "D" shape is the hole itself.
# Let's look at the vertical bar. It seems to be part of the solid key.
# So, it's a circular hole, plus a moon-crescent cut to the left?
# Let's try the most robust interpretation: A simple "D" shaped hole.
# Wait, looking at the very specific geometry:
# There is a vertical straight edge. To the right of it, an arc. This forms a D-shaped void.
# Inside this void, there is nothing. It's a hole.
# The image shows a "D" hole.
# Let's create a D-shaped hole.

cutout_shape = (
    cq.Workplane("XY")
    .center(6, 0) # Offset to the right side of the head
    .moveTo(0, 5) # Top of the vertical line
    .lineTo(0, -5) # Bottom of the vertical line
    .threePointArc((5, 0), (0, 5)) # Arc closing the D
    .close()
    .extrude(key_thickness)
)

# Wait, looking extremely closely at the crop provided:
# It is a circular hole.
# TO THE LEFT of the circular hole, there is a vertical bar.
# TO THE LEFT of the vertical bar, there is another small void?
# No, it looks like a "D" shaped hole with a circular hole *inside* it, but offset?
# Let's look at the negative space. The negative space is a D-shape.
# Let's assume a "D" shaped cut through the handle.

# Redefining Cutout based on standard icon tropes for this shape:
# A circular hole, but with a flat left side.
cutout_sketch = (
    cq.Workplane("XY")
    .workplane(offset=-key_thickness/2) # Start at bottom face
    .center(head_radius/2, 0)           # Move to the right side of head
    .moveTo(0, -4)                      # Start bottom of straight line
    .lineTo(0, 4)                       # Line up
    .radiusArc((0, -4), 4)              # Arc to close it
    .close()
    .extrude(key_thickness * 2)         # Cut through
)

# Apply the cut
result = key_body.cut(cutout_sketch)

# Optional: Add the specific inner detail if it's not just a D-hole.
# The image shows a thin vertical strip separating a small sliver from the main hole?
# No, it looks like a D-shaped hole where the straight edge is slightly curved or has a rim.
# Let's stick to the clean D-shaped hole which matches the silhouette.

# Refined parameters for better proportion match
result = (
    cq.Workplane("XY")
    # Draw half the profile and mirror or draw full profile
    .moveTo(-blade_length - tip_chamfer_length, 0)
    .lineTo(-blade_length, blade_width/2)
    .lineTo(0, blade_width/2)
    # The transition to the circular head
    .lineTo(0, head_radius) 
    # Actually, let's use a union approach for cleaner geometry like the first attempt
)

# Re-doing construction for a single cleaner solid
# Head
c_head = cq.Workplane("XY").circle(head_radius).extrude(key_thickness)

# Blade
p_blade = (
    cq.Workplane("XY")
    .moveTo(0, blade_width/2)
    .lineTo(-blade_length, blade_width/2)
    .lineTo(-blade_length - tip_chamfer_length, 0)
    .lineTo(-blade_length, -blade_width/2)
    .lineTo(0, -blade_width/2)
    .close()
    .extrude(key_thickness)
)

# Combine
base = c_head.union(p_blade)

# The specific D-cutout logic
# It sits on the right side of the head
cutout = (
    cq.Workplane("XY")
    .center(head_radius * 0.4, 0)
    .moveTo(0, -head_radius * 0.4)
    .lineTo(0, head_radius * 0.4)
    .threePointArc((head_radius * 0.4, 0), (0, -head_radius * 0.4))
    .close()
    .extrude(key_thickness)
)

# But wait, the image shows a ring *inside* a D-shape? 
# Or a D-shape with a hole?
# Let's look at the artifact: "D" outline. Inside, a circular hole. 
# This implies the "D" is a recess, and the circle is a through hole?
# Or maybe it's just a D-shaped hole.
# Let's implement the "D-shaped hole" as it's the most prominent feature.

result = base.cut(cutout)