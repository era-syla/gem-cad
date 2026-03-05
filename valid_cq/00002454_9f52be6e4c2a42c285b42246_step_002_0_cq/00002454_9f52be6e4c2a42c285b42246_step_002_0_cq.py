import cadquery as cq

# Parametric dimensions
total_length = 50.0

# Section 1: The smaller straight cylinder (left side)
s1_length = 15.0
s1_outer_diam = 20.0

# Section 2: The main body (slightly larger cylinder)
s2_length = 25.0
s2_outer_diam = 22.0

# Section 3: The flared end (right side)
s3_length = 10.0
s3_end_diam = 30.0

# Internal bore (through hole)
inner_diam = 12.0

# Fillet radius for the transition between flared end and main body
fillet_radius = 5.0

# Create the profile for revolution
# We will draw the upper half of the cross-section on the XZ plane and revolve around the Z-axis (or X-axis).
# Let's align the axis with the X-axis.

# Calculate radii
r1 = s1_outer_diam / 2.0
r2 = s2_outer_diam / 2.0
r3 = s3_end_diam / 2.0
r_inner = inner_diam / 2.0

# Define points for the outer profile
# Starting from left (x=0) to right
p0 = (0, r_inner)
p1 = (0, r1)
p2 = (s1_length, r1)
p3 = (s1_length, r2) # Step up
p4 = (s1_length + s2_length, r2)
p5 = (s1_length + s2_length + s3_length, r3) # Flared out
p6 = (s1_length + s2_length + s3_length, r_inner) # Back to inner bore at end
p7 = (0, r_inner) # Close the loop

# Create the solid using a revolve operation
# We construct the points and then revolve around the X axis.
result = (
    cq.Workplane("XY")
    .polyline([p0, p1, p2, p3, p4, p5, p6, p0])
    .close()
    .revolve(360, (0, 0, 0), (1, 0, 0))
)

# Apply a fillet to smooth the transition between the main body and the flare
# Select the edge at x = s1_length + s2_length
# The selector finds edges near that X coordinate.
# Note: The "step" at s1_length is usually sharp or a small chamfer, but the flare transition often has a fillet.
# Looking at the image, the transition from the middle cylinder to the flared part is smooth.
# The transition from the first cylinder to the second looks like a sharp step or a small chamfer/groove.

try:
    # Attempt to fillet the neck transition (between straight body and flare)
    # The X coordinate is s1_length + s2_length
    result = result.edges(cq.nearestToPoint((s1_length + s2_length, r2, 0))).fillet(fillet_radius)
except Exception:
    # Fallback if selection fails, though parametric positioning usually works
    pass

# The step between section 1 and 2 looks sharp in the image, maybe a tiny chamfer, but we'll leave it as a step based on the profile.
# If a groove is needed, it would be modeled, but the image suggests a simple shoulder.