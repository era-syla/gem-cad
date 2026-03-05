import cadquery as cq

# --- Parameters ---

# C-Ring Dimensions
ring_od = 45.0
ring_id_base = 36.0  # The wider inner diameter
ring_thickness = 5.0
ring_lobe_radius = 4.0
ring_groove_width = 2.0
ring_groove_depth = 1.0

# Lock Mechanism Dimensions
dial_od = 24.0
dial_width = 6.0
core_od = 14.0
clamp_length = 16.0
clamp_height_radius = 9.0  # Distance from center to screw boss centers
screw_hole_dia = 3.5
bore_dia = 6.0

# --- Geometry Construction ---

def create_wavy_ring():
    # 1. Create the main washer body (Full annulus initially)
    # Outer radius and base inner radius
    base = cq.Workplane("XY").circle(ring_od/2).circle(ring_id_base/2).extrude(ring_thickness)
    
    # 2. Add lobes (Convex bumps on the inner diameter)
    # We create cylinders centered on the base inner radius and fuse them
    lobes = cq.Workplane("XY")
    num_lobes = 5
    start_angle = 0
    end_angle = 180
    angle_step = (end_angle - start_angle) / (num_lobes - 1)
    
    for i in range(num_lobes):
        angle = start_angle + i * angle_step
        # Calculate position for the lobe center
        # Positioned on the ID circumference
        lobe = (cq.Workplane("XY")
                .transformed(rotate=(0, 0, angle))
                .center(ring_id_base/2, 0)
                .circle(ring_lobe_radius)
                .extrude(ring_thickness))
        lobes = lobes.union(lobe)
        
    # Fuse lobes to base
    ring_with_lobes = base.union(lobes)
    
    # 3. Cut inner clearance to ensure distinct lobes if needed
    # (Optional, effectively trimming the lobes if they protrude too far in, 
    # but here we assume the geometry is additive)
    
    # 4. Cut into a Semi-Circle (C-Shape)
    # We keep the top half (Y > epsilon)
    cutter_box = (cq.Workplane("XY")
                  .center(0, -ring_od/2)
                  .box(ring_od*2, ring_od, ring_thickness*2))
    c_ring = ring_with_lobes.cut(cutter_box)
    
    # 5. Create the Groove on the top face
    groove_radius = (ring_od + ring_id_base) / 4.0 # Midpoint radius approx
    groove = (cq.Workplane("XY")
              .workplane(offset=ring_thickness - ring_groove_depth)
              .circle(groove_radius + ring_groove_width/2)
              .circle(groove_radius - ring_groove_width/2)
              .extrude(ring_groove_depth * 2)) # Cut upwards
    
    c_ring = c_ring.cut(groove)
    
    return c_ring

def create_lock_mechanism():
    # Axis of the lock is aligned with X
    
    # 1. The Dial (Knurled Ring)
    dial = cq.Workplane("YZ").circle(dial_od/2).extrude(dial_width)
    
    # Knurling pattern (Cuts around the perimeter)
    knurl_cutters = (cq.Workplane("YZ")
                     .polarArray(dial_od/2, 0, 360, 24)
                     .circle(1.0)
                     .extrude(dial_width))
    dial = dial.cut(knurl_cutters)
    
    # 2. The Central Core (Front Face)
    # Extends through and slightly in front of dial
    core = (cq.Workplane("YZ")
            .workplane(offset=-2)
            .circle(core_od/2)
            .extrude(dial_width + 4))
            
    # Key Slot on Front Face
    slot = (cq.Workplane("YZ")
            .workplane(offset=dial_width + 1)
            .rect(3.0, core_od - 4)
            .extrude(2.0)) # Cut into the face? Or separate feature? 
                           # Usually a cut. Let's cut into the core.
    
    slot_cut = (cq.Workplane("YZ")
                .workplane(offset=dial_width + 2) # Start in front
                .rect(3.0, core_od - 2)
                .extrude(-4.0)) # Cut back
    core = core.cut(slot_cut)
    
    # 3. The Rear Clamp Body
    # A complex shape with a central bore and two mounting lobes
    # We construct this by creating solids for the lobes and hulling them
    
    # Base plane behind the dial
    clamp_wp = cq.Workplane("YZ").workplane(offset=-clamp_length)
    
    # Create the three constituent cylinders
    c_main = clamp_wp.circle(core_od/2).extrude(clamp_length)
    c_top = clamp_wp.center(0, clamp_height_radius).circle(4.5).extrude(clamp_length)
    c_bot = clamp_wp.center(0, -clamp_height_radius).circle(4.5).extrude(clamp_length)
    
    # Combine and Hull to create the organic bridged shape
    clamp_body = c_main.union(c_top).union(c_bot)
    try:
        clamp_body = clamp_body.hull()
    except:
        # Fallback if hull of 3D solids is not supported in specific version
        # We assume standard CQ 2.x
        pass
        
    # 4. Transverse Screw Hole
    # Vertical hole through the clamping lobes
    screw_hole = (cq.Workplane("XZ")
                  .workplane(offset=15)
                  .center(-clamp_length/2, 0)
                  .circle(screw_hole_dia/2)
                  .extrude(-30))
    clamp_body = clamp_body.cut(screw_hole)
    
    # 5. Side Split (Slot for clamping action)
    # Horizontal cut through the side
    split_cut = (cq.Workplane("XY")
                 .workplane(offset=0)
                 .center(-clamp_length/2, clamp_height_radius)
                 .box(clamp_length+2, 2.0, 10)) # Cut top lobe connection
    # clamp_body = clamp_body.cut(split_cut) # Optional detail
    
    # 6. Assembly
    # Combine Dial, Core, and Clamp
    lock = dial.union(core).union(clamp_body)
    
    # 7. Central Bore
    # Hole running through the entire length
    bore = cq.Workplane("YZ").circle(bore_dia/2).extrude(100, both=True)
    lock = lock.cut(bore)
    
    return lock

# --- Build and Layout ---

# Create parts
part_ring = create_wavy_ring()
part_lock = create_lock_mechanism()

# Position parts to match the image roughly
# Ring top-left, Lock bottom-right
part_ring = part_ring.rotate((0,0,0), (0,0,1), 135).translate((-35, 35, 0))
part_lock = part_lock.translate((10, -10, 0))

# Combine into result
result = part_ring.union(part_lock)