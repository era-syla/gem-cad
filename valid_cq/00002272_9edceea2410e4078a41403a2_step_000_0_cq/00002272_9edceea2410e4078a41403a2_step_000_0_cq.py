import cadquery as cq

# --- Parametric Dimensions ---
# Shaft dimensions
shaft_diameter = 6.0
shaft_length = 50.0

# Head dimensions
head_diameter = 10.0
head_height = 10.0

# Cutout (flat) dimensions on the head
# The cut appears to make the head width narrower in one direction
flat_width_from_center = 4.0  # Distance from center to the flat face
# Alternatively, this could be the depth of cut. Let's assume a distance from center.

# Hole dimensions
hole_diameter = 3.0
hole_depth = 5.0 # It looks like a blind hole, but could be through. Let's make it blind based on typical pin designs.

# --- Modeling ---

# 1. Create the main shaft
shaft = cq.Workplane("XY").circle(shaft_diameter / 2.0).extrude(shaft_length)

# 2. Create the head on top of the shaft
# We select the top face of the shaft to start the head
head = (
    shaft.faces(">Z")
    .workplane()
    .circle(head_diameter / 2.0)
    .extrude(head_height)
)

# 3. Create the flat cut on the side of the head
# We'll cut a large rectangle that is positioned to slice off a segment of the cylinder
# flat_width_from_center defines the distance from the Z-axis to the cut plane.
# We need to cut everything beyond this distance.
cut_box_size = head_diameter * 2 # Make it large enough to cut completely
cut_offset = flat_width_from_center + (cut_box_size / 2.0)

result = (
    head.faces(">Z")
    .workplane()
    # Create the hole
    .hole(hole_diameter, depth=hole_depth)
    # Move to the position for the flat cut
    .workplane(centerOption="CenterOfMass")
    .transformed(offset=cq.Vector(flat_width_from_center, 0, -head_height/2))
    # We want to cut from the side.
    # Let's try a different approach: selecting the top face again and making a cut extrude
    .workplane(centerOption="CenterOfMass", origin=(0,0,shaft_length + head_height))
    .moveTo(flat_width_from_center, 0)
    .rect(cut_box_size, cut_box_size, centered=False) # Draw a big rectangle starting at the cut line
    .cutBlind(-head_height) # Cut downwards through the head
)

# Refined approach for the cut to ensure correct orientation based on visual
# The visual shows the flat on the side. 
# Let's rebuild the sequence cleanly.

# 1. Base Shaft
result = cq.Workplane("XY").circle(shaft_diameter / 2).extrude(shaft_length)

# 2. Head
result = result.faces(">Z").workplane().circle(head_diameter / 2).extrude(head_height)

# 3. Central Hole
result = result.faces(">Z").workplane().hole(hole_diameter, hole_depth)

# 4. Flat on the head
# We want to cut a chunk off the side. A simple way is to draw a rectangle on the top face
# that overlaps the area to remove.
# Let's assume the flat reduces the radius on one side.
# Distance from center to flat face
dist_to_flat = 3.5 # Adjusted visually relative to likely 10mm head
cut_rect_width = head_diameter
cut_rect_height = head_diameter 

result = (
    result.faces(">Z")
    .workplane()
    # Move origin to the "flat" line location
    .center(dist_to_flat, 0)
    # Draw a rectangle that covers the area to be removed. 
    # Since we centered at (dist_to_flat, 0), drawing a rect centered=False 
    # will extend into positive X and positive/negative Y if defined right.
    # But rect(centered=True) is easier. Let's shift center to the middle of the material to remove.
    .center(cut_rect_width/2, 0)
    .rect(cut_rect_width, cut_rect_height)
    .cutBlind(-head_height)
)

# Export or visualization would happen here normally
# show_object(result)