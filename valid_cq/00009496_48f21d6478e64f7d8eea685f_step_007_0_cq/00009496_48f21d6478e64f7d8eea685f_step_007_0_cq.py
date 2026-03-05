import cadquery as cq
from math import sin, cos, radians

# --- Parametric Dimensions ---
# Main ring dimensions
ring_id = 40.0        # Inner diameter of the ring
ring_od = 50.0        # Outer diameter of the ring body
ring_thickness = 8.0  # Height/Thickness of the ring

# Lug (protrusion) dimensions
lug_width = 12.0      # Width of the rectangular protrusion
lug_extension = 6.0   # How far past the OD the lug extends
lug_chamfer = 2.0     # Size of the chamfer on the outer corners
lug_hole_dia = 2.0    # Diameter of the small hole in the lug face

# Derived dimensions
ring_radius_inner = ring_id / 2.0
ring_radius_outer = ring_od / 2.0
lug_total_length = ring_radius_outer + lug_extension

# --- Helper Function for Lug Geometry ---
def create_lug(angle):
    """
    Creates a single lug positioned at a specific angle.
    Using a Workplane oriented at the angle to draw the cross-section
    and extrude it.
    """
    # Create a workplane rotated to the correct angle
    # We position the workplane origin at the center, then rotate
    wp = cq.Workplane("XY").turn(angle).center(ring_radius_outer - 1.0, 0) # Start slightly inside to fuse well
    
    # Draw the rectangle for the lug
    # Note: On this rotated plane, X points radially outward, Y is tangential
    # We need to orient correctly. Let's try drawing on a plane tangent to the ring.
    
    # Alternative strategy: 
    # Draw the profile on the XY plane and rotate/translate it.
    # The lug is essentially a box added to the side.
    
    # Let's create the lug shape relative to the global origin first.
    # It sits on the X-axis.
    lug = (
        cq.Workplane("XY")
        .center(ring_radius_outer, 0) # Move to the edge of the ring
        .box(lug_extension * 2, lug_width, ring_thickness) # Create box, centered on the move point
        # Shift it so it starts slightly inside the ring ID/OD interface
        .translate((-lug_extension + 1.0, 0, 0)) 
    )
    
    # Add chamfers to the outer vertical edges and the top/bottom outer edges
    # The "outer" face is the one with the highest X value.
    # We select edges based on position.
    
    # Select the face furthest in +X direction
    outer_face = lug.faces(">X")
    
    # Chamfer the edges of the outer face
    lug = lug.edges(">X").chamfer(lug_chamfer)

    # Add the small hole
    lug = lug.faces(">X").workplane().circle(lug_hole_dia/2).cutThruAll()
    
    # Rotate the lug to the desired angle around Z axis
    lug = lug.rotate((0,0,0), (0,0,1), angle)
    
    return lug

# --- Main Construction ---

# 1. Create the base Ring
base_ring = (
    cq.Workplane("XY")
    .circle(ring_radius_outer)
    .circle(ring_radius_inner)
    .extrude(ring_thickness)
    .translate((0, 0, -ring_thickness/2)) # Center vertically on Z=0
)

# 2. Create the lugs and union them
lugs = []
for i in range(4):
    angle = i * 90
    
    # Calculate center position for the lug
    # We want to place a box at the periphery
    # Width is along tangent, Length is along radius
    
    # Local Lug construction
    lug_geo = (
        cq.Workplane("XY")
        .box(lug_extension + (ring_od - ring_id)/2, lug_width, ring_thickness)
        .translate(((ring_radius_outer + lug_extension/2) - (lug_extension + (ring_od - ring_id)/2)/2 + lug_extension/2, 0, 0))
    )
    
    # Refined Lug Construction to match image better
    # The lug starts inside the ring wall and extends out.
    # Total radial length needed = wall thickness + extension
    lug_radial_len = (ring_od - ring_id)/2 + lug_extension
    
    # Center of the box in X (radial)
    # It starts at ring_radius_inner and goes to ring_radius_outer + lug_extension
    center_x = ring_radius_inner + lug_radial_len / 2
    
    lug_geo = (
        cq.Workplane("XY")
        .box(lug_radial_len, lug_width, ring_thickness)
        .translate((center_x, 0, 0))
    )
    
    # Apply Chamfers
    # The image shows chamfers on the "tip" of the lug (the face furthest out).
    # It looks like the 4 corners of the outer face are chamfered.
    
    # Select edges on the outer face (>X)
    # We select the face, then get its edges.
    lug_geo = lug_geo.edges(cq.selectors.BoxSelector(
        (ring_radius_outer + lug_extension - 0.1, -lug_width/2 - 0.1, -ring_thickness/2 - 0.1),
        (ring_radius_outer + lug_extension + 0.1, lug_width/2 + 0.1, ring_thickness/2 + 0.1)
    ))
    
    # Applying chamfer to the outer face edges
    lug_geo = lug_geo.chamfer(lug_chamfer)
    
    # Add hole
    # Select outer face, draw circle, cut
    lug_geo = (
        lug_geo.faces(">X").workplane()
        .circle(lug_hole_dia / 2)
        .cutThruAll()
    )
    
    # Rotate into position
    lug_geo = lug_geo.rotate((0,0,0), (0,0,1), angle)
    lugs.append(lug_geo)

# 3. Combine everything
result = base_ring
for lug in lugs:
    result = result.union(lug)

# 4. Final fillets (optional but improves realism based on image softness)
# Fillet the junction between lugs and ring? The image looks fairly sharp there, 
# but maybe a tiny fillet. Let's stick to the sharp union for now as the image 
# has distinct lines, except for the explicit chamfers.

# Export or show
# show_object(result) # Only needed for CQ-editor
# result.export("model.step")