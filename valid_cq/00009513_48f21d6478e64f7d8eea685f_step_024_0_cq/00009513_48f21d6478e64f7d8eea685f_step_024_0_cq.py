import cadquery as cq
import math

# --- Parameter Definitions ---
# Outer Shell
outer_diameter = 100.0
outer_height = 50.0
wall_thickness = 1.0

# Central Block Base
base_width = 50.0
base_length = 50.0
base_height = 35.0
fillet_radius = 8.0

# Internal Cutouts
center_hole_dia = 20.0
pocket_depth = 25.0
side_cutout_width = 30.0
side_cutout_depth = 10.0

# Screw Holes
screw_hole_dia = 3.0
screw_hole_spacing = 25.0  # distance between holes
screw_hole_depth = 15.0

# --- Geometry Construction ---

# 1. Create the Outer Cylindrical Shell
# We create a solid cylinder and hollow it out
shell = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(outer_height)
    .faces(">Z")
    .shell(-wall_thickness)
)

# 2. Create the Central Block Structure
# Start with a rounded box
center_block = (
    cq.Workplane("XY")
    .box(base_length, base_width, base_height)
    .edges("|Z")
    .fillet(fillet_radius)
)

# Apply fillets to the top edges to match the smooth top look
center_block = center_block.edges(">Z").fillet(fillet_radius / 2.0)

# 3. Create the Complex Internal Cutout (The "U" shape or cavity)
# We will cut a large rectangular pocket from the top face
cutout_profile = (
    cq.Workplane("XY")
    .workplane(offset=base_height)  # Start at the top of the block
    .rect(side_cutout_width, base_width + 10)  # Make it wider than the block in Y
    .extrude(-pocket_depth)
)

# 4. Refine the Cutout with the "Bridge" feature
# The image shows a bridge-like structure remaining or a specific cut shape.
# Let's refine the cut to look more like the tiered pocket in the image.
# We cut a cross shape to open up the sides and center.

# Cut through the Y-axis sides
y_cut = (
    cq.Workplane("XY")
    .workplane(offset=base_height / 2.0)
    .rect(base_length - 15, base_width + 5)
    .extrude(base_height)
)

# Cut the central bore
center_bore = (
    cq.Workplane("XY")
    .circle(center_hole_dia / 2.0)
    .extrude(base_height)
)

# 5. Create the stepped screw mount features
# The image shows little plateaus inside the cutout for screws.
# We'll subtract material to leave these "bosses" or add them back.
# A robust way is to cut the main pocket, then add the internal mounting geometry.

# Let's try a subtractive approach on the main block.

# Main vertical cut from top
main_cavity = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .rect(side_cutout_width, base_width * 0.7)
    .extrude(-pocket_depth)
)

# Side slots (the openings on the cheeks)
side_slots = (
    cq.Workplane("YZ")
    .workplane(offset=base_length/2.0 - 5.0) # Slightly inside
    .center(0, base_height - pocket_depth/2.0)
    .rect(base_width * 0.4, pocket_depth)
    .extrude(-base_length) # Cut through
)

# 6. Detailed Internal Features (The Screw Bosses)
# Create a shape to cut away material leaving the screw mounting pads
boss_cutout_width = 12.0
boss_z_level = base_height - 5.0 # Just below top surface

# We need a shape that represents the "void" in the center.
void_shape = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .rect(base_length - 16, base_width - 16) # Inner area
    .extrude(-base_height + 5) # Leave floor
)

# The bridge feature (the arch in the middle)
arch_radius = 8.0
bridge_cut = (
    cq.Workplane("YZ")
    .workplane(offset=0)
    .center(0, base_height - 12)
    .circle(arch_radius)
    .extrude(base_length, both=True)
)

# Horizontal holes/slots on the sides of the block
side_holes = (
    cq.Workplane("YZ")
    .center(0, base_height / 2)
    .circle(5)
    .extrude(base_length + 5, both=True)
)

# Apply cuts to center block
center_block = (
    center_block
    .cut(void_shape)
    .cut(bridge_cut)
    .cut(center_bore)
)

# 7. Add the Screw Holes on the internal faces
# We need to locate the flat faces created inside the void
# Based on the image, these are on the "shoulders" inside.

screw_holes = (
    cq.Workplane("XY")
    .workplane(offset=base_height) # Top plane
    .rect(base_length - 20, 0.1, forConstruction=True) # Construction line along X
    .vertices() # Select ends
    .circle(screw_hole_dia / 2.0)
    .extrude(-screw_hole_depth)
)

center_block = center_block.cut(screw_holes)

# 8. Add stiffening ribs/fins connecting block to shell (visible at bottom of image)
rib_thickness = 4.0
rib = (
    cq.Workplane("XY")
    .rect(outer_diameter, rib_thickness)
    .extrude(10.0) # Height of ribs at bottom
)
rib2 = rib.rotate((0,0,0), (0,0,1), 90)

center_structure = center_block.union(rib).union(rib2)

# Intersect ribs with the inner diameter of shell to make them fit cleanly
# (Optional, but good practice. Here we just unite them)

# 9. Combine Everything
# The center block sits on the floor of the shell.
# The shell floor is at Z=0 to Z=wall_thickness (if we shelled inwards).
# Actually, the previous shell operation shells inwards, so floor is at Z=0.
# We move the center structure up by the floor thickness if needed, 
# but usually, these are molded together.

result = shell.union(center_structure)

# Refine the intersection between shell and structure if needed
# (The union handles this automatically)

# Final validation - ensure the center hole goes through the shell floor
final_bore = (
    cq.Workplane("XY")
    .circle(center_hole_dia / 2.0)
    .extrude(100, both=True)
)

result = result.cut(final_bore)