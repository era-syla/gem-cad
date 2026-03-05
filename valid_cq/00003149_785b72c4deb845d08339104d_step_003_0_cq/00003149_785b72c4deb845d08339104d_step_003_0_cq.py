import cadquery as cq

# Parameters
# Outer Ring
ring_outer_radius = 60.0
ring_thickness = 4.0
ring_height = 12.0
ring_hole_diameter = 1.5

# Central Lever Arm
arm_length = 40.0
arm_width = 15.0
arm_height = 6.0
arm_pivot_radius = 6.0  # Where it rotates
arm_handle_radius = 5.0  # The vertical post
arm_handle_height = 12.0
arm_bottom_post_radius = 4.0
arm_bottom_post_height = 4.0

# Separate Spacer/Washer
spacer_outer_radius = 12.0
spacer_inner_radius = 6.0
spacer_height = 12.0
spacer_small_hole_dia = 1.5
spacer_offset_x = 70.0 # Position relative to center
spacer_offset_y = 50.0

# --- Geometry Construction ---

# 1. Outer Ring
# Create a tube by drawing a circle and cutting a smaller one, extruded
ring = (cq.Workplane("XY")
        .circle(ring_outer_radius)
        .circle(ring_outer_radius - ring_thickness)
        .extrude(ring_height)
       )

# Add small hole to the ring
# Assuming position based on image (looks like it's on the top face)
ring = (ring.faces(">Z").workplane()
        .moveTo(ring_outer_radius - ring_thickness/2, 0)
        .hole(ring_hole_diameter)
       )

# 2. Lever Arm
# Main body of the arm - stadium shape (rectangle with rounded ends)
# Let's pivot at (0,0) for the arm construction, then move it if needed.
# The image shows it offset from center, but usually these rotate around a center.
# Let's assume one end is near center (0,0) and the other is out.
# Looking at the image, the arm seems to be floating inside. Let's build it at origin first.

arm_body = (cq.Workplane("XY")
            .center(0, 0)
            .rect(arm_length - arm_width, arm_width) # Center rectangle
            .extrude(arm_height)
            .edges("|Z").fillet(arm_width/2 - 0.01) # Round ends to make stadium shape
           )

# Shift arm body so the pivot point is roughly at (0,0) or slightly offset
# Based on image, the "pivot" (bottom post) is on the left, handle on right.
arm_body = arm_body.translate(((arm_length - arm_width)/2, 0, 0))

# Create the handle post (upwards)
handle_post = (cq.Workplane("XY")
               .workplane(offset=arm_height)
               .moveTo(arm_length - arm_width, 0) # Move to the far end
               .circle(arm_handle_radius)
               .extrude(arm_handle_height)
              )

# Create the bottom pivot post (downwards)
bottom_post = (cq.Workplane("XY")
               .moveTo(0, 0) # Pivot end
               .circle(arm_bottom_post_radius)
               .extrude(-arm_bottom_post_height)
              )

# Combine Arm parts
arm_assembly = arm_body.union(handle_post).union(bottom_post)

# Position the arm inside the ring. In the image, it's slightly offset from center.
# Let's move it to match the visual relative position.
arm_assembly = arm_assembly.translate((10, -10, ring_height/2 - arm_height/2))


# 3. Separate Spacer/Washer
spacer = (cq.Workplane("XY")
          .circle(spacer_outer_radius)
          .circle(spacer_inner_radius)
          .extrude(spacer_height)
         )

# Add small hole to spacer rim
spacer = (spacer.faces(">Z").workplane()
          .moveTo(spacer_outer_radius - (spacer_outer_radius-spacer_inner_radius)/2, 0)
          .hole(spacer_small_hole_dia)
         )

# Move spacer to the side as shown in image
spacer = spacer.translate((spacer_offset_x, spacer_offset_y, 0))

# Combine all into final result
result = ring.union(arm_assembly).union(spacer)