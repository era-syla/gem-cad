import cadquery as cq
import math

# Create a decorative oval/plaque cookie cutter shape
# This is a thin-walled frame with a decorative scalloped/baroque outline

def make_plaque_profile():
    """Create the outer decorative plaque profile using spline points"""
    # Define the outer decorative frame shape - an oval with decorative bumps
    # The shape has scalloped edges typical of a baroque/ornate frame
    
    pts_outer = []
    pts_inner = []
    
    # Parameters
    a_out = 75  # outer x radius
    b_out = 50  # outer y radius
    a_in = 65   # inner x radius
    b_in = 40   # inner y radius
    
    n = 120
    
    for i in range(n):
        angle = 2 * math.pi * i / n
        
        # Base ellipse with decorative modulation
        # Add bumps/scallops around the perimeter
        # More bumps on top/bottom (along y), fewer on sides
        bump_freq = 8
        bump_amp_x = 6
        bump_amp_y = 4
        
        # Phase offset to align bumps nicely
        phase_x = math.pi / 2
        
        bump = bump_amp_x * math.cos(angle) * math.cos(bump_freq * angle + phase_x) + \
               bump_amp_y * math.sin(angle) * math.cos(bump_freq * angle)
        
        r_out = 1.0 + bump / (a_out)
        r_in = 1.0 + bump * 0.7 / (a_in)
        
        x_out = a_out * r_out * math.cos(angle)
        y_out = b_out * r_out * math.sin(angle)
        
        x_in = a_in * r_in * math.cos(angle)
        y_in = b_in * r_in * math.sin(angle)
        
        pts_outer.append((x_out, y_out))
        pts_inner.append((x_in, y_in))
    
    return pts_outer, pts_inner

# Build using a different approach - extrude an ellipse ring with decorative shape
# Use spline to create the decorative outline

def build_frame():
    # Create outer profile points
    outer_pts = []
    inner_pts = []
    
    a_out = 80
    b_out = 52
    a_in = 68
    b_in = 40
    
    n = 80
    
    for i in range(n + 1):
        angle = 2 * math.pi * i / n
        
        # Decorative scallop modulation
        scallop = 1 + 0.06 * math.cos(8 * angle) + 0.03 * math.cos(4 * angle)
        
        x_out = a_out * scallop * math.cos(angle)
        y_out = b_out * scallop * math.sin(angle)
        
        x_in = a_in * scallop * math.cos(angle)
        y_in = b_in * scallop * math.sin(angle)
        
        outer_pts.append((x_out, y_out))
        inner_pts.append((x_in, y_in))
    
    return outer_pts, inner_pts

outer_pts, inner_pts = build_frame()

# Create outer shape
outer_wire = (
    cq.Workplane("XY")
    .spline(outer_pts)
    .close()
)

outer_face = outer_wire.extrude(8)

# Create inner cutout
inner_wire = (
    cq.Workplane("XY")
    .spline(inner_pts)
    .close()
)

inner_solid = inner_wire.extrude(8)

# Subtract inner from outer to get frame
result = outer_face.cut(inner_solid)