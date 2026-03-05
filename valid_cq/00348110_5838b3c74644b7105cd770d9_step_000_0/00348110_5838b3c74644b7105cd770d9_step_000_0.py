import cadquery as cq
import math

# --- Parameters ---
wire_diameter = 1.5
mean_diameter = 10.0
radius = mean_diameter / 2.0
pitch = wire_diameter  # Close-wound for tension spring
coils = 15
helix_height = coils * pitch

# --- Helper Functions ---
def make_helix_edge(pitch, height, radius):
    """Creates the helical edge for the main body"""
    # makeHelix creates a Wire, we extract the Edge
    return cq.Wire.makeHelix(pitch=pitch, height=height, radius=radius).Edges()[0]

# --- Geometry Construction ---

# 1. Bottom Hook
# Modeled as a 270-degree loop starting at the center axis (0,0,0)
# and winding outwards to connect to the helix start at (R, 0, 0)

# Points for Bottom Hook
p_bot_tip = cq.Vector(0, 0, 0)
p_bot_side_1 = cq.Vector(0, radius, -radius)
p_bot_bottom = cq.Vector(0, 0, -2 * radius)
p_bot_side_2 = cq.Vector(0, -radius, -radius)
p_helix_start = cq.Vector(radius, 0, 0)

# Tangents
t_bot_tip = cq.Vector(0, 1, 0)  # Starting tangent in Y direction
t_bot_side_2 = cq.Vector(0, 0, 1) # Tangent pointing up Z at the connection point
t_helix_start = cq.Vector(0, 1, pitch / (2 * math.pi * radius)).normalized()

# Arcs for the loop (YZ plane)
# Segment 1: Tip to Bottom (180 deg)
edge_bot_loop_1 = cq.Edge.makeThreePointArc(p_bot_tip, p_bot_side_1, p_bot_bottom)
# Segment 2: Bottom to Side connection (90 deg)
# Midpoint calculation for 90 deg arc
# Center is (0, 0, -R). Radius R. From (0, 0, -2R) to (0, -R, -R).
p_bot_mid_2 = cq.Vector(0, -radius * math.sin(math.radians(45)), -radius - radius * math.cos(math.radians(45)))
edge_bot_loop_2 = cq.Edge.makeThreePointArc(p_bot_bottom, p_bot_mid_2, p_bot_side_2)

# Transition Spline: Connects loop to helix start
# Bends from YZ plane to tangent of helix
edge_bot_trans = cq.Edge.makeSpline(
    [p_bot_side_2, p_helix_start],
    tangents=[t_bot_side_2, t_helix_start]
)

# 2. Main Helix Body
edge_helix = make_helix_edge(pitch, helix_height, radius)

# 3. Top Hook
# Symmetric to bottom hook, transitioning from helix end to center axis
p_helix_end = cq.Vector(radius, 0, helix_height)
p_top_side_1 = cq.Vector(0, radius, helix_height + radius)
p_top_top = cq.Vector(0, 0, helix_height + 2 * radius)
p_top_side_2 = cq.Vector(0, -radius, helix_height + radius)
p_top_tip = cq.Vector(0, 0, helix_height)

# Tangents
t_helix_end = cq.Vector(0, 1, pitch / (2 * math.pi * radius)).normalized()
t_top_side_1 = cq.Vector(0, 0, 1) # Tangent pointing up Z

# Transition Spline
edge_top_trans = cq.Edge.makeSpline(
    [p_helix_end, p_top_side_1],
    tangents=[t_helix_end, t_top_side_1]
)

# Arcs for the loop
# Segment 1: Side to Top to Side (180 deg)
edge_top_loop_1 = cq.Edge.makeThreePointArc(p_top_side_1, p_top_top, p_top_side_2)

# Segment 2: Side to Tip (90 deg to close loop at center)
p_top_mid_2 = cq.Vector(0, -radius * math.sin(math.radians(45)), helix_height + radius - radius * math.cos(math.radians(45)))
edge_top_loop_2 = cq.Edge.makeThreePointArc(p_top_side_2, p_top_mid_2, p_top_tip)

# --- Assembly ---

# Combine all edges into a single wire
spring_path = cq.Wire.assembleEdges([
    edge_bot_loop_1,
    edge_bot_loop_2,
    edge_bot_trans,
    edge_helix,
    edge_top_trans,
    edge_top_loop_1,
    edge_top_loop_2
])

# Create the solid by sweeping a circle profile along the path
# We create the profile on the XZ plane because the path starts at (0,0,0) with tangent (0,1,0) (Y-axis)
result = (
    cq.Workplane("XZ")
    .center(0, 0)
    .circle(wire_diameter / 2)
    .sweep(spring_path)
)