import cadquery as cq

# --- Parameters ---
# Overall dimensions estimated based on visual proportions
total_length = 100.0  # Total length of the fastener
shaft_diameter = 4.0  # Main shaft diameter
head_diameter = 14.0  # Diameter of the top flange/head
head_thickness = 2.0  # Thickness of the rim of the head
dome_height = 2.0     # Height of the domed section above the rim

# Sleeve/Ribbed section parameters
sleeve_length = 15.0  # Length of the thicker ribbed section under the head
sleeve_diameter = 6.5 # Diameter of the ribbed section
rib_count = 12        # Number of ribs
rib_depth = 0.2       # Depth of the cuts for the ribs

# Shaft detail parameters
knurl_section_start = sleeve_length  # Where knurling/texture starts relative to head bottom
knurl_section_length = 50.0          # Length of the textured part of shaft
tip_taper_length = 2.0               # Chamfer at the bottom

# --- Construction ---

# 1. Create the Head
# We'll make a revolved profile for the head to get the domed/washer shape
head_profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(head_diameter / 2, 0)       # Bottom outer edge
    .lineTo(head_diameter / 2, head_thickness) # Side edge
    .lineTo(shaft_diameter / 2 + 1.5, head_thickness) # Top flat part of rim
    .threePointArc(
        (shaft_diameter / 2, head_thickness + dome_height), 
        (0, head_thickness + dome_height)
    ) # Dome curve
    .close()
)

head = head_profile.revolve()

# Add a central hex recess (simulating a drive socket)
hex_drive = (
    cq.Workplane("XY")
    .workplane(offset=head_thickness + dome_height)
    .polygon(6, 4.0) # 4mm hex key size
    .extrude(-2.5)   # Depth of socket
)

head = head.cut(hex_drive)


# 2. Create the Ribbed Sleeve Section
# Base cylinder
sleeve = (
    cq.Workplane("XY")
    .workplane(offset=-sleeve_length)
    .circle(sleeve_diameter / 2)
    .extrude(sleeve_length)
)

# Create cuts to simulate the ribs
# We make a single cutting tool (a ring) and pattern it
rib_cut_tool = (
    cq.Workplane("XZ")
    .moveTo(sleeve_diameter / 2, 0)
    .lineTo(sleeve_diameter / 2 - rib_depth, 0.2)
    .lineTo(sleeve_diameter / 2 - rib_depth, -0.2)
    .close()
    .revolve()
)

# Distribute rib cuts along the sleeve
for i in range(rib_count):
    z_pos = - (sleeve_length / rib_count) * i - (sleeve_length / rib_count)/2
    # Translate the cut tool to position
    current_cut = rib_cut_tool.translate((0, 0, z_pos))
    sleeve = sleeve.cut(current_cut)

# 3. Create the Main Shaft
shaft_length_total = total_length - head_thickness # Approximation
shaft = (
    cq.Workplane("XY")
    .workplane(offset=-shaft_length_total)
    .circle(shaft_diameter / 2)
    .extrude(shaft_length_total)
)

# 4. Create "Knurling" / Texture on the Shaft
# The image shows a section of the shaft that is textured or has small ridges.
# Modeling true knurling is computationally expensive, so we will use
# small rings to simulate the texture shown in the middle of the shaft.
texture_start_z = -sleeve_length
texture_end_z = texture_start_z - knurl_section_length
num_texture_rings = 30

texture_cut_tool = (
    cq.Workplane("XZ")
    .moveTo(shaft_diameter / 2, 0)
    .lineTo(shaft_diameter / 2 - 0.1, 0.1)
    .lineTo(shaft_diameter / 2 - 0.1, -0.1)
    .close()
    .revolve()
)

for i in range(num_texture_rings):
    z_pos = texture_start_z - (knurl_section_length / num_texture_rings) * i
    current_cut = texture_cut_tool.translate((0, 0, z_pos))
    shaft = shaft.cut(current_cut)

# 5. Add Taper to Tip
# We can simply chamfer the bottom edge of the shaft
shaft = shaft.edges("<Z").chamfer(0.5)

# --- Assembly ---

# Combine all solid parts
# Note: CadQuery operations usually return a new object, so we union them sequentially
result = head.union(sleeve).union(shaft)

# Optional: Fillet the transition between sleeve and head for realism
result = result.edges(cq.selectors.NearestToPointSelector((0, sleeve_diameter/2, 0))).fillet(0.5)

# Export or display
# show_object(result)