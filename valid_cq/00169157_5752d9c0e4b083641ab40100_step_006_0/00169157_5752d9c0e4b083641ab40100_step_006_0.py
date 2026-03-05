import cadquery as cq

# Dimensions
total_length = 130.0
width = 14.0
wall_thickness = 1.5

# Define the master profile points for the side view (XZ plane)
# Coordinates are approximated based on the visual proportions
# Origin (0,0) is at the bottom-left of the main block section
outer_profile = [
    (0, 0),
    (0, 8),           # Step up at the front
    (-4, 8),          # Overhang underside
    (-6, 11),         # Angled nose bottom
    (-6, 20),         # Nose front vertical
    (0, 20),          # Nose top return
    (0, 26),          # Main block front face vertical
    (35, 26),         # Main block top
    (35, 16),         # Step down vertical
    (48, 16),         # Mid section flat
    (105, 5),         # Long slope down
    (115, 5),         # Flat before tip
    (115, 8),         # Tip block rear vertical
    (125, 8),         # Tip block top
    (125, 3),         # Tip block front vertical
    (128, 0),         # Tip point
    (0, 0)            # Return to start
]

# Create the main solid body
main_body = cq.Workplane("XZ").polyline(outer_profile).close().extrude(width)

# Define the inner profile to create the shell/pocket effect
# Manual offset ensures the complex shape is hollowed correctly
inner_profile = [
    (wall_thickness, wall_thickness),
    (wall_thickness, 8 + wall_thickness),
    (-4 + wall_thickness, 8 + wall_thickness),
    (-6 + wall_thickness, 11 + wall_thickness),
    (-6 + wall_thickness, 20 - wall_thickness),
    (0 + wall_thickness, 20 - wall_thickness),
    (0 + wall_thickness, 26 - wall_thickness),
    (35 - wall_thickness, 26 - wall_thickness),
    (35 - wall_thickness, 16 - wall_thickness),
    (48, 16 - wall_thickness),
    (105, 5 - wall_thickness),
    (115, 5 - wall_thickness),
    (115, 8 - wall_thickness),
    (125 - wall_thickness, 8 - wall_thickness),
    (125 - wall_thickness, wall_thickness)
]

# Create the pocket cutter geometry
# We extrude it to (width - wall_thickness) to leave a back wall
pocket = cq.Workplane("XZ").polyline(inner_profile).close().extrude(width - wall_thickness)
# Move the pocket to align with the front face (leaving the back wall)
pocket = pocket.translate((0, wall_thickness, 0))

# Cut the pocket from the main body
result = main_body.cut(pocket)

# Add the internal feature (rib/catch mechanism)
# Located inside the mid-section pocket
rib_pts = [
    (52, wall_thickness),
    (52, 10),
    (58, 12),
    (64, 10),
    (64, wall_thickness)
]
rib = cq.Workplane("XZ").workplane(offset=wall_thickness).polyline(rib_pts).close().extrude(width / 2)
result = result.union(rib)

# Create the top opening on the left main block
# This cuts a rectangular slot into the top surface
top_cut = cq.Workplane("XY").workplane(offset=26).rect(28, width - 2*wall_thickness).extrude(-12)
top_cut = top_cut.translate((17.5, 0, 0)) # Center the cut roughly on the block
result = result.cut(top_cut)

# Add a small notch at the very bottom front corner for detail
front_notch = cq.Workplane("XY").rect(6, 6).extrude(10).translate((0, 0, 0))
result = result.cut(front_notch)