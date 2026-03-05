import cadquery as cq

# Parameters
# Main U-Shape Tube
tube_diameter = 25.0
tube_wall_thickness = 2.0
tube_width = 400.0  # Outer width of U-shape
tube_length = 500.0 # Length of straight legs
corner_radius = 50.0

# Base Plate Frame
frame_width = 300.0 # Outer width of rectangular frame
frame_length = 350.0 # Outer length of rectangular frame
frame_thickness = 5.0
frame_member_width = 40.0 # Width of the flat bars

# Mounting Block (on one side)
block_width = 40.0
block_height = 40.0
block_length = 50.0
block_hole_diameter = tube_diameter + 0.5 # Slight clearance

# Mounting Holes on Plate
hole_dia = 6.0

# --- Helper logic for constructing the model ---

# 1. Create the U-Shaped Tube
# We'll use a sweep path.
path = (
    cq.Workplane("XY")
    .moveTo(-tube_width/2 + corner_radius, 0)
    .lineTo(-tube_width/2 + corner_radius, tube_length - corner_radius)
    .radiusArc((-tube_width/2 + corner_radius*2, tube_length), corner_radius) # Left corner
    .lineTo(tube_width/2 - corner_radius*2, tube_length)
    .radiusArc((tube_width/2 - corner_radius, tube_length - corner_radius), corner_radius) # Right corner
    .lineTo(tube_width/2 - corner_radius, 0)
)

# Create the profile for the tube
tube_outer = (
    cq.Workplane("XZ")
    .workplane(offset=0) # Start at the beginning of the path
    .circle(tube_diameter/2)
)

tube_inner = (
    cq.Workplane("XZ")
    .workplane(offset=0)
    .circle(tube_diameter/2 - tube_wall_thickness)
)

# Sweep to create the solid tube
solid_tube_outer = tube_outer.sweep(path)
solid_tube_inner = tube_inner.sweep(path)
u_tube = solid_tube_outer.cut(solid_tube_inner)

# 2. Create the Rectangular Base Plate Frame
# This looks like a rectangular frame with a large cutout
plate = (
    cq.Workplane("XY")
    .rect(frame_width, frame_length)
    .extrude(frame_thickness)
)

cutout = (
    cq.Workplane("XY")
    .rect(frame_width - 2*frame_member_width, frame_length - 2*frame_member_width)
    .extrude(frame_thickness)
)

frame = plate.cut(cutout)

# Drill mounting holes in the frame side members
# Assuming holes are symmetric on the bottom part of the side rails
hole_spacing_x = 20.0
hole_spacing_y = 20.0

# Create points for holes
hole_pts = []
# Left side holes
hole_pts.append((-frame_width/2 + frame_member_width/2 - hole_spacing_x/2, -frame_length/2 + 20))
hole_pts.append((-frame_width/2 + frame_member_width/2 + hole_spacing_x/2, -frame_length/2 + 20))
hole_pts.append((-frame_width/2 + frame_member_width/2 - hole_spacing_x/2, -frame_length/2 + 20 + hole_spacing_y))
hole_pts.append((-frame_width/2 + frame_member_width/2 + hole_spacing_x/2, -frame_length/2 + 20 + hole_spacing_y))

# Right side holes
hole_pts.append((frame_width/2 - frame_member_width/2 - hole_spacing_x/2, -frame_length/2 + 20))
hole_pts.append((frame_width/2 - frame_member_width/2 + hole_spacing_x/2, -frame_length/2 + 20))
hole_pts.append((frame_width/2 - frame_member_width/2 - hole_spacing_x/2, -frame_length/2 + 20 + hole_spacing_y))
hole_pts.append((frame_width/2 - frame_member_width/2 + hole_spacing_x/2, -frame_length/2 + 20 + hole_spacing_y))

frame = frame.faces(">Z").workplane().pushPoints(hole_pts).hole(hole_dia)

# Move the frame into position relative to the tube
# The frame seems to be attached to the bottom of the tube
frame = frame.translate((0, tube_length/2 - 100, -tube_diameter/2 - frame_thickness/2))


# 3. Create the Mounting Block
# This block is on the left leg of the U-tube, near the open end
block = (
    cq.Workplane("XY")
    .box(block_width, block_length, block_height)
)

# Cut the hole for the tube going through the block
block = (
    block.faces(">Y").workplane()
    .hole(block_hole_diameter)
)

# Add small mounting holes on top of the block (as seen in image)
block = (
    block.faces(">Z").workplane()
    .rect(block_width - 15, block_length - 15, forConstruction=True)
    .vertices()
    .hole(4.0)
)

# Position the block on the left leg
# Left leg x-position is roughly -tube_width/2 + corner_radius
block_x_pos = -tube_width/2 + corner_radius
block_y_pos = 50.0 # Distance from the start of the tube
block = block.translate((block_x_pos, block_y_pos, 0))

# 4. Combine everything
# The frame needs to be physically connected to the tube. In the image, it looks welded.
# We will union them.
result = u_tube.union(frame).union(block)

# Optional: Add fillets to the frame-tube connection points for realism (welds)
# This is computationally expensive, so often skipped in basic parametric scripts, 
# but we ensure valid geometry by unioning.

# Final Export
if __name__ == "__main__":
    # If running in CQ-Editor, this will visualize it
    try:
        show_object(result)
    except NameError:
        pass # Not running in CQ-Editor