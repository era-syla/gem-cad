import cadquery as cq
import math

# --- Parameters ---
thickness = 5.0             # Thickness of the plate
arm_outer_radius = 65.0     # Distance from center to the tip of the arms
waist_radius = 28.0         # Distance from center to the closest point of the side curves
arm_width = 24.0            # Width of the arm tip face
notch_width = 8.0           # Width of the rectangular cutout
notch_depth = 7.0           # Depth of the rectangular cutout
center_hole_diam = 6.0      # Diameter of the central hole
arm_hole_diam = 4.0         # Diameter of the holes on the arms
arm_hole_dist = 52.0        # Distance from center to the arm holes

# --- Helper Functions ---

def get_arm_profile_points(angle_deg):
    """
    Generates the list of points defining the tip of an arm, including the notch.
    Points are ordered for a Counter-Clockwise traversal of the entire shape.
    """
    angle_rad = math.radians(angle_deg)
    
    # Arm direction vector
    dx = math.cos(angle_rad)
    dy = math.sin(angle_rad)
    
    # CCW Tangent vector (-y, x) relative to direction
    tx = -dy
    ty = dx
    
    # Center of the arm tip face
    cx = dx * arm_outer_radius
    cy = dy * arm_outer_radius
    
    # Offsets
    hw = arm_width / 2.0
    hnw = notch_width / 2.0
    
    # Define points relative to tip center
    # We traverse the tip from "Clockwise" side to "Counter-Clockwise" side
    # Relative to the arm vector, this is Right to Left.
    
    # P1: Start corner (Right)
    p1 = (cx - tx * hw, cy - ty * hw)
    # P2: Notch start (Right)
    p2 = (cx - tx * hnw, cy - ty * hnw)
    # P3: Notch inner corner (Right)
    p3 = (p2[0] - dx * notch_depth, p2[1] - dy * notch_depth)
    # P4: Notch inner corner (Left)
    p4 = (p3[0] + tx * notch_width, p3[1] + ty * notch_width)
    # P5: Notch end (Left)
    p5 = (cx + tx * hnw, cy + ty * hnw)
    # P6: End corner (Left)
    p6 = (cx + tx * hw, cy + ty * hw)
    
    return [p1, p2, p3, p4, p5, p6]

def get_midpoint(angle_deg):
    """Calculates the midpoint of the arc between arms."""
    rad = math.radians(angle_deg)
    return (math.cos(rad) * waist_radius, math.sin(rad) * waist_radius)

# --- Geometry Construction ---

# Define the arm angles (X-shape)
arm_angles = [45, 135, 225, 315]
# Define the angles for the curve midpoints (between arms)
mid_angles = [90, 180, 270, 0]

# Initialize Workplane
wp = cq.Workplane("XY")

# Generate points for the first arm to start the path
pts0 = get_arm_profile_points(arm_angles[0])

# Move to the start point
wp = wp.moveTo(pts0[0][0], pts0[0][1])

# Loop through all 4 arms to build the continuous wire
for i in range(4):
    current_angle = arm_angles[i]
    next_angle = arm_angles[(i + 1) % 4]
    
    # Get points for the current arm
    pts = get_arm_profile_points(current_angle)
    
    # Draw the arm tip profile (Lines)
    # We skip pts[0] because the previous operation (moveTo or arc) ended there
    for p in pts[1:]:
        wp = wp.lineTo(p[0], p[1])
        
    # Draw the large arc to the next arm
    # Start point is current pts[-1] (Left corner of current arm)
    # End point is start corner (pts[0]) of next arm
    next_pts = get_arm_profile_points(next_angle)
    mid_pt = get_midpoint(mid_angles[i])
    
    wp = wp.threePointArc(mid_pt, next_pts[0])

# Close the wire and extrude
result = wp.close().extrude(thickness)

# --- Features (Holes) ---

# Central Hole
result = result.faces(">Z").workplane().circle(center_hole_diam / 2.0).cutThruAll()

# Arm Holes
# Based on the image, holes appear on the right-hand side arms (angles 45 and 315)
h1_pos = (math.cos(math.radians(45)) * arm_hole_dist, 
          math.sin(math.radians(45)) * arm_hole_dist)
h2_pos = (math.cos(math.radians(315)) * arm_hole_dist, 
          math.sin(math.radians(315)) * arm_hole_dist)

result = result.faces(">Z").workplane() \
               .pushPoints([h1_pos, h2_pos]) \
               .circle(arm_hole_diam / 2.0) \
               .cutThruAll()