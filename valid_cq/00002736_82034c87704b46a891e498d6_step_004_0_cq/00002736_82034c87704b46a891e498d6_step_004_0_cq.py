import cadquery as cq

# Parameters for the four pulley-like components
# Component 1 (Largest, left-most)
comp1_outer_dia = 20.0
comp1_thickness = 2.0
comp1_hub_dia = 6.0
comp1_hub_height = 2.0  # Above the main disk
comp1_hole_dia = 2.5
comp1_groove_depth = 0.5
comp1_groove_width = 0.5

# Component 2 (Smallest, second from left)
comp2_outer_dia = 8.0
comp2_thickness = 3.0
comp2_flange_dia = 10.0 # Top flange slightly wider
comp2_flange_thickness = 0.8
comp2_lower_shaft_dia = 5.0
comp2_lower_shaft_height = 2.0
comp2_hole_dia = 2.0

# Component 3 (Medium small, third from left)
comp3_outer_dia = 12.0
comp3_thickness = 3.0
comp3_hole_dia = 2.0
comp3_groove_depth = 0.5
comp3_groove_width = 0.5

# Component 4 (Medium large, right-most)
comp4_outer_dia = 16.0
comp4_thickness = 2.0
comp4_hub_dia = 6.0
comp4_hub_height = 2.0
comp4_hole_dia = 2.5
comp4_groove_depth = 0.5
comp4_groove_width = 0.5

# Spacing between components
spacing = 30.0

# --- Function to create a standard pulley/wheel shape ---
def create_pulley(outer_dia, thickness, hub_dia, hub_height, hole_dia, groove=True):
    # Base disk
    part = cq.Workplane("XY").circle(outer_dia / 2).extrude(thickness)
    
    # Hub
    if hub_height > 0:
        part = part.faces(">Z").workplane().circle(hub_dia / 2).extrude(hub_height)
    
    # Center Hole
    part = part.faces(">Z").workplane().hole(hole_dia)
    
    # Groove on the outer edge
    if groove:
        # Select the outer cylindrical face
        # We perform a cut using a revolved profile or a simple cut operation
        # A simple way is to create a cutting tool
        
        # Calculate vertical center of the main disk thickness
        z_center = thickness / 2.0
        
        # Create a cutter ring
        cutter = (
            cq.Workplane("XY")
            .workplane(offset=z_center)
            .circle(outer_dia / 2 + 0.1) # Slightly larger to ensure cut starts outside
            .circle(outer_dia / 2 - 0.5) # Depth of cut
            .extrude(0.5/2, both=True)   # Width of cut
        )
        # Often easier to use a 2D profile sweep or revolve for grooves, 
        # but let's try a direct cut operation on the edge for simplicity in this script style
        
        # Alternative approach: Revolve a groove profile
        # Create a profile on the XZ plane at the radius
        groove_profile = (
            cq.Workplane("XZ")
            .workplane(offset=0) # centered
            .moveTo(outer_dia/2, z_center - 0.25)
            .lineTo(outer_dia/2 - 0.5, z_center - 0.25)
            .lineTo(outer_dia/2 - 0.5, z_center + 0.25)
            .lineTo(outer_dia/2, z_center + 0.25)
            .close()
        )
        # Revolve cut is tricky without a dedicated axis reference in newer CQ versions sometimes
        # Let's use a simpler boolean subtraction of a ring (torus-like or cylinder)
        
        cutter_ring = (
            cq.Workplane("XY")
            .workplane(offset=z_center - 0.25)
            .circle(outer_dia/2 + 1) # Outer boundary of cutter
            .circle(outer_dia/2 - 0.2) # Inner boundary (depth)
            .extrude(0.5)
        )
        part = part.cut(cutter_ring)
        
    return part

# --- Function specifically for Component 2 (stepped shape) ---
def create_stepped_pulley():
    # Top flange
    p = cq.Workplane("XY").circle(comp2_flange_dia / 2).extrude(comp2_flange_thickness)
    
    # Main body/groove area
    p = p.faces(">Z").workplane().circle(comp2_outer_dia / 2).extrude(comp2_thickness - comp2_flange_thickness)
    
    # Lower shaft
    p = p.faces("<Z").workplane().circle(comp2_lower_shaft_dia / 2).extrude(comp2_lower_shaft_height)
    
    # Hole through all
    p = p.faces(">Z").workplane().hole(comp2_hole_dia)
    
    # Groove (simulated on the main body section)
    # Positioning the groove in the middle of the main body section
    z_groove = comp2_flange_thickness + (comp2_thickness - comp2_flange_thickness)/2
    
    cutter = (
        cq.Workplane("XY")
        .workplane(offset=z_groove - 0.25)
        .circle(comp2_flange_dia) # Large outer
        .circle(comp2_outer_dia/2 - 0.2) # Depth
        .extrude(0.5)
    )
    p = p.cut(cutter)
    
    return p

# --- Function for simple thick washer type (Comp 3) ---
def create_simple_grooved_wheel(outer_dia, thickness, hole_dia):
    part = cq.Workplane("XY").circle(outer_dia / 2).extrude(thickness)
    part = part.faces(">Z").workplane().hole(hole_dia)
    
    # Groove
    z_center = thickness / 2.0
    cutter = (
        cq.Workplane("XY")
        .workplane(offset=z_center - 0.25)
        .circle(outer_dia/2 + 1)
        .circle(outer_dia/2 - 0.2)
        .extrude(0.5)
    )
    part = part.cut(cutter)
    return part


# --- Build Components ---

# 1. Large Pulley
part1 = create_pulley(comp1_outer_dia, comp1_thickness, comp1_hub_dia, comp1_hub_height, comp1_hole_dia)

# 2. Small Stepped Pulley
part2 = create_stepped_pulley()

# 3. Medium Small Pulley
part3 = create_simple_grooved_wheel(comp3_outer_dia, comp3_thickness, comp3_hole_dia)

# 4. Medium Large Pulley
part4 = create_pulley(comp4_outer_dia, comp4_thickness, comp4_hub_dia, comp4_hub_height, comp4_hole_dia)

# --- Arrange in assembly ---
# We translate them along the X axis to match the image layout
# Left to right: Part 1, Part 2, Part 3, Part 4

loc1 = part1.translate((-1.5 * spacing, 0, 0))
loc2 = part2.translate((-0.5 * spacing, 0, 0))
loc3 = part3.translate((0.5 * spacing, 0, 0))
loc4 = part4.translate((1.5 * spacing, 0, 0))

# Combine into one object
result = loc1.union(loc2).union(loc3).union(loc4)