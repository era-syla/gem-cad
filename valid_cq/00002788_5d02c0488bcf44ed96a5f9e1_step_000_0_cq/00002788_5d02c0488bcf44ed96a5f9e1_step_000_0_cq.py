import cadquery as cq
from math import pi, cos, sin, radians

def involute_gear(module, num_teeth, thickness, pressure_angle=20.0, clearance=0.0, backlash=0.0):
    """
    Generate an involute gear profile.
    
    Args:
        module: The module of the gear (pitch diameter / number of teeth).
        num_teeth: Number of teeth.
        thickness: Thickness of the gear (extrusion height).
        pressure_angle: Pressure angle in degrees (default 20).
        clearance: Clearance between teeth roots (default 0).
        backlash: Backlash allowance (default 0).
    
    Returns:
        A CadQuery Workplane object representing the gear.
    """
    
    # Gear Calculations
    pitch_diameter = module * num_teeth
    base_diameter = pitch_diameter * cos(radians(pressure_angle))
    addendum = module
    dedendum = 1.25 * module + clearance
    
    outer_radius = (pitch_diameter / 2.0) + addendum
    root_radius = (pitch_diameter / 2.0) - dedendum
    
    # Generate the involute curve for one tooth flank
    # Number of points for the involute curve
    num_points = 20 
    
    def involute_point(t, base_r):
        x = base_r * (cos(t) + t * sin(t))
        y = base_r * (sin(t) - t * cos(t))
        return x, y

    # Calculate the involute curve points
    # We need to find the t value where the involute hits the outer radius
    # r^2 = x^2 + y^2 = rb^2 * (1 + t^2)
    # t_max = sqrt((r_outer / r_base)^2 - 1)
    t_max = ((outer_radius / (base_diameter/2.0))**2 - 1)**0.5
    
    involute_points = []
    for i in range(num_points + 1):
        t = (i / num_points) * t_max
        involute_points.append(involute_point(t, base_diameter/2.0))
    
    # Tooth thickness angle at pitch circle
    # Arc length = pi * m / 2 (standard tooth thickness)
    # Angle = Arc length / Radius = (pi * m / 2) / (m * N / 2) = pi / N
    tooth_thickness_angle = pi / num_teeth
    
    # Angle where the involute curve intersects the pitch circle
    # inv(alpha) = tan(alpha) - alpha
    # We know the pressure angle at pitch circle is 'pressure_angle'
    pa_rad = radians(pressure_angle)
    inv_pa = tan_pa = sin(pa_rad)/cos(pa_rad) - pa_rad
    
    # The involute generated starts at angle 0. At pitch radius, its angle is inv_pa.
    # We want the center of the tooth to be at angle 0.
    # The half thickness angle is tooth_thickness_angle / 2.
    # So we need to rotate the flank by: (tooth_thickness_angle / 2 + inv_pa)
    # Wait, coordinate system:
    # If the involute starts at X axis (angle 0), at pitch radius R, the angular position is inv_pa.
    # We want the tooth to be symmetric around X axis.
    # The tooth has a width of `tooth_thickness_angle` at pitch radius.
    # So the right flank should pass through angle -tooth_thickness_angle/4 relative to centerline?
    # No, usually we center a tooth or a gap. Let's center a tooth on the X axis.
    # The angular width is `tooth_thickness_angle`.
    # So the right flank intersection with pitch circle is at -tooth_thickness_angle/2.
    # The generated involute point at pitch circle is at angle `inv_pa`.
    # So we need to rotate the generated involute by -(inv_pa + tooth_thickness_angle/2).
    # Let's adjust for backlash here if needed: subtract backlash angle / 2
    
    backlash_angle = backlash / (pitch_diameter / 2.0)
    half_tooth_angle = tooth_thickness_angle / 2.0 - (backlash_angle / 4.0)
    
    rotation_offset = -(inv_pa + half_tooth_angle)
    
    # Create the full tooth profile points
    # 1. Right flank (rotate involute_points)
    right_flank = []
    for x, y in involute_points:
        # Rotate by rotation_offset
        angle = rotation_offset
        xr = x * cos(angle) - y * sin(angle)
        yr = x * sin(angle) + y * cos(angle)
        right_flank.append((xr, yr))
        
    # 2. Left flank (mirror of right flank)
    left_flank = []
    for x, y in reversed(right_flank):
        left_flank.append((x, -y))
        
    # 3. Top land (arc connecting top of flanks)
    # Not purely necessary if points are close, but good for closed loop.
    # We will just connect the last point of right to first of left.
    
    # 4. Root fillet / bottom land
    # We need to connect the bottom of the left flank to the bottom of the next tooth's right flank.
    # The angle between teeth is 2 * pi / num_teeth.
    
    # Let's build one tooth shape as a wire
    # Points: Root -> Right Flank -> Top -> Left Flank -> Root
    
    # Root point calculation needs care to ensure we don't go below root radius
    # The involute starts at base circle. If root_radius < base_radius, we need a radial line.
    
    pts = []
    
    # Check if root radius is smaller than base radius
    if root_radius < base_diameter / 2.0:
        # Add a point at the root radius for the start of the flank
        # Radial line from root to base circle
        x_base, y_base = right_flank[0]
        # Angle of the start of the involute
        angle_start = math.atan2(y_base, x_base)
        pts.append((root_radius * cos(angle_start), root_radius * sin(angle_start)))
    
    pts.extend(right_flank)
    pts.extend(left_flank)
    
    if root_radius < base_diameter / 2.0:
         x_base, y_base = left_flank[-1]
         angle_end = math.atan2(y_base, x_base)
         pts.append((root_radius * cos(angle_end), root_radius * sin(angle_end)))

    # Now we have points for one tooth centered on X axis.
    # We need to replicate this N times.
    
    # It is often easier in CadQuery to construct the full wire for the gear by making a custom plugin or complex loop,
    # but for simplicity, let's define a single tooth solid or wire and pattern it.
    
    # However, CadQuery's gear plugin is standard, but to be self-contained:
    # Let's use `cq.Workplane("XY").gear(...)` if available in recent versions or plugins, 
    # but to ensure execution without extra libraries, we will approximate or use the `parametric_gear` logic.
    
    # SIMPLIFIED APPROACH: Use a robust approximation or manual point generation for the whole loop.
    
    total_points = []
    
    for i in range(num_teeth):
        theta = 2 * pi * i / num_teeth
        
        # Rotate the single tooth points by theta
        tooth_pts = []
        for x, y in pts:
            xr = x * cos(theta) - y * sin(theta)
            yr = x * sin(theta) + y * cos(theta)
            tooth_pts.append((xr, yr))
            
        total_points.extend(tooth_pts)
        
    # Create the wire and extrude
    # Note: This simple point connection creates straight lines between teeth roots. 
    # For a high-fidelity visual, this is usually sufficient.
    
    return cq.Workplane("XY").polyline(total_points).close().extrude(thickness)


import math

# --- Parameters based on visual estimation ---
# The gear has a large number of teeth, roughly 60-80 based on counting a quadrant.
# Let's assume typical dimensions for a gear of this proportion.
module = 1.0           # Scale factor
num_teeth = 68         # Counted approx
gear_thickness = 10.0  # Main gear face width
hub_diameter = 25.0    # Diameter of the central raised part
hub_height = 5.0       # Extra height of the hub above the gear face
bore_diameter = 12.0   # Center hole diameter

# Calculate derived dimensions
pitch_diameter = module * num_teeth

# --- Construct the Gear ---
# 1. Create the main gear body with teeth
# We use the custom function defined above for independence
gear = involute_gear(module=module, num_teeth=num_teeth, thickness=gear_thickness)

# 2. Create the Hub
# The hub is a cylinder on top of the gear. 
# Since the gear is extruded on XY plane (Z=0 to Z=thickness), we place the hub on the top face.
hub = (cq.Workplane("XY")
       .workplane(offset=gear_thickness)
       .circle(hub_diameter / 2.0)
       .extrude(hub_height))

# 3. Combine Gear and Hub
result_solid = gear.union(hub)

# 4. Create the Central Bore
# Cut a hole through the entire assembly
result = (result_solid
          .faces("<Z") # Select bottom face
          .workplane()
          .circle(bore_diameter / 2.0)
          .cutThruAll())

# Export or Render
if __name__ == "__main__":
    # If running in CQ-editor
    try:
        show_object(result)
    except NameError:
        pass