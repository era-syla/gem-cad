import cadquery as cq
from math import cos, sin, radians

# --- Parameters ---
outer_radius = 60.0       # Distance from center to tip
inner_radius = 20.0       # Distance from center to valley
thickness = 5.0           # Thickness of the plate
hole_diameter = 12.0      # Diameter of the central hole
blade_curve_radius = 80.0 # Radius of the concave blade edges
valley_fillet = 8.0       # Radius of the fillet at the valleys
blade_chamfer = 2.0       # Size of the bevel on the blades
hole_chamfer = 1.0        # Size of the bevel on the hole

# --- Modeling ---

# 1. Create the star profile
# Start at the first tip (Angle 0)
wp = cq.Workplane("XY").moveTo(outer_radius, 0)

# Loop to create the 4 arms of the star
for i in range(4):
    # Angles for the current valley and the next tip
    angle_valley = i * 90 + 45
    angle_next_tip = (i + 1) * 90
    
    # Coordinates for the valley point
    val_x = inner_radius * cos(radians(angle_valley))
    val_y = inner_radius * sin(radians(angle_valley))
    
    # Coordinates for the next tip point
    tip_x = outer_radius * cos(radians(angle_next_tip))
    tip_y = outer_radius * sin(radians(angle_next_tip))
    
    # Create concave arcs connecting Tip -> Valley -> Next Tip
    # Using a negative radius with radiusArc creates a curve to the "right" 
    # of the path (inward for a CCW traversal), creating the concave blade shape.
    wp = wp.radiusArc((val_x, val_y), -blade_curve_radius)
    wp = wp.radiusArc((tip_x, tip_y), -blade_curve_radius)

# 2. Extrude the base shape
result = wp.close().extrude(thickness)

# 3. Fillet the valleys (inner corners)
# We select vertical edges (|Z) and filter for those close to the center 
# to distinguish valleys from tips.
threshold_dist = (outer_radius + inner_radius) / 2
valley_edges = [
    e for e in result.edges("|Z").vals() 
    if e.Center().Length < threshold_dist
]
result = result.newObject(valley_edges).fillet(valley_fillet)

# 4. Chamfer the outer blade edges
# Select all edges on the top face (>Z). At this stage, this selects the entire perimeter.
result = result.faces(">Z").edges().chamfer(blade_chamfer)

# 5. Cut the center hole
result = result.faces(">Z").workplane().circle(hole_diameter / 2).cutThruAll()

# 6. Chamfer the center hole
# Select the edge on the top face closest to the origin (0,0)
result = result.faces(">Z").edges(cq.NearestToPointSelector((0, 0))).chamfer(hole_chamfer)

# The 'result' variable now contains the final solid geometry.