import cadquery as cq
import math

# Build a bicycle helmet shape using ellipsoid-like form with vents

# Main helmet shell - create an ellipsoidal dome shape
# We'll build it by revolving a profile and then cutting vent holes

def make_helmet():
    # Create the main helmet body using a lofted/revolved approach
    # Helmet dimensions: ~200mm wide, ~150mm tall, ~220mm long
    
    # Create base ellipsoid-like shape for helmet
    # Use a series of scaled circles lofted together
    
    # Main dome - create by scaling a sphere
    # Approximate helmet as a flattened ellipsoid
    
    r_x = 110  # width half
    r_y = 90   # height half  
    r_z = 115  # length half
    
    # Create the helmet shell by making an ellipsoid
    # We'll use a revolved profile in XZ plane, then scale
    
    # Profile points for helmet (half profile in XY plane)
    # The helmet is roughly egg-shaped, taller at back, open at bottom
    
    pts = [
        (0, 0),      # bottom center
        (95, 10),    # bottom side
        (105, 40),   # lower side
        (108, 80),   # mid side
        (95, 115),   # upper side
        (70, 140),   # near top
        (30, 155),   # top area
        (0, 158),    # top center
    ]
    
    # Create the outer shell by revolving
    outer = (
        cq.Workplane("XY")
        .center(0, 0)
        .polyline(pts)
        .close()
        .revolve(360, (0, 0, 0), (0, 1, 0))
    )
    
    # Scale to make it non-circular (elongate in Z direction)
    # CadQuery doesn't have scale, so we'll use a different approach
    
    # Instead, build helmet using loft of ellipses at different heights
    heights = [0, 20, 50, 80, 110, 135, 150, 158]
    # Radii at each height [rx, ry] (x=side, z=front-back)
    radii_x = [95, 105, 108, 105, 95, 75, 40, 5]
    radii_z = [110, 122, 125, 120, 108, 85, 45, 5]
    
    # Build helmet using a solid of revolution approach
    # Create elliptical cross sections and loft
    
    wires = []
    for i, h in enumerate(heights):
        rx = radii_x[i]
        rz = radii_z[i]
        if rx < 2:
            rx = 2
        if rz < 2:
            rz = 2
        wire = cq.Workplane("XY").workplane(offset=h).ellipse(rx, rz).wires().val()
        wires.append(wire)
    
    helmet_solid = cq.Workplane("XY").add(wires).toPending().loft()
    
    # Cut the bottom to create the opening
    helmet_solid = (
        helmet_solid
        .cut(
            cq.Workplane("XY").workplane(offset=-50).box(400, 400, 100).translate((0, 0, -75))
        )
    )
    
    # Add vents - horizontal elongated holes on the sides
    # Front vents
    vent_positions = [
        # (x_offset, z_offset, height, angle)
        (0, 90, 55, 0),   # front center vent
        (0, 85, 75, 0),   # second front vent
        (0, 75, 95, 0),   # third vent
    ]
    
    # Create vent cutters - elongated ellipsoids rotated to follow helmet surface
    for (xo, zo, ho, ang) in vent_positions:
        vent = (
            cq.Workplane("XZ")
            .workplane(offset=ho)
            .center(xo, zo)
            .ellipse(35, 8)
            .extrude(25, both=True)
        )
        helmet_solid = helmet_solid.cut(vent)
    
    # Side vents (left and right)
    side_vent_data = [
        (70, 40, 55),
        (72, 20, 75),
        (68, 0, 90),
    ]
    
    for (xo, zo, ho) in side_vent_data:
        for sign in [-1, 1]:
            vent = (
                cq.Workplane("YZ")
                .workplane(offset=sign * xo)
                .center(zo, ho)
                .ellipse(25, 7)
                .extrude(20, both=True)
            )
            helmet_solid = helmet_solid.cut(vent)
    
    # Add edge fillets to smooth the helmet
    try:
        result = helmet_solid.edges("|Z").fillet(3)
    except:
        result = helmet_solid
    
    return result

result = make_helmet()