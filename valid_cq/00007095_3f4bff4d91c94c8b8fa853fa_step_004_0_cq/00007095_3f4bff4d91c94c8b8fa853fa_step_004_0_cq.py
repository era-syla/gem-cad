import cadquery as cq

# --- Parameter Definitions ---
rail_length = 500.0  # Total length of the rail
rail_diameter = 16.0 # Diameter of the cylindrical shaft part
base_width = 30.0    # Width of the bottom aluminum support
base_height = 20.0   # Total height of the support structure (excluding shaft protrusion)
shaft_offset = 18.0  # Height from bottom to center of the shaft
mounting_hole_spacing = 150.0 # Distance between mounting holes
hole_diameter = 5.5  # Diameter of mounting holes (for M5)

# --- Geometry Construction ---

# 1. Create the profile of the support rail
# The profile consists of a base rectangle and a neck that holds the shaft
def create_rail_profile(length):
    # Base dimensions
    w = base_width
    h = base_height
    offset = shaft_offset
    r = rail_diameter / 2.0
    
    # Sketch the cross-section
    # We will draw half and mirror, or draw the full shape. Let's draw full.
    # The shape is roughly a "T" or inverted "Y" shape with a circular top.
    
    # Bottom support block (trapezoidal or rectangular with side indentations)
    # Let's approximate the SBR rail support profile
    
    sketch = (
        cq.Sketch()
        .rect(w, h/2) # Simple base rectangle for the bottom flange
        .reset()
        .vertices()
        .circle(r) # The shaft itself
        .moved(cq.Location(cq.Vector(0, offset - h/4, 0))) # Move circle up
    )
    
    # More accurate profile approach using a polyline and extrusion
    # Coordinates for the right half of the cross-section (Z-up for 2D profile)
    # Origin at bottom center
    
    # Support dimensions
    flange_h = 5.0
    neck_w = rail_diameter * 0.8 # Slightly narrower than rail
    
    pts = [
        (0, 0),
        (base_width/2, 0),
        (base_width/2, flange_h),
        (neck_w/2, offset), # Connect flange to shaft center area
        (0, offset)
    ]
    
    # Create the support base extrusion
    support = (
        cq.Workplane("YZ")
        .polyline(pts)
        .mirrorY() # Mirror around Y axis (which is vertical Z in 3D world effectively)
        .extrude(length)
    )
    
    # Create the cylindrical shaft
    shaft = (
        cq.Workplane("YZ")
        .center(0, offset)
        .circle(rail_diameter/2)
        .extrude(length)
    )
    
    # Union them
    rail_assembly = support.union(shaft)
    
    # Clean up the intersection (optional filleting could be added here)
    # Let's add the specific shape seen in image: support wraps around shaft a bit
    # The polyline simple connection might clip inside.
    # Let's refine the support shape to "cup" the rail.
    
    return rail_assembly

# Let's rebuild with a more robust single sketch extrusion for the support
def create_linear_rail(length):
    # Dimensions for SBR16-like profile
    SBR_W = 40.0 # Base Width
    SBR_h = 5.0  # Flange height
    SBR_G = 25.0 # Distance from base to shaft center
    SBR_D = 16.0 # Shaft Diameter
    
    # Create the aluminum support profile
    # Drawing on YZ plane, extruding along X
    support_sketch = (
        cq.Workplane("YZ")
        .moveTo(-SBR_W/2, 0)
        .lineTo(SBR_W/2, 0)
        .lineTo(SBR_W/2, SBR_h)
        .lineTo(SBR_D/2, SBR_G) # Simplified neck
        .lineTo(-SBR_D/2, SBR_G)
        .lineTo(-SBR_W/2, SBR_h)
        .close()
        .extrude(length)
    )
    
    # Create the steel shaft
    shaft = (
        cq.Workplane("YZ")
        .center(0, SBR_G)
        .circle(SBR_D/2)
        .extrude(length)
    )
    
    full_rail = support_sketch.union(shaft)
    
    # Add mounting holes
    # Calculate number of holes based on spacing
    num_holes = int(length / mounting_hole_spacing)
    
    # Create points along the length
    # Center the pattern
    total_span = (num_holes - 1) * mounting_hole_spacing
    start_x = (length - total_span) / 2
    
    hole_locs = []
    for i in range(num_holes):
        x_pos = start_x + (i * mounting_hole_spacing)
        # We extruded along X, but origin is at start. 
        # Need to adjust relative to the workplane origin.
        hole_locs.append((x_pos, 0)) # (x, y) on the XY plane for vertical drilling
    
    # Cut holes
    # The rail was extruded along normal of YZ, which is X.
    # We want to drill down from Top (Z).
    
    final_rail = (
        full_rail
        .faces("<Z") # Select bottom face
        .workplane()
        .pushPoints(hole_locs)
        .hole(hole_diameter)
    )
    
    return final_rail

# Create two rails
rail1 = create_linear_rail(rail_length)
rail2 = create_linear_rail(rail_length).translate((0, 100, 0)) # Offset the second rail

# Combine into one result object
result = rail1.union(rail2)