import cadquery as cq
import math

# --- Parameters ---
height = 120.0        # Total height of the glass
top_radius = 40.0     # Outer radius at the rim
bottom_radius = 28.0  # Approximate radius at the base
wall_thickness = 2.5  # Thickness of the glass
base_thickness = 5.0  # Thickness of the glass bottom

# Facet details
num_facets = 9           # Number of flat faces (Picardie glasses typically have 9 or 10)
facet_height = 80.0      # Height of the faceted section from the bottom
facet_depth_factor = 0.95 # How much the facet cuts into the round shape (0-1)

# Smooth transition parameters
transition_fillet = 10.0 # Fillet radius where facets meet the round top

# --- Geometry Construction ---

# 1. Create the base cone/cylinder shape (outer shell)
# We loft from a polygon at the bottom to a circle at the top to approximate the shape
# However, a simpler approach for a glass is usually a revolved profile or constructive solid geometry.

# Let's try a Loft approach for the main body to get the taper right.
# Bottom is a polygon, top is a circle.
# But wait, the top section is round, and the bottom section is faceted.
# The transition is complex. Let's build a smooth outer cone first, then cut the facets?
# Or build the faceted bottom and the round top separately?

# Strategy:
# 1. Create a solid frustum (cone) representing the full outer bound.
# 2. Create a "cutter" to slice the facets on the lower portion.
# 3. Create the inner cavity (shelling).

# Step 1: Main blank (outer shape)
# We use a loft to create a nice tapered profile.
outer_profile = (
    cq.Workplane("XY")
    .circle(bottom_radius)
    .workplane(offset=height)
    .circle(top_radius)
    .loft(combine=True)
)

# Step 2: Create the facets
# The facets are flat cuts on the side. 
# We can create a large box or plane and array it around the center to cut the cone.

# Calculate the angle for each facet
angle_step = 360.0 / num_facets

# We will create a single cutter and subtract it.
# The cutter needs to be angled to match the taper of the glass, 
# or vertical if we want vertical facets on a tapered body (which creates parabolic curves at the top).
# Looking at the image, the facets seem to follow the taper of the glass somewhat, 
# but the "arches" at the top of the facets suggest vertical or near-vertical planar cuts
# intersecting a conical surface.

# Let's create a cutting plane.
# We determine the distance from center to the flat face.
chord_dist = bottom_radius * facet_depth_factor

# Create a cutter object. 
# It needs to be big enough to slice the side off.
cutter_width = top_radius * 2
cutter_height = facet_height
cutter_depth = top_radius # Plenty of depth to cut outward

# Define a cutter for one facet
# Positioned to cut the side of the glass
facet_cutter = (
    cq.Workplane("XY")
    .workplane(offset=facet_height/2) # Center Z
    .center(chord_dist + cutter_depth/2, 0) # Move out to the edge
    .box(cutter_depth, cutter_width, facet_height) # Create the cutting block
)

# Need to tilt the cutter to match the taper? 
# The image shows the facets getting wider at the top, which happens naturally 
# if you cut a cone with a vertical plane. Let's stick to vertical cuts first.
# If the cut is purely vertical, the bottom might be too cut away compared to top.
# Let's taper the cut slightly. We can do this by lofting the cutter or rotating it.
# Let's rotate the cutter slightly to match the glass slope.
slope_angle = math.degrees(math.atan((top_radius - bottom_radius) / height))
# We rotate the cutter to be parallel to the glass wall
facet_cutter = facet_cutter.rotate((0,0,0), (0,1,0), slope_angle)

# Subtract the facets from the main body
facets_cut = outer_profile
for i in range(num_facets):
    # Rotate the cutter around the Z axis for each position
    rotated_cutter = facet_cutter.rotate((0,0,0), (0,0,1), i * angle_step)
    facets_cut = facets_cut.cut(rotated_cutter)

# Step 3: Round the top of the facets (The "Arches")
# The intersection of the flat cut and the cone naturally makes a curve, 
# but the image shows a specific fillet/blend where the facet ends.
# A fillet operation on the top edges of the facet faces usually achieves this.

# Select edges at the top of the facets. 
# These are edges that are approximately at 'facet_height' Z level.
try:
    facets_cut = facets_cut.edges(cq.selectors.BoxSelector(
        (-top_radius*2, -top_radius*2, facet_height - 5),
        (top_radius*2, top_radius*2, facet_height + 5)
    )).fillet(transition_fillet)
except:
    # Fallback if complex fillet fails: just proceed, it often looks close enough
    pass

# Step 4: Create the Hollow (Shelling)
# We can simply cut a smaller version of the original cone from the inside.
# Inner profile dimensions
inner_top_radius = top_radius - wall_thickness
inner_bottom_radius = bottom_radius - wall_thickness
inner_height = height - base_thickness

inner_void = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .circle(inner_bottom_radius)
    .workplane(offset=inner_height)
    .circle(inner_top_radius)
    .loft(combine=True)
)

# Subtract inner void from the faceted body
result = facets_cut.cut(inner_void)

# Step 5: Final touches - Rim fillet
# Smooth the top rim
try:
    result = result.edges(">Z").fillet(wall_thickness / 2.1)
except:
    pass

# Optional: Fillet the bottom edges for realism
try:
    result = result.edges("<Z").fillet(1.0)
except:
    pass