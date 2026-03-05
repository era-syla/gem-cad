import cadquery as cq

# Parametric dimensions for the frame
frame_width = 100.0   # Total width of the frame
frame_height = 150.0  # Total height of the frame
frame_depth = 15.0    # Thickness of the main outer frame
border_width = 15.0   # Width of the frame border (face width)

# Dimensions for the inner recessed part (the "rabbet" or stepped section)
recess_depth = 5.0    # How far the inner step goes back
recess_offset = 5.0   # How much smaller the inner back frame is (step width)

# Create the main outer frame
# 1. Start with a rectangle
# 2. Extrude to depth
outer_frame = (
    cq.Workplane("XY")
    .rect(frame_width, frame_height)
    .extrude(frame_depth)
)

# Create the cutout for the center (the window)
# The cutout size is the outer dimensions minus twice the border width
cutout_width = frame_width - (2 * border_width)
cutout_height = frame_height - (2 * border_width)

outer_frame_hollow = (
    outer_frame.faces(">Z")
    .workplane()
    .rect(cutout_width, cutout_height)
    .cutThruAll()
)

# Create the inner stepped profile (the back lip/rabbet)
# This sits behind the main frame, often slightly inset
back_frame_width = frame_width - (2 * recess_offset)
back_frame_height = frame_height - (2 * recess_offset)
back_cutout_width = cutout_width # The opening remains the same
back_cutout_height = cutout_height

# We construct this by creating a plate on the back and cutting the hole
back_plate = (
    cq.Workplane("XY")
    .workplane(offset=-recess_depth) # Shift down to start behind the main frame
    .rect(back_frame_width, back_frame_height)
    .extrude(recess_depth)
)

# Combine the main frame with the back plate extension
# Note: In the image, it looks like a single solid piece with a "stepped" profile.
# The previous `outer_frame_hollow` is the front face. 
# We need to add the back extension, but ensure the center is open.

# Let's rebuild more cleanly as a single sketch with multiple steps or booleans.
# Strategy: 
# 1. Create the full outer block.
# 2. Create the back "step" block (slightly smaller).
# 3. Union them.
# 4. Cut the central hole through everything.

# Step 1: Front Block
front_block = (
    cq.Workplane("XY")
    .rect(frame_width, frame_height)
    .extrude(frame_depth)
)

# Step 2: Back Block (The step)
# Looking at the image, there is a step on the outer edge at the back.
# It seems the front face is the largest, and there is a smaller extrusion behind it.
# Or, the back is the largest and the front is a smaller frame?
# Let's look closely at the corners.
# The front face (closest to viewer) seems to be a simple rectangular frame.
# Behind it, there is a slightly smaller frame attached.

back_extension_depth = 5.0 
back_extension_inset = 4.0 # The step in from the outer edge

back_block = (
    cq.Workplane("XY")
    .workplane(offset=-back_extension_depth)
    .rect(frame_width - (2 * back_extension_inset), frame_height - (2 * back_extension_inset))
    .extrude(back_extension_depth)
)

combined_solid = front_block.union(back_block)

# Step 3: Cut the central hole
# The hole goes through everything.
hole_width = frame_width - (2 * border_width)
hole_height = frame_height - (2 * border_width)

result = (
    combined_solid
    .faces(">Z")
    .workplane()
    .rect(hole_width, hole_height)
    .cutThruAll()
)

# Optional: Adding the small detail inside the bottom frame?
# The image shows a tiny rectangular notch or artifact on the bottom inner sill.
# It looks like a small depression or slot on the inner face of the bottom member.

notch_width = 15.0
notch_depth = 2.0
notch_height = 1.0

# Select the bottom inner face
# We can find it by position.
result = (
    result
    .faces("<Y")       # Bottom outer face
    .faces(">Y")       # Bottom inner face (inside the hole)
    .workplane(centerOption="CenterOfBoundBox")
    .rect(notch_width, notch_depth) # dimensions on the face plane
    .cutBlind(-notch_height) # Cut downwards into the frame
)

# Note: The "cutBlind" direction depends on normal. 
# Since we selected an inner face looking "up" (technically >Y relative to the bottom bar, but <Y relative to global?),
# selecting faces usually sets the normal outward.
# The bottom inner face of the frame is facing +Y (towards the center).
# So cutting -Z (into the material) might need orientation adjustment.
# Let's verify selection logic for the notch:
# The bottom bar is at approx y = -frame_height/2 + border_width/2.
# Its top face is inside the window hole.

# A more robust way to add the notch:
# Create a cutting tool positioned exactly where we want it.
notch_tool = (
    cq.Workplane("XY")
    .workplane(offset=frame_depth - notch_height) # Position near top surface
    .center(0, -frame_height/2 + border_width/2) # Move to bottom bar center
    .rect(notch_width, 4.0) # Width and "thickness" of cut
    .extrude(notch_height + 1.0) # Extrude up
)

# Apply the cut
result = result.cut(notch_tool)