import cadquery as cq
import math

def involute_gear(module, num_teeth, thickness, helix_angle=0, pressure_angle=20, clearance=0.1, backlash=0.1):
    """
    Helper function to create a simplified involute gear.
    CadQuery doesn't have a built-in involute profile generator in the core kernel that is exposed easily
    as a single function, so we approximate or use a parametric curve approach.
    For this complex assembly, a simplified tooth profile is sufficient to represent the visual geometry.
    """
    
    pitch_radius = module * num_teeth / 2.0
    addendum = module
    dedendum = 1.25 * module
    outer_radius = pitch_radius + addendum
    root_radius = pitch_radius - dedendum
    
    # Base circle for involute
    base_radius = pitch_radius * math.cos(math.radians(pressure_angle))
    
    # Create the gear profile
    # This is a simplified trapezoidal approximations for robustness in this generative context
    # Real involute generation is much more verbose.
    
    tooth_angle = 360.0 / num_teeth
    half_tooth_angle = tooth_angle / 4.0 # Roughly half the tooth thickness at pitch circle
    
    # Points for one tooth
    # We will just cut slots out of a cylinder to make an external gear
    # Or cut slots out of a ring to make an internal gear
    
    return cq.Workplane("XY").gear(
        module=module,
        teeth_number=num_teeth,
        width=thickness,
        pressure_angle=pressure_angle,
        helix_angle=helix_angle,
        clearance=clearance,
        backlash=backlash
    )

# Since the built-in gear function is sometimes not available or varies by CQ version/plugins, 
# let's build the geometry using basic primitives and parametric features to ensure execution.
# The image shows a complex assembly: 
# 1. A large outer Ring Gear.
# 2. A "Sun" gear or inner structure that is actually a Carrier with multiple gears.
# 3. A second, smaller ring gear mounted offset or coaxially.
# Looking closely, this is a Compound Planetary Gear setup, likely a LEGO-compatible part often called a "Turntable" or "Power Functions" part.
# Specifically, it resembles the LEGO Technic Turntable Type 2 (Top and Bottom parts).
# The image shows the bottom part (black/grey) with an inner ring of teeth and outer mounting holes,
# and a top part (light grey) which is a smaller spur gear that meshes with the inner teeth.
# Actually, wait, the image shows a large ring gear with EXTERNAL teeth, and a complex inner structure with holes.
# AND another smaller gear sitting on top.
# Let's approximate the visual style: A large external gear with a complex web of holes, and a smaller gear segment.

def create_lego_technic_turntable_style():
    # Dimensions (approximated for LEGO Technic scale)
    module = 1.0
    outer_teeth = 56  # Typical large turntable outer teeth
    inner_holes_radius = 20
    thickness = 8.0
    
    # 1. Main Ring Gear (The large outer part)
    # ---------------------------------------
    # Basic cylinder
    outer_radius = (outer_teeth * module) / 2 + module
    inner_radius_rim = outer_radius - 5.0 # Rim thickness
    
    # Create the gear profile (external teeth)
    # Using a simplified gear generator for the outer ring
    try:
        # Try using the cq-gears functionality if available in the environment, 
        # but fallback to manual tooth cutting for standard CQ compatibility.
        # We will manually cut teeth to be safe.
        
        # Base ring
        ring_gear = cq.Workplane("XY").circle(outer_radius).extrude(thickness)
        
        # Cut teeth
        tooth_depth = 2.2 * module
        tooth_width_top = 1.5 * module # Approximate
        num_teeth = 60 # Visual count approximation
        
        # Define a cutter for the space between teeth
        # A trapezoid representing the gear gap
        cutter_w_top = (2 * math.pi * outer_radius / num_teeth) * 0.6
        cutter_w_bot = cutter_w_top * 0.4
        
        cutter_pts = [
            (-cutter_w_top/2, outer_radius + 1),
            (cutter_w_top/2, outer_radius + 1),
            (cutter_w_bot/2, outer_radius - tooth_depth),
            (-cutter_w_bot/2, outer_radius - tooth_depth)
        ]
        
        cutter = cq.Workplane("XY").polyline(cutter_pts).close().extrude(thickness)
        
        # Polar array the cutter and subtract
        for i in range(num_teeth):
            angle = i * (360.0 / num_teeth)
            rotated_cutter = cutter.rotate((0,0,0), (0,0,1), angle)
            ring_gear = ring_gear.cut(rotated_cutter)
            
    except Exception:
        # Fallback simple cylinder if complex geo fails
        ring_gear = cq.Workplane("XY").circle(30).extrude(8)

    # 2. Inner Webbing and Holes
    # --------------------------
    # The image shows a complex pattern of cylinders (Technic pin holes) inside the ring.
    # Let's create a solid disc inside the ring first, then cut holes.
    
    web_thickness = 4.0
    web_z_offset = (thickness - web_thickness) / 2
    
    # Inner disc connecting to the ring
    inner_disc = cq.Workplane("XY").workplane(offset=web_z_offset).circle(outer_radius - tooth_depth).extrude(web_thickness)
    
    # Combine ring and disc
    base_part = ring_gear.union(inner_disc)
    
    # Create the pattern of Technic holes (cylinders with countersinks)
    # The pattern looks like a hexagonal or radial packing of circles.
    
    hole_radius = 2.4 # Standard Lego pin hole approx radius (4.8mm diameter)
    boss_radius = 4.0 # Wall thickness around hole
    boss_height = thickness
    
    # Create a list of positions for the holes based on the image
    # There is an outer ring of holes and an inner dense packing.
    hole_positions = []
    
    # Outer ring of bosses
    r_outer_holes = 22
    for i in range(12):
        angle = i * (360/12)
        rad = math.radians(angle)
        hole_positions.append((r_outer_holes * math.cos(rad), r_outer_holes * math.sin(rad)))

    # Inner ring of bosses
    r_inner_holes = 12
    for i in range(6):
        angle = i * (360/6) + 30 # Offset
        rad = math.radians(angle)
        hole_positions.append((r_inner_holes * math.cos(rad), r_inner_holes * math.sin(rad)))
        
    # Center hole
    hole_positions.append((0,0))
    
    # Create Bosses (cylinders) at these positions
    bosses = cq.Workplane("XY")
    for pos in hole_positions:
        bosses = bosses.moveTo(pos[0], pos[1]).circle(boss_radius).extrude(thickness)
        
    # Union bosses to base
    main_body = base_part.union(bosses)
    
    # Cut holes through the bosses
    holes = cq.Workplane("XY")
    for pos in hole_positions:
        # Main through hole
        holes = holes.moveTo(pos[0], pos[1]).circle(hole_radius).extrude(thickness)
        # Counterbores (visual style of technic beams)
        holes = holes.moveTo(pos[0], pos[1]).rect(hole_radius*0.5, thickness*2).extrude(thickness).rotate((0,0,0),(0,0,1), 45) # Cross slots often found
        
    # Apply cuts
    main_body = main_body.cut(holes)
    
    # Cut away material between bosses to make it look like a web/spokes
    # We essentially intersect the main body with a shape defined by the bosses + some connecting material
    # A simpler approach is to cut "voids" between the bosses.
    
    # Let's cut 6 large voids in the middle ring area to simulate the spoke structure
    void_cutter = cq.Workplane("XY").workplane(offset=-1).moveTo(17, 0).circle(3.5).extrude(thickness + 2)
    for i in range(6):
        angle = i * (360/6) + 15
        main_body = main_body.cut(void_cutter.rotate((0,0,0), (0,0,1), angle))

    # 3. The Second (Smaller) Gear
    # ----------------------------
    # The image shows a smaller gear segment sitting on top or nested. 
    # It looks like a "quarter gear" or a smaller ring gear section.
    # In the provided image, it actually looks like two concentric gears, one inside the other?
    # No, it looks like a differential casing or a planetary carrier.
    # Let's add the smaller semi-circular gear rack seen in the foreground.
    
    # Create a partial gear arc
    small_gear_radius = 18
    small_gear_thickness = 6
    
    # Arc shape
    small_gear_base = cq.Workplane("XY").workplane(offset=2).circle(small_gear_radius).extrude(small_gear_thickness)
    inner_cut = cq.Workplane("XY").workplane(offset=2).circle(small_gear_radius - 4).extrude(small_gear_thickness)
    small_gear_ring = small_gear_base.cut(inner_cut)
    
    # Cut it to be a semi-circle (approx 180 degrees)
    # Actually looking at the image, it's a full smaller gear nested inside, but offset?
    # No, it looks like a second ring gear stacked on top but smaller diameter.
    # Let's make it a full smaller gear for structural coherence.
    
    small_teeth_num = 28
    small_gear_outer_R = small_gear_radius
    
    # Cut teeth on small gear
    small_cutter_w = (2 * math.pi * small_gear_outer_R / small_teeth_num) * 0.5
    small_cutter = cq.Workplane("XY").polyline([
        (-small_cutter_w/2, small_gear_outer_R + 1),
        (small_cutter_w/2, small_gear_outer_R + 1),
        (small_cutter_w/4, small_gear_outer_R - 2.0),
        (-small_cutter_w/4, small_gear_outer_R - 2.0)
    ]).close().extrude(small_gear_thickness).translate((0,0,2)) # Lift to z=2
    
    for i in range(small_teeth_num):
        angle = i * (360.0 / small_teeth_num)
        rotated_cutter = small_cutter.rotate((0,0,0), (0,0,1), angle)
        small_gear_ring = small_gear_ring.cut(rotated_cutter)
        
    # Offset the small gear to the side as implied by the complex overlapping geometry in the image
    # In the image, there is a distinct smaller arc of teeth.
    small_gear_ring = small_gear_ring.translate((5, 5, 4)) # Move it up and offset
    
    # 4. Final Composition
    # --------------------
    # The image is very busy. It looks like an exploded view or a mechanism with many parts.
    # We will combine the main ring with the inner web, and place the smaller gear 'inside' or on top.
    
    # To better match the image which shows a sort of "Planetary" arrangement:
    # We have the big outer ring (main_body).
    # We will add 3 planetary gears inside.
    
    planet_radius = 8
    planet_teeth = 12
    planet_pos_radius = 16
    
    planet_base = cq.Workplane("XY").circle(planet_radius).extrude(thickness)
    # Simple tooth cut for planets
    p_cutter = cq.Workplane("XY").rect(1.5, 2.5).extrude(thickness).translate((0, planet_radius, 0))
    for i in range(planet_teeth):
        planet_base = planet_base.cut(p_cutter.rotate((0,0,0), (0,0,1), i*(360/planet_teeth)))
    
    # Add hole to planet
    planet_base = planet_base.cut(cq.Workplane("XY").circle(hole_radius).extrude(thickness))
    
    # Place planets
    planets = cq.Workplane("XY")
    for i in range(3):
        angle = i * (360/3)
        rad = math.radians(angle)
        x = planet_pos_radius * math.cos(rad)
        y = planet_pos_radius * math.sin(rad)
        planets = planets.union(planet_base.translate((x, y, 0)))

    # Since the image is one assembly, we union everything.
    # Note: In real CAD, these would be separate bodies.
    # The prompt asks for "this 3D CAD model", implying the assembly.
    
    # The "Inner Gear" in the image is likely the one we created as 'small_gear_ring',
    # but let's position it centrally to look like a sun gear.
    sun_gear = small_gear_ring.translate((-5, -5, -4)) # Reset translation
    sun_gear = sun_gear.translate((0,0,2)) # Slightly raised
    
    # Combine
    result = main_body.union(planets)
    
    # Add the distinct half-gear arch seen in the front of the image
    # This looks like a specific mounting bracket.
    arch_radius = 25
    arch = cq.Workplane("XY").workplane(offset=thickness).circle(arch_radius).extrude(4)
    arch = arch.cut(cq.Workplane("XY").workplane(offset=thickness).circle(arch_radius-4).extrude(4))
    # Cut to make it an arc
    box_cut = cq.Workplane("XY").workplane(offset=thickness).rect(60, 30).extrude(4).translate((0, -20, 0))
    arch = arch.cut(box_cut)
    
    # Add teeth to the arch (Crown gear style?)
    # Let's just fuse it for visual fidelity of "complexity"
    result = result.union(arch)

    return result

# Generate the model
result = create_lego_technic_turntable_style()