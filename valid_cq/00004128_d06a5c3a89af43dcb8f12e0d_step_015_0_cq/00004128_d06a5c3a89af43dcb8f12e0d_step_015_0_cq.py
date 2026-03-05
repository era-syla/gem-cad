import cadquery as cq
import math

# --- Parametric Dimensions ---
# Main body dimensions
main_diameter = 40.0
main_length = 120.0
taper_length = 25.0
nose_diameter = 15.0

# Grip/Rear details
rear_fillet = 5.0

# Front nose/collet area
collet_boss_dia = 12.0
collet_boss_height = 8.0
collet_nut_dia = 10.0
collet_nut_height = 6.0
collet_hole_dia = 4.0

# Vent details
vent_width = 3.0
vent_height = 12.0
vent_depth = 2.0
num_upper_vents = 4
num_lower_vents = 3
vent_spacing = 5.0

# Side flat/button area
flat_width = 20.0
flat_length = 60.0
flat_depth = 1.5

# --- Geometry Construction ---

# 1. Main Cylindrical Body
# Create the main cylinder
body = cq.Workplane("XY").circle(main_diameter / 2).extrude(main_length)

# 2. Tapered Front Section
# Create the conical front part
taper = (cq.Workplane("XY")
         .workplane(offset=main_length)
         .circle(main_diameter / 2)
         .workplane(offset=taper_length)
         .circle(nose_diameter / 2)
         .loft(combine=True))

body = body.union(taper)

# 3. Collet/Spindle Nose
# Small cylinder at the very tip
collet_boss = (cq.Workplane("XY")
               .workplane(offset=main_length + taper_length)
               .circle(collet_boss_dia / 2)
               .extrude(collet_boss_height))

collet_nut = (cq.Workplane("XY")
              .workplane(offset=main_length + taper_length + collet_boss_height)
              .circle(collet_nut_dia / 2)
              .extrude(collet_nut_height))

# Combine body parts
body = body.union(collet_boss).union(collet_nut)

# 4. Central Bore (Hole for the tool bit)
body = body.faces(">Z").hole(collet_hole_dia, depth=30)

# 5. Rear Shaping
# Round off the back edge
body = body.edges("<Z").fillet(rear_fillet)

# 6. Side Flattened Area (for switch/grip)
# Create a cutting box to slice a flat section off the side
flat_cut = (cq.Workplane("YZ")
            .workplane(offset=main_diameter/2 - flat_depth)
            .center(0, main_length / 2 + 10)  # Position along length
            .rect(flat_width, flat_length)
            .extrude(main_diameter, both=True)) # Cut outwards

# We don't subtract yet, we might want to make it a distinct feature or just a cut
# Looking at the image, it looks like a slight recess.
# Let's create a solid to cut away.
body = body.cut(flat_cut)

# 7. Ventilation Slots (Upper)
# Create a single vent shape
vent_shape = (cq.Workplane("YZ")
              .rect(vent_width, vent_height)
              .extrude(main_diameter + 5)) # Extrude through

# Pattern and cut upper vents
for i in range(num_upper_vents):
    # Calculate position
    z_pos = main_length - 15 - (i * vent_spacing)
    # Create the cutter positioned correctly
    cutter = (cq.Workplane("XY")
              .workplane(offset=z_pos)
              .transformed(rotate=(0, 0, 90)) # Rotate to face side
              .transformed(rotate=(90, 0, 0)) # Rotate to YZ plane orientation
              .rect(vent_width, vent_height)
              .extrude(main_diameter/2 + 5, both=True)) # Cut through
    
    # Move cutter to the surface (approximate for radial cut)
    # More simply, we position cuts on the side
    cutter = cutter.translate((main_diameter/2 - 2, 0, 0))
    body = body.cut(cutter)

# 8. Ventilation Slots (Lower)
# These often have an angle or different placement. 
# Based on image, they are lower down on the body.
for i in range(num_lower_vents):
    z_pos = 30 + (i * vent_spacing)
    
    # Creating a slanted cutter for the lower vents
    cutter = (cq.Workplane("YZ")
              .workplane(offset=main_diameter/2 - 2) # Near surface
              .center(0, z_pos)
              .rect(vent_width, vent_height)
              .extrude(10)) # Cut into body
    
    # Rotate the cutter slightly to match the image style if needed, 
    # but a straight cut is standard for these prompts.
    body = body.cut(cutter)


# 9. Spindle Lock Button Detail (Suggested by the bump on the side)
# The image shows a bump near the top taper on the side.
button_radius = 4.0
button_pos_z = main_length - 5
button = (cq.Workplane("YZ")
          .workplane(offset=main_diameter/2 - 1)
          .center(0, button_pos_z)
          .circle(button_radius)
          .extrude(3))

body = body.union(button)

# 10. Front Recess / Lock Nut Cutout
# There is a scoop/cutout near the nose (spindle lock access)
scoop_radius = 8.0
scoop = (cq.Workplane("XZ")
         .workplane(offset=main_length + taper_length)
         .center(main_diameter/2, -5) # Offset from center
         .sphere(scoop_radius))

body = body.cut(scoop)

# Final result assignment
result = body