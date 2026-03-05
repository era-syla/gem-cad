import cadquery as cq

# Define parametric dimensions
# Main dimensions of the tire
outer_radius = 50.0  # Overall outer radius of the tire
inner_radius = 28.0  # Inner radius where the rim would sit
tire_width = 30.0    # Total width of the tire (axial direction)

# Profile control points
# We will define half of the cross-section profile and then mirror it, or revolve a full profile.
# Let's define the cross-section in the XZ plane (where Z is the axis of revolution).
# The profile needs to be offset from the Z-axis by the radius.

# Profile shape parameters
sidewall_curvature = 8.0 # Radius for the sidewall curve
tread_curvature = 20.0   # Radius for the main tread surface
bead_radius = 2.0        # Small radius at the very inner edge

# Calculation of key points for the profile
# We'll construct a sketch on the XZ plane.
# Center of the tire cross-section is roughly at (outer_radius + inner_radius)/2
section_center_r = (outer_radius + inner_radius) / 2
section_height_h = (outer_radius - inner_radius)

# Let's build the profile using a Workplane and geometric primitives
# We will draw the cross-section on the XZ plane. The Y axis will be the axis of revolution later.
# Wait, CadQuery's revolve typically revolves around the Z axis of the workplane? 
# Or we can specify an axis. Standard revolve is around Y axis for a sketch on XZ plane usually 
# if we think of standard lathe operations, but usually in CQ we draw on XZ and revolve around Z axis.

# Let's try drawing on the XZ plane. The X coordinate corresponds to the Radius. The Z coordinate corresponds to the Width.
# The revolution will be around the Z-axis of the global coordinate system (which is vertical in the image)? No, looking at the image, 
# if Z is up, the tire is standing up. 
# Let's stick to standard convention: Tire lies flat on XY plane initially, or stands up.
# Let's create the cross-section on the XZ plane and revolve around the Z-axis. This creates a tire lying flat.
# To match the image orientation (isometric view of a standing tire), we can rotate it at the end.

def create_tire_profile():
    # Helper variables for the profile shape
    # r is the radial distance from the center of the tire
    # w is the axial width (z-direction in the sketch plane)
    
    r_outer = outer_radius
    r_inner = inner_radius
    w_half = tire_width / 2.0
    
    # Points for the profile (counter-clockwise)
    # 1. Start at inner bead, positive width
    p1 = (r_inner, w_half * 0.7) 
    
    # 2. Outer edge of sidewall
    p2 = (r_inner + (r_outer-r_inner)*0.3, w_half)
    
    # 3. Shoulder
    p3 = (r_outer - (r_outer-r_inner)*0.1, w_half * 0.8)
    
    # 4. Center of tread (max radius)
    p4 = (r_outer, 0.0)
    
    # Mirror points for the bottom half
    p5 = (p3[0], -p3[1])
    p6 = (p2[0], -p2[1])
    p7 = (p1[0], -p1[1])
    
    # Inner straight line to close the loop
    # We might want a slight curve there too, but straight is fine for a generic tire bead area
    
    # Create the sketch
    s = (
        cq.Sketch()
        .segment(p1, p2)
        .segment(p2, p3)
        .segment(p3, p4)
        .segment(p4, p5)
        .segment(p5, p6)
        .segment(p6, p7)
        .segment(p7, p1)
        .assemble()
        .vertices()
        .fillet(3.0) # Apply fillets to smooth the transition between segments
    )
    return s

# A more precise way to get that specific "bulging" shape is using splines or arcs.
# Let's try a spline-based approach for a smoother, more organic tire look.

# Define points for the right half of the cross-section (positive X in sketch, representing width)
# We will draw on the XY plane: X is radial distance, Y is width. Revolve around Y axis? 
# Let's stick to X = Radius, Y = Width (axial).
# We want to revolve around the vertical axis (X=0).

# Points: (Radius, Width)
# Top-most point (Tread center): (outer_radius, 0)
# Side-wall bulge: (some_mid_radius, tire_width/2)
# Inner bead: (inner_radius, some_smaller_width)

pt_tread = (outer_radius, 0)
pt_shoulder = (outer_radius - 5, tire_width/2 - 2)
pt_sidewall = (inner_radius + (outer_radius-inner_radius)/2, tire_width/2)
pt_bead_top = (inner_radius, tire_width/2 * 0.6)
pt_bead_bottom = (inner_radius, -tire_width/2 * 0.6)
pt_sidewall_bottom = (inner_radius + (outer_radius-inner_radius)/2, -tire_width/2)
pt_shoulder_bottom = (outer_radius - 5, -tire_width/2 + 2)

# Create the solid
result = (
    cq.Workplane("XZ")  # Draw on XZ plane. X is radial, Z is axial.
    .moveTo(pt_bead_top[0], pt_bead_top[1])
    .spline(
        [pt_sidewall, pt_shoulder, pt_tread],
        includeCurrent=True,
        tangents=[(0, 1), (0, -1)] # Vertical tangent at sidewall, vertical at tread? No.
                                  # Tangent at tread should be vertical (0, -1) in (R, Z) coords to be flat at peak? 
                                  # Actually tangent at tread (max R) should be along Z axis (0, -1) or (0,1).
    )
    .spline(
        [pt_shoulder_bottom, pt_sidewall_bottom, pt_bead_bottom],
        includeCurrent=True,
        tangents=[(0, -1), (0, 1)] # Continue smoothness
    )
    .close() # Close back to start with a straight line for the inner rim face
    .revolve(360, (0,0,0), (0,1,0)) # Revolve around Z-axis of the Workplane (which is Global Z)
)

# Alternative simplified construction using geometric primitives which is often more robust
# Let's make a torus and cut the inside to make it look like a tire.
# The image shows a very smooth, continuous outer surface.
# Let's use a parametric cross-section approach which is cleaner.

def tire_cross_section(r_in, r_out, width):
    # R is horizontal, Z is vertical in the 2D profile view
    # Center of tire profile roughly at R = (r_in + r_out)/2, Z = 0
    
    r_mid = (r_in + r_out) / 2
    section_h = (r_out - r_in) / 2 # Half-height of section
    w_half = width / 2
    
    # Control points for a Spline representing the outer shell
    p0 = (r_in, w_half * 0.5)  # Bead start
    p1 = (r_in + section_h * 0.3, w_half) # Sidewall max width
    p2 = (r_out - section_h * 0.2, w_half * 0.8) # Shoulder
    p3 = (r_out, 0) # Tread center
    p4 = (r_out - section_h * 0.2, -w_half * 0.8)
    p5 = (r_in + section_h * 0.3, -w_half)
    p6 = (r_in, -w_half * 0.5) # Bead end
    
    return (
        cq.Workplane("XZ")
        .moveTo(*p0)
        .spline([p1, p2, p3, p4, p5, p6], includeCurrent=True)
        .close()
        .revolve(360, (0,0,0), (0,0,1))
    )

# Instantiate
result = tire_cross_section(inner_radius, outer_radius, tire_width)

# Optional: Add the concentric grooves seen on the sidewall in the image
# This adds a bit of detail to match the 'texture' implied by the lines
# We can do this by cutting small rings.
for r_groove in [32, 34, 36]:
    groove = (
        cq.Workplane("XZ")
        .moveTo(r_groove, 0)
        .circle(0.2) # Small cutting circle
        .revolve(360, (0,0,0), (0,0,1))
    )
    # We need to position this circle on the surface of the tire. 
    # This is complex with a spline surface. 
    # Instead, let's just create the main shape which is the primary request.
    pass

# The result variable is already set.