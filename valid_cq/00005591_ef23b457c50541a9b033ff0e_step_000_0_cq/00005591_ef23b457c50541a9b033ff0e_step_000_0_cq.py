import cadquery as cq

# Parametric dimensions for a smartphone model (approx. iPhone 5/SE style)
height = 123.8
width = 58.6
thickness = 7.6
corner_radius = 8.0
chamfer_size = 0.6  # Diamond cut edges

# Screen dimensions
screen_margin_side = 4.0
screen_margin_top_bottom = 16.0
screen_depth = 0.1

# Home button dimensions
home_button_y_offset = -(height/2) + (screen_margin_top_bottom/2)
home_button_radius = 5.0
home_button_depth = 0.2
home_button_square_side = 3.5

# Top Speaker/Camera area
speaker_width = 8.0
speaker_height = 1.5
speaker_y_offset = (height/2) - (screen_margin_top_bottom/2)
camera_radius = 1.5
camera_x_offset = -6.0

# Side buttons (Volume & Mute)
mute_switch_height = 4.0
mute_switch_width = 2.0
mute_switch_y = height/2 - 20
vol_button_radius = 2.0
vol_up_y = mute_switch_y - 10
vol_down_y = vol_up_y - 10
button_protrusion = 0.5

# Top Power Button
power_button_width = 8.0
power_button_depth = 2.5
power_button_x = width/4

# --- Modeling ---

# 1. Main Body
# Extrude basic rounded rectangle
main_body = (
    cq.Workplane("XY")
    .rect(width, height)
    .extrude(thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# Apply chamfers to top and bottom edges (characteristic of this design)
main_body = (
    main_body.edges("#Z") # Select edges perpendicular to Z (top and bottom faces)
    .chamfer(chamfer_size)
)

# 2. Screen Area
# Create a recess for the screen
screen_width = width - (2 * screen_margin_side)
screen_height = height - (2 * screen_margin_top_bottom)

screen_cutout = (
    cq.Workplane("XY")
    .workplane(offset=thickness)
    .rect(screen_width, screen_height)
    .extrude(-screen_depth)
)

result = main_body.cut(screen_cutout)

# 3. Home Button
# Circular concave area
home_cutout = (
    cq.Workplane("XY")
    .workplane(offset=thickness)
    .center(0, home_button_y_offset)
    .circle(home_button_radius)
    .extrude(-home_button_depth)
)
result = result.cut(home_cutout)

# Square symbol on home button
home_square = (
    cq.Workplane("XY")
    .workplane(offset=thickness - home_button_depth)
    .center(0, home_button_y_offset)
    .rect(home_button_square_side, home_button_square_side)
    .extrude(0.05) # Slightly raised or just a surface feature
    .edges("|Z").fillet(0.5) # Soften the square edges
)
result = result.union(home_square)

# 4. Ear Speaker and Front Camera
speaker_slot = (
    cq.Workplane("XY")
    .workplane(offset=thickness)
    .center(0, speaker_y_offset)
    .rect(speaker_width, speaker_height)
    .extrude(-0.5)
    .edges("|Z").fillet(0.5)
)
result = result.cut(speaker_slot)

front_camera = (
    cq.Workplane("XY")
    .workplane(offset=thickness)
    .center(camera_x_offset, speaker_y_offset)
    .circle(camera_radius/2)
    .extrude(-0.5)
)
result = result.cut(front_camera)

# 5. Side Buttons (Left Side) - Mute Switch, Volume Up, Volume Down
# We need to construct these on the side face (YZ plane relative to the object)

# Mute Switch (rectangular)
mute_switch = (
    cq.Workplane("YZ")
    .workplane(centerOption="CenterOfMass", offset=-(width/2)) # Left side
    .center(mute_switch_y, thickness/2)
    .rect(mute_switch_height, mute_switch_width) # Swapped because of orientation
    .extrude(-button_protrusion) 
)
result = result.union(mute_switch)

# Volume Up (Circular)
vol_up = (
    cq.Workplane("YZ")
    .workplane(centerOption="CenterOfMass", offset=-(width/2))
    .center(vol_up_y, thickness/2)
    .circle(vol_button_radius)
    .extrude(-button_protrusion)
)
result = result.union(vol_up)

# Volume Down (Circular)
vol_down = (
    cq.Workplane("YZ")
    .workplane(centerOption="CenterOfMass", offset=-(width/2))
    .center(vol_down_y, thickness/2)
    .circle(vol_button_radius)
    .extrude(-button_protrusion)
)
result = result.union(vol_down)

# 6. Power Button (Top Edge)
power_btn = (
    cq.Workplane("XZ")
    .workplane(centerOption="CenterOfMass", offset=(height/2)) # Top side
    .center(power_button_x, thickness/2)
    .rect(power_button_width, power_button_depth)
    .extrude(button_protrusion)
    .edges("|Y").fillet(0.5)
)
result = result.union(power_btn)

# 7. Antenna Bands (Cosmetic cuts on the sides)
# Two thin lines near top and bottom on the back/sides
band_thickness = 0.5
band_depth = 0.05
top_band_y = (height/2) - 8
bottom_band_y = -(height/2) + 8

# A simple way to represent these is slicing thin cuts, but to keep geometry simple
# and robust, we will just leave the solid form as is, as they are flush in reality.
# Instead, let's ensure the main body shape is refined.

# Final cleanup/refining
# Re-apply chamfer to buttons for realistic look if needed, but the current scale is small.
result = result.combine()