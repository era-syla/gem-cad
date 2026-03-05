import cadquery as cq

# --- Parameter Definitions ---
# Overall dimensions
shaft_width = 10.0
shaft_thickness = 4.0
shaft_length = 150.0

# Top "Pick" head dimensions
head_width_total = 100.0  # Tip to tip width
head_center_height = 20.0
head_tip_height = 10.0
head_curve_radius = 80.0  # Radius for the curved top/bottom of the head
top_nub_width = 12.0
top_nub_height = 5.0
hole_diameter = 4.0

# Slider/Stop dimensions
slider_width = 25.0
slider_height = 10.0
slider_thickness = 8.0
slider_pos_from_bottom = 60.0

# --- Modeling ---

# 1. Create the main vertical shaft
# Use the center of the top face as the origin for Z to make positioning easier
shaft = (
    cq.Workplane("XY")
    .rect(shaft_width, shaft_thickness)
    .extrude(-shaft_length)
)

# 2. Create the curved "Pick" head
# We will draw the profile on the front face (XZ plane) and extrude
head_profile = (
    cq.Workplane("XZ")
    .workplane(offset=-shaft_thickness / 2) # Align with back of shaft
    .moveTo(0, 0)
    
    # Draw the profile
    # Start at center bottom of the head connection
    .lineTo(shaft_width / 2, 0)
    .lineTo(shaft_width / 2, -10) # Small overlap down the shaft for strength
    .lineTo(-shaft_width / 2, -10)
    .lineTo(-shaft_width / 2, 0)
    .lineTo(0, 0) # Back to center
    
    # Now draw the main arc shape
    .moveTo(-shaft_width / 2, 0)
    # Left arm curve
    .threePointArc((-head_width_total/4, head_center_height/2), (-head_width_total/2, -head_tip_height))
    .lineTo(-head_width_total/2, -head_tip_height + 5) # Thickness at tip
    # Top curve left side
    .threePointArc((-head_width_total/4, head_center_height), (-top_nub_width/2, head_center_height))
    # Top Nub
    .lineTo(-top_nub_width/2, head_center_height + top_nub_height)
    .lineTo(top_nub_width/2, head_center_height + top_nub_height)
    .lineTo(top_nub_width/2, head_center_height)
    # Top curve right side
    .threePointArc((head_width_total/4, head_center_height), (head_width_total/2, -head_tip_height + 5))
    .lineTo(head_width_total/2, -head_tip_height)
    # Right arm curve
    .threePointArc((head_width_total/4, head_center_height/2), (shaft_width/2, 0))
    .close()
    .extrude(shaft_thickness)
)

# Cut the hole in the head
head_with_hole = (
    head_profile
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .moveTo(0, head_center_height - 5) # Approximate position based on image
    .hole(hole_diameter)
)


# 3. Create the Slider/Stop
# This is a separate block partway down the shaft
slider = (
    cq.Workplane("XY")
    .workplane(offset=-(shaft_length - slider_pos_from_bottom))
    .rect(slider_width, slider_thickness)
    .extrude(slider_height)
)

# Cut the shaft slot out of the slider
# We create a slightly larger box than the shaft to represent the hole, 
# but since this is a boolean union in the final single-part representation,
# we model it as if it's a solid piece attached to the shaft or slid onto it.
# Based on the image, it looks like a single assembly or print.
# Let's make the slider hollow to accept the shaft.
slider_hollow = (
    slider
    .faces(">Z")
    .workplane()
    .rect(shaft_width + 0.5, shaft_thickness + 0.5) # Slight tolerance or visual gap
    .cutBlind(-slider_height)
)

# --- Combine Parts ---
# Union the shaft and the head
part1 = shaft.union(head_with_hole)

# Union the slider
# Note: In a real assembly, the slider might be a separate object.
# The image shows them as one distinct set of geometries. 
# We will combine them into one result object.
result = part1.union(slider_hollow)

# Export for visualization (optional in script, but good practice)
# cq.exporters.export(result, "tool.step")