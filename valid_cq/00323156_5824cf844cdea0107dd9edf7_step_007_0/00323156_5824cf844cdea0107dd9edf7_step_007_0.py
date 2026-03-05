import cadquery as cq
import math

# --- Parameters ---
# Main body dimensions
width = 12.0
arm_straight_len = 18.0
arm_bent_len = 48.0
bend_angle = 32.0  # degrees
arm_thick_hinge = 11.0
arm_thick_tip = 4.0

# Hinge dimensions
hinge_outer_dia = 12.0
hinge_pin_dia = 5.0
slot_width = 5.0

# Serration details
num_teeth = 8
tooth_depth = 1.2

# Derived values
hinge_rad = hinge_outer_dia / 2.0
pin_rad = hinge_pin_dia / 2.0
rad = math.radians(bend_angle)

# --- Geometry Construction ---

# 1. Define Key Points (XZ Plane, Hinge Center at Origin)
p_hinge_top = (0, hinge_rad)
p_bend_top = (arm_straight_len, hinge_rad)

# Calculate tip position
tip_dx = arm_bent_len * math.cos(rad)
tip_dy = -arm_bent_len * math.sin(rad)
p_tip_top = (p_bend_top[0] + tip_dx, p_bend_top[1] + tip_dy)

# Calculate tip bottom (perpendicular to arm axis)
norm_x = math.sin(rad)
norm_y = math.cos(rad)
p_tip_bot = (p_tip_top[0] - arm_thick_tip * norm_x, 
             p_tip_top[1] - arm_thick_tip * norm_y)

# Bottom point where serrations end (under the straight section)
p_base_bot = (arm_straight_len, hinge_rad - arm_thick_hinge)

p_hinge_bot = (0, -hinge_rad)

# 2. Build Profile Path
pts = [p_hinge_top, p_bend_top, p_tip_top, p_tip_bot]

# Generate Serrations (from tip bottom to base bottom)
# Vector representing the baseline of the serrations
vx = p_base_bot[0] - p_tip_bot[0]
vy = p_base_bot[1] - p_tip_bot[1]
baseline_len = math.sqrt(vx**2 + vy**2)

# Normal vector pointing "into" the material (Right-Up relative to the Left-Up baseline)
# Rotate vector (vx, vy) 90 degrees Clockwise
nx = vy / baseline_len
ny = -vx / baseline_len

step_x = vx / num_teeth
step_y = vy / num_teeth

curr_x, curr_y = p_tip_bot

for i in range(num_teeth):
    # Calculate next peak on the baseline
    next_peak_x = p_tip_bot[0] + (i + 1) * step_x
    next_peak_y = p_tip_bot[1] + (i + 1) * step_y
    
    # Calculate the valley point (inset into the material)
    valley_x = curr_x + nx * tooth_depth
    valley_y = curr_y + ny * tooth_depth
    
    pts.append((valley_x, valley_y))
    pts.append((next_peak_x, next_peak_y))
    
    curr_x, curr_y = next_peak_x, next_peak_y

pts.append(p_hinge_bot)

# 3. Create Solid
# Create the profile wire
profile = cq.Workplane("XZ").polyline(pts)

# Close the profile with the arc at the hinge back
# Connects p_hinge_bot to p_hinge_top via (-R, 0)
profile = profile.threePointArc((-hinge_rad, 0), p_hinge_top).close()

# Extrude to create the main solid
# Centered extrusion makes symmetry operations easier
body = profile.extrude(width / 2.0, both=True)

# 4. Hinge Detail
# Cut the central slot for the clevis
# Create a cutting tool centered on Y=0
cutter = cq.Workplane("XZ").rect(hinge_outer_dia * 3, hinge_outer_dia * 3).extrude(slot_width / 2.0, both=True)
body = body.cut(cutter)

# Add the hinge pin bridging the gap
pin = cq.Workplane("XZ").circle(pin_rad).extrude(width / 2.0, both=True)
result = body.union(pin)

# 5. Finishing
# Chamfer the top outer edges
# Select edges on top faces (+Z) that are on the outer sides (abs(y) approx width/2)
try:
    edges_to_chamfer = result.faces("+Z").edges().filter(lambda e: abs(e.center().y) > (width/2.0 - 1.0))
    result = result.chamfer(0.8, edges_to_chamfer)
except:
    # Fallback in case of selection issues
    pass

# Export or Render
if 'show_object' in globals():
    show_object(result)