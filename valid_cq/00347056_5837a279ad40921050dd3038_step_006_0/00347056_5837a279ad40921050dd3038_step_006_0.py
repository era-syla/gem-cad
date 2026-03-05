import cadquery as cq
import math

def bicycle_front_triangle():
    # ---------------------------------------------------------
    # Frame Parameters (Geometry based on modern Trail Bike)
    # ---------------------------------------------------------
    # Dimensions in mm
    reach = 460.0
    stack = 620.0
    st_angle_deg = 74.0
    st_length = 440.0
    ht_angle_deg = 65.0
    ht_length = 130.0
    
    # Tube diameters
    bb_od = 41.0  # BB92 pressfit approx
    bb_width = 92.0
    st_od = 34.9
    st_id = 30.9
    ht_od = 56.0  # ZS56
    ht_id = 44.0
    dt_od = 54.0
    tt_od = 38.0
    
    # ---------------------------------------------------------
    # 1. Bottom Bracket Shell
    # ---------------------------------------------------------
    # Centered at (0,0,0)
    bb = (cq.Workplane("YZ")
          .circle(bb_od / 2.0)
          .extrude(bb_width, both=True))
    
    bb_cut = (cq.Workplane("YZ")
              .circle(30.0 / 2.0) # Inner hole
              .extrude(bb_width + 2.0, both=True))
    
    result = bb.cut(bb_cut)

    # ---------------------------------------------------------
    # 2. Seat Tube (ST)
    # ---------------------------------------------------------
    # Calculate vector for seat tube angle
    st_rad = math.radians(st_angle_deg)
    # Vector pointing up-back
    st_vec = cq.Vector(-math.cos(st_rad), 0, math.sin(st_rad))
    
    # Plane perpendicular to ST axis
    st_plane = (cq.Workplane("XZ")
                .transformed(rotate=(0, 90 - st_angle_deg, 0)))
    
    st_solid = (st_plane
                .circle(st_od / 2.0)
                .extrude(st_length))
                
    st_void = (st_plane
               .circle(st_id / 2.0)
               .extrude(st_length + 5.0)) # Through top
               
    st_solid = st_solid.cut(st_void)
    
    # Seat clamp slot at the top
    st_top_pt = st_vec * st_length
    slot = (cq.Workplane("XY")
            .translate((st_top_pt.x, st_top_pt.y, st_top_pt.z - 20))
            .box(40, 4, 30))
            
    st_solid = st_solid.cut(slot)
    result = result.union(st_solid)

    # ---------------------------------------------------------
    # 3. Head Tube (HT)
    # ---------------------------------------------------------
    # Defined by Reach and Stack to the top-center of HT
    ht_top = cq.Vector(reach, 0, stack)
    
    # Calculate bottom point based on angle and length
    # Head angle is measured from horizontal. 
    # Tube leans back, so bottom is further forward (+X) than top.
    ht_rad = math.radians(ht_angle_deg)
    ht_dx = ht_length * math.cos(ht_rad)
    ht_dz = ht_length * math.sin(ht_rad)
    ht_bot = ht_top + cq.Vector(ht_dx, 0, -ht_dz)
    
    ht_center = (ht_top + ht_bot) / 2.0
    
    # Plane for HT
    ht_plane = (cq.Workplane("XZ")
                .translate((ht_center.x, ht_center.y, ht_center.z))
                .transformed(rotate=(0, 90 - ht_angle_deg, 0)))
                
    ht_solid = (ht_plane
                .circle(ht_od / 2.0)
                .extrude(ht_length, both=True))
    
    # Bearing Cups / Flanges
    ht_flange_top = (ht_plane
                     .workplane(offset=ht_length/2.0 - 10)
                     .circle(ht_od/2.0 + 3.0)
                     .extrude(10))
    ht_flange_bot = (ht_plane
                     .workplane(offset=-ht_length/2.0)
                     .circle(ht_od/2.0 + 3.0)
                     .extrude(10))
                     
    ht_solid = ht_solid.union(ht_flange_top).union(ht_flange_bot)
    
    ht_void = (ht_plane
               .circle(ht_id / 2.0)
               .extrude(ht_length + 2.0, both=True))
               
    ht_solid = ht_solid.cut(ht_void)
    result = result.union(ht_solid)

    # ---------------------------------------------------------
    # 4. Down Tube (DT)
    # ---------------------------------------------------------
    # Connects HT bottom-back to BB front-top
    dt_start = ht_bot + cq.Vector(-10, 0, 15) # Offset on HT surface
    dt_end = cq.Vector(25, 0, 30) # Offset on BB surface
    
    # Control Points for S-Bend
    # Leaving HT perpendicular to HT axis
    # Normal to HT in XZ roughly points (-sin, 0, -cos) if angle is from horizontal
    dt_p1 = dt_start + cq.Vector(-50, 0, -30) 
    # Entering BB horizontalish
    dt_p2 = dt_end + cq.Vector(60, 0, 50)
    
    dt_path = (cq.Workplane("XZ")
               .moveTo(dt_start.x, dt_start.z)
               .spline([(dt_p1.x, dt_p1.z), (dt_p2.x, dt_p2.z), (dt_end.x, dt_end.z)], includeCurrent=True))
    
    # Create solid by sweeping
    # We define profile on YZ plane, rotated to match start tangent approx
    dt_profile_plane = (cq.Workplane("YZ")
                        .transformed(offset=dt_start, rotate=(0, -ht_angle_deg - 20, 0)))

    dt_solid = (dt_profile_plane
                .circle(dt_od / 2.0)
                .sweep(dt_path))
    
    # Inner cut
    dt_inner = (dt_profile_plane
                .circle((dt_od - 4.0) / 2.0)
                .sweep(dt_path))
                
    result = result.union(dt_solid.cut(dt_inner))

    # ---------------------------------------------------------
    # 5. Top Tube (TT)
    # ---------------------------------------------------------
    # Connects HT top-back to ST
    tt_start = ht_top + cq.Vector(-15, 0, -15)
    
    # Intersection on ST (approx 75% up)
    tt_end = st_vec * (st_length * 0.85)
    
    # Curve midpoint (Swoop)
    tt_mid = (tt_start + tt_end) / 2.0
    tt_mid = tt_mid + cq.Vector(0, 0, -25) # Drop down for curvature
    
    tt_path = (cq.Workplane("XZ")
               .moveTo(tt_start.x, tt_start.z)
               .spline([(tt_mid.x, tt_mid.z), (tt_end.x, tt_end.z)], includeCurrent=True))
               
    tt_profile_plane = (cq.Workplane("YZ")
                        .transformed(offset=tt_start, rotate=(0, -ht_angle_deg, 0)))
                        
    tt_solid = (tt_profile_plane
                .circle(tt_od / 2.0)
                .sweep(tt_path))
                
    tt_inner = (tt_profile_plane
                .circle((tt_od - 3.0) / 2.0)
                .sweep(tt_path))
                
    result = result.union(tt_solid.cut(tt_inner))

    # ---------------------------------------------------------
    # 6. Suspension Mounts
    # ---------------------------------------------------------
    
    # --- Lower Pivot (Main Pivot) ---
    pivot_pos = st_vec * 90.0
    
    # Create base block
    pivot_block = (cq.Workplane("XY")
                   .box(50, 30, 50)
                   .rotate((0,0,0), (0,1,0), -st_angle_deg)
                   .translate(pivot_pos)
                   .translate((25, 0, 10))) # Shift forward
                   
    # Cutout for linkage
    pivot_gap = (cq.Workplane("XY")
                 .box(60, 16, 60)
                 .rotate((0,0,0), (0,1,0), -st_angle_deg)
                 .translate(pivot_pos)
                 .translate((30, 0, 10)))
                 
    pivot_final = pivot_block.cut(pivot_gap)
    
    # Pivot bearing holes
    pivot_hole = (cq.Workplane("YZ")
                  .circle(8.0)
                  .extrude(100, both=True)
                  .translate(pivot_pos.toTuple())
                  .translate((25, 0, 10)))
                  
    pivot_final = pivot_final.cut(pivot_hole)
    result = result.union(pivot_final)
    
    # --- Upper Shock Mount ---
    shock_pos = st_vec * 300.0
    
    shock_mount = (cq.Workplane("XY")
                   .box(50, 24, 45)
                   .rotate((0,0,0), (0,1,0), -st_angle_deg)
                   .translate(shock_pos)
                   .translate((25, 0, 0)))
                   
    # Sculpting the mount
    sculpt_cut = (cq.Workplane("YZ")
                  .moveTo(0, 0)
                  .rect(20, 20) # Remove material center
                  .extrude(100, both=True)
                  .translate(shock_pos.toTuple())
                  .translate((35, 0, 0)))

    # Shock eyelet hole
    shock_hole = (cq.Workplane("YZ")
                  .circle(6.0)
                  .extrude(100, both=True)
                  .translate(shock_pos.toTuple())
                  .translate((35, 0, 5)))
                  
    shock_mount = shock_mount.cut(shock_hole)
    
    # Add a triangular gusset/web shape cut for style
    result = result.union(shock_mount)

    return result

# Generate the model
result = bicycle_front_triangle()