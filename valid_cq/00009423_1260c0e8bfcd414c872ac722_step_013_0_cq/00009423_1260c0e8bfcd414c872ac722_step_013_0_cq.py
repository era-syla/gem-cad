import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions based on visual estimation
total_length = 80.0
total_height = 30.0
total_thickness = 20.0

# Central block dimensions
center_width = 30.0
center_drop = 15.0  # How far the center hangs down below the wings

# V-groove / Dovetail dimensions
groove_top_width = 16.0
groove_depth = 12.0
groove_angle = 60.0 # Standard dovetail/V-groove angle

# Side wing holes
hole_diameter = 6.0
hole_offset_x = (total_length - center_width) / 4.0 + center_width / 2.0  # Centered in the wing
hole_height_z = (total_height - center_drop) / 2.0 # Centered vertically in the wing

# --- Modeling ---

# 1. Create the base shape.
# We will draw the front profile and extrude it.
# The profile looks like a "T" shape but upside down, or a block with wings.

# Let's define the profile points relative to the center origin (0,0) at the top middle.
# Coordinates are (x, y)
pts = [
    (-total_length / 2, 0),                        # Top left corner
    (total_length / 2, 0),                         # Top right corner
    (total_length / 2, -(total_height - center_drop)), # Right wing bottom
    (center_width / 2, -(total_height - center_drop)), # Right wing inner corner
    (center_width / 2, -total_height),             # Center block bottom right
    (-center_width / 2, -total_height),            # Center block bottom left
    (-center_width / 2, -(total_height - center_drop)),# Left wing inner corner
    (-total_length / 2, -(total_height - center_drop)) # Left wing bottom
]

base = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .extrude(total_thickness)
)

# 2. Create the Dovetail/V-groove Cut
# We will sketch the triangle/trapezoid on the top face and cut through.
# The image shows a cut that gets narrower as it goes deeper.
# It looks like a simple trapezoidal dovetail slot.

# Calculate the bottom width based on the angle (assuming symmetric)
import math
groove_bottom_width = groove_top_width - 2 * (groove_depth / math.tan(math.radians(groove_angle)))

# Let's verify the visual look. The image actually looks more like a V-block cut 
# where the sides slope inwards. It might just be a V-cut with a flat bottom.
# Let's define the trapezoid points for the cut profile on the front face (XZ plane).
# The cut starts at the top edge (y=0) and goes down.

cut_pts = [
    (-groove_top_width / 2, 0),
    (groove_top_width / 2, 0),
    (groove_bottom_width / 2, -groove_depth),
    (-groove_bottom_width / 2, -groove_depth)
]

# We need to orient this cut correctly. The previous extrusion was along Y.
# So we select the front face of the object to sketch on, or just use the same plane logic.
# Since we extruded along Y (positive), the object is from y=0 to y=total_thickness.
# Let's just cut the initial shape.

result = (
    base
    .faces(">Z") # Select the top face
    .workplane()
    .center(0, 0)
    # Drawing the trapezoid profile for the swept cut or simple sketch extrusion
    # Actually, it's easier to draw the profile on the side (XZ) and cut across Y?
    # No, the previous profile was drawn on XZ.
    # Let's go back to the base Workplane("XZ") approach to add the cut there.
    # But cutting an existing solid is often easier.
    
    # Let's draw the cut profile on the front face (XZ plane essentially) and cut-extrude.
    # We need to make sure we are cutting through the thickness.
)

# Re-doing the cut logic for clarity:
# Create a cutter solid
cutter = (
    cq.Workplane("XZ")
    .polyline(cut_pts)
    .close()
    .extrude(total_thickness)
)

result = base.cut(cutter)

# 3. Add Mounting Holes
# The holes are on the side wings, going through the thickness (Y axis).
# We can select the front faces of the wings or just use coordinates.

result = (
    result
    .faces(">Y") # Select the front face (positive Y)
    .workplane()
    # Position for the right hole
    .pushPoints([(hole_offset_x, -(total_height - center_drop) / 2.0),
                 (-hole_offset_x, -(total_height - center_drop) / 2.0)])
    .hole(hole_diameter)
)

# Note on the image: The cut seems to have a flat bottom, consistent with the trapezoidal code above.
# The orientation in the viewer will match the XZ draw plane, extruded along Y.