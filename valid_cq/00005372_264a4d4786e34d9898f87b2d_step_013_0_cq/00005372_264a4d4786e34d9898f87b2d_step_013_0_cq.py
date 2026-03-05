import cadquery as cq

# Parametric Dimensions
base_length = 50.0       # Length of the top square frame
base_width = 40.0        # Width of the top square frame
base_thickness = 4.0     # Thickness of the frame walls
base_height = 8.0        # Height of the top rectangular frame section

guard_length = 40.0      # Length of the angled extension
guard_angle = 45.0       # Angle of the extension relative to the base
guard_thickness = 4.0    # Thickness of the extension plate

legs_height = 30.0       # Distance from top frame to bottom
legs_curve_radius = 25.0 # Radius for the curved cutouts on the side
bottom_circle_dia = 20.0 # Diameter of the theoretical bottom connection

# 1. Create the Top Frame
# We start with a solid block and will shell or cut it later.
# Let's create the outer shape first.
frame = (cq.Workplane("XY")
         .rect(base_length, base_width)
         .extrude(base_height)
         )

# 2. Create the Angled Guard
# This is attached to one of the shorter sides.
# We create a sketch on the side face and extrude it.
guard_plane = (frame.faces(">X").workplane()
               .transformed(rotate=(0, -guard_angle, 0)))

guard = (guard_plane
         .center(0, -base_height/2) # Align with the bottom of the frame
         .rect(guard_length, base_width)
         .extrude(guard_thickness)
         )
         
# Combine the frame and guard before adding fillets to the guard corners
# We need to shift the guard to align properly with the edge
# Instead of complex transforms, let's build the side profile and extrude across.

# Alternative Approach: Side Profile Extrusion
# This captures the frame side and the angled guard in one go.
profile_sketch = (cq.Workplane("XZ")
                  .moveTo(0, 0)
                  .lineTo(base_length/2, 0) # Top right corner
                  .lineTo(base_length/2, -base_height) # Bottom right corner
                  # Angled part
                  .polarLine(guard_length, -guard_angle) 
                  .polarLine(guard_thickness, 90-guard_angle)
                  .polarLine(-guard_length, 180-guard_angle)
                  # Back to frame
                  .lineTo(-base_length/2, -base_height)
                  .lineTo(-base_length/2, 0)
                  .close()
                  )

main_body = profile_sketch.extrude(base_width)

# Center the body
main_body = main_body.translate((0, -base_width/2, 0))

# 3. Create the Cutout for the Frame
# Remove material from the center to make it a frame
cutout_rect = (cq.Workplane("XY")
               .rect(base_length - 2*base_thickness, base_width - 2*base_thickness)
               .extrude(-base_height * 2) # Cut through downwards
               )

body_with_hole = main_body.cut(cutout_rect)

# 4. Create the Legs/Struts Structure
# The legs curve inwards to a central point/ring at the bottom.
# This looks like a loft or a revolution, but can be approximated with subtractive geometry.
# Let's create a block below the frame and carve it out.

# Create the solid volume for the legs
leg_block = (cq.Workplane("XY")
             .workplane(offset=-base_height)
             .rect(base_length, base_width)
             .extrude(-legs_height)
             )

# Cut the center vertically
center_cut = (cq.Workplane("XY")
              .rect(base_length - 2*base_thickness, base_width - 2*base_thickness)
              .extrude(-100) # Cut all the way down
              )

# Define the side cutouts to create the "legs"
# We need cutouts on X and Y axes that curve.

# Side Cutout (Along Y axis, cutting sides)
side_cut_sketch = (cq.Workplane("YZ")
                   .workplane(offset=0)
                   .moveTo(0, -base_height)
                   .threePointArc((0, -(base_height + legs_height)), (legs_height*0.6, -(base_height + legs_height/2)))
                   .lineTo(legs_height*2, -(base_height + legs_height))
                   .lineTo(legs_height*2, -base_height)
                   .close()
                   )
side_cut = side_cut_sketch.extrude(base_length*2, both=True)


# Front/Back Cutout (Along X axis, cutting front/back)
front_cut_sketch = (cq.Workplane("XZ")
                    .workplane(offset=0)
                    .moveTo(0, -base_height)
                    # Create a curved arc for the leg profile
                    .threePointArc((0, -(base_height + legs_height)), (legs_height*0.8, -(base_height + legs_height/2)))
                    .lineTo(legs_height*2, -(base_height + legs_height))
                    .lineTo(legs_height*2, -base_height)
                    .close()
                   )
front_cut = front_cut_sketch.extrude(base_width*2, both=True)


# Refine the Leg Block
shaped_legs = leg_block.cut(center_cut).cut(side_cut).cut(front_cut)


# 5. Join Parts
result = body_with_hole.union(shaped_legs)

# 6. Final Filleting
# Fillet the corners of the angled guard
result = result.edges(">X and <Z").fillet(5.0)

# Fillet the join between legs and frame for strength/aesthetics (optional based on image)
# result = result.edges("|Z").fillet(1.0) 

# Ensure the coordinate system is sensible (Top of frame at Z=0)
# No translation needed as built.