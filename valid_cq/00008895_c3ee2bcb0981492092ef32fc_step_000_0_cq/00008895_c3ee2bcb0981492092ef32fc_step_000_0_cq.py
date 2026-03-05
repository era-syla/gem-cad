import cadquery as cq

# --- Parameter Definitions ---
# Base dimensions
base_diameter = 80.0
base_thickness = 5.0

# Vertical housing dimensions
housing_height = 100.0
housing_outer_radius = 25.0  # Radius of the curved back
housing_width = 40.0         # Width of the rectangular front opening section
wall_thickness = 5.0

# Internal cutout dimensions (the U-shape)
inner_width = housing_width - (2 * wall_thickness)
inner_depth = 35.0 # Depth from front face to back wall inner surface

# Vertical slot/groove details (T-slot like features on the front edges)
slot_width = 2.0
slot_depth = 2.0
slot_offset = 2.0 # Distance from the outer edge

# --- Geometry Construction ---

# 1. Create the Circular Base
base = cq.Workplane("XY").circle(base_diameter / 2).extrude(base_thickness)

# 2. Create the Vertical Housing Profile
# The housing has a curved back (semi-circleish) and straight sides
# We'll sketch this on the top surface of the base

# Define the outer profile
# Center of the semi-circle part will be offset so the flat face is somewhat centered
center_offset = -10.0 

housing_sketch = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .moveTo(housing_width / 2, 0)
    .lineTo(housing_width / 2, center_offset)
    # Create the back arc. 
    # We go from (width/2, offset) to (-width/2, offset) via a point that defines the curve
    .threePointArc((0, center_offset - housing_outer_radius), (-housing_width / 2, center_offset))
    .lineTo(-housing_width / 2, 0)
    .close()
)

# Extrude the main solid block first
housing_solid = housing_sketch.extrude(housing_height)

# 3. Create the Internal Cavity (The large cutout)
# We want to remove material from the front face inward
cutout_width = housing_width - (2 * wall_thickness)
# We need to cut deep enough. Let's calculate based on the profile.
cutout_sketch = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .rect(cutout_width, inner_depth * 2, centered=(True, True)) # Draw a large rect
    .translate((0, inner_depth)) # Move it so it cuts from the front face inwards
)

# Cut the main cavity
housing_with_cavity = housing_solid.cut(cutout_sketch.extrude(housing_height))

# 4. Create the Vertical Grooves/Slots
# These are small indentations on the front vertical faces.
# Left Groove
left_groove = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .rect(slot_width, slot_depth, centered=(True, True))
    .translate((-housing_width/2 + wall_thickness/2, 0)) # Position on left wall face
)

# Right Groove
right_groove = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .rect(slot_width, slot_depth, centered=(True, True))
    .translate((housing_width/2 - wall_thickness/2, 0)) # Position on right wall face
)

# Cut the grooves
housing_final = (
    housing_with_cavity
    .cut(left_groove.extrude(housing_height))
    .cut(right_groove.extrude(housing_height))
)

# 5. Combine Base and Housing
# We also need to cut the base where the housing is open, to match the image
# The image shows the floor of the housing recessed into the base slightly or the base has a hole.
# Actually, looking closely, the "floor" inside the U-shape is at the same level as the base top, 
# but there is a rectangular depression in the base extending forward.

floor_cutout = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .rect(cutout_width, inner_depth + 10, centered=(True, False)) # Extra length for the front extension
    .translate((0, -10)) # Adjust start position
    .extrude(-1.0) # Cut down into the base slightly (e.g. 1mm deep recess)
)

result = base.union(housing_final).cut(floor_cutout)

# Export or display the result (optional line for local testing, typically user just wants 'result')
# cq.exporters.export(result, "vertical_housing.step")