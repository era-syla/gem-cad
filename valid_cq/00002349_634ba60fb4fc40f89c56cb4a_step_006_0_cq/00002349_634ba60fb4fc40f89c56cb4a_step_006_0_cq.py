import cadquery as cq
import math

# --- Parameters ---
prop_diameter = 200.0  # Total diameter of the propeller
hub_diameter = 18.0    # Diameter of the central hub cylinder
hub_height = 8.0       # Thickness of the hub
shaft_diameter = 4.0   # Diameter of the central shaft hole

blade_length = (prop_diameter - hub_diameter) / 2.0
blade_width_root = 18.0   # Width of the blade near the hub
blade_width_tip = 6.0    # Width of the blade at the tip
blade_thickness_root = 4.0 # Thickness of the blade airfoil near the hub
blade_thickness_tip = 1.5  # Thickness of the blade airfoil at the tip
pitch_angle_root = 20.0  # Twist angle at the root (degrees)
pitch_angle_tip = 10.0    # Twist angle at the tip (degrees)

# --- Helper Functions ---

def airfoil_profile(width, thickness):
    """
    Creates a simple symmetric airfoil-like cross-section (lens shape).
    Returns a list of points (x, y) for the profile centered at (0,0).
    The profile is in the XY plane.
    """
    # A simple lens shape made of two arcs or splines would work.
    # Let's approximate with a spline through points.
    
    # Points: Leading Edge (-w/2, 0), Top (0, t/2), Trailing Edge (w/2, 0), Bottom (0, -t/2)
    # We add intermediate points for better curvature.
    
    pts = [
        (-width/2, 0),                # Leading edge
        (-width*0.25, thickness*0.4), # Upper front
        (0, thickness/2),             # Upper max
        (width*0.25, thickness*0.35), # Upper back
        (width/2, 0),                 # Trailing edge
        (width*0.25, -thickness*0.35),# Lower back
        (0, -thickness/2),            # Lower max
        (-width*0.25, -thickness*0.4) # Lower front
    ]
    return pts

def make_blade(length, w_root, w_tip, t_root, t_tip, angle_root, angle_tip):
    """
    Creates a single twisted blade using lofting.
    """
    # Define sections along the blade length
    num_sections = 10
    sections = []
    
    for i in range(num_sections + 1):
        t = i / num_sections
        # Interpolate parameters
        current_width = w_root + t * (w_tip - w_root)
        current_thickness = t_root + t * (t_tip - t_root)
        current_angle = angle_root + t * (angle_tip - angle_root)
        
        # Calculate radial position. Start slightly outside hub center to avoid self-intersection issues at loft start
        # but practically we want it to start at the hub radius.
        # We will position the sketches relative to the hub center.
        radial_pos = hub_diameter/2.0 + t * length
        
        # Get profile points
        pts = airfoil_profile(current_width, current_thickness)
        
        # Create a sketch for this section
        # We need to position it at 'radial_pos' along X, then rotate it.
        # CadQuery's workplane logic:
        # 1. Create workplane at correct Z height (which corresponds to radial position here if we orient blade along Z)
        #    OR create workplane offset along an axis.
        # Let's orient the blade along the X-axis of the world.
        
        # Workplane normal to X-axis at x = radial_pos
        wp = cq.Workplane("YZ").workplane(offset=radial_pos)
        
        # Create the face. Rotate needs a reference. The profile is defined in local coords.
        # We rotate the profile points manually or use the sketch rotation.
        # The pitch angle rotates the airfoil around the radial axis (X-axis).
        # In the YZ plane, this is a rotation around the center (0,0).
        
        # Create closed wire (spline)
        face = wp.transformed(rotate=(current_angle, 0, 0)).spline(pts).close().val()
        sections.append(face)

    # Create solid by lofting through sections
    blade_solid = cq.Solid.makeLoft(sections)
    return blade_solid

# --- Main Construction ---

# 1. Create the Central Hub
# The image shows a somewhat rectangular center, likely flattened for the motor shaft interface, 
# blending into the cylindrical shape. Let's make a cylindrical hub with a flat top/bottom.
hub = cq.Workplane("XY").circle(hub_diameter/2).extrude(hub_height)

# Flatten sides to make it look more like the picture (rectangular center section)
# This is optional but adds realism based on the specific prop style in the image.
# We cut away sides.
hub = hub.faces(">Z").workplane().rect(hub_diameter*0.6, hub_diameter+2).cutThruAll()
# Wait, cutting a rectangle larger than diameter does nothing if centered. 
# The image shows a hub that transitions to the blades. 
# Let's keep it simple: A cylinder that is slightly flattened.
# Or just a simple cylinder as a robust base.
hub = cq.Workplane("XY").rect(hub_diameter, hub_diameter*0.6).extrude(hub_height)
# Add a central cylinder for the actual structural hub to smooth edges
hub_cyl = cq.Workplane("XY").circle(hub_diameter/2.2).extrude(hub_height)
hub = hub.union(hub_cyl)


# 2. Create the Shaft Hole
hub = hub.faces(">Z").workplane().hole(shaft_diameter)

# 3. Create One Blade
# We align the blade along the X-axis.
blade_surf = make_blade(blade_length, blade_width_root, blade_width_tip, 
                        blade_thickness_root, blade_thickness_tip, 
                        pitch_angle_root, pitch_angle_tip)

# Convert the raw Solid object back to a Workplane object for manipulation
blade1 = cq.Workplane("XY").add(blade_surf)

# Position the blade vertically to match the hub center
# The blade was generated along +X, centered on YZ plane.
# The hub is centered on Z=0 to Z=hub_height. Its center is Z=hub_height/2.
blade1 = blade1.translate((0, 0, hub_height/2))

# 4. Create the Second Blade (Rotate 180 degrees)
blade2 = blade1.rotate((0,0,0), (0,0,1), 180)

# 5. Combine Everything
result = hub.union(blade1).union(blade2)

# Optional: Fillet the connection between blade and hub for strength and aesthetics
# Finding the edges at the root can be tricky parametrically, so we apply a general fillet 
# if possible, or skip to ensure stability.
try:
    # Select edges that are near the hub radius
    result = result.edges(cq.selectors.RadiusNthSelector(0)).fillet(1.0)
except:
    pass # Filleting complex lofts can sometimes fail

# Final adjustments to match the visual style of the image (slender, dark grey typically)
# The code produces the geometry.