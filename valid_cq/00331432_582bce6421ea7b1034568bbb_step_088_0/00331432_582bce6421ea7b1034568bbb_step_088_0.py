import cadquery as cq

# ------------------------------------------------------------------------------
# Parameter Definitions
# ------------------------------------------------------------------------------
wire_radius = 1.5           # Radius of the tube cross-section
bend_radius = 80.0          # Radius of the main arc
leg_length = 35.0           # Length of the straight sections
groove_width = 0.6          # Width of the indentations
groove_depth = 0.25         # Depth of the indentations
groove_positions = [4.0, 8.0] # Distance from the tips to the groove centers

# ------------------------------------------------------------------------------
# Modeling
# ------------------------------------------------------------------------------

# 1. Define the Sweep Path
# The geometry consists of two straight legs connected by a 180-degree arc.
# We define this path in the XY plane.
# Start point: Right leg tip (bend_radius, -leg_length, 0)
path = (
    cq.Workplane("XY")
    .moveTo(bend_radius, -leg_length)
    .lineTo(bend_radius, 0)  # Straight line up to the arc start
    .threePointArc((0, bend_radius), (-bend_radius, 0)) # 180-degree arc
    .lineTo(-bend_radius, -leg_length) # Straight line down for left leg
)

# 2. Create the Solid Wire (Sweep)
# Create the circular profile on the XZ plane aligned with the start of the path.
# Normal of XZ plane is Y-axis, which matches the tangent of the leg.
result = (
    cq.Workplane("XZ")
    .workplane(offset=-leg_length) # Move plane to the tip of the leg
    .moveTo(bend_radius, 0)        # Move to the center of the wire
    .circle(wire_radius)
    .sweep(path)
)

# 3. Create and Cut Grooves
# We construct 'cutter' tools (tubes) at specific locations and subtract them.
for dist in groove_positions:
    y_pos = -leg_length + dist
    
    # Define the cutter geometry: a tube representing the negative space of the groove
    # We do this for both the right leg (x > 0) and left leg (x < 0)
    
    # Right Leg Cutter
    cutter_right = (
        cq.Workplane("XZ")
        .workplane(offset=y_pos)
        .moveTo(bend_radius, 0)
        .circle(wire_radius + 1.0)       # Outer boundary (clearance)
        .circle(wire_radius - groove_depth) # Inner boundary (groove floor)
        .extrude(groove_width)
    )
    
    # Left Leg Cutter
    cutter_left = (
        cq.Workplane("XZ")
        .workplane(offset=y_pos)
        .moveTo(-bend_radius, 0)
        .circle(wire_radius + 1.0)
        .circle(wire_radius - groove_depth)
        .extrude(groove_width)
    )
    
    # Apply the cuts
    result = result.cut(cutter_right).cut(cutter_left)

# 4. Finishing Details
# Apply a small fillet to the ends of the wire for a polished look.
# We select the faces at the minimum Y coordinate (the tips).
try:
    result = result.faces("<Y").edges().fillet(0.2)
except Exception:
    pass # Skip fillet if geometry prevents it (e.g. overlap with groove)
