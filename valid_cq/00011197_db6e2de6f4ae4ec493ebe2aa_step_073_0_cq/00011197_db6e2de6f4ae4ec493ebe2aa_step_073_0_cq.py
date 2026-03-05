import cadquery as cq

# Parametric dimensions
main_diameter = 50.0  # Outer diameter of the main cylinder
main_height = 30.0    # Height of the main cylinder
wall_thickness = 2.0  # Thickness of the shell
fillet_radius = 3.0   # Radius for the top edge fillet

# Center boss parameters
boss_diameter = 12.0
boss_height = 5.0     # Height extending from the top face
boss_hole_diameter = 6.0

# Side slot parameters
slot_width = 8.0
slot_length = 15.0  # Length from center axis to outer edge
slot_offset = 12.0  # Distance from center

# Wing/Tab parameters
wing_width = 6.0
wing_length = 8.0
wing_thickness = 3.0
wing_fillet = 1.0
wing_offset_radius = 14.0 # Distance from center to start of wing

# 1. Create the main cylindrical body (hollow shell)
# We start with a solid cylinder, then shell it.
main_body = (
    cq.Workplane("XY")
    .circle(main_diameter / 2)
    .extrude(main_height)
)

# Apply fillet to the top edge before shelling to get smooth internal corners
main_body = main_body.edges(">Z").fillet(fillet_radius)

# Shell the body, opening the bottom face ("<Z")
main_body = main_body.faces("<Z").shell(-wall_thickness)


# 2. Create the Center Boss
# Select top face, draw circle, extrude up
center_boss = (
    main_body.faces(">Z")
    .workplane()
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)

# Cut the through-hole in the center boss
result_with_boss = (
    center_boss.faces(">Z")
    .workplane()
    .circle(boss_hole_diameter / 2)
    .cutBlind("next") # Cut through everything downwards
)


# 3. Create the Side Tabs (Wings)
# We will create one tab and mirror it or pattern it.
# Let's create a sketch for the tab on the top face.

def create_tab(loc):
    return (
        cq.Workplane("XY")
        .rect(wing_length, wing_width)
        .extrude(wing_thickness)
        .edges("|Z").fillet(wing_fillet) # Fillet vertical edges
        .edges(">Z").fillet(wing_fillet) # Fillet top edges
    )

# Position the tabs. Based on the image, they are 180 degrees apart.
# Let's place them on the X-axis.
tab_dist = wing_offset_radius + (wing_length/2)

tab_right = (
    cq.Workplane("XY")
    .workplane(offset=main_height) # Move to top of cylinder
    .center(tab_dist, 0)
    .rect(wing_length, wing_width)
    .extrude(wing_thickness)
    .edges().fillet(wing_fillet) # Apply generous fillet to smooth it out like the image
)

tab_left = (
    cq.Workplane("XY")
    .workplane(offset=main_height)
    .center(-tab_dist, 0)
    .rect(wing_length, wing_width)
    .extrude(wing_thickness)
    .edges().fillet(wing_fillet)
)

# Union the tabs to the main body
result_with_tabs = result_with_boss.union(tab_right).union(tab_left)


# 4. Create the Slotted Cutout
# Looking at the image, there is an obround/slot cut into the face.
# It sits on the Y-axis (perpendicular to tabs).

slot_cutout = (
    result_with_tabs.faces(">Z")
    .workplane()
    .center(0, -slot_offset) # Move down on Y axis
    .slot2D(slot_length, slot_width, angle=90) # 90 degree for vertical orientation
    .cutBlind(-wall_thickness * 2) # Cut through the wall
)

# 5. Final Lip/Rim detail on the bottom
# The image shows a small lip or flare at the bottom opening.
base_rim = (
    cq.Workplane("XY")
    .circle(main_diameter / 2 + 1.0) # Slightly larger
    .extrude(1.0) # Thin base
)
# Union this rim, but ensure the inside is still open
final_shape = slot_cutout.union(base_rim)
# Re-cut the main bore to ensure the rim didn't close it
final_shape = (
    final_shape.faces("<Z")
    .workplane()
    .circle((main_diameter / 2) - wall_thickness)
    .cutBlind(main_height)
)

result = final_shape