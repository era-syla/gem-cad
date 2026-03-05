import cadquery as cq

def make_part(is_male=True):
    # Core dimensions
    L_body = 14
    W_body = 12
    H_body = 8
    T_wall = 2
    T_floor = 2
    
    # 1. Main Box Body
    part = cq.Workplane("XY").box(L_body, W_body, H_body, centered=(False, True, False))
    
    # 2. Main inner cutout (open top and open front/back between walls)
    cutout = cq.Workplane("XY").workplane(offset=T_floor).box(
        L_body, W_body - 2*T_wall, H_body, centered=(False, True, False)
    )
    part = part.cut(cutout)
    
    # 3. Side windows
    win_L = 6
    win_H = 4
    win_Z = 4
    win_cut = (cq.Workplane("XZ")
               .workplane(offset=-W_body/2 - 1)
               .center(L_body/2, win_Z)
               .box(win_L, win_H, W_body + 2, centered=(True, True, False)))
    part = part.cut(win_cut)
    
    # 4. Floor hole
    part = part.cut(cq.Workplane("XY").center(L_body/2, 0).circle(2.5).extrude(H_body))
    
    # 5. Front Tab
    L_tab = 6
    W_neck = 4
    W_head = 8
    L_head = 2
    T_tab = T_floor
    
    tab_neck = cq.Workplane("XY").center(-L_tab, 0).box(L_tab, W_neck, T_tab, centered=(False, True, False))
    tab_head = cq.Workplane("XY").center(-L_tab - L_head, 0).box(L_head, W_head, T_tab, centered=(False, True, False))
    part = part.union(tab_neck).union(tab_head)
    
    # 6. Ears
    ear_L = 4
    ear_R = 4
    pts = [(L_body, 0), (L_body + ear_L, 0), (L_body + ear_L, H_body), (L_body, H_body)]
    
    if is_male:
        # Male ears step inwards to fit inside female ears
        ear_outer_Y = W_body/2 - T_wall
        ear_inner_Y = ear_outer_Y - T_wall
        
        # Right ear with outward pin
        ear_R_base = cq.Workplane("XZ").workplane(offset=ear_inner_Y).polyline(pts).close().extrude(T_wall)
        ear_R_round = cq.Workplane("XZ").workplane(offset=ear_inner_Y).center(L_body + ear_L, H_body/2).circle(ear_R).extrude(T_wall)
        pin_R = cq.Workplane("XZ").workplane(offset=ear_outer_Y).center(L_body + ear_L, H_body/2).circle(1.5).extrude(T_wall)
        ear_R_shape = ear_R_base.union(ear_R_round).union(pin_R)
        
        # Left ear with outward pin
        ear_L_base = cq.Workplane("XZ").workplane(offset=-ear_outer_Y).polyline(pts).close().extrude(T_wall)
        ear_L_round = cq.Workplane("XZ").workplane(offset=-ear_outer_Y).center(L_body + ear_L, H_body/2).circle(ear_R).extrude(T_wall)
        pin_L = cq.Workplane("XZ").workplane(offset=-ear_outer_Y).center(L_body + ear_L, H_body/2).circle(1.5).extrude(-T_wall)
        ear_L_shape = ear_L_base.union(ear_L_round).union(pin_L)
        
        part = part.union(ear_R_shape).union(ear_L_shape)
        
    else:
        # Female ears are flush with the outer body walls
        ear_outer_Y = W_body/2
        ear_inner_Y = ear_outer_Y - T_wall
        
        # Right ear with through hole
        ear_R_base = cq.Workplane("XZ").workplane(offset=ear_inner_Y).polyline(pts).close().extrude(T_wall)
        ear_R_round = cq.Workplane("XZ").workplane(offset=ear_inner_Y).center(L_body + ear_L, H_body/2).circle(ear_R).extrude(T_wall)
        ear_R_shape = ear_R_base.union(ear_R_round)
        hole_R = cq.Workplane("XZ").workplane(offset=ear_inner_Y - 1).center(L_body + ear_L, H_body/2).circle(1.5).extrude(T_wall + 2)
        ear_R_shape = ear_R_shape.cut(hole_R)
        
        # Left ear with through hole
        ear_L_base = cq.Workplane("XZ").workplane(offset=-ear_outer_Y).polyline(pts).close().extrude(T_wall)
        ear_L_round = cq.Workplane("XZ").workplane(offset=-ear_outer_Y).center(L_body + ear_L, H_body/2).circle(ear_R).extrude(T_wall)
        ear_L_shape = ear_L_base.union(ear_L_round)
        hole_L = cq.Workplane("XZ").workplane(offset=-ear_outer_Y - 1).center(L_body + ear_L, H_body/2).circle(1.5).extrude(T_wall + 2)
        ear_L_shape = ear_L_shape.cut(hole_L)
        
        part = part.union(ear_R_shape).union(ear_L_shape)
        
    return part

# Create the male part (left side in image)
p1 = make_part(is_male=True)
p1 = p1.rotate((0, 0, 0), (0, 0, 1), 90).translate((0, -25, 0))

# Create the female part (right side in image)
p2 = make_part(is_male=False)
p2 = p2.rotate((0, 0, 0), (0, 0, 1), -90).translate((0, 25, 0))

# Combine both parts into a single result
result = p1.union(p2)