import cadquery as cq

# Parameters for the box
box_length = 80.0
box_width = 60.0
box_height = 40.0
wall_thickness = 2.0

# Parameters for the cutouts
side_window_width = 25.0
side_window_height = 15.0
side_window_offset_z = 5.0 # Offset from the top edge

end_window_width = 15.0
end_window_height = 10.0
end_window_offset_z = 5.0 # Offset from the top edge

circular_hole_diam = 6.0
circular_hole_offset_x = 20.0 # From center to right
circular_hole_offset_z = -5.0 # From center down (relative to face center) - visually adjusted

# Parameters for the feet
foot_length = 10.0
foot_width = 40.0 # Spanning most of the width but not all
foot_height = 5.0
foot_spacing = 50.0 # Center-to-center spacing along length

# 1. Create the main box body (hollowed out)
# Start with a solid block
main_body = cq.Workplane("XY").box(box_length, box_width, box_height)

# Create the hollow interior (shelling the top face)
# Selecting the top face (+Z) and shelling inward
result = main_body.faces("+Z").shell(-wall_thickness)

# 2. Add Cutouts

# Rectangular cutout on the long side (Back face in standard view, looks like left-back in iso)
# We'll target the -Y face (or +Y depending on orientation preference, let's assume +Y is back)
# Based on image, the long side facing left-back has a large rectangular cutout.
result = (result.faces(">Y").workplane()
          .center(0, (box_height/2) - (side_window_height/2) - side_window_offset_z)
          .rect(side_window_width, side_window_height)
          .cutThruAll())

# Rectangular cutout on the short side (Right-back face)
# We'll target the +X face
result = (result.faces(">X").workplane()
          .center(0, (box_height/2) - (end_window_height/2) - end_window_offset_z)
          .rect(end_window_width, end_window_height)
          .cutThruAll())

# Circular hole on the front long face (-Y)
# The hole is positioned near the corner.
result = (result.faces("<Y").workplane()
          .center((box_length/2) - 10, 0) # Position near the right edge of the face
          .circle(circular_hole_diam / 2)
          .cutThruAll())


# 3. Add Feet
# We will add two rectangular feet to the bottom face (-Z)
# Create a sketch for the feet on the bottom plane

feet = (cq.Workplane("XY")
        .workplane(offset=-box_height/2) # Move to bottom of box
        .rect(foot_spacing + foot_length, foot_width) # Outer boundary helper
        .rect(foot_spacing - foot_length, foot_width) # Inner boundary helper
        .extrude(-foot_height) # Extrude downwards
        )

# The logic above creates a hollow frame. Let's make distinct blocks instead for cleaner parametric logic.
foot1 = (cq.Workplane("XY")
         .workplane(offset=-box_height/2)
         .center(-foot_spacing/2, 0)
         .rect(foot_length, foot_width)
         .extrude(-foot_height))

foot2 = (cq.Workplane("XY")
         .workplane(offset=-box_height/2)
         .center(foot_spacing/2, 0)
         .rect(foot_length, foot_width)
         .extrude(-foot_height))

# Combine everything
result = result.union(foot1).union(foot2)

# Export or Render
# show_object(result)