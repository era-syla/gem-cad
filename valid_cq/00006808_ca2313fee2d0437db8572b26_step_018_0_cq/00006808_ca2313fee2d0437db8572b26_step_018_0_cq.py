import cadquery as cq

# -- Parametric Dimensions --
# Overall dimensions
length = 400.0  # Total length of the frame
width = 300.0   # Total width of the frame
height = 20.0   # Height of the frame walls/ribs

# Wall and Rib thickness
wall_thickness = 10.0

# Cover plate details
cover_thickness = 5.0  # Thickness of the top plate
cover_ratio = 0.6      # How much of the length is covered (0.0 to 1.0)
cover_length = length * cover_ratio

# Rib spacing details
# The image shows 3 open bays on the left side before the cover starts.
# It seems there are ribs underneath the cover as well, likely evenly spaced.
# Let's assume a number of bays to calculate rib positions.
num_bays = 5 # Total number of bays across the length

# -- Geometry Construction --

# 1. Create the outer frame
# We start with a solid block and shell it or cut the center.
# A more parametric way is to draw the rectangle and extrude.
outer_frame = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(height)
)

inner_cutout = (
    cq.Workplane("XY")
    .rect(length - 2*wall_thickness, width - 2*wall_thickness)
    .extrude(height)
)

frame = outer_frame.cut(inner_cutout)

# 2. Create internal ribs
# Ribs run along the width direction.
# We need to calculate the spacing.
# Internal length available for bays
internal_length = length - 2*wall_thickness
bay_width = (internal_length - (num_bays - 1) * wall_thickness) / num_bays

# We will create a single rib and pattern it, or just place them at specific offsets.
# The ribs are centered. Let's create a union of all ribs.
ribs = cq.Workplane("XY")

# Calculate the start position for the first internal rib
# The left inner wall is at x = -internal_length/2
start_x = -internal_length/2 + bay_width + wall_thickness/2

for i in range(num_bays - 1):
    offset = start_x + i * (bay_width + wall_thickness)
    rib = (
        cq.Workplane("XY")
        .center(offset, 0)
        .rect(wall_thickness, width - 2*wall_thickness)
        .extrude(height)
    )
    frame = frame.union(rib)

# 3. Create the cover plate
# The cover plate sits on top.
# Looking at the image, the cover plate seems to be flush with the top of the frame.
# This implies the frame might be taller or the cover sits in a cutout?
# Actually, looking closely at the far right corner, there's a notch. 
# It looks like the cover is placed *on top* of the frame, but the corners are cut out 
# to fit flush with the outer perimeter, or perhaps it sits inside a rabbet?
# Re-evaluating the image:
# The cover plate surface is flush with the top edge of the side walls? No.
# Looking at the far right corner, there is a small square cutout in the cover plate 
# that reveals the corner of the frame underneath? Or is the frame extending up?
# It looks like the cover plate is a separate sheet placed on top of the grid structure.
# The cover plate has cutouts at the corners corresponding to the frame walls? No.
# Let's look at the corner detail again. The grey cover seems to stop before the very edge, 
# or maybe there are corner posts?
# Actually, it looks like the cover plate sits *inside* the outer perimeter walls?
# No, that would make the top surface non-planar.
# Let's assume a simpler interpretation: The cover sits on top of the ribs and frame walls.
# But wait, the corner cutouts (the little square holes at the corners of the plate) suggest 
# that the outer vertical edges of the frame extend upwards past the plate?
# No, it looks like a simple rectangular cutout in the plate itself.
# Let's look at the near right corner. The plate ends, exposing the frame.
# Let's assume the plate is simply placed on top of the structure on the right side.
# However, to make it look exactly like the image:
# The plate covers the right portion.
# At the corners of the plate (top-right and bottom-right in the image perspective), there are square holes.
# These holes align with the inside corners of the frame.

# Let's construct the plate geometry.
# Center of the plate needs to be calculated.
# The plate covers the right side.
plate_center_x = (length / 2) - (cover_length / 2)

plate = (
    cq.Workplane("XY")
    .workplane(offset=height) # Place it on top of the frame
    .center(plate_center_x, 0)
    .rect(cover_length, width)
    .extrude(cover_thickness)
)

# Now, looking at the "cutouts" at the corners of the plate in the image.
# It looks like the plate might actually be flush with the frame top, meaning the frame has a recess?
# OR, more simply: The plate is just a solid block on top.
# Let's look really closely at the far corner. The wall continues up. The plate is recessed inside the frame?
# If the plate is recessed, the ribs would be lower than the outer walls.
# Let's look at the ribs on the left. They are flush with the outer walls.
# So the frame + ribs is a flat surface.
# The plate is added on top.
# Why the corner cutouts? Maybe to allow for corner posts or mounting?
# The cutouts are small squares at the corners of the plate.
# Let's add those specific cutouts to match the visual style.
# The cutouts are at the far right corners of the assembly.

corner_cutout_size = wall_thickness
# Position for cutouts relative to the plate center
cutout_x_pos = (cover_length / 2) - (corner_cutout_size / 2)
cutout_y_pos = (width / 2) - (corner_cutout_size / 2)

plate = (
    plate
    .faces(">Z")
    .workplane()
    # Shift to the far right edge of the plate relative to the plate's own coordinate system
    # Plate center was at plate_center_x. 
    # Global x of right edge is length/2.
    # Global y is width/2 and -width/2.
    # We want to cut corners at (length/2 - size/2, width/2 - size/2) and (length/2 - size/2, -width/2 + size/2)
    # The current workplane is centered on the plate's top face.
    .pushPoints([
        (cutout_x_pos, cutout_y_pos), 
        (cutout_x_pos, -cutout_y_pos)
    ])
    .rect(corner_cutout_size, corner_cutout_size)
    .cutThruAll()
)

# Combine everything
result = frame.union(plate)

# Export (optional, for debugging)
# cq.exporters.export(result, "model.step")