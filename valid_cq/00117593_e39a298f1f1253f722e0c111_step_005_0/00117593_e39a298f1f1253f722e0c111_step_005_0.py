import cadquery as cq

# --- Parametric Dimensions ---
# Body dimensions (Disk)
body_diameter = 14.0
body_thickness = 5.0
edge_fillet = 2.0  # Radius for the rounded edges of the disk

# Lead dimensions
lead_pitch = 7.5       # Distance between leads
lead_thick_dia = 1.4   # Diameter of the upper coating/insulation
lead_thin_dia = 0.6    # Diameter of the lower wire
lead_thick_len = 3.5   # Length of the upper thick section
lead_thin_len = 12.0   # Length of the lower wire section

# --- Geometry Construction ---

# 1. Create the Main Body
# We construct a cylinder on the XZ plane (standing upright) and extrude along Y.
# 'both=True' centers the extrusion on the plane.
body = (
    cq.Workplane("XZ")
    .circle(body_diameter / 2.0)
    .extrude(body_thickness, both=True)
)

# Apply fillets to the front and back circular edges to achieve the rounded look
# We select edges of type CIRCLE to avoid selecting potential seam edges
body = body.edges("%CIRCLE").fillet(edge_fillet)

# 2. Define Lead Construction Function
def create_lead(x_pos):
    """Creates a stepped lead at the specified X position."""
    
    # Determine start Z height. We start slightly inside the body 
    # (bottom of body is at Z = -body_diameter/2)
    z_start = -(body_diameter / 2.0) + 1.5
    
    # Create the thicker upper section (insulation drip)
    # Workplane XY has Z as normal. We offset to z_start.
    upper_seg = (
        cq.Workplane("XY")
        .center(x_pos, 0)
        .workplane(offset=z_start)
        .circle(lead_thick_dia / 2.0)
        .extrude(-lead_thick_len)
    )
    
    # Create the thinner lower section (wire)
    # Start from the bottom face of the upper segment
    lower_seg = (
        upper_seg.faces("<Z")
        .workplane()
        .circle(lead_thin_dia / 2.0)
        .extrude(-lead_thin_len)
    )
    
    # Combine segments
    lead = upper_seg.union(lower_seg)
    
    # Add a small fillet at the transition step for realism
    # Select edge nearest to the transition point
    transition_pt = (x_pos, 0, z_start - lead_thick_len)
    try:
        lead = lead.edges(cq.NearestToPointSelector(transition_pt)).fillet(0.3)
    except Exception:
        # Fallback if geometry kernel fails on small feature
        pass
        
    return lead

# 3. Generate Leads
lead_left = create_lead(-lead_pitch / 2.0)
lead_right = create_lead(lead_pitch / 2.0)

# 4. Final Boolean Union
result = body.union(lead_left).union(lead_right)