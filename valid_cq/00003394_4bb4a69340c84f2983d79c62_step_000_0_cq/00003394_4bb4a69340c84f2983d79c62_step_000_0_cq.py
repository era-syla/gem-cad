import cadquery as cq

# Parametric dimensions for the Finial
finial_base_radius = 12.0
finial_main_bulb_radius = 18.0
finial_cone_height = 25.0
finial_cone_base_radius = 15.0
finial_neck_radius = 6.0
finial_neck_length = 8.0
finial_collar_radius = 8.0
finial_collar_thick = 3.0
finial_top_radius = 10.0
finial_overall_height = 70.0 # Approximate, derived from parts

# Parametric dimensions for the Ferrules (small pieces)
ferrule_base_radius = 6.0
ferrule_base_thick = 1.5
ferrule_body_radius = 4.0
ferrule_body_height = 4.0
ferrule_hole_side = 3.0 # Square hole size

def create_finial():
    # Constructing the profile for revolution
    # We will build this along the Y-axis and revolve around Y
    
    # 1. The pointy tip (Cone-like shape)
    # Using a 3-point arc or spline for the organic curve would be best, 
    # but a revolved profile is easier to construct piecewise.
    
    # Let's create a workplane on XZ plane to draw the profile to revolve around Z
    pts = [
        (0, 0),  # Tip
        (finial_cone_base_radius, 20), # End of cone section
        (finial_cone_base_radius, 22), # Small vertical step
        (finial_main_bulb_radius, 30), # Widest part of first bulb
        (finial_base_radius, 40),      # Narrowing
        (finial_main_bulb_radius + 2, 45), # Second rim/flange
        (finial_main_bulb_radius + 2, 48), # Thickness of rim
        (finial_neck_radius, 55),      # Neck start
        (finial_neck_radius, 55 + finial_neck_length), # Neck end
        (finial_collar_radius, 55 + finial_neck_length), # Collar start
        (finial_collar_radius, 55 + finial_neck_length + finial_collar_thick), # Collar end
        (0, 55 + finial_neck_length + finial_collar_thick) # Axis
    ]
    
    # Using spline for the main body to get that organic "onion" look
    # We need to break it down. Let's try a pure solid construction approach instead of a single complex profile revolve
    # This is often more robust in CQ.
    
    # Bottom cone/tip
    p1 = cq.Workplane("XY").circle(finial_cone_base_radius).extrude(20)
    # Taper the extrusion to a point? No, let's revolve a specific profile.
    
    # Profile approach is cleaner for this specific ornate shape.
    # Let's define points for a Spline on the XZ plane.
    
    # Section 1: The Tip
    s1 = (
        cq.Workplane("XZ")
        .moveTo(0, 0)
        .spline([(finial_cone_base_radius * 0.8, 10), (finial_cone_base_radius, 20)], includeCurrent=True)
        .lineTo(0, 20)
        .close()
        .revolve()
    )
    
    # Section 2: The Middle "Bulb" (Ogee curve)
    s2 = (
        cq.Workplane("XZ")
        .workplane(offset=20)
        .moveTo(0,0)
        .lineTo(finial_cone_base_radius, 0)
        .threePointArc((finial_main_bulb_radius, 7), (finial_base_radius, 14)) # The bulb shape
        .lineTo(0, 14)
        .close()
        .revolve()
    )
    
    # Section 3: The Wide Flange/Disk
    s3 = (
        cq.Workplane("XZ")
        .workplane(offset=34)
        .moveTo(0,0)
        .lineTo(finial_base_radius, 0)
        .spline([(finial_main_bulb_radius + 4, 3), (finial_base_radius, 6)], includeCurrent=True)
        .lineTo(0, 6)
        .close()
        .revolve()
    )

    # Section 4: The Neck and Collar
    s4 = (
        cq.Workplane("XY")
        .workplane(offset=40)
        .circle(finial_neck_radius).extrude(finial_neck_length)
    )
    
    s5 = (
        cq.Workplane("XY")
        .workplane(offset=40 + finial_neck_length - 2) # Overlap slightly
        .circle(finial_collar_radius).extrude(finial_collar_thick)
    )
    
    # Combine
    finial = s1.union(s2).union(s3).union(s4).union(s5)
    
    # Rotate to match image orientation roughly (laying down)
    finial = finial.rotate((0,0,0), (1,0,0), -90).rotate((0,0,0), (0,0,1), -45)
    
    return finial

def create_ferrule():
    # Base disk
    base = cq.Workplane("XY").circle(ferrule_base_radius).extrude(ferrule_base_thick)
    
    # Body cylinder
    body = (
        cq.Workplane("XY")
        .workplane(offset=ferrule_base_thick)
        .circle(ferrule_body_radius)
        .extrude(ferrule_body_height)
    )
    
    ferrule = base.union(body)
    
    # Cut square hole
    ferrule = (
        ferrule.faces(">Z")
        .workplane()
        .rect(ferrule_hole_side, ferrule_hole_side)
        .cutBlind(-(ferrule_body_height + ferrule_base_thick))
    )
    
    # Chamfer the top edge slightly for realism
    ferrule = ferrule.edges(">Z").chamfer(0.2)
    
    return ferrule

# Create parts
main_finial = create_finial()
ferrule_1 = create_ferrule().translate((30, -30, 0))
ferrule_2 = create_ferrule().translate((50, -10, 0))

# Combine all into one result
result = main_finial.union(ferrule_1).union(ferrule_2)