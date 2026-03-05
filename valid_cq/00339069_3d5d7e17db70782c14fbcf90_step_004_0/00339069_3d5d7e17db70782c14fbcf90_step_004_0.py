import cadquery as cq
import math

# --- Parameters ---
outer_radius = 50.0   # Radius of the tip of the teeth
inner_radius = 42.0   # Radius of the root of the teeth
thickness = 2.0       # Thickness of the blade
hole_diameter = 5.0   # Diameter of the central hole
num_teeth = 24        # Number of teeth on the saw blade

# Ratio of the angular pitch used for the cutting face (steep drop)
# 0.2 means the steep face takes 20% of the tooth angle, the back slope takes 80%
tooth_face_ratio = 0.2 

# --- Geometry Generation ---

points = []
angle_step = 2 * math.pi / num_teeth

for i in range(num_teeth):
    base_angle = i * angle_step
    
    # Define angles for the tip and the root of the current tooth
    # To create teeth that point Clockwise (standard for saw blades), 
    # we define the sequence traversing Counter-Clockwise:
    # 1. Tip (Outer Radius)
    # 2. Steep Drop to Root (Inner Radius)
    # 3. Shallow Rise to next Tip
    
    tip_angle = base_angle
    root_angle = base_angle + (angle_step * tooth_face_ratio)
    
    # Calculate Cartesian coordinates for Tip
    tx = outer_radius * math.cos(tip_angle)
    ty = outer_radius * math.sin(tip_angle)
    points.append((tx, ty))
    
    # Calculate Cartesian coordinates for Root
    rx = inner_radius * math.cos(root_angle)
    ry = inner_radius * math.sin(root_angle)
    points.append((rx, ry))

# Create the saw blade body
# 1. Draw the profile using the calculated points
# 2. Close the wire to form a face
# 3. Extrude to create the 3D solid
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
)

# Cut the central mounting hole
result = (
    result
    .faces(">Z")
    .workplane()
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)