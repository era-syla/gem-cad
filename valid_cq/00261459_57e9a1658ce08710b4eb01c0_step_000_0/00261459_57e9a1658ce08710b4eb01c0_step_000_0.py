import cadquery as cq

def create_engine_assembly():
    # Parametric dimensions
    r_body = 5.0
    r_rear = 7.0
    l_nose = 22.0
    l_front = 15.0
    l_rib_1 = 3.0
    l_mid = 18.0
    l_trans = 8.0
    l_rear = 28.0
    
    # 1. Nose Cone (Lofted from tip to body radius)
    # Aligned along X axis, tip at x = -l_nose
    nose = (cq.Workplane("YZ")
            .workplane(offset=-l_nose).circle(0.1)
            .workplane(offset=l_nose).circle(r_body)
            .loft())
            
    current_x = 0
    
    # 2. Front Body Section
    front = (cq.Workplane("YZ")
             .workplane(offset=current_x)
             .circle(r_body)
             .extrude(l_front))
    current_x += l_front
    
    # 3. Ribbed Connector
    # Core cylinder
    core = (cq.Workplane("YZ")
            .workplane(offset=current_x)
            .circle(r_body - 0.5)
            .extrude(l_rib_1))
    
    # Rib rings
    rings = cq.Assembly()
    ring_w = 0.5
    num_rings = int(l_rib_1 / (ring_w * 2))
    for i in range(num_rings):
        r = (cq.Workplane("YZ")
             .workplane(offset=current_x + i*ring_w*2)
             .circle(r_body)
             .extrude(ring_w))
        rings.add(r)
        
    ribbed_1 = core.union(rings.toCompound())
    current_x += l_rib_1
    
    # 4. Mid Body Section
    mid = (cq.Workplane("YZ")
           .workplane(offset=current_x)
           .circle(r_body)
           .extrude(l_mid))
           
    # Fins (Cruciform configuration)
    fin_len = 12.0
    fin_height = 8.0
    fin_thick = 0.6
    fin_x_start = current_x + 2.0
    
    # Define single fin shape
    fin_prof = (cq.Workplane("XY")
                .polyline([(fin_x_start, r_body - 0.5), 
                           (fin_x_start + fin_len, r_body - 0.5), 
                           (fin_x_start + fin_len, r_body + fin_height), 
                           (fin_x_start + fin_len * 0.3, r_body + fin_height)])
                .close()
                .extrude(fin_thick)
                .translate((0,0, -fin_thick/2)) # Center on Z axis
               )
    
    # Rotate and union 4 fins
    fins = fin_prof
    for i in range(1, 4):
        fins = fins.union(fin_prof.rotate((0,0,0), (1,0,0), i*90))
        
    current_x += l_mid
    
    # 5. Transition Cone
    trans = (cq.Workplane("YZ")
             .workplane(offset=current_x).circle(r_body)
             .workplane(offset=l_trans).circle(r_rear)
             .loft())
    current_x += l_trans
    
    # 6. Rear Casing
    rear = (cq.Workplane("YZ")
            .workplane(offset=current_x)
            .circle(r_rear)
            .extrude(l_rear))
            
    # Vents on Rear Casing
    vent_x = current_x + 3
    num_vents = 16
    vent_l = 4.0
    
    # Create a cutter object
    cutter = (cq.Workplane("XY")
              .workplane(offset=r_rear) # Move radially to surface
              .moveTo(vent_x + vent_l/2, 0)
              .box(vent_l, 1.5, 3.0) # Length, Width, Depth
              )
              
    for i in range(num_vents):
        angle = i * (360.0 / num_vents)
        rear = rear.cut(cutter.rotate((0,0,0), (1,0,0), angle))
        
    # Exhaust Hollow
    exhaust = (cq.Workplane("YZ")
               .workplane(offset=current_x + l_rear)
               .circle(r_rear - 1.2)
               .extrude(-8.0)) # Cut into the body
    rear = rear.cut(exhaust)
    
    # Combine main fuselage components
    fuselage = nose.union(front).union(ribbed_1).union(mid).union(trans).union(rear).union(fins)
    
    # 7. Landing Gear / Wheels
    # Located under the mid section
    gear_x_pos = fin_x_start + fin_len / 2
    gear_strut_len = 8.0
    axle_z = -r_body - gear_strut_len + 1.0
    axle_len = 16.0
    
    # Vertical Strut
    strut = (cq.Workplane("XY")
             .workplane(offset=-r_body + 1)
             .moveTo(gear_x_pos, 0)
             .rect(4, 2)
             .extrude(-gear_strut_len))
             
    # Axle
    axle_bar = (cq.Workplane("XZ")
                .workplane(offset=axle_z)
                .moveTo(gear_x_pos, 0)
                .circle(1.2)
                .extrude(axle_len/2, both=True)) # Extrudes along Y (normal to XZ)

    # Wheel creation function
    wheel_r = 5.5
    wheel_w = 3.0
    
    def make_wheel(y_pos):
        # Main tire
        w = (cq.Workplane("XZ")
             .workplane(offset=axle_z)
             .moveTo(gear_x_pos, 0)
             .circle(wheel_r)
             .extrude(wheel_w)
             .translate((0, y_pos, 0)))
             
        # Rim recess
        recess = (cq.Workplane("XZ")
                  .workplane(offset=axle_z)
                  .moveTo(gear_x_pos, 0)
                  .circle(wheel_r - 1.5)
                  .extrude(0.8))
        
        # Apply recesses to both sides
        w = w.cut(recess.translate((0, y_pos, 0)))
        w = w.cut(recess.translate((0, y_pos + wheel_w - 0.8, 0)))
        
        # Hub cap
        hub = (cq.Workplane("XZ")
               .workplane(offset=axle_z)
               .moveTo(gear_x_pos, 0)
               .circle(1.0)
               .extrude(wheel_w + 0.5)
               .translate((0, y_pos - 0.25, 0)))
               
        return w.union(hub)

    # Create two wheels
    w_left = make_wheel(-axle_len/2)
    w_right = make_wheel(axle_len/2 - wheel_w)
    
    gear = strut.union(axle_bar).union(w_left).union(w_right)
    
    return fuselage.union(gear)

# Create two engines side by side
offset_distance = 12.0
engine1 = create_engine_assembly().translate((0, offset_distance, 0))
engine2 = create_engine_assembly().translate((0, -offset_distance, 0))

# Combine into final result
result = engine1.union(engine2)