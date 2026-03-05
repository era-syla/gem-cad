import cadquery as cq

# Define parametric variables for the Pawn
base_diameter = 30.0
base_height = 4.0
fillet_radius = 2.0
stem_bottom_diameter = 18.0
stem_top_diameter = 8.0
stem_height = 30.0
collar_diameter = 12.0
collar_thickness = 2.0
head_diameter = 14.0

def make_pawn():
    # 1. Base construction
    # We start with the bottom-most disk
    base = cq.Workplane("XY").circle(base_diameter / 2).extrude(base_height)
    
    # Add a fillet to the top edge of the base to create the first smooth transition
    base = base.edges(">Z").fillet(fillet_radius)
    
    # 2. Stem construction
    # The stem is a loft or a revolution. A loft between two circles is easiest here.
    # We create the stem on top of the base.
    
    # Plane for the start of the stem (top of base)
    stem_start_plane = base.faces(">Z").workplane()
    
    # Plane for the end of the stem
    stem_end_plane = stem_start_plane.workplane(offset=stem_height)
    
    # Define the bottom circle of the stem
    c1 = stem_start_plane.circle(stem_bottom_diameter / 2)
    
    # Define the top circle of the stem
    c2 = stem_end_plane.circle(stem_top_diameter / 2)
    
    # Create the lofted stem
    stem = c1.loft(combine=False) # Don't combine yet to keep logic clean
    
    # 3. Collar (the small ring below the head)
    # We place this on top of the stem
    collar = (
        stem.faces(">Z").workplane()
        .circle(collar_diameter / 2)
        .extrude(collar_thickness, combine=False)
    )
    
    # 4. Head (Sphere)
    # We place the sphere on top of the collar.
    # We need to find the center point for the sphere.
    # The sphere sits on the collar, so its center is radius distance above the collar top.
    head_z_offset = base_height + stem_height + collar_thickness + (head_diameter / 2) * 0.8 # Slightly sunk in
    
    head = (
        cq.Workplane("XY")
        .workplane(offset=head_z_offset)
        .sphere(head_diameter / 2)
    )
    
    # 5. Combine all parts
    pawn = base.union(stem).union(collar).union(head)
    
    # 6. Apply smoothing/fillets to make it look organic like the image
    # Fillet the transition between stem and base
    # We select edges near the bottom of the stem
    try:
        pawn = pawn.edges(cq.selectors.NearestToPointSelector((0, 0, base_height))).fillet(3.0)
    except:
        pass # Fallback if geometry is tricky

    # Fillet the transition between stem and collar
    try:
        pawn = pawn.edges(cq.selectors.NearestToPointSelector((0, 0, base_height + stem_height))).fillet(1.0)
    except:
        pass
        
    return pawn

# Create the first pawn
pawn1 = make_pawn()

# Create the second pawn and move it
pawn2 = make_pawn().translate((45, 15, 0))

# Combine them into the final result
result = pawn1.union(pawn2)