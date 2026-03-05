import cadquery as cq

# --- Parametric Dimensions ---
# Base Frame Dimensions
frame_width = 80.0
frame_depth = 50.0
frame_height = 60.0
leg_thickness = 8.0
bottom_rail_height = 8.0
bottom_rail_offset = 5.0 # Height from ground to bottom of rail (if any, usually 0 or small)

# Top Block Dimensions
block_width = 60.0  # Slightly narrower than frame
block_depth = 30.0  # Narrower than frame
block_height = 50.0
curved_top_radius = 120.0 # Radius for the curved top surface

# --- Construction ---

# 1. Create the Base Frame
# We'll start with a solid block and shell/cut it, or build it up. 
# Building it up with profiles is often cleaner for frames.

# Let's use a subtraction method for the main frame volume.
frame_outer = cq.Workplane("XY").box(frame_width, frame_depth, frame_height)

# Create the cutting tool for the main opening (front/back)
cut_width_fb = frame_width - 2 * leg_thickness
cut_height_main = frame_height - leg_thickness - bottom_rail_height # Leaves top and bottom bars

# Create the cutting tool for the side openings
cut_depth_side = frame_depth - 2 * leg_thickness

# Cut Front/Back
frame = (frame_outer
         .faces("+Z").workplane().center(0, 0)
         # We need to cut through, leaving legs.
         # Actually, creating a sketch on the faces is easier.
        )

# Alternative approach: Build components and union. It's more parametric-friendly.
# Let's do the "Box with cuts" approach, it's robust.

# Main block
base = cq.Workplane("XY").box(frame_width, frame_depth, frame_height)

# Cut Front and Back faces (through all)
cut_front_back = (cq.Workplane("XZ")
                  .workplane(offset=frame_depth/2.0 + 1) # Start outside
                  .center(0, 0) # Center of the face
                  .rect(frame_width - 2*leg_thickness, frame_height - 2*leg_thickness)
                  .extrude(-(frame_depth + 2)) # Cut through
                  )

# Cut Left and Right faces (through all)
cut_left_right = (cq.Workplane("YZ")
                  .workplane(offset=frame_width/2.0 + 1)
                  .center(0, 0)
                  .rect(frame_depth - 2*leg_thickness, frame_height - 2*leg_thickness)
                  .extrude(-(frame_width + 2))
                  )

# Apply cuts to base to make the hollow frame
frame = base.cut(cut_front_back).cut(cut_left_right)

# Add the bottom cross-bar
# The image shows a cross bar at the bottom connecting the long sides.
cross_bar = (cq.Workplane("XY")
             .workplane(offset=-frame_height/2.0 + leg_thickness/2.0)
             .box(leg_thickness, frame_depth - 2*leg_thickness, leg_thickness)
             )

frame = frame.union(cross_bar)


# 2. Create the Top Block
# This sits on top of the frame. It has a curved top face.

# Base block shape
block_base = (cq.Workplane("XY")
              .workplane(offset=frame_height/2.0) # Start at top of frame
              .box(block_width, block_depth, block_height, centered=(True, True, False))
              )

# Create the curve cut. 
# The curve goes along the long axis (Width). It's highest in the middle.
# We will create a cutting tool that is the inverse of the curve.
# Or simpler: Extrude the profile with the curve.

# Let's redefine the block by extruding a profile from the side (XZ plane)
# This allows us to draw the arc easily.
top_face_center_z = frame_height/2.0 + block_height

# Calculate the sagitta or chord to position the arc correctly
# We want an arc that peaks at block_height.
# Center of arc needs to be below.
# (x-x0)^2 + (z-z0)^2 = r^2
# Peak point: (0, top_face_center_z)
# Side points: (+- block_width/2, somewhat lower)

# It's easier to create a large cylinder and intersect it.
curved_cutter = (cq.Workplane("XZ")
                 .workplane(offset= -block_depth/2.0 - 5) # Start behind
                 .moveTo(0, top_face_center_z - curved_top_radius) # Move to center of circle
                 .circle(curved_top_radius)
                 .extrude(block_depth + 10)
                 )

# We want the intersection of the box and this cylinder.
# But wait, the curve is convex (bulging out).
# So we need to position the cylinder center *below* the block so the top edge of the circle forms the top face.

# Re-doing block with intersection approach
# 1. Create a rectangular prism for the full potential bounding box
raw_block = (cq.Workplane("XY")
             .workplane(offset=frame_height/2.0)
             .box(block_width, block_depth, block_height, centered=(True, True, False))
             )

# 2. Create the cylinder for intersection.
# The cylinder runs along Y axis. 
# Center is at X=0, Z = (top of block) - radius.
cyl_center_z = (frame_height/2.0 + block_height) - curved_top_radius

trimming_cylinder = (cq.Workplane("YZ")
                     .workplane(offset=0) # centered YZ plane
                     .center(0, cyl_center_z) # Move local Z up/down (which is global Z here effectively relative to plane origin)
                     # Wait, Workplane("YZ") X is global Y, Y is global Z.
                     # We want cylinder along Y axis? No, the curve is seen from the "front", 
                     # meaning the generator line is along the depth (Y). 
                     # So we look at XZ plane.
                     )

# Let's use the XZ plane for the profile.
# We will draw the shape: straight sides, flat bottom, curved top.
block_profile = (cq.Workplane("XZ")
                 .workplane(offset=-block_depth/2.0)
                 .moveTo(block_width/2.0, frame_height/2.0) # Bottom right
                 .lineTo(-block_width/2.0, frame_height/2.0) # Bottom left
                 .lineTo(-block_width/2.0, frame_height/2.0 + block_height - 5) # Top left (start of arc area approx)
                 # Three point arc: End point and a point on the arc? 
                 # Or use radius arc.
                 .lineTo(-block_width/2.0, frame_height/2.0 + block_height - (block_width**2)/(8*curved_top_radius)) # rough geometric side height
                 .radiusArc((block_width/2.0, frame_height/2.0 + block_height - (block_width**2)/(8*curved_top_radius)), curved_top_radius) # Arching to right side
                 .close()
                 .extrude(block_depth)
                 )

# The radiusArc can be tricky with exact heights. Let's use intersection method, it's mathematically precise for specific radius.
cylinder_cutter = (cq.Workplane("YZ")
                   .workplane(offset=0)
                   .transformed(rotate=(0,0,90)) # Now viewing XZ basically
                   .moveTo(0, (frame_height/2.0 + block_height) - curved_top_radius)
                   .circle(curved_top_radius)
                   .extrude(block_depth*2) # Make it long enough
                   )
# The cylinder is oriented along Z now due to circle on XY-ish plane extruded. 
# Let's stick to the simplest intersection.

# Final attempt at Block Logic:
# 1. Box
b_box = cq.Workplane("XY").workplane(offset=frame_height/2.0).box(block_width, block_depth, block_height, centered=(True, True, False))
# 2. Cylinder running along Y axis (depth), centered at X=0, Z=low
cutter_cyl = (cq.Workplane("XZ") # Draw on Front plane
              .moveTo(0, (frame_height/2.0 + block_height) - curved_top_radius)
              .circle(curved_top_radius)
              .extrude(block_depth + 10, both=True) # Extrude along Y
              )

# Intersect the box with the cylinder to get the curved top
final_block = b_box.intersect(cutter_cyl)

# Combine Frame and Block
result = frame.union(final_block)