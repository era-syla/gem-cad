import cadquery as cq

# Parameters for the reducer
large_diameter = 50.0  # Diameter of the larger end
small_diameter = 25.0  # Diameter of the smaller end
wall_thickness = 2.0   # Thickness of the walls

large_section_length = 25.0 # Length of the straight large cylinder
small_section_length = 20.0 # Length of the straight small cylinder
transition_length = 35.0    # Length of the transition zone

# Calculate radii
r_large = large_diameter / 2.0
r_small = small_diameter / 2.0

# 1. Create the outer profile to revolve
# We will draw half the cross-section and revolve it.
# The profile consists of:
# - A straight line for the large cylinder
# - A spline/curve for the transition
# - A straight line for the small cylinder
# - Then offsetting or creating the inner wall

# Define points for the outer profile
p0 = (0, 0) # Start at center (but we are drawing radial distance on Y, length on X)
# Actually, let's draw in X-Y plane where Y is radial distance and X is axial length.

# Points along the top edge (outer surface)
# Start of large cylinder
p_start_large = (0, r_large)
# End of large cylinder / Start of transition
p_end_large = (large_section_length, r_large)
# End of transition / Start of small cylinder
p_start_small = (large_section_length + transition_length, r_small)
# End of small cylinder
p_end_small = (large_section_length + transition_length + small_section_length, r_small)

# Create the solid by revolving a profile
# We will create the outer shell first.
# Using a spline for a smooth "S-curve" transition looks best matching the image.
# We need control points for the spline to ensure tangency at the straight sections.
# Tangent at p_end_large is horizontal (1, 0)
# Tangent at p_start_small is horizontal (1, 0)

# Let's use the loft operation with sections for a very clean transition, 
# or a revolve operation with a spline. A revolve is more robust for a pipe.

# Using CadQuery's sketch or wire builder:
# We build the outer wire, then offset it inwards to get thickness, close it, and revolve.

total_length = large_section_length + transition_length + small_section_length

# Function to build the profile
def make_reducer_profile():
    s = cq.Sketch()
    
    # Outer path
    s = s.segment((0, r_large), (large_section_length, r_large)) # Large straight section
    
    # Smooth transition using a spline. 
    # To get a nice S-curve, we define start/end points and tangents.
    # CadQuery spline support can be tricky with specific tangents in a single chain easily.
    # An alternative is a cubic Bezier or just point interpolation.
    # Let's manually define two control points for a cubic Bezier behavior:
    # CP1: extending horizontally from the large cylinder
    # CP2: extending horizontally back from the small cylinder
    
    cp1 = (large_section_length + transition_length * 0.5, r_large)
    cp2 = (large_section_length + transition_length * 0.5, r_small)
    
    # Note: simple spline through points might overshoot. 
    # A standard reducer transition usually follows a specific curve, often a bell or conic.
    # Let's try a tangent arc or spline. The image looks like a tangent continuous loft.
    # Let's use the spline method with tangents defined implicitly by control points if possible,
    # or just use `tangentArc` if it were a simple radius, but this is an S-curve.
    # Let's use a parametric curve approach by drawing edge by edge.
    
    return s

# Let's use the solid construction approach:
# 1. Create large cylinder
# 2. Create small cylinder
# 3. Loft between them (or loft between two circles)
# 4. Shell the result.

# Create the workplanes for the loft
wp_large_end = cq.Workplane("XY").workplane(offset=large_section_length)
wp_small_start = cq.Workplane("XY").workplane(offset=large_section_length + transition_length)

# 1. Base Cylinder (Large)
large_cyl = cq.Workplane("XY").circle(r_large).extrude(large_section_length)

# 2. Small Cylinder
# We create it at the far end
small_cyl = wp_small_start.circle(r_small).extrude(small_section_length)

# 3. Transition (Loft)
# To get the smooth tangency (G1 or G2 continuity) shown in the image, 
# a standard ruled loft might have sharp creases.
# CadQuery's `loft` creates a ruled surface by default unless `ruled=False` is used, 
# but even then, tangent continuity to the adjacent cylinders isn't automatic without guide rails.
# 
# Better approach for this specific smooth shape: Revolve a wire.

# Define the path points for the revolution
pts = [
    (0, r_large),
    (large_section_length, r_large),
    (large_section_length + transition_length, r_small),
    (total_length, r_small),
    (total_length, r_small - wall_thickness),
    (large_section_length + transition_length, r_small - wall_thickness),
    (large_section_length, r_large - wall_thickness),
    (0, r_large - wall_thickness),
    (0, r_large) # Close loop
]

# We need the transition segments (index 1-2 and 5-6) to be curves.
# Let's build the wire segment by segment.

path = cq.Workplane("XZ")

# Start at inner bottom corner
path = path.moveTo(0, r_large - wall_thickness)
path = path.lineTo(large_section_length, r_large - wall_thickness)

# Curve down (Inner transition)
# We use a spline. We need intermediate points to make it look like an S-curve.
mid_x = large_section_length + transition_length / 2.0
mid_y_inner = (r_large + r_small) / 2.0 - wall_thickness
# Creating a spline for the inner transition
path = path.spline(
    [(large_section_length + transition_length, r_small - wall_thickness)],
    tangents=[(1, 0), (1, 0)],
    includeCurrent=True
)

path = path.lineTo(total_length, r_small - wall_thickness) # Inner small straight
path = path.lineTo(total_length, r_small) # Face at small end
path = path.lineTo(large_section_length + transition_length, r_small) # Outer small straight

# Curve up (Outer transition)
# Spline back to the large section radius
mid_y_outer = (r_large + r_small) / 2.0
path = path.spline(
    [(large_section_length, r_large)],
    tangents=[(-1, 0), (-1, 0)],
    includeCurrent=True
)

path = path.lineTo(0, r_large) # Outer large straight
path = path.close() # Close face at large end

# Revolve
result = path.revolve(360, (0,0,0), (1,0,0))

# Export to verify (optional in script, but good practice)
# cq.exporters.export(result, "reducer.step")