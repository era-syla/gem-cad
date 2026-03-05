import cadquery as cq

# Define parametric dimensions for the shape
thickness = 2.0
overall_height = 80.0
top_width = 12.0
bottom_width = 4.0

# Define points for the spline/curve profile
# We will define the outer boundary using a series of points to approximate the S-curve
pts = [
    (5, 0),         # Bottom tip right
    (0, 0),         # Bottom tip left
    (-10, 30),      # Mid-section belly outer
    (-5, 60),       # Neck transition outer
    (0, 75),        # Top head left
    (5, 80),        # Top head peak
    (10, 75),       # Top head right
    (5, 60),        # Neck transition inner
    (-3, 30),       # Mid-section belly inner
]

# Create the main profile using a spline for smooth curvature and close it with a line
# Note: Splines can be tricky, so we'll build a face from a wire.
profile_wire = (
    cq.Workplane("XY")
    .spline(pts, includeCurrent=True)
    .close()
)

# Extrude the profile to create the solid body
body = profile_wire.extrude(thickness)

# Add the two mounting holes at the top
# Estimated positions relative to the top feature
hole_diam_1 = 3.0
hole_diam_2 = 2.5

# Position 1: Near the very top
result = (
    body.faces(">Z") # Select the top face (though extrude is usually Z-up, let's work on the XY plane logic)
    .workplane()
    # Since we extruded in Z, the profile is on XY. Let's orient correctly.
    # Actually, the previous step extruded the XY profile in Z. 
    # Let's perform the cuts perpendicular to the profile face (through the thickness).
)

# Re-approach: It's easier to subtract from the workplane before extruding or cut the solid.
# Let's cut the solid.
# The holes are in the "head" section. Based on the points (0,75) to (10,75).
hole1_pos = (5.0, 75.0) # Near top
hole2_pos = (2.0, 68.0) # Slightly lower and left

result = (
    body
    .faces("<Z") # Select the bottom face (Z=0 plane)
    .workplane()
    .moveTo(*hole1_pos)
    .circle(hole_diam_1 / 2)
    .cutThruAll()
    .moveTo(*hole2_pos)
    .circle(hole_diam_2 / 2)
    .cutThruAll()
)

# Optional: Fillet the edges for a smoother look similar to the render
# The render looks fairly sharp but maybe has a tiny chamfer or fillet.
# Let's apply a small fillet to the vertical edges (the perimeter).
result = result.edges("|Z").fillet(0.5)

# Final check of orientation. The image shows it standing up. 
# The current model lies flat on XY. Let's rotate it to stand up for the "view".
result = result.rotate((0,0,0), (1,0,0), 90)