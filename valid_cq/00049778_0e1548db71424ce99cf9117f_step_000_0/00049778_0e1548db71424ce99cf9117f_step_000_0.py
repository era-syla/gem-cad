import cadquery as cq

# --- Part 1: Cross Filter Gasket ---
def make_cross_filter(od=30.0, id=26.0, h=4.0, thickness=3.0):
    # Outer Ring
    ring = cq.Workplane("XY").circle(od/2).circle(id/2).extrude(h)
    
    # Internal Cross Structure
    cross_bars = (
        cq.Workplane("XY")
        .rect(od, thickness).extrude(h)
        .union(cq.Workplane("XY").rect(thickness, od).extrude(h))
    )
    
    # Trim bars to fit inside the OD
    bounding_cyl = cq.Workplane("XY").circle(od/2).extrude(h)
    cross_structure = cross_bars.intersect(bounding_cyl)
    
    # Combine
    return ring.union(cross_structure)

# --- Part 2: Ribbed Bellows Connector ---
def make_ribbed_bellows(od=26.0, id=18.0, h=14.0):
    # Create profile in XZ plane to revolve around Z axis
    # The default revolve axis for XZ plane is Z-axis (local Y of the plane)
    
    r_inner = id / 2.0
    r_base = (od / 2.0) - 2.0
    r_peak = od / 2.0
    
    # Define points for the outer wall profile (two bumps)
    # Start bottom-inner
    pts = [
        (r_inner, 0),
        (r_base, 0)
    ]
    
    # We will build the profile using a wire construction for better control
    # Base line
    p = cq.Workplane("XZ").moveTo(r_inner, 0).lineTo(r_base, 0)
    
    # First bump (arc)
    p = p.threePointArc((r_peak, h * 0.25), (r_base, h * 0.5))
    
    # Second bump (arc)
    p = p.threePointArc((r_peak, h * 0.75), (r_base, h))
    
    # Top and inner close
    p = p.lineTo(r_inner, h).close()
    
    # Revolve 360 degrees
    return p.revolve()

# --- Part 3: Bushing (Center Cylinder) ---
def make_bushing(od=16.0, id=6.0, h=8.0):
    part = cq.Workplane("XY").circle(od/2).extrude(h)
    part = part.faces(">Z").hole(id)
    
    # Add a chamfer/countersink to the top hole edge
    # Selecting the inner circle on the top face
    part = part.faces(">Z").edges(cq.selectors.RadiusNthSelector(0)).chamfer(1.5)
    
    # Fillet the outer bottom edge slightly for realism
    part = part.faces("<Z").edges().fillet(0.5)
    
    return part

# --- Part 4: Flat Washer ---
def make_washer(od=18.0, id=10.0, h=4.0):
    part = cq.Workplane("XY").circle(od/2).circle(id/2).extrude(h)
    # Slight fillet on all edges
    part = part.edges().fillet(0.5)
    return part

# --- Part 5: O-Ring / Grommet ---
def make_grommet(od=16.0, section_r=2.5):
    major_r = (od / 2.0) - section_r
    # Create a torus
    # CadQuery's solid primitive creation or revolving a circle
    # Let's revolve a circle on XZ
    part = (
        cq.Workplane("XZ")
        .moveTo(major_r, section_r) # Position center of circle
        .circle(section_r)
        .revolve()
    )
    return part

# --- Part 6: Slotted Cap ---
def make_slotted_cap(od=12.0, h=4.0, slot_w=2.0, slot_d=1.5):
    part = cq.Workplane("XY").circle(od/2).extrude(h)
    
    # Cut the slot across the top face
    part = (
        part.faces(">Z")
        .workplane()
        .rect(od * 1.5, slot_w) # Rectangle wider than diameter
        .cutBlind(-slot_d)
    )
    return part

# --- Assemble the Parts ---

# Generate geometries
p1_cross = make_cross_filter()
p2_bellows = make_ribbed_bellows()
p3_bushing = make_bushing()
p4_washer = make_washer()
p5_grommet = make_grommet()
p6_slotted = make_slotted_cap()

# Position them in the scene
# Coordinates estimated to match the layout in the image
# (Back-Right)
cross_loc = p1_cross.translate((15, 30, 0))
# (Far Right)
bellows_loc = p2_bellows.translate((35, 5, 0))
# (Center)
bushing_loc = p3_bushing.translate((10, 0, 0))
# (Center-Left)
washer_loc = p4_washer.translate((-10, -2, 0))
# (Back-Left)
grommet_loc = p5_grommet.translate((-2, 18, 0))
# (Far Left)
slotted_loc = p6_slotted.translate((-25, -5, 0))

# Combine all into a single result object
result = (
    cross_loc
    .union(bellows_loc)
    .union(bushing_loc)
    .union(washer_loc)
    .union(grommet_loc)
    .union(slotted_loc)
)