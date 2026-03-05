import cadquery as cq

# Parametric dimensions
box_length = 150.0  # Total length of the box
box_width = 80.0    # Total width of the box
box_height = 40.0   # Total height of the box
wall_thickness = 10.0 # Thickness of the walls (looks fairly thick)
floor_thickness = 5.0 # Thickness of the bottom

# Flange details (the side walls with holes)
flange_hole_count = 10
flange_hole_diameter = 4.0
flange_hole_margin = 5.0 # Distance from edge to hole center (approx)

# Cutout details for the small notch on the short side
notch_width = 15.0
notch_depth = 5.0
notch_height = 5.0 # How far down it cuts

# Create the main block
base = cq.Workplane("XY").box(box_length, box_width, box_height)

# Create the inner cutout to make it a box/container
# We subtract a smaller box from the top face
interior_length = box_length - (2 * wall_thickness)
interior_width = box_width - (2 * wall_thickness)
# Note: The short sides seem to have thicker walls or the flange area is the wall.
# Let's assume uniform wall thickness for the long sides, but check the short sides.
# Looking closely, the "back" short side is flush with the top. The "front" short side is also a wall.
# The long sides act like flanges.

# Let's refine the shell strategy.
# It looks like a solid block with a large rectangular pocket milled out.
pocket_length = box_length - 2 * wall_thickness
pocket_width = box_width - 2 * wall_thickness
pocket_depth = box_height - floor_thickness

# Create the main hollowed-out shape
main_body = (
    base
    .faces(">Z")
    .workplane()
    .rect(pocket_length, pocket_width)
    .cutBlind(-pocket_depth)
)

# Add the row of holes on the long sides (flanges)
# We need two rows of holes.
# Calculate spacing for the holes
long_side_length = box_length
# Distance between first and last hole centers
hole_span = long_side_length - (2 * wall_thickness/2) # Start/end roughly centered on corner block area?
# Actually, let's just use regular spacing along the rim.
hole_y_offset = (box_width / 2) - (wall_thickness / 2)

# Create points for the holes
# Left side holes (negative Y)
left_holes = (
    main_body
    .faces(">Z")
    .workplane()
    .rarray(
        xSpacing=(box_length - 20) / (flange_hole_count - 1), 
        ySpacing=1, 
        xCount=flange_hole_count, 
        yCount=1, 
        center=True
    )
    .translate((0, -hole_y_offset, 0)) # Move to the correct Y side
    .hole(flange_hole_diameter)
)

# Right side holes (positive Y)
# We can just continue from the previous object or perform the same operation
result_with_holes = (
    left_holes
    .faces(">Z")
    .workplane()
    .rarray(
        xSpacing=(box_length - 20) / (flange_hole_count - 1), 
        ySpacing=1, 
        xCount=flange_hole_count, 
        yCount=1, 
        center=True
    )
    .translate((0, hole_y_offset, 0)) # Move to the other Y side
    .hole(flange_hole_diameter)
)

# Create the small notch on the short side wall
# It appears on one of the short ends (let's say -X side)
# It cuts into the top rim.
result = (
    result_with_holes
    .faces(">Z")
    .workplane()
    .translate((-box_length/2 + wall_thickness/2, 0, 0)) # Position on the short wall
    .rect(wall_thickness + 2, notch_width) # Make rectangle wide enough to cut through wall
    .cutBlind(-notch_depth)
)