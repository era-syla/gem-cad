import cadquery as cq
import math

# --- Parameters ---
stock_length = 50.0
stock_width = 8.0
stock_height = 12.0

barrel_length = 60.0
barrel_width = 6.0
barrel_height = 5.0

bow_span = 80.0
bow_curve_radius = 60.0
bow_thickness = 4.0
bow_width = 8.0

scope_radius = 4.0
scope_length = 25.0

trigger_handle_height = 15.0
trigger_handle_width = 6.0

foot_stirrup_radius = 12.0
foot_stirrup_thickness = 2.0

# --- Helper Functions ---

def create_stock():
    # Main body of the stock/butt
    pts = [
        (0, 0),
        (stock_length, 0),
        (stock_length, stock_height * 0.6),
        (stock_length - 5, stock_height),
        (10, stock_height),
        (0, stock_height * 0.7)
    ]
    stock = (cq.Workplane("XY")
             .polyline(pts).close()
             .extrude(stock_width)
             .translate((-stock_length, -stock_width/2, 0)))
    
    # Fillet edges for a smoother look
    stock = stock.edges("|Y").fillet(1.0)
    return stock

def create_barrel():
    # The rail where the arrow sits
    barrel = (cq.Workplane("XY")
              .rect(barrel_length, barrel_width)
              .extrude(barrel_height)
              .translate((barrel_length/2, 0, stock_height/2)))
    
    # Create the groove for the bolt
    groove = (cq.Workplane("XY")
              .rect(barrel_length + 2, barrel_width * 0.4)
              .extrude(barrel_height * 0.3)
              .translate((barrel_length/2, 0, stock_height/2 + barrel_height - barrel_height*0.3)))
    
    barrel = barrel.cut(groove)
    
    # Add a slot cutout in the front section
    slot = (cq.Workplane("XY")
            .slot2D(15, 2)
            .extrude(barrel_height + 2)
            .translate((barrel_length * 0.7, 0, stock_height/2 - 1)))
            
    barrel = barrel.cut(slot)
    return barrel

def create_trigger_mechanism():
    # Handle grip
    handle_pts = [
        (0, 0),
        (8, 0),
        (6, -trigger_handle_height),
        (-2, -trigger_handle_height)
    ]
    handle = (cq.Workplane("XZ")
              .polyline(handle_pts).close()
              .extrude(trigger_handle_width)
              .translate((-5, trigger_handle_width/2, 0))) # Center it
    
    # Trigger guard/assembly block
    block = (cq.Workplane("XY")
             .rect(15, stock_width)
             .extrude(stock_height * 0.8)
             .translate((-5, 0, 0)))
             
    return handle.union(block)

def create_bow_arms():
    # Define a curved path for the bow limbs
    path = (cq.Workplane("XY")
            .moveTo(barrel_length, 0)
            .threePointArc((barrel_length - 10, bow_span/2), (barrel_length - 25, bow_span))
            )
            
    # Profile of the limb (tapered rectangle)
    limb_profile = (cq.Workplane("YZ")
                    .rect(bow_thickness, bow_width)
                    )

    # Sweep is tricky without a constructed path object, let's use lofting or extrusion with rotation
    # Simpler approach: Extrude a curved shape
    
    # Left Limb
    limb_l = (cq.Workplane("XY")
              .moveTo(barrel_length, 0)
              .threePointArc((barrel_length - 5, bow_span/2.5), (barrel_length - 20, bow_span/1.8))
              .lineTo(barrel_length - 22, bow_span/1.8)
              .threePointArc((barrel_length - 7, bow_span/2.5), (barrel_length - 2, 0))
              .close()
              .extrude(bow_width)
              .translate((0, 0, stock_height/2 - bow_width/2)))

    # Right Limb (Mirror)
    limb_r = limb_l.mirror("XZ")
    
    return limb_l.union(limb_r)

def create_string():
    # Creating the bow string
    # Tip of left limb
    p1 = (barrel_length - 20, bow_span/1.8, stock_height/2)
    # Tip of right limb
    p2 = (barrel_length - 20, -bow_span/1.8, stock_height/2)
    # Trigger mechanism point (cocked position)
    p_center = (-5, 0, stock_height/2 + 2)
    
    # Simple straight lines for the string
    string_diam = 0.5
    
    s1 = (cq.Workplane("XY")
          .polyline([(p1[0], p1[1]), (p_center[0], p_center[1])])
          .close() # Dummy close to make a shape but we really want a path
    )
    # Better way: cylinder from point to point
    
    def make_cylinder_between(pt1, pt2, r):
        v1 = cq.Vector(pt1)
        v2 = cq.Vector(pt2)
        diff = v2 - v1
        length = diff.Length
        
        # Orient cylinder
        c = (cq.Workplane("XY")
             .circle(r)
             .extrude(length)
             .rotate((0,0,0), (0,1,0), 90) # align with X
             )
             
        # This rotation logic is complex for arbitrary vectors in CQ without Plane setup.
        # Fallback: sweep a circle along a path
        path = cq.Workplane("XY").moveTo(pt1[0], pt1[1]).lineTo(pt2[0], pt2[1])
        # We need 3D points.
        
        # Simplest approximate approach for code generation:
        # Create a thin rectangular beam rotated
        angle = math.degrees(math.atan2(pt2[1]-pt1[1], pt2[0]-pt1[0]))
        mid = ((pt1[0]+pt2[0])/2, (pt1[1]+pt2[1])/2)
        
        beam = (cq.Workplane("XY")
                .rect(length, r*2)
                .extrude(r*2)
                .rotate((0,0,0), (0,0,1), angle)
                .translate((mid[0], mid[1], pt1[2]-r)))
        return beam

    str1 = make_cylinder_between(p_center, p1, string_diam)
    str2 = make_cylinder_between(p_center, p2, string_diam)
    
    return str1.union(str2)

def create_scope():
    # Main tube
    tube = (cq.Workplane("YZ")
            .circle(scope_radius)
            .extrude(scope_length)
            .translate((-15, 0, stock_height + 8))) # Position above stock
            
    # Eyepiece (larger)
    eye = (cq.Workplane("YZ")
           .circle(scope_radius * 1.3)
           .extrude(5)
           .translate((-15, 0, stock_height + 8)))
           
    # Objective lens (larger)
    obj = (cq.Workplane("YZ")
           .circle(scope_radius * 1.4)
           .extrude(5)
           .translate((-15 + scope_length - 5, 0, stock_height + 8)))
           
    # Mounts
    mount1 = (cq.Workplane("XY")
              .rect(4, 4)
              .extrude(8)
              .translate((-10, 0, stock_height)))
              
    mount2 = (cq.Workplane("XY")
              .rect(4, 4)
              .extrude(8)
              .translate((-15 + scope_length - 10, 0, stock_height)))
              
    return tube.union(eye).union(obj).union(mount1).union(mount2)

def create_stirrup():
    # The foot stirrup at the front
    
    # Path for the stirrup
    path = (cq.Workplane("XY")
            .moveTo(barrel_length, -foot_stirrup_radius)
            .threePointArc((barrel_length + foot_stirrup_radius*1.5, 0), (barrel_length, foot_stirrup_radius))
            )
            
    # Since sweeping a profile along a wire is specific, we'll approximate with a cut cylinder
    outer = (cq.Workplane("XY")
             .circle(foot_stirrup_radius + foot_stirrup_thickness)
             .extrude(foot_stirrup_thickness)
             .translate((barrel_length + foot_stirrup_radius, 0, stock_height/2 - foot_stirrup_thickness/2)))
             
    inner = (cq.Workplane("XY")
             .circle(foot_stirrup_radius)
             .extrude(foot_stirrup_thickness * 3)
             .translate((barrel_length + foot_stirrup_radius, 0, stock_height/2 - foot_stirrup_thickness*1.5)))
             
    ring = outer.cut(inner)
    
    # Cut it to make it a 'D' shape or stirrup shape attached to the barrel
    cutter = (cq.Workplane("XY")
              .rect(foot_stirrup_radius * 2, foot_stirrup_radius * 4)
              .extrude(10)
              .translate((barrel_length, 0, 0)))
              
    # Actually we want the arc part facing forward
    # Let's just create a U-shape pipe manually
    
    stirrup_shape = (cq.Workplane("XY")
             .moveTo(barrel_length, -foot_stirrup_radius)
             .lineTo(barrel_length + foot_stirrup_radius, -foot_stirrup_radius)
             .threePointArc((barrel_length + foot_stirrup_radius * 1.8, 0), (barrel_length + foot_stirrup_radius, foot_stirrup_radius))
             .lineTo(barrel_length, foot_stirrup_radius)
             .lineTo(barrel_length, foot_stirrup_radius - foot_stirrup_thickness) # Thickness
             .lineTo(barrel_length + foot_stirrup_radius, foot_stirrup_radius - foot_stirrup_thickness)
             .threePointArc((barrel_length + foot_stirrup_radius * 1.8 - foot_stirrup_thickness, 0), 
                            (barrel_length + foot_stirrup_radius, -foot_stirrup_radius + foot_stirrup_thickness))
             .lineTo(barrel_length, -foot_stirrup_radius + foot_stirrup_thickness)
             .close()
             .extrude(foot_stirrup_thickness)
             .translate((0,0, stock_height/2 - foot_stirrup_thickness/2))
             )

    return stirrup_shape

# --- Assembly ---

stock = create_stock()
barrel = create_barrel()
trigger = create_trigger_mechanism()
limbs = create_bow_arms()
string = create_string()
scope = create_scope()
stirrup = create_stirrup()

# Combine all parts
result = (stock
          .union(barrel)
          .union(trigger)
          .union(limbs)
          .union(string)
          .union(scope)
          .union(stirrup))

# Rotate to match isometric view approximation
result = result.rotate((0,0,0), (0,0,1), -45).rotate((0,0,0), (1,0,0), -30)