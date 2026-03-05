import cadquery as cq

# Parameters for the Spacer/Standoff (Top Part)
spacer_length = 30.0
spacer_outer_diam = 12.0
spacer_inner_diam = 6.0
spacer_position = (0, 15, 15)  # Position to match the approximate layout in the image
spacer_rotation = (45, 0, 0)   # Tilted rotation

# Parameters for the End Cap/Plug (Bottom Part)
cap_cyl_height = 10.0
cap_diam = 8.0
cap_dome_height = 4.0      # Height of the rounded top portion
cap_hole_diam = 2.0        # Small hole at the top
cap_position = (0, -5, 0)  # Position relative to origin

# --- Create Part 1: The Spacer ---
# Create the main cylinder
spacer = (cq.Workplane("XY")
          .circle(spacer_outer_diam / 2.0)
          .extrude(spacer_length)
          )

# Cut the through-hole
spacer = (spacer.faces(">Z")
          .workplane()
          .circle(spacer_inner_diam / 2.0)
          .cutBlind(-spacer_length)
          )

# Rotate and move the spacer to match the visual arrangement
spacer = spacer.rotate((0,0,0), (1,0,0), -60).translate(spacer_position)


# --- Create Part 2: The End Cap ---
# Create the cylindrical base
cap_base = (cq.Workplane("XY")
            .circle(cap_diam / 2.0)
            .extrude(cap_cyl_height)
            )

# Create the dome. 
# We'll create a sphere and intersect it, or revolve a profile. 
# A fillet on a cylinder is easiest if it's a perfect hemisphere, 
# but for a specific dome height, a revolution is more robust.
# Let's use the fillet method if radius = diameter/2, otherwise a revolution.
# Looking at the image, it looks like a full hemisphere or close to it.
cap_dome = (cap_base.faces(">Z")
            .workplane()
            .sphere(cap_diam / 2.0) # Create a sphere on top
            # We need to cut off the bottom half of the sphere that is inside the cylinder
            # But CadQuery unions automatically merge touching solids often.
            # A cleaner way for a specific shape: Revolve a profile.
            )

# Alternative robust approach for the Cap: Revolve a profile
# Profile: a rectangle for the base, an arc for the top.
# Let's draw the profile on the XZ plane.
pts = [
    (0, 0),
    (cap_diam / 2.0, 0),
    (cap_diam / 2.0, cap_cyl_height),
    (0, cap_cyl_height + cap_dome_height) # Top center point
]

# We need an arc from (r, h) to (0, h+dome_h).
# Using a 3-point arc or tangent arc.
# Let's construct it as a single solid using a profile and revolve.
cap = (cq.Workplane("XZ")
       .moveTo(0, 0)
       .lineTo(cap_diam / 2.0, 0)
       .lineTo(cap_diam / 2.0, cap_cyl_height)
       .radiusArc((0, cap_cyl_height + cap_dome_height), -cap_diam/2.0) # Negative radius for convex arc
       .lineTo(0, 0)
       .close()
       .revolve()
       )

# Create the small hole on top of the cap
cap = (cap.faces(">Z")
       .workplane()
       .circle(cap_hole_diam / 2.0)
       .cutBlind(-cap_cyl_height/2) # Assume shallow hole or through hole
       )

# Move the cap to position
cap = cap.translate(cap_position)

# Combine both parts into one result for visualization
result = spacer.union(cap)