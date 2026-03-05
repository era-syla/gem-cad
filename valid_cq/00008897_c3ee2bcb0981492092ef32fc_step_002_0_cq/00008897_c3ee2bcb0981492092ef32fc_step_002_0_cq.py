import cadquery as cq

# --- Parameters ---
# Overall dimensions based on visual estimation
base_diameter = 50.0
base_thickness = 4.0
cylinder_outer_diameter = 34.0
cylinder_height = 80.0
wall_thickness = 3.0

# Groove/Slot details (for sliding something in)
slot_width = 3.0
slot_depth = 2.0
open_width = 20.0  # Width of the front opening

# --- Construction ---

# 1. Base Plate
# Create a circular base
base = cq.Workplane("XY").circle(base_diameter / 2.0).extrude(base_thickness)

# 2. Main Cylindrical Body
# Create the main cylinder starting from the top of the base
body_sketch = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .circle(cylinder_outer_diameter / 2.0)
    .extrude(cylinder_height)
)

# 3. Create the Inner Cavity (The U-shape)
# We need to cut a U-shape out of the cylinder. 
# This looks like a rectangle combined with a slot.
# Let's calculate the inner dimensions.
inner_radius = (cylinder_outer_diameter / 2.0) - wall_thickness
box_width = cylinder_outer_diameter # Wide enough to cut through
cutout_depth = (cylinder_outer_diameter / 2.0) + 5.0 # Deep enough to clear front

# Create a cutting tool for the main opening
# We'll center a rectangle that cuts out the front and center
cutout_shape = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .rect(open_width, cutout_depth * 2) # Width is the opening width, Depth is large
    .extrude(cylinder_height)
    # Move it forward to cut the front face
    .translate((0, -cylinder_outer_diameter/2.0, 0)) 
)

# 4. Create the Internal Profile with Grooves
# Instead of simple subtraction, it's better to sketch the specific "C" or "U" profile with the grooves.
# Let's define the cross-section of the vertical pillar.

# Calculate points for the profile sketch
r_out = cylinder_outer_diameter / 2.0
r_in = r_out - wall_thickness
groove_w = slot_width
groove_d = slot_depth
opening_half_w = open_width / 2.0

# We will sketch the shape to be EXTRUDED (the wall itself), rather than cutting.
# This is often more robust.
def create_profile_sketch(plane):
    return (
        plane
        # Outer semi-circle
        .moveTo(r_out, 0)
        .threePointArc((0, r_out), (-r_out, 0))
        .lineTo(-r_out, -r_out) # Extend back slightly if needed, but the image shows a flat back cut?
                                # Actually, looking closer, it's a cylinder cut flat at the front.
                                # Let's stick to the subtractive method or a complex sketch.
                                # Sketch approach:
        # Start at front-right outer edge
        .moveTo(opening_half_w, -r_out) # Assuming front is -Y
        .lineTo(opening_half_w, 0)      # Go to center-ish
        # ... this is getting complex coordinate math. 
        # Let's go back to Subtractive Constructive Solid Geometry (CSG), it's easier to read.
    )

# --- Revised CSG Strategy ---

# Step 1: Base
result = cq.Workplane("XY").circle(base_diameter / 2.0).extrude(base_thickness)

# Step 2: The Main Vertical Cylinder (Solid)
pillar = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .circle(cylinder_outer_diameter / 2.0)
    .extrude(cylinder_height)
)

# Step 3: Cut the Main Internal Pocket (Rectangular prism)
# The pocket seems to be square/rectangular inside the round exterior.
pocket_side = (cylinder_outer_diameter) - (2 * wall_thickness)
# We need to position this pocket. It looks like it goes through the center.
# But wait, there are T-slots/grooves.

# Let's make a custom "Cutting Tool" profile that represents the negative space.
# The negative space is a rectangle with two tabs sticking out (forming the grooves in the positive).
cut_width_main = open_width
cut_depth_main = cylinder_outer_diameter # Make it deep enough
groove_offset = 2.0 # Distance from the front face into the groove

# Define the negative shape on the XY plane
cutter_sketch = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .moveTo(-open_width/2.0, -cylinder_outer_diameter/2.0) # Front Left
    .lineTo(-open_width/2.0, cylinder_outer_diameter/2.0 - wall_thickness) # Back Left (inside wall)
    .lineTo(open_width/2.0, cylinder_outer_diameter/2.0 - wall_thickness)  # Back Right
    .lineTo(open_width/2.0, -cylinder_outer_diameter/2.0) # Front Right
    .close()
    .extrude(cylinder_height)
)

# Create the T-slot/Groove cutters
# These are wider rectangles placed along the sides of the main cut
groove_cutter_left = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .rect(slot_depth, slot_width) # A small rectangle
    .extrude(cylinder_height)
    .translate((-open_width/2.0 - slot_depth/2.0, 0, 0)) # Position on left wall
)

groove_cutter_right = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .rect(slot_depth, slot_width)
    .extrude(cylinder_height)
    .translate((open_width/2.0 + slot_depth/2.0, 0, 0)) # Position on right wall
)

# Combine the cutters
full_cutter = cutter_sketch.union(groove_cutter_left).union(groove_cutter_right)

# 4. Perform the Cut on the Pillar
pillar = pillar.cut(full_cutter)

# 5. Trim the front of the Cylinder to make it flat
# The image shows the cylinder is flattened at the front face (where the opening is)
front_trim = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .rect(cylinder_outer_diameter * 2, cylinder_outer_diameter)
    .extrude(cylinder_height)
    .translate((0, -cylinder_outer_diameter, 0)) # Move completely in front
)
# Adjust position to slice just at the opening width
y_cutoff = - (open_width / 2.0) # Heuristic: usually flat face aligns with opening? 
# Looking at the image, the flat face is distinct from the inner cutout.
# Let's assume the flat face is at Y = -10 (approx)
flat_face_y = -10.0
front_trim = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .rect(cylinder_outer_diameter * 2, cylinder_outer_diameter)
    .extrude(cylinder_height)
    .translate((0, -cylinder_outer_diameter/2.0 - 15.0, 0)) # Move way front
)
# Actually, simply cutting a box from the front works best.
# The face seems to be tangential to the opening or slightly set back.
# Let's define the flat face based on coordinate geometry.
# We cut everything with Y < -something.
flattening_tool = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .moveTo(-cylinder_outer_diameter, -10.0) # Start left, slightly back from center
    .lineTo(cylinder_outer_diameter, -10.0)
    .lineTo(cylinder_outer_diameter, -cylinder_outer_diameter*2)
    .lineTo(-cylinder_outer_diameter, -cylinder_outer_diameter*2)
    .close()
    .extrude(cylinder_height)
)

# Re-evaluating the image:
# The shape is a 'C' channel with a curved back.
# The internal cut is rectangular.
# The front faces are flat.
# There are grooves inside the vertical walls.

# Let's do a pure sketch based extrusion for the vertical part. It's cleaner.

# Center of circle at (0,0)
# Outer Radius = 17
# Inner "Box" width = 20
# Inner "Box" length = goes back to near the rear wall.
# Wall thickness = 3.

# Define the 2D profile of the vertical walls
pillar_profile = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .moveTo(open_width/2.0, -10) # Front Right Face
    .lineTo(open_width/2.0, 0)   # Into the wall
    # Right Groove
    .lineTo(open_width/2.0 + slot_depth, 0) 
    .lineTo(open_width/2.0 + slot_depth, slot_width)
    .lineTo(open_width/2.0, slot_width)
    # Continue back wall right side
    .lineTo(open_width/2.0, 15) # Arbitrary depth back
    .lineTo(-open_width/2.0, 15) # Across the back
    # Left side mirror
    .lineTo(-open_width/2.0, slot_width)
    .lineTo(-open_width/2.0 - slot_depth, slot_width)
    .lineTo(-open_width/2.0 - slot_depth, 0)
    .lineTo(-open_width/2.0, 0)
    .lineTo(-open_width/2.0, -10) # Front Left Face
    # Close shape with outer arc
    .threePointArc((0, cylinder_outer_diameter/2.0), (open_width/2.0, -10)) # This is tricky to get perfect arc
    .close()
)

# Correct approach: Difference of Solids.
# 1. Cylinder
cyl = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .circle(cylinder_outer_diameter/2.0)
    .extrude(cylinder_height)
)

# 2. Front Flat Cut (The chord)
# We want the flat face to start where the opening width matches the chord length? 
# No, let's just cut the front off at a specific Y.
front_cut_y = -cylinder_outer_diameter/2.0 + 4.0 # 4mm from front tangent
front_cutter = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .rect(cylinder_outer_diameter*2, cylinder_outer_diameter)
    .extrude(cylinder_height)
    .translate((0, -cylinder_outer_diameter/2.0 - (cylinder_outer_diameter/2.0 + front_cut_y), 0))
)
cyl = cyl.cut(front_cutter)

# 3. Inner Rectangular Pocket
pocket_depth = cylinder_outer_diameter - wall_thickness - abs(front_cut_y)
pocket = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .rect(open_width, cylinder_outer_diameter) # Depth is exaggerated to ensure cut
    .extrude(cylinder_height)
    .translate((0, 5, 0)) # Shift back to leave wall thickness at rear
)

# 4. Grooves
# Vertical slots on the sides of the pocket
groove_l = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .rect(slot_depth * 2, slot_width) # width, height (in 2d)
    .extrude(cylinder_height)
    .translate((-open_width/2.0, 5, 0)) # Position relative to pocket center
)
groove_r = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .rect(slot_depth * 2, slot_width)
    .extrude(cylinder_height)
    .translate((open_width/2.0, 5, 0))
)

# Apply cuts
cyl = cyl.cut(pocket).cut(groove_l).cut(groove_r)

# 5. Base Indentation
# The image shows a rectangular indentation on the base plate matching the inner pocket.
base_indent = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness - 1.0) # Start 1mm below top of base
    .rect(open_width, cylinder_outer_diameter/2.0 + 5) # Roughly matching the pocket footprint
    .extrude(1.0)
    .translate((0, 5, 0))
)
# Need to match the exact pocket footprint for the indent
# Let's recreate the union of pocket + grooves for the base indent
footprint_sketch = (
    cq.Workplane("XY")
    .rect(open_width, cylinder_outer_diameter)
    .translate((0, 5, 0))
)
# Since we can't easily union sketches in this chain without variables, let's just use the solids.
indent_solid = pocket.union(groove_l).union(groove_r)
# Move it down to intersect the base
indent_solid = indent_solid.translate((0,0, -cylinder_height + (base_thickness - 1.0) - base_thickness))
# Actually, simpler to just re-extrude
base_cutout_shape = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness - 1.5)
    .rect(open_width, cylinder_outer_diameter) # Main pocket area
    .extrude(1.5)
    .translate((0, 5, 0))
)

# Combine Final Result
result = base.union(cyl).cut(base_cutout_shape)

# Chamfer the base bottom edge for aesthetics (visible in image)
try:
    result = result.edges(cq.selectors.NearestToPointSelector((0,0,0))).chamfer(1.0)
except:
    pass # Fallback if selection fails

# Fillet the top opening edges slightly
try:
    result = result.edges("|Z").filter(lambda e: e.Center().z > base_thickness + 10).fillet(0.5)
except:
    pass