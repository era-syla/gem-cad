import cadquery as cq

# ==========================================
# Parameter Definitions
# ==========================================

# Main Cylinder Dimensions
cyl_length = 80.0       # Length of the central tube section
cyl_radius = 20.0       # Radius of the central tube (Diameter 40)
cap_thickness = 12.0    # Thickness of the end caps
cap_radius = 26.0       # Radius of the end caps (Diameter 52)

# Mounting Bracket Dimensions
mount_width = 20.0      # Thickness of the bracket in the Y-direction
mount_reach = 22.0      # Distance from the end cap face to the pin hole center
mount_tip_radius = 12.0 # Radius of the rounded end of the bracket
mount_top_offset = 18.0 # Height from center axis to the top flat face
pin_hole_diam = 10.0    # Diameter of the main mounting pin hole
port_hole_diam = 4.0    # Diameter of the small port hole on top

# ==========================================
# Geometry Construction
# ==========================================

# 1. Main Body Assembly (Tube + End Caps)
# ----------------------------------------

# Central Tube
# Created along the X-axis, offset to start after the first cap
tube = (cq.Workplane("YZ")
        .workplane(offset=cap_thickness)
        .circle(cyl_radius)
        .extrude(cyl_length)
        )

# Left End Cap (at X=0)
cap_left = (cq.Workplane("YZ")
            .circle(cap_radius)
            .extrude(cap_thickness)
            )

# Right End Cap (at end of tube)
cap_right = (cq.Workplane("YZ")
             .workplane(offset=cap_thickness + cyl_length)
             .circle(cap_radius)
             .extrude(cap_thickness)
             )

# Union the cylindrical parts into the main body
body = cap_left.union(tube).union(cap_right)

# Apply fillets to the outer edges of the caps for a realistic look
# We select edges with the largest radius (the outer rim of the caps)
try:
    body = body.edges(cq.selectors.RadiusNthSelector(0)).fillet(2.0)
except Exception:
    pass

# 2. Mounting Brackets
# ----------------------------------------
def create_bracket():
    """
    Creates a single mounting bracket geometry.
    The geometry is built at the origin, designed to attach to a face at X=0 
    and extend into negative X direction.
    """
    # A. Rectangular Block (The body connecting cap to pivot)
    # Extends from X=0 to X=-mount_reach
    # Z-height: from -mount_tip_radius (bottom) to +mount_top_offset (top)
    block = (cq.Workplane("XY")
             .workplane(offset=-mount_tip_radius)
             .moveTo(0, 0)
             # Create rectangle: X goes from -mount_reach to 0, Y centered
             .rect(mount_reach, mount_width, centered=False) 
             .center(-mount_reach, -mount_width/2)
             .extrude(mount_top_offset + mount_tip_radius)
             )
    
    # B. Rounded Tip (Cylinder at the pivot point)
    # Oriented along Y-axis, centered at X=-mount_reach, Z=0
    tip = (cq.Workplane("XZ")
           .moveTo(-mount_reach, 0)
           .circle(mount_tip_radius)
           .extrude(mount_width/2, both=True) # Symmetric extrusion along Y
           )
    
    # Combine block and rounded tip
    bracket = block.union(tip)
    
    # C. Main Pivot Hole (Through the side, along Y-axis)
    bracket = (bracket
               .faces(">Y").workplane()
               .moveTo(-mount_reach, 0)
               .circle(pin_hole_diam / 2.0)
               .cutThruAll()
               )
    
    # D. Top Port Hole (Through the top face, along Z-axis)
    bracket = (bracket
               .faces(">Z").workplane()
               .moveTo(-mount_reach, 0)
               .circle(port_hole_diam / 2.0)
               .cutBlind(-15.0) # Blind cut downwards
               )
    
    return bracket

# Generate Left Mount (Foreground)
mount_left = create_bracket()

# Generate Right Mount (Background)
# Mirror the left mount across YZ plane to flip it for the opposite end (facing +X)
# Translate it to the total length of the assembly
total_assembly_length = cap_thickness * 2 + cyl_length
mount_right = create_bracket().mirror("YZ").translate((total_assembly_length, 0, 0))

# ==========================================
# Final Composition
# ==========================================

# Combine main body with both mounts
result = body.union(mount_left).union(mount_right)

# Optional: Add fillets at the junction between the tube and the end caps
# Selecting the second largest radius edges (the tube radius)
try:
    result = result.edges(cq.selectors.RadiusNthSelector(1)).fillet(1.0)
except Exception:
    pass