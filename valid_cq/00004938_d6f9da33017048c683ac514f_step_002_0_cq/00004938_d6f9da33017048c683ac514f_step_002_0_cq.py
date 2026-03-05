import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions of the block
block_width = 20.0  # Width of the plate
block_height = 80.0 # Total height of the plate
block_depth = 10.0  # Total thickness

# Teeth parameters
tooth_depth = 2.0   # How deep the teeth cuts are
tooth_pitch = 4.0   # Distance between tooth peaks
tooth_gap = 2.0     # Width of the gap between teeth (valley)
# Calculating tooth thickness based on pitch and gap, assuming simple rectangular or trapezoidal profile.
# Looking at the image, they look like square or rectangular ribs.
tooth_thickness = tooth_pitch - tooth_gap 

# Layout of the toothed sections
# It appears there is a top section, a bottom section, and a gap in the middle.
# Let's define the number of teeth in each section.
num_teeth_per_section = 6
section_spacing = 20.0 # Approximate space in the middle

# Central hole
hole_diameter = 6.0

# --- Geometry Construction ---

# 1. Create the main base block
base = cq.Workplane("XY").box(block_width, block_height, block_depth)

# 2. Define a function to create a single cut for the tooth gap
# The image shows ribs. It's often easier to cut the valleys.
# Let's assume the front face is at +Z or -Z relative to center, 
# but box creates it centered. Front face is at z = block_depth/2.

# We will cut rectangular grooves to form the teeth.
def make_grooves(loc):
    # This creates a solid that represents the material to be removed
    return cq.Workplane("XY").rect(block_width + 5.0, tooth_gap).extrude(tooth_depth + 1.0) # slightly wider and deeper to ensure cut

# Calculate positions for the grooves
# The block is centered at (0,0,0). Y ranges from -40 to 40.
# We need two arrays of cuts.

groove_centers = []

# Middle flat section height
mid_section_height = 20.0
start_y_top = mid_section_height / 2.0 + tooth_thickness # Starting just above the middle section
start_y_bottom = -mid_section_height / 2.0 - tooth_thickness # Starting just below the middle section

# Generate groove positions for top section
# If we want N teeth, we need grooves between them or defined by the profile.
# Looking closely, it looks like rectangular ridges. Let's model by cutting slots.
# Top Section:
# Let's iterate upwards from the middle.
current_y = mid_section_height / 2.0 + tooth_gap/2.0
for i in range(num_teeth_per_section):
    groove_centers.append((0, current_y))
    current_y += tooth_pitch

# Bottom Section:
# Let's iterate downwards from the middle.
current_y = -(mid_section_height / 2.0 + tooth_gap/2.0)
for i in range(num_teeth_per_section):
    groove_centers.append((0, current_y))
    current_y -= tooth_pitch

# Create the cutter object by placing rectangles at all groove positions
cutter = (
    cq.Workplane("XY")
    .pushPoints(groove_centers)
    .rect(block_width * 1.2, tooth_gap) # Make cut wider than block
    .extrude(tooth_depth)
)

# Move the cutter to the front face of the block
# The box is centered, so the front face is at Z = block_depth / 2
# We want to cut *into* the face, so we position the extrusion to overlap.
# The cutter was extruded in +Z by default.
# We need to move it so its top face aligns with block top face or sits properly.
# Actually, simpler approach: create the cutter on the face.

# Let's retry the cut using the face reference directly
result = base.faces(">Z").workplane().pushPoints(groove_centers).rect(block_width * 1.2, tooth_gap).cutBlind(-tooth_depth)

# 3. Create the central hole
# The hole is in the center of the block (0,0) on the XY plane.
result = result.faces(">Z").workplane().center(0, 0).hole(hole_diameter)

# Optional: Add small chamfers to the back edges or corners if desired, 
# but the image looks sharp-edged. We will leave as is.

# Final assignment
result = result