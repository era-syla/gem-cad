import cadquery as cq

# Parametric dimensions
# Handle/Bottom section dimensions
handle_diameter = 20.0
handle_length = 50.0

# Middle shaft/neck dimensions
neck_diameter = 12.0
neck_length = 20.0

# Top flared head dimensions
head_base_diameter = 12.0  # Matches neck diameter
head_top_diameter = 25.0
head_height = 8.0
fillet_radius = 4.0 # For the smooth transition at the top

def create_part():
    # 1. Create the main handle (cylinder)
    # We'll build up from the Z plane
    handle = cq.Workplane("XY").circle(handle_diameter / 2).extrude(handle_length)

    # 2. Create the neck (smaller cylinder) on top of the handle
    # Select the top face of the handle to start drawing the neck
    neck = (handle.faces(">Z")
            .workplane()
            .circle(neck_diameter / 2)
            .extrude(neck_length))

    # 3. Create the flared head
    # A simple extrusion or loft could work, but looking at the image, 
    # the flare has a curved profile. A revolution is often cleaner for this shape,
    # but a loft with a fillet is easier to construct parametrically given the primitive shapes.
    # Let's try a simple cone first, then fillet the top edge heavily to get that rounded look.
    
    # Selecting the top of the neck
    part_with_head = (neck.faces(">Z")
                      .workplane()
                      .circle(head_top_diameter / 2) # Top circle
                      .workplane(offset=-head_height) # Go back down
                      .circle(neck_diameter / 2) # Bottom circle (matching neck)
                      .loft(combine=True))

    # The image shows a very distinct rounded profile for the head, almost like a trumpet bell.
    # A standard loft creates straight sides. 
    # Let's refine the approach for the head to match the curvature better using a Revolve.
    
    # Alternative Strategy: Construct the profile and revolve it.
    # Profile points:
    # (0, 0) -> Center bottom
    # (handle_radius, 0) -> Bottom corner
    # (handle_radius, handle_len) -> Top of handle
    # (neck_radius, handle_len) -> Step in
    # (neck_radius, handle_len + neck_len) -> Top of neck/Base of head
    # ... curve to ...
    # (head_radius, total_height) -> Top outer rim
    
    # However, CadQuery's stack-based approach is often more readable. 
    # Let's stick to the stack approach but fix the head shape.
    # The head looks like a spherical segment or a heavily filleted cone.
    
    # Let's recreate just the head part using a Revolve operation on a separate Workplane for better control
    # or apply a large fillet to the transition if we modeled it as a step.
    
    # Let's go back to the simple cone loft, but apply a fillet to the transition 
    # between the flat top face and the side of the cone.
    # Looking closely at the image, the top face is slightly convex or flat, but the transition is very round.
    
    # Let's try a simpler approach: Cylinder -> Cylinder -> Cone -> Fillet
    
    final_geo = (
        cq.Workplane("XY")
        # 1. Handle
        .circle(handle_diameter / 2).extrude(handle_length)
        # 2. Neck
        .faces(">Z").workplane()
        .circle(neck_diameter / 2).extrude(neck_length)
        # 3. Head (Conical section)
        .faces(">Z").workplane()
        .circle(neck_diameter / 2) # Base of loft
        .workplane(offset=head_height)
        .circle(head_top_diameter / 2) # Top of loft
        .loft(combine=True)
    )
    
    # Now we apply fillets to smooth it out to look like the image.
    # The image shows a smooth transition from the neck to the head.
    # We select the edge where the neck meets the cone.
    
    # Select the edge at the base of the head (neck-to-head transition)
    # This creates the "trumpet" curve.
    try:
        final_geo = final_geo.edges(f"Z>{handle_length + neck_length - 0.1} and Z<{handle_length + neck_length + 0.1}").fillet(head_height * 0.6)
    except:
        # Fallback if selection is tricky, though parametric Z height usually works
        pass
        
    # The top edge of the head is also rounded
    final_geo = final_geo.edges(">Z").fillet(1.0)
    
    return final_geo

# Generate the result
result = create_part()