import cadquery as cq
import math

def create_engine():
    # --- Parameters ---
    # Main Engine Block
    block_length = 180
    block_width = 100
    block_height = 90
    block_fillet = 10

    # Crankcase Front (Transmission area)
    front_length = 120
    front_width = 90
    front_height = 80
    
    # Cylinder Dimensions
    cyl_angle = 90  # V-angle
    cyl_bore_outer = 60
    cyl_height = 90
    fin_count = 12
    fin_thickness = 2
    fin_gap = 3
    fin_protrusion = 10 # How much wider fins are than the bore
    
    # Cylinder Head
    head_height = 35
    head_width = 85
    head_length = 75
    
    # Intake/Exhaust details
    port_diam = 18
    
    # --- Helper Functions ---
    
    def create_finned_cylinder(height, bore_rad, fin_count, fin_thk, fin_gap, fin_prot):
        # Core cylinder
        cyl = cq.Workplane("XY").circle(bore_rad).extrude(height)
        
        # Create fins
        fin_profile = cq.Workplane("XY").circle(bore_rad + fin_prot).extrude(fin_thk)
        fins = fin_profile
        
        for i in range(1, fin_count):
            z_offset = i * (fin_thk + fin_gap)
            if z_offset < height - 5: # Leave room at top
                # Vary fin shape slightly to match typical engine profiles (often squared off)
                # Here we keep circular for simplicity but add cuts
                new_fin = fin_profile.translate((0,0, z_offset))
                fins = fins.union(new_fin)
        
        # Combine core and fins
        combined = cyl.union(fins)
        
        # Add cutouts for pushrod tubes or bolt access (common on these engines)
        cutout = cq.Workplane("XY").rect(20, bore_rad*2.5).extrude(height)
        combined = combined.cut(cutout.translate((bore_rad, 0, 0)))
        combined = combined.cut(cutout.translate((-bore_rad, 0, 0)))

        return combined

    def create_cylinder_head(width, length, height):
        # Basic rounded box shape
        head = (cq.Workplane("XY")
                .rect(width, length)
                .extrude(height)
                .edges("|Z").fillet(15)
                .edges(">Z").fillet(5)
                )
        
        # Add rocker cover definition
        cover_seam = (cq.Workplane("XY")
                      .rect(width + 2, length + 2)
                      .extrude(2)
                      .translate((0,0, height * 0.6))
                      )
        
        head = head.union(cover_seam)
        
        # Add some stylized details (bolt bosses)
        boss = cq.Workplane("XY").circle(6).extrude(height).translate((width/2 - 10, 0, 0))
        head = head.union(boss)
        head = head.union(boss.mirror("YZ"))
        
        return head

    # --- Construction ---

    # 1. Crankcase / Engine Block
    # Main body
    crankcase = (cq.Workplane("XY")
                 .rect(block_length, block_width)
                 .extrude(block_height)
                 .edges("|Z").fillet(block_fillet)
                 .edges("|Y").fillet(5)
                 )
    
    # Front section (Transmission/Front cover)
    front_cover = (cq.Workplane("XY")
                   .workplane(offset=block_height/2) # Align somewhat centrally
                   .rect(front_length, front_width)
                   .extrude(front_height)
                   .translate((block_length/2 + front_length/2 - 20, 0, -10)) # Position forward
                   .edges().fillet(8)
                   )
    
    # Rear Flywheel/Clutch housing area
    rear_housing = (cq.Workplane("YZ")
                    .circle(block_width/1.8)
                    .extrude(30)
                    .translate((-block_length/2 - 15, block_height/2, 0))
                    )

    base_engine = crankcase.union(front_cover).union(rear_housing)

    # 2. Cylinders
    # We need to position them in a V configuration.
    # Assuming longitudinal crankshaft (Moto Guzzi style), cylinders stick out L and R.
    # Let's say Z is up, X is forward/back, Y is Left/Right.
    # The image shows cylinders angled upwards.
    
    # Construct one cylinder assembly
    cyl_geo = create_finned_cylinder(cyl_height, cyl_bore_outer/2, fin_count, fin_thickness, fin_gap, fin_protrusion)
    head_geo = create_cylinder_head(head_width, head_length, head_height).translate((0,0, cyl_height))
    
    full_cylinder = cyl_geo.union(head_geo)
    
    # Left Cylinder
    left_cyl = (full_cylinder
                .rotate((0,0,0), (1,0,0), -cyl_angle/2) # Tilt out
                .translate((20, block_width/2 - 10, block_height)) # Position on block
                )
    
    # Right Cylinder
    right_cyl = (full_cylinder
                 .rotate((0,0,0), (1,0,0), cyl_angle/2) # Tilt out opposite way
                 .translate((-20, -block_width/2 + 10, block_height)) # Staggered position (offset X usually)
                 )
    
    engine = base_engine.union(left_cyl).union(right_cyl)

    # 3. Details
    
    # Oil Sump
    sump = (cq.Workplane("XY")
            .rect(block_length - 20, block_width - 20)
            .extrude(15)
            .translate((0,0,-15))
            .edges("|Z").fillet(5)
            )
    engine = engine.union(sump)
    
    # Front Starter/Alternator cover details
    front_detail_cyl = (cq.Workplane("YZ")
                        .circle(25)
                        .extrude(40)
                        .translate((block_length/2 + front_length - 30, block_height/2 + 20, 0))
                        )
    engine = engine.union(front_detail_cyl)
    
    # Intake Manifold stubs (simplified)
    intake_stub = cq.Workplane("XY").circle(10).extrude(30)
    
    # Position intakes pointing inwards
    left_intake = (intake_stub
                   .rotate((0,0,0), (1,0,0), -cyl_angle/2 + 90)
                   .translate((20, 10, block_height + 40))
                   )
    right_intake = (intake_stub
                    .rotate((0,0,0), (1,0,0), cyl_angle/2 - 90)
                    .translate((-20, -10, block_height + 40))
                   )
    
    engine = engine.union(left_intake).union(right_intake)

    # Exhaust headers stubs
    exhaust_stub = cq.Workplane("XY").circle(12).extrude(20)
    left_ex = (exhaust_stub
               .rotate((0,0,0), (1,0,0), -cyl_angle/2 - 90) # Point down/out
               .translate((20, 60, block_height + 30))
               )
    right_ex = (exhaust_stub
                .rotate((0,0,0), (1,0,0), cyl_angle/2 + 90)
                .translate((-20, -60, block_height + 30))
                )
    
    engine = engine.union(left_ex).union(right_ex)
    
    # Rotation to match image orientation roughly (isometric view handled by viewer, but we can align axes)
    # The image has front facing right-ish.
    return engine

result = create_engine()