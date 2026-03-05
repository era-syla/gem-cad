import cadquery as cq
import math

# --- Parameter Definitions ---
outer_diameter = 50.0   # Diameter of the cylinder to the tips of the teeth
height = 30.0           # Height of the cylinder
num_teeth = 36          # Total number of teeth around the circumference
tooth_depth = 2.0       # How deep each groove is cut
tooth_width_ratio = 0.5 # Ratio of tooth width to gap width (0.5 means equal width)

# --- Derived Calculations ---
radius = outer_diameter / 2.0
inner_radius = radius - tooth_depth
angle_per_tooth = 360.0 / num_teeth

# --- Geometry Construction ---

# 1. Create the base cylinder
base = cq.Workplane("XY").circle(radius).extrude(height)

# 2. Define the profile of a single cutting tool (the negative space)
# We will cut grooves into the cylinder.
# The cutter shape is roughly a trapezoid or rounded rectangle.
# We'll construct a 2D profile and extrude it, then use it to cut.

# Calculate the width of the cut at the circumference
circumference = math.pi * outer_diameter
cut_width = (circumference / num_teeth) * (1 - tooth_width_ratio)

# To make the cut, we'll create a sketch on the XY plane for one gap
# We position a rectangle (or trapezoid) at the edge
cutter_sketch = (
    cq.Workplane("XY")
    .moveTo(radius, 0)
    .rect(tooth_depth * 2, cut_width) # Make the rectangle wide enough to cut through the edge
    .extrude(height)
)

# 3. Create the pattern of cuts
# We perform a polar pattern of the cutter around the center
cutters = (
    cutter_sketch
    .rotate((0,0,0), (0,0,1), 0) # Initial orientation
)

# Apply the cut for every tooth position
result = base
for i in range(num_teeth):
    angle = i * angle_per_tooth
    # Create a rotated copy of the cutter
    rotated_cutter = cutter_sketch.rotate((0,0,0), (0,0,1), angle)
    # Cut the material
    result = result.cut(rotated_cutter)

# Optimization Note: While the loop method works, CadQuery has a 'polarArray' feature
# which is often cleaner for creating the sketches before extrusion.
# Let's refactor for a more robust parametric approach using a single sketch operation.

def gear_profile(r_outer, r_inner, num_teeth):
    """
    Generates points for a simplified gear-like profile.
    """
    points = []
    angle_step = 2 * math.pi / num_teeth
    
    # We create points: inner, inner, outer, outer for each tooth section
    # This creates a "square wave" wrapped around a circle
    
    # Adjust angular width of the 'tooth' vs the 'gap'
    tooth_ratio = 0.5 
    
    for i in range(num_teeth):
        theta_start = i * angle_step
        theta_mid1 = theta_start + (angle_step * (1-tooth_ratio)/2)
        theta_mid2 = theta_start + angle_step - (angle_step * (1-tooth_ratio)/2)
        theta_end = (i + 1) * angle_step
        
        # Calculate coordinates
        # Point 1: Start of gap (Outer radius)
        # Actually, let's trace: Tooth start -> Tooth end -> Gap start -> Gap end
        
        # Current logic: Let's assume the tooth is at the outer radius and gap is inner
        
        # Angle 1: Start of tooth (Outer)
        theta_1 = i * angle_step
        x1 = r_outer * math.cos(theta_1)
        y1 = r_outer * math.sin(theta_1)
        
        # Angle 2: End of tooth top flat (Outer)
        theta_2 = i * angle_step + (angle_step * 0.5) 
        # Making it slightly trapezoidal looks better, but simple square wave is safer first.
        # Let's apply a slight inset angle for the walls to make it look like the image.
        wall_angle_offset = angle_step * 0.1
        
        theta_tooth_start = i * angle_step + wall_angle_offset
        theta_tooth_end = (i+1) * angle_step - wall_angle_offset
        
        # Gap center is at i*angle_step (inner radius)
        # Tooth center is at i*angle_step + angle_step/2 (outer radius)
        
        # Let's rebuild the point logic to be continuous
        center_angle = i * angle_step
        next_center_angle = (i + 1) * angle_step
        half_step = angle_step / 2
        
        # Tooth tip (outer)
        pt1_x = r_outer * math.cos(center_angle + half_step * 0.3)
        pt1_y = r_outer * math.sin(center_angle + half_step * 0.3)
        
        pt2_x = r_outer * math.cos(next_center_angle - half_step * 0.3)
        pt2_y = r_outer * math.sin(next_center_angle - half_step * 0.3)
        
        # Tooth valley (inner)
        pt3_x = r_inner * math.cos(next_center_angle + half_step * 0.3)
        pt3_y = r_inner * math.sin(next_center_angle + half_step * 0.3)
        
        pt4_x = r_inner * math.cos(next_center_angle + 2*half_step - half_step * 0.3)
        pt4_y = r_inner * math.sin(next_center_angle + 2*half_step - half_step * 0.3)

        # Simplified approach: CadQuery's gear plugin is great, but standard CQ primitives
        # are requested. Let's use the polyline approach.
        pass

# --- Final Refined Approach: Parametric Sketch with Polyline ---
# This is much faster and generates a cleaner topology than boolean cutting 36 times.

points = []
angle_step = 2 * math.pi / num_teeth
tooth_span_angle = angle_step * 0.5 # 50% tooth, 50% gap

# Define how much the tooth tapers (make walls slight angled, not 90 deg)
taper_angle = angle_step * 0.1 

for i in range(num_teeth):
    base_angle = i * angle_step
    
    # Coordinates for one tooth cycle (Valley -> Wall -> Top -> Wall)
    
    # 1. Start of Valley (Inner Radius)
    theta1 = base_angle + taper_angle
    p1 = (inner_radius * math.cos(theta1), inner_radius * math.sin(theta1))
    
    # 2. Start of Tooth Top (Outer Radius)
    theta2 = base_angle + (angle_step/2) - taper_angle
    p2 = (outer_diameter/2 * math.cos(theta2), outer_diameter/2 * math.sin(theta2))
    
    # 3. End of Tooth Top (Outer Radius)
    theta3 = base_angle + (angle_step/2) + taper_angle
    p3 = (outer_diameter/2 * math.cos(theta3), outer_diameter/2 * math.sin(theta3))
    
    # 4. End of Valley / Start of next (Inner Radius)
    theta4 = base_angle + angle_step - taper_angle
    p4 = (inner_radius * math.cos(theta4), inner_radius * math.sin(theta4))
    
    points.extend([p1, p2, p3, p4])

# Close the profile automatically by extrusion logic or ensure last point connects
# Workplane.polyline automatically closes if extruded usually, or we can explicit close.

result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(height)
)

# Optional: Add small fillets to vertical edges to match the soft look in the image
# This can be computationally expensive with many edges, but looks better.
# result = result.edges("|Z").fillet(0.2)