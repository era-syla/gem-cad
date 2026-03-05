import cadquery as cq

def create_bearing(id=10, od=30, width=9, seal_recess=0.5):
    """
    Creates a simplified parametric ball bearing model.
    
    :param id: Inner Diameter
    :param od: Outer Diameter
    :param width: Total Width
    :param seal_recess: Depth of the seal recess
    """
    
    # Radii
    ir = id / 2.0
    or_val = od / 2.0
    
    # Ring thicknesses (approximate for visual realism)
    ring_thickness = (or_val - ir) * 0.25
    
    inner_ring_od = ir + ring_thickness
    outer_ring_id = or_val - ring_thickness
    
    # Create the outer ring
    outer_ring = (cq.Workplane("XY")
                  .circle(or_val)
                  .circle(outer_ring_id)
                  .extrude(width)
                  .translate((0, 0, -width/2)))
                  
    # Create the inner ring
    inner_ring = (cq.Workplane("XY")
                  .circle(inner_ring_od)
                  .circle(ir)
                  .extrude(width)
                  .translate((0, 0, -width/2)))
    
    # Create the cage/seal (simplified as a solid cylinder between rings, slightly recessed)
    seal_width = width - (2 * seal_recess)
    seal = (cq.Workplane("XY")
            .circle(outer_ring_id - 0.1) # Small gap
            .circle(inner_ring_od + 0.1)
            .extrude(seal_width)
            .translate((0, 0, -seal_width/2)))
    
    # Add a slight groove or detail to the seal to make it look like a bearing race/seal
    # by subtracting a small ring in the middle or just leaving it flat.
    # For a visual match to the image, the seal is recessed.
    
    # Combine parts
    bearing = outer_ring.union(inner_ring).union(seal)
    
    # Add chamfers to the outer edges of rings for realism
    bearing = bearing.edges(cq.selectors.RadiusNthSelector(0)).chamfer(width*0.05)
    bearing = bearing.edges(cq.selectors.RadiusNthSelector(-1)).chamfer(width*0.05)

    return bearing

# --- Parameters based on visual estimation of standard bearing proportions ---

# Bearing 1 (Larger, Left) - Looks like a 6000 series, maybe 608 or similar proportions
b1_id = 8.0
b1_od = 22.0
b1_width = 7.0

# Bearing 2 (Smaller, Right) - Looks deeper relative to diameter, maybe a small needle bearing or just a smaller ball bearing
b2_id = 4.0
b2_od = 10.0
b2_width = 6.0 # Proportionally wider

# --- Generate Geometry ---

# Create the first bearing
bearing1 = create_bearing(id=b1_id, od=b1_od, width=b1_width)

# Position Bearing 1 (Bottom Left in image)
# Moving it slightly forward and down
bearing1 = bearing1.translate((-15, -15, 0)).rotate((1,0,0), (0,0,0), 60).rotate((0,0,1), (0,0,0), 30)

# Create the second bearing
bearing2 = create_bearing(id=b2_id, od=b2_od, width=b2_width)

# Position Bearing 2 (Top Right in image)
# Moving it back and up
bearing2 = bearing2.translate((15, 15, 10)).rotate((0,1,0), (0,0,0), -45).rotate((1,0,0), (0,0,0), -20)

# Combine into a single result
result = bearing1.union(bearing2)