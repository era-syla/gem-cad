import cadquery as cq
import math

# Bevel gear parameters
num_teeth = 16
outer_radius = 40
inner_radius = 12
hub_radius = 15
height = 15
tooth_height = 6
cone_angle = 35  # degrees for the bevel cone

# Create the base cone frustum shape for bevel gear
# The gear has a conical profile - wider at bottom, narrower at top

def make_bevel_gear():
    # Base parameters
    n = num_teeth
    r_outer = outer_radius
    r_inner = hub_radius
    r_hole = inner_radius
    h = height
    
    # Create the main conical body using revolution of a profile
    # Profile: conical frustum shape
    
    # The bevel gear body - tapered from large outer to smaller inner
    # Bottom face is flat, top face is angled
    
    # Create profile for revolution
    # Points define the cross-section
    r_top_outer = r_outer * 0.55  # top outer radius (narrower due to cone)
    r_bottom_outer = r_outer
    r_top_inner = r_inner
    r_bottom_inner = r_inner
    
    # Make the base body as a truncated cone
    base = (
        cq.Workplane("XY")
        .workplane()
        .add(
            cq.Solid.makeCone(r_bottom_outer, r_top_outer, h)
        )
    )
    
    # Use loft-based approach instead
    # Create bottom circle and top circle, loft between them
    bottom_wire = cq.Workplane("XY").circle(r_bottom_outer).wires().val()
    top_wire = cq.Workplane("XY").workplane(offset=h).circle(r_top_outer).wires().val()
    
    # Build the conical frustum body
    body = cq.Workplane("XY")
    
    # Make truncated cone shell using shell of points
    pts_bottom = []
    pts_top = []
    
    tooth_profiles = []
    
    for i in range(n):
        angle = 360.0 / n * i
        half_tooth = 360.0 / n * 0.35
        
        # Bottom tooth profile (wide at bottom)
        angle_left = math.radians(angle - half_tooth)
        angle_right = math.radians(angle + half_tooth)
        angle_center = math.radians(angle)
        
        # Tooth tip at bottom - extends beyond base circle
        r_tip_bot = r_bottom_outer + tooth_height
        r_tip_top = r_top_outer + tooth_height * 0.4
        
    # Build using polygon approximation per tooth segment
    # Use a different approach: create the gear by cutting and adding teeth to a cone
    
    # Step 1: Create truncated cone (main body)
    cone_body = (
        cq.Workplane("XY")
        .add(cq.Solid.makeCone(r_bottom_outer, r_top_outer, h))
    )
    
    # Step 2: Create inner hole cylinder
    hole = (
        cq.Workplane("XY")
        .circle(r_hole)
        .extrude(h + 1)
    )
    
    # Cut hole from cone
    gear_body = cone_body.cut(hole)
    
    # Step 3: Add teeth by creating tooth solids and unioning
    # Create a single tooth as a lofted solid
    
    all_teeth = None
    
    for i in range(n):
        angle_deg = 360.0 / n * i
        angle_rad = math.radians(angle_deg)
        half_ang = math.radians(360.0 / n * 0.38)
        
        # Bottom face tooth profile (at z=0)
        # Tooth extends radially outward
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        r_base_b = r_bottom_outer
        r_tip_b = r_bottom_outer + tooth_height
        
        r_base_t = r_top_outer
        r_tip_t = r_top_outer + tooth_height * 0.45
        
        # Bottom points
        bl1 = (r_base_b * math.cos(angle_rad - half_ang), r_base_b * math.sin(angle_rad - half_ang), 0)
        br1 = (r_base_b * math.cos(angle_rad + half_ang), r_base_b * math.sin(angle_rad + half_ang), 0)
        bt1 = (r_tip_b * cos_a, r_tip_b * sin_a, 0)
        
        # Top points
        bl2 = (r_base_t * math.cos(angle_rad - half_ang * 0.6), r_base_t * math.sin(angle_rad - half_ang * 0.6), h)
        br2 = (r_base_t * math.cos(angle_rad + half_ang * 0.6), r_base_t * math.sin(angle_rad + half_ang * 0.6), h)
        bt2 = (r_tip_t * cos_a, r_tip_t * sin_a, h)
        
        # Create tooth as a solid using vertices
        tooth_pts_bottom = [bl1[:2], bt1[:2], br1[:2]]
        tooth_pts_top = [bl2[:2], bt2[:2], br2[:2]]
        
        # Build tooth bottom face
        bot_face = (cq.Workplane("XY")
                    .polyline(tooth_pts_bottom + [tooth_pts_bottom[0]])
                    .close()
                    )
        
        top_face = (cq.Workplane("XY")
                    .workplane(offset=h)
                    .polyline(tooth_pts_top + [tooth_pts_top[0]])
                    .close()
                    )
        
        try:
            tooth = (cq.Workplane("XY")
                     .polyline([bl1[:2], bt1[:2], br1[:2], bl1[:2]])
                     .close()
                     .workplane(offset=h)
                     .polyline([bl2[:2], bt2[:2], br2[:2], bl2[:2]])
                     .close()
                     .loft()
                     )
            
            if all_teeth is None:
                all_teeth = tooth
            else:
                all_teeth = all_teeth.union(tooth)
        except:
            pass
    
    if all_teeth is not None:
        result_gear = gear_body.union(all_teeth)
    else:
        result_gear = gear_body
    
    return result_gear

result = make_bevel_gear()