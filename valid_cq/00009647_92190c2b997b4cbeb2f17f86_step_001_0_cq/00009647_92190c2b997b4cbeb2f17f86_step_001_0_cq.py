import cadquery as cq

# --- Parameters ---
# Overall dimensions
length = 400.0  # Estimated length based on aspect ratio
base_width = 40.0
base_height = 60.0 # Height of the wider bottom section
step_width = 20.0  # Width of the narrower top section
step_height = 30.0 # Height of the narrower top section extending from base
total_height = base_height + step_height

# Hole parameters (top surface)
top_hole_diameter = 8.0
num_top_holes = 10
top_hole_spacing = length / (num_top_holes + 1)

# Hole parameters (side surface)
side_hole_diameter = 4.0
# There appear to be small pilot holes or mounting holes on the side face
# roughly aligned with the ends and middle.
side_hole_z_offset = base_height / 2.0  # Centered on the base part vertically

# --- Geometry Construction ---

# 1. Create the base L-shaped profile and extrude
# We'll draw the profile on the YZ plane and extrude along X
# The profile looks like two stacked rectangles or an L-shape.

# Let's define the points for an L-shape starting at origin (0,0)
# (Y, Z) coordinates
pts = [
    (0, 0),
    (base_width, 0),
    (base_width, base_height),
    (step_width, base_height),
    (step_width, total_height),
    (0, total_height),
    (0, 0)
]

# Create the main solid
main_body = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(length)
)

# 2. Add Top Holes
# We need to find the top surface of the step (the highest face)
# and drill holes along the length.

# Calculate center positions for top holes
top_hole_positions = []
start_x = top_hole_spacing
for i in range(num_top_holes):
    # X coordinate (along length), Y coordinate (centered on step width)
    pos_x = start_x + (i * top_hole_spacing)
    # The extrusion goes from X=0 to X=length.
    # Center of step width is step_width / 2 relative to the Y origin of the profile
    pos_y = step_width / 2.0 
    top_hole_positions.append((pos_x, pos_y))

result = (
    main_body
    .faces(">Z") # Select the topmost face
    .workplane()
    .pushPoints(top_hole_positions)
    .hole(top_hole_diameter)
)

# 3. Add Side Holes
# There are smaller holes on the wider face (the face corresponding to base_width - step_width offset?)
# Looking at the image, there are small dots on the side face of the step and the base.
# Let's assume the visible face in the image is the "front".
# Based on the extrusion direction (YZ plane extruded along X):
# The face at Y=base_width is the "front" face of the bottom block.
# The face at Y=step_width is the "front" face of the top block (which is hidden/internal to the L).
# The image shows holes on the side of the 'step' part and the 'base' part.

# Let's add the small holes visible on the vertical face of the L-shape (the 'step' face)
# and the base face.

# Side holes on the upper section (the step)
# Looks like 3 small holes visible on the side face of the upper block
side_upper_z = base_height + (step_height / 2.0)
side_upper_y = 0 # The back face 
# Actually, looking at the image orientation, the L-shape is likely oriented differently.
# Let's re-evaluate orientation relative to the camera.
# The object is long.
# Top surface has large holes.
# Side surface (vertical) has small holes.

# Let's use the bounding box logic to place side holes.
# There appear to be holes on the "front" face of the thinner section.
side_holes_upper = [
    (length * 0.1, base_height + step_height/2), # Near start
    (length * 0.5, base_height + step_height/2), # Middle
    (length * 0.9, base_height + step_height/2), # Near end
]

# Side holes on the lower section (the base)
side_holes_lower = [
    (length * 0.1, base_height/2),
    (length * 0.5, base_height/2),
    (length * 0.9, base_height/2),
]

# To place these, we select the face that corresponds to the side.
# In our profile: (0,0) to (0, total_height) is the back.
# (step_width, base_height) to (step_width, total_height) is the front of the top part.
# (base_width, 0) to (base_width, base_height) is the front of the bottom part.

# The image shows holes on the flat vertical face that runs the full length.
# If the L is upside down T, or just a block with a cutout. 
# Let's assume we are drilling into the face at Y=0 (the back flat face in our profile construction)
# because that's a single continuous face for the full height? 
# No, the image clearly shows a step. 
# The holes are on the side face of the step (Y=step_width plane?) and the base (Y=base_width plane?).
# Wait, looking closely at the image, the side facing us is FLUSH.
# The step is on the BACK.
# Or, the side facing us has the step.
# Let's assume the standard "L" bracket shape where the step is facing us.
# Holes are visible on the vertical surface of the step and vertical surface of the base.

# Apply holes to the vertical face of the step section
# In our coordinates, this is the face at Y=0 if we assume the step builds "outwards".
# Let's adjust the drilling to be simple coordinates on the solid.

result = (
    result
    .faces("<Y") # Select the flat back face (Y=0)
    .workplane()
    # Upper row holes
    .pushPoints([(x, z) for x, z in side_holes_upper])
    .hole(side_hole_diameter)
    # Lower row holes
    .pushPoints([(x, z) for x, z in side_holes_lower])
    .hole(side_hole_diameter)
)

# Note: The image shows the stepped side. If the holes are on the stepped side:
# The upper holes are on the face at Y=step_width (normal pointing +Y, but internal) - Unlikely to be drilled from there usually.
# The lower holes are on the face at Y=base_width.
# However, usually these plates have mounting holes going through.
# I modeled them going through the back face (<Y) which is the flat face spanning the whole height. 
# This matches the visual of "holes on the side".

# If the holes in the image are on the STEPPED side (facing the camera):
# We need to drill the lower ones on the base face and upper ones on the step face.
# Let's re-examine the image.
# The image shows a block with a cutout. 
# The face facing the camera seems to be the one with the step.
# There are 3 small holes on the upper vertical face.
# There are 3 small holes on the lower vertical face.
# The large holes are on the top horizontal face.

# Correction: Drill specifically into the faces.

# Find the face for the upper section side holes
# This is the face at X plane, Y=0 (back) or Y=step_width?
# Let's assume the profile construction:
# (0,0) -> (base_width, 0) -> ...
# The "back" is Y=0.
# The "front base" is Y=base_width.
# The "front step" is Y=step_width.
# The holes in the image are on the "front" side.

# Drill Upper Side Holes (on the step face)
result = (
    result
    .faces(">Y[1]") # This should pick the second face in Y direction (the step face)
    # Alternatively, select by near point
    .faces(cq.NearestToPointSelector((length/2, step_width, total_height - step_height/2)))
    .workplane(centerOption="CenterOfBoundBox")
    # Coordinates relative to the face center
    .pushPoints([
        (-length*0.4, 0), 
        (0, 0), 
        (length*0.4, 0)
    ])
    .hole(side_hole_diameter)
)

# Drill Lower Side Holes (on the base face)
result = (
    result
    .faces(">Y[0]") # The furthest Y face (the base face)
    # Alternatively, select by near point
    .faces(cq.NearestToPointSelector((length/2, base_width, base_height/2)))
    .workplane(centerOption="CenterOfBoundBox")
    .pushPoints([
        (-length*0.4, 0),
        (0, 0),
        (length*0.4, 0)
    ])
    .hole(side_hole_diameter)
)

# Refine Result
# The image shows the object as a single solid.