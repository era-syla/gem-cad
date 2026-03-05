import cadquery as cq

# Parameters
outer_radius = 50.0  # Outer radius of the top/bottom pads
inner_radius = 20.0  # Inner radius of the central gap
pad_thickness = 5.0  # Thickness of the top/bottom arc pads
total_height = 40.0  # Total height of the object
gap_width = 10.0     # Width of the gaps separating the four quadrants
fillet_radius = 2.0  # Slight rounding for aesthetics (optional but good practice)

# Calculated dimensions
mid_height = total_height / 2.0
connector_height = total_height - (2 * pad_thickness)
connector_width = 10.0 # Width of vertical connecting pillar

# Create a single quadrant
def create_quadrant():
    # 1. Create the base wedge shape (top pad)
    # We will work in the XY plane and extrude up
    
    # Define an arc segment for the top pad
    # The shape is essentially a pie slice with the tip cut off, or an arc sector.
    # However, looking closely, it's a sector minus a square central hole area.
    # Let's start simpler: make a full cylinder, cut it, and intersect.
    
    # Better approach for quadrant: Sketching on a plane
    # The quadrant looks like a 90-degree sector of an annulus.
    
    # Let's model one "unit" consisting of top pad, bottom pad, and connector.
    # It occupies roughly the +X/+Y quadrant.
    
    # --- Top Pad ---
    # Sketch the 90-degree arc shape
    # Center is at origin.
    top_pad = (
        cq.Workplane("XY")
        .workplane(offset=total_height/2 - pad_thickness)
        .moveTo(inner_radius, 0)
        .lineTo(outer_radius, 0)
        .threePointArc((outer_radius * 0.7071, outer_radius * 0.7071), (0, outer_radius)) # 90 degree arc
        .lineTo(0, inner_radius)
        .threePointArc((inner_radius * 0.7071, inner_radius * 0.7071), (inner_radius, 0)) # 90 degree arc
        .close()
        .extrude(pad_thickness)
    )

    # --- Bottom Pad ---
    # Same as top, just mirrored or created at the bottom
    bottom_pad = (
        cq.Workplane("XY")
        .workplane(offset=-total_height/2)
        .moveTo(inner_radius, 0)
        .lineTo(outer_radius, 0)
        .threePointArc((outer_radius * 0.7071, outer_radius * 0.7071), (0, outer_radius))
        .lineTo(0, inner_radius)
        .threePointArc((inner_radius * 0.7071, inner_radius * 0.7071), (inner_radius, 0))
        .close()
        .extrude(pad_thickness)
    )

    # --- Connector ---
    # The connector connects the top and bottom. It looks like a curved vertical wall 
    # or a "waist". It tapers in. 
    # Looking closely at the image:
    # The connector seems to be a solid block that follows the radial lines 
    # but might be chamfered or filleted heavily.
    # Actually, it looks like a loft or a revolution.
    # Let's look at the profile in the radial direction.
    # It seems to go from the inner radius of the pad, curve inward towards the center, then back out.
    # But wait, looking at the sharp corner in the middle of the connector...
    # It looks like a square or rectangular pillar that has been intersected with a revolution.
    
    # Let's try a simpler interpretation: 
    # It's a vertical pillar at the corner (inner radius), connecting top and bottom.
    # The profile creates a "hourglass" shape on the faces.
    
    # Let's define the connector profile on the symmetry plane (e.g., at 45 degrees) and revolve it?
    # No, the sides are flat (planar) along X and Y axes.
    # This suggests it is an extrusion of a specific profile along the Z axis, 
    # or a loft between top/bottom rectangles.
    
    # Re-evaluating geometry based on shadows:
    # The inner vertical face seems curved (part of a cylinder).
    # The side faces (along X=0 and Y=0 planes) are flat.
    # There is a conic/curved transition from the vertical pillar to the horizontal pads.
    
    # Let's build a central core and subtract.
    # Core: A 90-degree sector of a thick tube.
    core = (
        cq.Workplane("XY")
        .workplane(offset=-total_height/2 + pad_thickness)
        .moveTo(inner_radius, 0)
        .lineTo(inner_radius + pad_thickness, 0) # Make it thick enough
        .threePointArc(((inner_radius + pad_thickness) * 0.7071, (inner_radius + pad_thickness) * 0.7071), (0, inner_radius + pad_thickness))
        .lineTo(0, inner_radius)
        .threePointArc((inner_radius * 0.7071, inner_radius * 0.7071), (inner_radius, 0))
        .close()
        .extrude(total_height - 2*pad_thickness)
    )
    
    # Now adding the "fillet" or chamfer transition.
    # It looks like a large chamfer or conic sweep between the vertical core and the horizontal pads.
    # Instead of complex lofts, let's create a profile on the side faces and revolve/extrude.
    
    # Alternative strategy:
    # 1. Create the full sector block (top to bottom).
    # 2. Cut away the "waist" from the outside.
    
    full_sector = (
         cq.Workplane("XY")
        .workplane(offset=-total_height/2)
        .moveTo(inner_radius, 0)
        .lineTo(outer_radius, 0)
        .threePointArc((outer_radius * 0.7071, outer_radius * 0.7071), (0, outer_radius))
        .lineTo(0, inner_radius)
        .threePointArc((inner_radius * 0.7071, inner_radius * 0.7071), (inner_radius, 0))
        .close()
        .extrude(total_height)
    )
    
    # Cutout profile. We need to cut away the material between the pads.
    # The cut looks like a revolution of a shape.
    # Let's imagine a sketch on a vertical plane passing through the origin.
    # It cuts inwards.
    
    # Let's try creating the specific geometry by unioning the top/bottom pads
    # and a central "hourglass" pillar.
    
    # Define the pillar profile. It's square-ish in plan view (bounded by X and Y axes).
    # It sits at the inner corner.
    pillar_sq_size = (outer_radius - inner_radius) / 2 # Guessing size
    
    # Let's try a loft approach for the pillar to get that curve.
    # Bottom rect of pillar (at z = -h/2 + t)
    # Mid rect of pillar (at z = 0, smaller)
    # Top rect of pillar (at z = h/2 - t)
    
    # Actually, looking at the image, the curved surface is CONICAL.
    # It looks like a cone (or hyperboloid) connecting the top plate to a narrower center.
    
    # Let's build the "Waist"
    # Create a cone/cylinder hybrid.
    # Inner radius is constant (inner_radius).
    # Outer radius varies from (outer_radius/something) at pads to (smaller) at center.
    
    # Let's define a profile to revolve.
    # The profile is on the R-Z plane.
    # Points:
    # (inner_radius, -total_height/2)
    # (outer_radius, -total_height/2)
    # (outer_radius, -total_height/2 + pad_thickness)
    # ... curve inward ...
    # (waist_radius, 0)
    # ... curve outward ...
    # (outer_radius, total_height/2 - pad_thickness)
    # (outer_radius, total_height/2)
    # (inner_radius, total_height/2)
    # close
    
    waist_radius = inner_radius + 5.0 # Just a bit thicker than the hole
    
    # We construct the solid by revolving a profile 90 degrees
    # The profile defines the cross-section of one quadrant wall.
    
    pts = [
        (inner_radius, -total_height/2),
        (outer_radius, -total_height/2),
        (outer_radius, -total_height/2 + pad_thickness),
        (waist_radius, 0),
        (outer_radius, total_height/2 - pad_thickness),
        (outer_radius, total_height/2),
        (inner_radius, total_height/2)
    ]
    
    # Make the revolution
    quadrant_solid = (
        cq.Workplane("XZ")
        .polyline(pts)
        .close()
        .revolve(90, (0,0,0), (0,1,0)) # Revolve around Z axis (which is Y in this sketch plane context? No, standard revolve axis)
        # In Workplane("XZ"), X is horizontal, Z is vertical. We revolve around Z-axis (0,0,1) conceptually.
        # Cadquery revolve takes axisStart and axisEnd. 
        # For "XZ" plane, local Y is global Z. Local X is global X.
        # We want to revolve around global Z. In local coords of "XZ", that is the Y axis vector (0, 1).
    )
    
    # The revolution creates a curved outer face.
    # However, the image shows FLAT side faces (where the cuts are).
    # The revolution creates curved side faces if we just do 90 deg.
    # Wait, a 90 deg revolve creates flat faces at the start and end angles. That matches the image.
    # The outer face (radius) is curved. That matches.
    # The inner face (radius) is curved. That matches.
    # The "cut" faces are the start/end of the revolve. That matches.
    
    # The only issue is the specific shape of the curve between pad and waist.
    # polyline gives straight lines (conical sections).
    # spline gives curves.
    
    # Refined profile with spline for the waist
    s_pts = [
        (outer_radius, -total_height/2 + pad_thickness),
        (waist_radius, 0),
        (outer_radius, total_height/2 - pad_thickness)
    ]
    
    # We need to construct the wire carefully.
    # 1. Straight line Bottom-Inner to Bottom-Outer
    # 2. Straight line Bottom-Outer to Bottom-Pad-Top
    # 3. Spline down to waist and up to Top-Pad-Bottom
    # 4. Straight line Top-Pad-Bottom to Top-Outer
    # 5. Straight line Top-Outer to Top-Inner
    # 6. Straight line Top-Inner to Bottom-Inner
    
    # Note: The image shows the top pad has a constant thickness, then a sharp corner, then the curve starts.
    # Wait, actually looking very closely at the image:
    # The top surface is flat.
    # The outer radius is cylindrical (vertical).
    # The transition from the pad to the center pillar is the curve.
    # The outer vertical face of the pad exists.
    
    # My previous points assumed the curve goes all the way to the outer radius.
    # Correct logic:
    # Pad is a cylinder segment.
    # Connector is a smaller "waist" shape.
    
    pad_hang_over = 15.0 # How much the pad sticks out past the connector
    connector_outer_radius_at_pad = outer_radius # It seems to blend fully
    # Actually, looking at the top-left quadrant in the image:
    # There is a vertical face at the outer edge.
    # Then horizontal face (under side of pad).
    # Then the curve starts towards the center.
    
    # Revised Profile Points:
    # 1. (inner_radius, -total_height/2)  -> Start bottom inner
    # 2. (outer_radius, -total_height/2)  -> Bottom outer edge
    # 3. (outer_radius, -total_height/2 + pad_thickness) -> Bottom pad thickness side
    # 4. (outer_radius - 10, -total_height/2 + pad_thickness) -> Move in slightly on underside? 
    #    Actually, let's assume the curve starts immediately or after a small flat.
    #    Let's assume a simple loft from a rectangle/arc at the pad to a smaller one at the center.
    
    # Let's stick to the Revolve method, it generates the cleanest geometry for this radial symmetry.
    # We just need to tune the profile.
    
    # Define profile in XZ plane (where X is radial, Z is vertical)
    # Z=0 is center.
    
    mid_waist_radius = inner_radius + 6.0
    
    # Using spline for the "hourglass" curve
    quadrant = (
        cq.Workplane("XZ")
        .moveTo(inner_radius, -total_height/2)
        .lineTo(outer_radius, -total_height/2)
        .lineTo(outer_radius, -total_height/2 + pad_thickness)
        # Spline curve for the neck
        .spline([(mid_waist_radius, 0), (outer_radius, total_height/2 - pad_thickness)], includeCurrent=True)
        .lineTo(outer_radius, total_height/2)
        .lineTo(inner_radius, total_height/2)
        .close()
        .revolve(90, (0,0,0), (0,1,0)) 
    )
    
    return quadrant

# Create one quadrant
q1 = create_quadrant()

# The image shows gaps between the quadrants.
# The `revolve(90)` creates a shape from angle 0 to 90.
# We need to position these to have gaps.
# The gap width is `gap_width`.
# We need to shift the quadrants away from the center lines (X and Y axes) by gap_width/2.
# However, shifting a radial slice by x/y breaks the circular outer shape (it becomes oval-ish).
# Usually in these designs, the "gap" is a parallel cut.
# The easiest way to achieve the parallel gap look while maintaining outer curvature 
# is to arrange them 90 degrees apart and then move them along the diagonal 45?
# No, just move along X and Y.
# Or simpler: Create the 4 quadrants in place (rotated), then apply a "Slot" cut or move them.

# Method A: Move them.
# If we move q1 by (gap/2, gap/2), the inner radius corner moves away from origin.
# This matches the image (there is a central void).

offset_val = gap_width / 2.0

# Q1 is currently in +X/+Z (revolve creates typically from X axis towards Y).
# Let's orient Q1 to be centered around 45 degrees?
# Default revolve in XY plane starts at X and goes towards Y.
# So Q1 occupies 0 to 90 degrees.
# We want to translate it by (offset, offset, 0).

q1_moved = q1.translate((offset_val, offset_val, 0))
q2_moved = q1.rotate((0,0,0), (0,0,1), 90).translate((-offset_val, offset_val, 0))
q3_moved = q1.rotate((0,0,0), (0,0,1), 180).translate((-offset_val, -offset_val, 0))
q4_moved = q1.rotate((0,0,0), (0,0,1), 270).translate((offset_val, -offset_val, 0))

# Combine
final_obj = q1_moved.union(q2_moved).union(q3_moved).union(q4_moved)

# Add fillets?
# The image shows fairly sharp edges on the outside, but maybe slight fillets on the vertical edges.
# The request asks for parametric dimensions, we have them.

result = final_obj