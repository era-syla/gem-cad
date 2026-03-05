import cadquery as cq

# Parametric dimensions
length = 150.0       # Total length of the enclosure
width = 80.0         # Total width of the enclosure
total_height = 20.0  # Total height (top + bottom halves)
corner_radius = 5.0  # Radius of the main corners
wall_thickness = 2.0 # Thickness of the walls (implied)

# Screw hole parameters
hole_diameter = 3.0
counterbore_diameter = 6.0
counterbore_depth = 2.0
hole_inset_x = 10.0  # Distance from center to hole along X
hole_inset_y = 10.0  # Distance from center to hole along Y

# Calculate derived dimensions for hole positions
# Holes are typically placed symmetrically near the corners
hole_pos_x = (length / 2.0) - hole_inset_x
hole_pos_y = (width / 2.0) - hole_inset_y

# Create the base shape (a rounded box)
# We create the overall block first
base = (
    cq.Workplane("XY")
    .box(length, width, total_height)
    .edges("|Z")
    .fillet(corner_radius)
)

# Create the "parting line" feature
# Looking at the image, there is a distinct seam. 
# We can model this by creating a groove or just assume it's an assembly view.
# However, often these simple renders are single bodies with a feature.
# Let's model it as a solid block with the screw holes, and a small groove 
# around the perimeter to represent the join between top and bottom halves.

groove_height = 0.5
groove_depth = 0.5
parting_z = 0  # Center of the box in Z

groove = (
    cq.Workplane("XY")
    .workplane(offset=parting_z - groove_height/2)
    .rect(length + 2, width + 2) # Make it bigger to cut through
    .extrude(groove_height)
)

# Actually, a better way to visualize the "lid" aspect shown in the image
# (where there's a visible line around the middle) is just to leave it as a solid block
# but maybe add a tiny chamfer or just rely on the user understanding it's an enclosure.
# The image shows a very simple rectangular prism with rounded corners and 4 counterbored holes.
# The horizontal line suggests two halves. I will model the solid shape.

# Define hole locations
locations = [
    (hole_pos_x, hole_pos_y),
    (hole_pos_x, -hole_pos_y),
    (-hole_pos_x, hole_pos_y),
    (-hole_pos_x, -hole_pos_y),
]

# Create the counterbored holes
result = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints(locations)
    .cboreHole(hole_diameter, counterbore_diameter, counterbore_depth)
)

# Optional: To replicate the "seam" look more accurately based on the image rendering style,
# we can create a small cut around the perimeter at Z=0 (since box is centered at Z=0 by default).
# The default box center is (0,0,0), so Z ranges from -height/2 to +height/2.
# The seam appears to be roughly in the middle.

seam_cut = (
    cq.Workplane("XY")
    .rect(length + 10, width + 10) # Outer rectangle large enough to surround object
    .rect(length - 0.2, width - 0.2) # Inner rectangle slightly smaller than object
    .extrude(0.2) # Very thin cut
    .translate((0, 0, -0.1)) # Center the cut at Z=0
)

# Since the prompt asks for the model based on the image, and the image clearly shows
# a seam line, let's create a subtle groove to represent the interface between top and bottom.
# However, doing a complex boolean for a visual seam might be overkill.
# The primary geometry is the rounded box with holes. 
# I will add a very subtle groove to represent the parting line seen in the image.

# Re-defining the seam logic to be robust with rounded corners
path = base.section(height=0) # Get the cross section at the middle
seam_profile = (
    cq.Workplane("XZ")
    .workplane(offset=-width/2) # Start at the edge
    .moveTo(length/2, 0) # Move to the profile start on the surface
    .rect(1.0, 0.2) # Create a small cutting profile
)

# A simpler approach for the seam that is robust:
# Just create the main shape. The line in the image might just be the rendering of two stacked solids.
# I will simulate this by ensuring the final object `result` is the single solid shown.
# If I look closely, the bottom half seems slightly inset or there is a reveal.
# Let's stick to the most definitive features: Rounded box, 4 holes.

# Refined approach:
# 1. Create the main block.
# 2. Apply fillets.
# 3. Apply holes.
# 4. (Optional but nice) Add a tiny V-groove or just leave as is.
# The image shows a distinct horizontal line. I'll add a tiny chamfer cut to hint at it.

seam_tool = (
    cq.Workplane("XY")
    .rect(length + 5, width + 5)
    .rect(length - 0.5, width - 0.5) # Just inside the perimeter
    .extrude(0.1)
    .edges("|Z")
    .fillet(corner_radius) 
    .translate((0,0,-0.05))
)
# Note: Boolean operations for cosmetic seams can be flaky. 
# I will produce the clean solid geometry of the enclosure case.

result = (
    cq.Workplane("XY")
    .box(length, width, total_height)
    .edges("|Z")
    .fillet(corner_radius)
    .faces(">Z")
    .workplane()
    .pushPoints(locations)
    .cboreHole(hole_diameter, counterbore_diameter, counterbore_depth)
)

# To mimic the visual "two halves" look, we can cut a tiny slice out of the middle perimeter
# essentially chamfering the meeting edges.
# Let's select the edges at Z=0? No, box is centered.
# We can select edges on the side faces that are horizontal.
# But `box` creates a primitive.
# Let's just output the high quality solid. The line is likely a parting line.

# Final check of the code structure
# 1. Imports -> Correct
# 2. Parameters -> Correct
# 3. Base shape -> Correct
# 4. Holes -> Correct
# 5. Result variable -> Correct