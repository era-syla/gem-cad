import cadquery as cq

def create_model():
    # --- Parametric Dimensions ---
    # Central Barrel
    r_mid = 24.0
    x_mid = 14.0
    x_cone_end = 28.0
    r_cone_end = 16.0
    x_band_end = 32.0
    x_boss_end = 40.0
    r_boss = 10.0
    hole_radius = 6.0
    
    # Side Block
    y_start = 8.0
    z_top = 34.0
    y_top_end = 26.0
    y_mid = 46.0
    z_mid_upper = 12.0
    z_mid_lower = -12.0
    y_bot_end = 26.0
    z_bot = -34.0
    block_span = x_cone_end
    
    # Top Hexagon Boss
    hex_y_pos = 17.0
    hex_base_z = z_top
    boss_r = 8.0
    boss_h = 4.0
    hex_circum_d = 12.0
    hex_h = 14.0
    
    # --- Geometry Construction ---
    
    # 1. Main Barrel (Revolved Profile)
    barrel_sk = (
        cq.Workplane("XZ")
        .moveTo(0, r_mid)
        .lineTo(x_mid, r_mid)
        .lineTo(x_cone_end, r_cone_end)
        .lineTo(x_band_end, r_cone_end)
        .lineTo(x_band_end, r_boss)
        .lineTo(x_boss_end, r_boss)
        .lineTo(x_boss_end, 0)
        .lineTo(0, 0)
        .close()
    )
    barrel_half = barrel_sk.revolve(360, (0, 0, 0), (1, 0, 0))
    barrel = barrel_half.union(barrel_half.mirror("YZ"))
    
    # 2. Side Block (Extruded Profile)
    block_sk = (
        cq.Workplane("YZ")
        .moveTo(y_start, z_top)
        .lineTo(y_top_end, z_top)
        .lineTo(y_mid, z_mid_upper)
        .lineTo(y_mid, z_mid_lower)
        .lineTo(y_bot_end, z_bot)
        .lineTo(y_start, z_bot)
        .close()
    )
    block = block_sk.extrude(block_span * 2).translate((-block_span, 0, 0))
    
    # Merge main bodies
    body = barrel.union(block)
    
    # 3. Top Features (Boss and Hex Post)
    top_boss = (
        cq.Workplane("XY", origin=(0, hex_y_pos, hex_base_z))
        .circle(boss_r)
        .extrude(boss_h)
    )
    
    top_hex = (
        cq.Workplane("XY", origin=(0, hex_y_pos, hex_base_z + boss_h))
        .polygon(6, hex_circum_d)
        .extrude(hex_h)
    )
    
    body = body.union(top_boss).union(top_hex)
    
    # 4. Central Cut (Through Hole)
    hole = cq.Workplane("YZ").circle(hole_radius).extrude(200, both=True)
    body = body.cut(hole)
    
    # 5. Detail Features (Chamfers)
    try:
        # Chamfer the top face of the hex post
        body = body.faces(">Z").chamfer(1.0)
    except:
        pass
        
    try:
        # Chamfer the outer ends of the cylindrical bosses
        body = body.faces("<X or >X").chamfer(1.5)
    except:
        pass
        
    return body

result = create_model()