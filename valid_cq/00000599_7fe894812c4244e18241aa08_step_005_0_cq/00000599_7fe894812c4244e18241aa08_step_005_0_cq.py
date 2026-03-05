import cadquery as cq

# Parametric dimensions for a standard ball bearing (e.g., 608 size roughly)
# You can adjust these to change the bearing size
outer_diameter = 22.0
inner_diameter = 8.0
thickness = 7.0

# Calculated dimensions for races
# Let's define the radial thickness of the races
outer_race_thickness = 2.5
inner_race_thickness = 2.5

# Radius for the chamfers on the edges
chamfer_size = 0.5

# Dimensions for the groove/seal area
# This creates the visual separation between races
groove_depth = 0.5
seal_gap = 0.5  # Gap between inner/outer race and the seal

# Calculate intermediate radii
r_outer = outer_diameter / 2.0
r_inner = inner_diameter / 2.0

r_outer_race_inner = r_outer - outer_race_thickness
r_inner_race_outer = r_inner + inner_race_thickness

# Create the main cylinder
main_body = cq.Workplane("XY").circle(r_outer).extrude(thickness)

# Create the center bore
bore = cq.Workplane("XY").circle(r_inner).extrude(thickness)

# Cut the bore from the main body
bearing = main_body.cut(bore)

# Create the recess for the seal/shield on both sides
# This separates the inner and outer races visually
# We need to cut a ring out of the face
seal_cut_outer_r = r_outer_race_inner
seal_cut_inner_r = r_inner_race_outer

# Create the cut shape for the "groove" or seal recess
# We cut from the top face down and the bottom face up
# The cut is an annulus (ring)
seal_recess = (
    cq.Workplane("XY")
    .workplane(offset=thickness)  # Top face
    .circle(seal_cut_outer_r)
    .circle(seal_cut_inner_r)
    .extrude(-groove_depth)
)

seal_recess_bottom = (
    cq.Workplane("XY")
    .circle(seal_cut_outer_r)
    .circle(seal_cut_inner_r)
    .extrude(groove_depth)
)

# Apply the cuts
bearing = bearing.cut(seal_recess).cut(seal_recess_bottom)

# Create the seal itself (the flat part inside the groove)
# It sits slightly lower than the face
seal_thickness = 0.5 # Arbitrary thickness for the seal plate
seal_plate = (
    cq.Workplane("XY")
    .workplane(offset=thickness - groove_depth)
    .circle(seal_cut_outer_r - 0.1) # Slight clearance
    .circle(seal_cut_inner_r + 0.1)
    .extrude(-seal_thickness)
)
# Add a seal on the bottom too for symmetry
seal_plate_bottom = (
    cq.Workplane("XY")
    .workplane(offset=groove_depth)
    .circle(seal_cut_outer_r - 0.1)
    .circle(seal_cut_inner_r + 0.1)
    .extrude(seal_thickness)
)

# Add the seals to the main object
bearing = bearing.union(seal_plate).union(seal_plate_bottom)

# Apply chamfers to the outer edges
# Select the outer circular edges of the cylinder
bearing = bearing.edges(cq.selectors.RadiusNthSelector(0)).chamfer(chamfer_size)

# Apply chamfers to the inner bore edges
# Select the inner circular edges
bearing = bearing.edges(cq.selectors.RadiusNthSelector(-1)).chamfer(chamfer_size)

# Optional: Add small fillets or chamfers to the race transitions for realism
# We select edges based on the radius of the seal cut area
# This is a bit tricky with selectors, so we'll target the face edges specifically
try:
    # Inner race outer edge
    bearing = bearing.edges(cq.selectors.RadiusNthSelector(1)).chamfer(chamfer_size/2)
    # Outer race inner edge
    bearing = bearing.edges(cq.selectors.RadiusNthSelector(2)).chamfer(chamfer_size/2)
except:
    # Fallback if selection fails depending on CQ version specific geometry
    pass

result = bearing