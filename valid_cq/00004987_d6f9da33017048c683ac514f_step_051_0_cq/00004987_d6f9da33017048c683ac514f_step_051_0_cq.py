import cadquery as cq

# Parametric dimensions
plate_width = 50.0
plate_height = 50.0
plate_thickness = 4.0

# Central large bore
center_hole_diameter = 32.0

# Corner mounting holes
corner_hole_diameter = 3.5
corner_hole_spacing = 42.0  # Distance between centers

# Inner mounting holes
inner_hole_diameter = 3.0
inner_hole_spacing_x = 30.0 # Approximate from visual
inner_hole_spacing_y = 30.0 # Approximate from visual

# Back boss dimensions
boss_width = 44.0
boss_height = 44.0
boss_thickness = 10.0  # Total thickness including plate
corner_radius = 3.0    # For the plate corners
boss_corner_radius = 2.0 # For the boss corners

# Cutout on the side of the boss (visible on the left)
side_cutout_depth = 5.0
side_cutout_width = 15.0

# Create the main front plate
# Start with a rectangle and fillet corners
plate = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(plate_thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# Create the rear boss
# It's a slightly smaller rectangle extruded from the back of the plate
boss = (
    cq.Workplane("XY")
    .rect(boss_width, boss_height)
    .extrude(-boss_thickness + plate_thickness) # Extrude downwards relative to XY
    .edges("|Z")
    .fillet(boss_corner_radius)
)

# Combine plate and boss
# We need to move the boss to align with the bottom face of the plate if we started both at Z=0
# However, extruding negative creates it below. The join operation handles this.
main_body = plate.union(boss)

# Create the side cutouts on the boss
# There appear to be cutouts on the left/right sides (or just one side visible)
# Let's assume symmetry for a generic motor mount style part
side_cutout = (
    cq.Workplane("XZ")
    .workplane(offset=-plate_height/2) # Move to the side
    .center(0, -boss_thickness/2)      # Center roughly in the boss thickness
    .rect(side_cutout_width, boss_thickness) # Create a rectangle to cut
    .extrude(side_cutout_depth)        # Cut into the body
)

# Apply the side cutouts (assuming on the left side based on image perspective)
# The image shows a cut on the left (-X) side.
cutout_solid = (
    cq.Workplane("YZ")
    .workplane(offset=-plate_width/2) # Left face
    .center(0, -boss_thickness/2 + plate_thickness/2) # Center vertically on the boss part
    .rect(boss_height/2, boss_thickness) # Large enough to clear
    .extrude(side_cutout_depth) # Cut inward
)

# Actually, looking closer, the "cutout" might just be that the boss 
# isn't a full rectangle, or has a specific shape. 
# Let's refine the boss shape. It looks like a NEMA stepper motor face.
# A NEMA 17 face is 42mm x 42mm usually.
# Let's stick to the subtractive method on the boss.
# The image shows reliefs on the sides of the raised block.

# Re-strategy for the boss:
# 1. Solid block.
# 2. Cut the relief on the left side (and likely right side for symmetry).
relief_cut = (
    cq.Workplane("YZ")
    .workplane(offset=-plate_width/2)
    .center(0, -boss_thickness/2)
    .rect(20, boss_thickness) # Arbitrary width to create the notch
    .extrude(3) # Depth of the relief
)
# Mirror for the other side
relief_cut_2 = (
    cq.Workplane("YZ")
    .workplane(offset=plate_width/2)
    .center(0, -boss_thickness/2)
    .rect(20, boss_thickness)
    .extrude(-3) 
)

main_body = main_body.cut(relief_cut).cut(relief_cut_2)


# Drilling Holes

# 1. Large center hole
main_body = (
    main_body.faces(">Z")
    .workplane()
    .hole(center_hole_diameter)
)

# 2. Corner mounting holes (4x)
main_body = (
    main_body.faces(">Z")
    .workplane()
    .rect(corner_hole_spacing, corner_hole_spacing, forConstruction=True)
    .vertices()
    .hole(corner_hole_diameter)
)

# 3. Inner mounting holes (2x visible, likely 4x or diagonal pattern)
# The image shows two smaller holes closer to the center, aligned diagonally or near corners.
# They look like NEMA mounting holes (31mm spacing usually for NEMA 17).
# Let's place them diagonally.
main_body = (
    main_body.faces(">Z")
    .workplane()
    .rect(inner_hole_spacing_x, inner_hole_spacing_y, forConstruction=True)
    .vertices()
    .hole(inner_hole_diameter)
)

# Orient the view to match the image roughly
# The image shows the back/boss side facing somewhat away, front plate facing us
result = main_body