import cadquery as cq

# --- Parametric Definitions ---
sphere_radius = 50.0  # Main sphere size
cutout_radius = 8.0   # Radius of the circular details
cutout_depth = 0.5    # How deep the details are cut/imprinted

# --- Modeling Steps ---

# 1. Create the main sphere
main_sphere = cq.Workplane("XY").sphere(sphere_radius)

# 2. Create the tool for the top cutout
# We create a cylinder and position it at the top pole
top_tool = (
    cq.Workplane("XY")
    .circle(cutout_radius)
    .extrude(sphere_radius + 5) # Make it tall enough to reach
    .translate((0, 0, 0))       # Centered
)

# 3. Create the tool for the side cutout
# We create a cylinder and position it on the equator (e.g., along X axis)
side_tool = (
    cq.Workplane("YZ")
    .circle(cutout_radius)
    .extrude(sphere_radius + 5)
    .translate((0, 0, 0)) 
    .rotate((0,0,0), (0,1,0), 90) # Rotate to align with X axis
)

# 4. Create the equatorial line/groove
# A thin torus or a cylinder subtraction could work, but looking closely 
# at the image, it's a very thin parting line. 
# A simple way to represent this visual feature without complex surfacing 
# is a very thin, shallow cut.
groove_thickness = 0.2
groove_tool = (
    cq.Workplane("XY")
    .circle(sphere_radius + 1) # Outer bound
    .circle(sphere_radius - cutout_depth) # Inner bound
    .extrude(groove_thickness)
    .translate((0, 0, -groove_thickness/2)) # Center vertically
)

# The image shows circular regions that look like shallow recesses or caps.
# Let's subtract just the tips of the cylinders to create the circular "caps" visual.

# Creating intersection bodies to act as the "caps" or slightly offset surfaces
# is complex. A more robust way to match the visual is to make shallow cuts.

# Position top tool for shallow cut
top_cut_tool = (
    cq.Workplane("XY")
    .workplane(offset=sphere_radius - cutout_depth)
    .circle(cutout_radius)
    .extrude(cutout_depth * 2)
)

# Position side tool for shallow cut
# We need to orient a workplane facing the X direction
side_cut_tool = (
    cq.Workplane("YZ")
    .workplane(offset=sphere_radius - cutout_depth)
    .circle(cutout_radius)
    .extrude(cutout_depth * 2)
)

# --- Boolean Operations ---

# Since the image is a bit ambiguous (are they holes, flat spots, or raised?),
# the most standard CAD interpretation for this "Death Star" or "Ball Joint" look
# is often flat spots or shallow recesses. 

# Let's perform a cut to create the flat circular faces on the sphere surface.
# This creates the visual boundary seen in the image.
result = main_sphere.cut(top_cut_tool).cut(side_cut_tool).cut(groove_tool)

# If we strictly want the surface "scribed" line look without flat spots, 
# another approach is intersecting, but the cut is the most manufacturing-realistic.

# Final refinement: The equator line in the image seems to stop at the circle.
# To achieve that, we need to subtract the side circle tool from the groove tool first.
# Let's rebuild that logic.

# Re-strategy for the groove:
# 1. Create the full ring groove.
# 2. Subtract the area of the side circle from the groove tool so the line doesn't pass through it.
groove_interrupted = groove_tool.cut(side_cut_tool)

# Apply cuts to main sphere
result = main_sphere.cut(top_cut_tool).cut(side_cut_tool).cut(groove_interrupted)