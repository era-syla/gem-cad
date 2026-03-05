import cadquery as cq

# --- Parameter Definitions ---
# Main block dimensions
unit_size = 20.0  # Basic unit for grid alignment (estimated)
block_height = 10.0
arm_width = 10.0
arm_length = 30.0

# Hole parameters
hole_dia = 5.0
counterbore_dia = 8.0 # For hex cutouts or larger openings
hex_size = 8.0 # Flat-to-flat distance
hex_depth = 3.0

# Stack parameters
num_layers = 4
gap_height = 10.0 # Vertical spacing between certain layers

# --- Helper Functions ---

def create_y_connector():
    """
    Creates a single Y-shaped connector component.
    The shape consists of a central hub and three arms extending out.
    """
    # Create the central body and arms
    # We'll sketch the profile on the XY plane and extrude it
    
    # Define points for a Y-shape profile
    # Center is at origin
    # Arm 1: +X
    # Arm 2: +Y
    # Arm 3: -X, but shifted
    
    # Let's model it as a union of rectangles for simplicity and robustness
    
    # Center hub
    center = cq.Workplane("XY").box(unit_size, unit_size, block_height)
    
    # Arm extending +X
    arm_x = cq.Workplane("XY").center(unit_size/2 + arm_length/2 - 2, 0).box(arm_length, arm_width, block_height)
    
    # Arm extending +Y
    arm_y = cq.Workplane("XY").center(0, unit_size/2 + arm_length/2 - 2).box(arm_width, arm_length, block_height)

    # Arm extending -Y (Wait, looking at image, it's roughly T or Y shaped)
    # Let's look closer at the image.
    # It looks like a central block with arms.
    # Top-most piece:
    # - Has an arm going Right (+X)
    # - Has an arm going Back (+Y)
    # - Has an arm going Left (-X) but it's offset? 
    # Actually, it looks like a "Corner Piece" (L-shape) plus extensions.
    
    # Let's try to construct one unique geometric element that is repeated/stacked.
    # The geometry appears to be a 3-way vertex.
    # Let's assume a central cube.
    # 1. Arm extending +X. End of arm has a perpendicular tab.
    # 2. Arm extending +Y.
    # 3. Arm extending -X.
    
    # Let's refine the shape based on the visible features:
    # Central junction.
    # Arm 1 (Right): Rectangular, hole in top, hex socket on end face.
    # Arm 2 (Back): Rectangular, hole in top, hex socket on end face.
    # Arm 3 (Front/Left): This looks like the mating interface.
    
    thickness = 10.0
    width = 10.0
    length_short = 20.0
    length_long = 35.0
    
    # Base shape: A cross or T shape
    base = cq.Workplane("XY")
    
    # 1. Main horizontal beam (X-axis)
    # The beam seems to go from x=-15 to x=+35
    beam_x = base.box(60, width, thickness)
    
    # 2. Vertical beam (Y-axis) attached to the +X side
    # It sticks out in +Y direction
    beam_y = base.center(15, 15).box(width, 20, thickness)
    
    combined = beam_x.union(beam_y)
    
    # --- Fillets ---
    # There are fillets at the internal corners
    combined = combined.edges("|Z").fillet(2.0)
    
    # --- Holes ---
    # Top vertical holes
    # Hole on +X arm
    combined = combined.faces(">Z").workplane().center(15, 0).hole(hole_dia)
    # Hole on +Y arm
    combined = combined.faces(">Z").workplane().center(15, 15).hole(hole_dia)
    # Hole on -X arm
    combined = combined.faces(">Z").workplane().center(-15, 0).hole(hole_dia)
    
    # --- Hex Sockets / Side holes ---
    # Hex socket on the end of the +Y arm
    combined = combined.faces(">Y").workplane().polygon(6, hex_size).cutBlind(-hex_depth)
    combined = combined.faces(">Y").workplane().hole(hole_dia)
    
    # Hex socket on the end of the +X arm
    combined = combined.faces(">X").workplane().polygon(6, hex_size).cutBlind(-hex_depth)
    combined = combined.faces(">X").workplane().hole(hole_dia)
    
    # The -X end has a square protrusion plate?
    # Looking at the left side of the image, there is a square plate with a square hole.
    # It seems to be attached to the -X end.
    
    plate_size = 16.0
    plate_thickness = 4.0
    
    # Create the plate on the -X face
    plate = (cq.Workplane("YZ")
             .workplane(offset=-30) # Move to the end of the beam (approx -30)
             .box(plate_size, plate_size, plate_thickness)
             )
    
    # Add square hole to plate
    plate = plate.faces("<X").workplane().rect(6, 6).cutBlind(-10) # Through cut
    
    # Union the plate to the main body
    # We need to position the plate correctly. The beam_x was centered at origin.
    # length was 60, so ends are at -30 and +30.
    # The box command centers the object, so workplane offset needs to handle placement.
    
    # Let's attach the plate properly
    final_part = combined.union(plate)
    
    # There are hex sockets on the SIDE faces of the beams too (along Y axis faces of X-beam)
    # Side hole on the X-beam (facing -Y)
    final_part = final_part.faces("<Y").workplane().center(15, 0).polygon(6, hex_size).cutBlind(-hex_depth)
    final_part = final_part.faces("<Y").workplane().center(15, 0).hole(hole_dia)

    # Side hole on the X-beam (facing -Y) near the other end
    final_part = final_part.faces("<Y").workplane().center(-15, 0).polygon(6, hex_size).cutBlind(-hex_depth)
    final_part = final_part.faces("<Y").workplane().center(-15, 0).hole(hole_dia)

    # There is a small conical pin sticking out of the +X end face corner?
    # Visible on the top right component.
    # Let's add that detail.
    pin = (cq.Workplane("YZ")
           .workplane(offset=30)
           .center(3, 0) # Offset from center
           .circle(1.5).workplane(offset=3).circle(1.0)
           .loft()
           )
    
    final_part = final_part.union(pin)

    return final_part

# --- Assembly Construction ---

# Generate the base component
part = create_y_connector()

# Create the assembly by stacking and rotating
# The image shows 4 units in a specific configuration.
# 1. Bottom Unit
# 2. Middle Unit (Looks identical to bottom, just stacked on top)
# 3. Another Middle Unit
# 4. Top Unit 
# Wait, looking closely:
# The bottom unit is isolated.
# Then there is a gap.
# Then a stack of 3 units directly on top of each other.

# Let's organize the positions.
# Result accumulator
result = cq.Assembly()

# Unit 1 (Bottom)
# It's oriented with the Y-arm pointing "Back-Right" in the view?
# Let's assume standard orientation and rotate the view later.
# In the image, the bottom unit has the square plate on the left.
result = part

# Stack of 3 units above it.
# There is a vertical gap.
vertical_pitch = 10.0 # Height of the block
stack_gap = 10.0 # Visual gap between bottom block and the stack

# Unit 2 (First in stack)
pos2 = cq.Location(cq.Vector(0, 0, vertical_pitch + stack_gap))
part2 = part.val().moved(pos2)
result = result.union(part2)

# Unit 3 (Second in stack)
pos3 = cq.Location(cq.Vector(0, 0, 2 * vertical_pitch + stack_gap))
part3 = part.val().moved(pos3)
result = result.union(part3)

# Unit 4 (Top in stack)
# This one looks slightly different or rotated? 
# No, looks like the same orientation, just stacked.
pos4 = cq.Location(cq.Vector(0, 0, 3 * vertical_pitch + stack_gap))
part4 = part.val().moved(pos4)
result = result.union(part4)

# Re-evaluating the image:
# The bottom piece is actually connected to the piece above it via the "Square Plate" vertical section.
# The square plates form a vertical column on the left.
# The square plates are TALLER than the beams.
# Let's adjust the "Square Plate" in the component definition.

def create_refined_component():
    beam_thickness = 10.0
    beam_width = 10.0
    
    # 1. The Main Horizontal Beam (X-axis)
    # Defined from local origin extending right.
    # Length approx 40mm
    beam_x = cq.Workplane("XY").box(50, beam_width, beam_thickness)
    
    # 2. The Cross Arm (Y-axis)
    # Located at +X end
    beam_y = cq.Workplane("XY").center(15, 10).box(beam_width, 20, beam_thickness)
    
    # 3. The Vertical End Plate (at -X end)
    # This plate is taller than the beam to allow interlocking/stacking without gaps at the plate,
    # even if there are gaps between beams.
    plate_height = 20.0 # Twice the beam thickness to span the gap?
    # Or maybe the components are just stacked tight and the gap is a design feature of the beam?
    # Let's assume the components stack directly on the plates.
    
    plate = (cq.Workplane("YZ")
             .workplane(offset=-25)
             .box(plate_height, 20, 5) # Height, Width, Thickness
             )
    
    # Square hole in plate
    plate = plate.faces(">X").workplane().rect(6, 6).cutBlind(-10)
    
    # Combine
    body = beam_x.union(beam_y).union(plate)
    
    # Fillets
    body = body.edges("|Z").fillet(1.0)
    
    # --- Holes and Hexes ---
    
    # Top Holes (Z-axis)
    # Center
    body = body.faces(">Z").workplane().hole(5.0)
    # Right (+X)
    body = body.faces(">Z").workplane().center(20, 0).hole(5.0)
    # Back (+Y arm)
    body = body.faces(">Z").workplane().center(15, 15).hole(5.0)
    
    # Front Hexes (Y-axis facing -Y)
    # Center
    body = body.faces("<Y").workplane().center(0, 0).polygon(6, 8.0).cutBlind(-3.0)
    body = body.faces("<Y").workplane().center(0, 0).hole(5.0)
    
    # Right side
    body = body.faces("<Y").workplane().center(20, 0).polygon(6, 8.0).cutBlind(-3.0)
    body = body.faces("<Y").workplane().center(20, 0).hole(5.0)

    # Back Hex (+Y face of the arm)
    body = body.faces(">Y").workplane().center(15, 0).polygon(6, 8.0).cutBlind(-3.0)
    body = body.faces(">Y").workplane().center(15, 0).hole(5.0)
    
    # Right End Hex (+X face)
    body = body.faces(">X").workplane().center(0, 0).polygon(6, 8.0).cutBlind(-3.0)
    body = body.faces(">X").workplane().center(0, 0).hole(5.0)
    
    # Conical pin on the right arm corner
    pin = (cq.Workplane("YZ")
           .workplane(offset=25) # End of beam x
           .center(5, 0)
           .circle(2).workplane(offset=4).circle(1)
           .loft()
           )
    
    body = body.union(pin)
    
    return body

# Final Assembly Logic
comp = create_refined_component()

# Stack 4 of them
# The plates are height 20, beams are height 10.
# If we stack them with spacing 20, the plates touch and beams have 10 gap.
pitch = 20.0

r1 = comp
r2 = comp.translate((0, 0, pitch))
r3 = comp.translate((0, 0, pitch*2))
r4 = comp.translate((0, 0, pitch*3))

# Looking at image, the bottom unit is separated by a gap from the stack of 3 above it.
# The top 3 seem to be a block. The bottom one is separate.
# But they all share the same vertical alignment on the left plate.
# The gap is between the beams.

# Actually, the image shows:
# 1 bottom unit.
# A gap.
# A middle unit.
# No gap (tight stack).
# Top unit.
# Wait, let's count the plates on the left.
# There are 4 squares visible on the left column.
# The bottom one is separated.
# The top 3 are stacked tightly.
# However, the code logic `r1`, `r2`... handles the geometry.
# To match the specific "gap" vs "tight" look:
# The plates are 20mm high. The beams are 10mm high.
# If we stack at z=0, z=20, z=40...
# The plates touch perfectly (creating a solid column).
# The beams have a 10mm air gap between them.
# This matches the image perfectly (gaps between horizontal arms, solid column on left).

result = r1.union(r2).union(r3).union(r4)