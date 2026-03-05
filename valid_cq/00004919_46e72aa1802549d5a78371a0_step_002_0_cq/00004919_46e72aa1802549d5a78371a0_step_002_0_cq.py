import cadquery as cq

# Parameters for the box
length = 100.0   # Total length of the box
width = 75.0     # Total width of the box
height = 40.0    # Total height of the box
corner_radius = 8.0  # Radius of the vertical corners
top_edge_radius = 2.0 # Radius of the fillet on the top edge
lid_height = 8.0 # Height of the top section (lid)
groove_depth = 0.5 # Depth of the indentation between lid and base

# 1. Create the main block (base + lid combined shape)
# We start with a 2D rectangle and extrude it.
main_body = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(height)
)

# 2. Round the four vertical corners
main_body = main_body.edges("|Z").fillet(corner_radius)

# 3. Create the "lid" separation feature.
# The image shows a subtle line/groove near the top. We can model this 
# by creating a sketch of the profile and cutting it, or simply adding a 
# small chamfer/fillet to separate the top part visually.
# Alternatively, it looks like a slight overhang or step. 
# A common style for these enclosures is a lid that sits flush but has a small chamfer at the seam.
# Let's create a small groove to represent the seam line.

seam_plane = main_body.faces(">Z").workplane(offset=-lid_height)
# We will cut a tiny groove around the perimeter at this height
# but simpler is to just model the top fillet as requested.

# Let's apply the fillet on the very top face edges
result = main_body.edges(">Z").fillet(top_edge_radius)

# Optional: To make it look more like an assembly (lid + base) as hinted by the line,
# we can create a small cut. However, usually, simpler is better for a single solid representation.
# Looking closely at the image, there is a distinct line about 1/5th from the top.
# It looks like a small chamfer or a lip. Let's add a small detail there.

# Define the seam height
seam_z = height - lid_height

# We can create a small indentation or chamfer at the seam_z level.
# Let's try to select the edges at the perimeter at a specific Z height, 
# but since it's a smooth solid, no edge exists there yet.
# We can create a cut.

# Let's stick to the primary geometry which is a rounded box with a top fillet. 
# The "line" might just be a rendering artifact of a multi-part assembly or a texture.
# However, often these plastic enclosures have a slight step.
# Let's assume the user wants the single solid block shape shown.

# Refined approach based on visual inspection:
# It looks like a base box with a lid on top. The lid has a top fillet.
# The seam is visible.
# Let's create it as a union of two parts if we want the seam line, 
# or just the solid if we want the outer hull. 
# The prompt asks for the "3D CAD model", usually implying the geometry.
# I will generate the solid block with the fillets as the most robust interpretation.

# Final Geometry Construction:
# 1. Box of size L x W x H
# 2. Vertical edges filleted.
# 3. Top edge filleted.
# 4. To mimic the visual "seam", we can't easily do it without splitting the object or complex sweeping.
#    However, looking at the smooth shading, it's likely just a single solid block in this context.
#    Wait, looking very closely at the crop, there is a slight indentation.
#    Let's add a tiny groove to make it realistic.

path = result.section(height=seam_z)
# This creates a wire at the seam height. 
# Creating a small sweep to cut a groove is complex and might fail robustly.
# Let's keep it clean: A beautiful rounded box.

# If we interpret the image as a standard electronic enclosure:
# It usually has a bottom part and a top part. 
# The top part has a slightly larger radius or a chamfer at the bottom edge meeting the base.
# But simply, it is a rounded box.

result = (
    cq.Workplane("XY")
    .box(length, width, height)
    .edges("|Z")
    .fillet(corner_radius)
    .edges(">Z")
    .fillet(top_edge_radius)
)

# If the user strictly wants the visual of the seam line, we can add a tiny cut.
# Create a tool to cut the groove
groove_cutter = (
    cq.Workplane("XY")
    .rect(length + 5, width + 5) # Larger than box
    .rect(length - 2, width - 2) # Smaller inner, but we need the wall
    .extrude(0.2) # Very thin
    .translate((0, 0, seam_z)) # Move to seam height
)

# This is getting too specific without knowing if it's desired.
# The safest, most correct "CAD model" of the shape shown is the filleted box.
# The horizontal line is likely the parting line of the mold or assembly.
# I will provide the clean, solid geometry code.

# Re-evaluating the image: There is a distinct separate "lid" geometry.
# It looks like the lid has a small Chamfer at its bottom edge where it meets the box.
# Let's model it as one solid but with a small cut to represent that groove.

# Method:
# 1. Base Box
# 2. Lid Box
# 3. Stack them

base_h = height - lid_height
base = (
    cq.Workplane("XY")
    .box(length, width, base_h)
    .edges("|Z")
    .fillet(corner_radius)
    .translate((0, 0, base_h / 2))
)

lid = (
    cq.Workplane("XY")
    .box(length, width, lid_height)
    .edges("|Z")
    .fillet(corner_radius)
    .edges(">Z")
    .fillet(top_edge_radius)
    .translate((0, 0, base_h + lid_height / 2))
)

# To get the seam line effect, we can chamfer the bottom of the lid slightly
lid = lid.edges("<Z").chamfer(0.5)

result = base.union(lid)