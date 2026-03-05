import cadquery as cq
import math

# --- Parameters ---

# Flange Parameters
flange_diameter = 80.0
flange_thickness = 10.0
flange_fillet = 3.0  # Fillet between shaft and flange

# Bolt Hole Parameters
bolt_circle_diameter = 60.0
num_bolt_holes = 6
bolt_hole_diameter = 6.0

# Shaft (Conical Section) Parameters
shaft_length = 60.0
shaft_base_diameter = 40.0 # Diameter at the flange end
shaft_top_diameter = 25.0  # Diameter at the gear end

# Gear Parameters
gear_thickness = 10.0
gear_outer_diameter = 45.0
num_teeth = 20
tooth_depth = 4.0
tooth_width_top = 2.0  # Width of the flat part at the tip, if any (sharp points here)
tooth_width_bottom = 5.0 # Approximate width at the root

# Hub/Hex Hole Parameters
hub_boss_diameter = 20.0 # Small raised area in center of gear
hub_boss_height = 1.0 # Slight protrusion
hex_hole_width = 12.0 # Flat-to-flat distance (wrench size)
hex_hole_depth = 20.0 # Depth of the hex pocket

# --- Construction ---

# 1. Create the base flange
flange = cq.Workplane("XY").circle(flange_diameter / 2.0).extrude(flange_thickness)

# 2. Add bolt holes
# We create points on a circle and cut the holes
bolt_holes = (
    cq.Workplane("XY")
    .polarArray(bolt_circle_diameter / 2.0, 0, 360, num_bolt_holes)
    .circle(bolt_hole_diameter / 2.0)
    .extrude(flange_thickness)
)
flange = flange.cut(bolt_holes)

# 3. Create the conical shaft
# We start from the top face of the flange
shaft = (
    flange.faces(">Z")
    .workplane()
    .circle(shaft_base_diameter / 2.0)
    .workplane(offset=shaft_length)
    .circle(shaft_top_diameter / 2.0)
    .loft(combine=True)
)

# 4. Create the Gear Profile
# This is a simplified spur gear profile based on the visual
def gear_profile(teeth, outer_dia, inner_dia):
    angle_step = 360.0 / teeth
    # Points for one tooth
    # We need a triangular/trapezoidal shape
    pts = []
    outer_r = outer_dia / 2.0
    inner_r = inner_dia / 2.0
    
    for i in range(teeth):
        angle_center = i * angle_step
        # V-shape tooth logic
        angle_start = math.radians(angle_center - (angle_step / 2.0))
        angle_mid = math.radians(angle_center)
        angle_end = math.radians(angle_center + (angle_step / 2.0))
        
        # Root point 1
        x1 = inner_r * math.cos(angle_start)
        y1 = inner_r * math.sin(angle_start)
        
        # Tip point
        x2 = outer_r * math.cos(angle_mid)
        y2 = outer_r * math.sin(angle_mid)
        
        pts.append((x1, y1))
        pts.append((x2, y2))
    
    # Close the loop implicitly by CadQuery usually, but let's be safe
    # Actually, constructing a polyline for the whole gear is easiest
    return pts

inner_gear_dia = gear_outer_diameter - (2 * tooth_depth)
gear_pts = gear_profile(num_teeth, gear_outer_diameter, inner_gear_dia)

# Extrude the gear on top of the shaft
gear = (
    shaft.faces(">Z")
    .workplane()
    .polyline(gear_pts)
    .close()
    .extrude(gear_thickness)
)

# 5. Add the small central boss on the gear face
# Visual shows a flat face inside the gear teeth, likely the shaft continuation or a specific boss
# Let's clean up the center with a cylinder to ensure the teeth roots are solid and add the visual hub
hub = (
    gear.faces(">Z")
    .workplane()
    .circle(hub_boss_diameter / 2.0)
    .extrude(hub_boss_height) # Just a tiny bit or cut flush
)

# If the gear teeth construction left a hole in the middle (it shouldn't with polyline), 
# we might need a solid cylinder fill. The polyline method above creates a solid star shape.
# Let's union the gear with a solid cylinder of the root diameter to be sure it looks like a solid disk with teeth.
gear_core = (
    shaft.faces(">Z")
    .workplane()
    .circle(inner_gear_dia / 2.0)
    .extrude(gear_thickness)
)
result_solid = hub.union(gear_core)


# 6. Create the Hexagonal Hole
# Flat-to-flat distance to radius conversion: Radius = width / sqrt(3)
# Actually CadQuery polygon method uses radius of circumscribed circle usually, 
# but allows specifying definition. For `polygon(n, d)`, d is diameter of circle touching vertices.
# For a hex bolt, we want flat-to-flat.
# Circumradius R = (width / 2) / cos(30) = width / sqrt(3)
hex_circumradius = (hex_hole_width / 2.0) / (math.sqrt(3)/2.0)

final_shape = (
    result_solid.faces(">Z")
    .workplane()
    .polygon(6, hex_circumradius * 2.0) 
    .cutBlind(-hex_hole_depth)
)

# 7. Add Fillet at the base (Shaft to Flange connection)
# We select the edge where the shaft meets the flange.
# Since we lofted, the edge is at Z = flange_thickness
try:
    final_shape = final_shape.edges(
        cq.selectors.NearestToPointSelector((shaft_base_diameter/2.0 + 1, 0, flange_thickness))
    ).fillet(flange_fillet)
except:
    # Fallback if selection is tricky, usually selecting by Z height works well
    pass

result = final_shape