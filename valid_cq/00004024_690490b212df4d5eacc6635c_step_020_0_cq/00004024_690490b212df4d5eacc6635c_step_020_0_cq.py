import cadquery as cq

# --- Parameters ---
# Central Hub dimensions
hub_diameter = 20.0
hub_thickness = 12.0
hub_fillet_radius = 4.0  # Controls the roundness of the hub edge

# Blade dimensions
num_blades = 5
blade_root_radius = hub_diameter / 2.0 - 1.0  # Slightly embedded
blade_tip_radius = 22.0
blade_thickness = 2.0
blade_angle_width = 30.0  # Angular width of the blade at the tip (approx)

# --- Modeling ---

# 1. Create the Central Hub
# We start with a cylinder and fillet the edges to get that rounded look.
hub = cq.Workplane("XY").circle(hub_diameter / 2.0).extrude(hub_thickness)

# Fillet the top and bottom edges to make it rounded like a pebble/oblate spheroid
hub = hub.edges("not |Z").fillet(hub_fillet_radius)


# 2. Create a Single Blade
# We'll create a profile on the side and revolve/extrude it, or more simply,
# extrude a shape and intersect/cut to shape.
# Let's try creating a blade cross-section from the top view (XY plane) and extruding it.

# Define the blade shape using a polar-like construction or points.
# The blade looks like a section of an annulus or a wedge.
# Let's define it on the XY plane.

def create_blade():
    # Helper to create a wedge shape for the blade
    # We create a shape that flares out
    
    # Points for a single blade polygon
    # Inner width at root
    w_inner = 3.0
    # Outer width at tip
    w_outer = 8.0 
    
    # We'll draw it laying flat then rotate/position it
    # But better yet, draw it in position relative to origin.
    
    # Let's draw the blade profile on the YZ plane (side view) and extrude along X?
    # No, the blades radiate.
    
    # Let's make a generic blade shape first.
    # It looks somewhat trapezoidal or like a sector.
    
    # Let's draw on XY plane centered at origin, then move it out.
    # Actually, the blades look twisted or just straight radial fins. They look straight in the image.
    
    # Points for the blade profile (viewed from front face of hub)
    # It's essentially a rectangle that gets wider or follows a sector.
    
    # Let's define the blade on the XZ plane, assuming the hub axis is Z.
    # But wait, looking at the image, the hub axis seems to be pointing towards us-ish.
    # If the hub is a cylinder along Z.
    
    # Let's use the current hub orientation (Z is axis).
    
    # Create a box and cut it? Or sketch a polygon?
    # The blade profile viewed from the top (looking down Z) is a rectangle (thickness).
    # The blade profile viewed from the side (looking at the blade face) is the wedge shape.
    
    # Let's construct a workplane on the XZ plane to draw the blade outline.
    blade_shape = (
        cq.Workplane("XZ")
        .workplane(offset=0) # Centered
        .moveTo(blade_root_radius, -hub_thickness/2 + 2) # Start near bottom of hub, slightly inset
        .lineTo(blade_tip_radius, -hub_thickness/2 )     # Bottom tip corner
        .lineTo(blade_tip_radius + 2, hub_thickness/2 + 2)       # Top tip corner (flaring out)
        .lineTo(blade_root_radius, hub_thickness/2 )     # Top root corner
        .close()
        .extrude(blade_thickness/2.0, both=True) # Extrude symmetrically to get thickness
    )
    
    # The simple polygon above might not capture the curve perfectly.
    # Let's refine the points to match the image better.
    # The image shows blades that are wider at the tip than the root? 
    # Actually, looking closely, they look fairly rectangular but angled.
    # Let's try a simpler approach: A box that is moved and rotated.
    
    # Re-evaluating blade shape from image:
    # They look like flat plates. The outer edge is curved (arc).
    # The side edges are straight radius lines.
    
    # Let's draw the outline on the flat face (XY) and extrude? No, they stand up.
    
    # Let's draw a wedge shape on the XY plane and extrude it in Z.
    # Then rotate it 90 degrees to stand up? No.
    
    # Best approach for radial blades:
    # 1. Create a workplane rotated to the correct angle around Z.
    # 2. Draw the side profile of the blade (radius vs Z-height).
    # 3. Extrude the thickness.
    
    # Side profile points (r, z):
    # (r_min, z_bot), (r_max, z_bot_outer), (r_max, z_top_outer), (r_min, z_top)
    
    r_min = hub_diameter / 2.0 - 2.0 # Embed inside hub
    r_max = 28.0
    
    # The blade seems to flare outward slightly or is just a sector.
    # The outer edge looks like an arc in the image.
    
    # Let's construct one blade.
    blade = (
        cq.Workplane("XY")
        .workplane(offset=0)
        .center(0, 0)
        # We will create a block and then cut it to shape or sketch the shape directly
        # Let's sketch on a plane perpendicular to the radial vector.
        # It's easier to just make a box and intersect it with a cylinder/cone, 
        # but the blade shape is specific.
        
        # Let's go with the sketch-on-rotated-plane approach.
        # But CadQuery handles this easily by rotating the result.
        
        # Draw on XZ plane (Side view)
        .transformed(rotate=(90, 0, 0)) # Rotate to draw on XZ plane effectively
    )
    
    # Define points for the blade side profile (Trapezoid with curved top?)
    # Based on image:
    # Root is attached to hub. Tip is further out.
    # The "top" and "bottom" edges (in Z direction of hub) seem slightly angled or curved.
    # The outer edge is an arc centered at origin.
    
    pts = [
        (r_min, -hub_thickness/3.0),   # Bottom inner
        (r_max, -hub_thickness/2.0 - 2), # Bottom outer (flares down)
        (r_max, hub_thickness/2.0 + 2),  # Top outer (flares up)
        (r_min, hub_thickness/3.0)     # Top inner
    ]
    
    # Actually, simpler:
    # It looks like a segment of a disk.
    
    # Let's try creating a solid block and cutting it.
    w = cq.Workplane("XY").box(r_max*2, blade_thickness, hub_thickness * 1.5)
    
    # Shift it to be a radial fin
    w = w.translate((r_max, 0, 0))
    
    # Now we need to shape it. 
    # The outer edge is circular (cylinder cut).
    # The inner edge is circular (cylinder cut, handled by hub overlap).
    # The top and bottom edges?
    
    # Let's try sketching the profile on the "flat" face of the blade.
    # The blade is thin in Y.
    # We draw on XZ plane.
    
    sk = (
        cq.Workplane("XZ")
        .moveTo(r_min, -3.0) # Inner bottom
        .lineTo(r_max, -8.0) # Outer bottom
        .lineTo(r_max, 8.0)  # Outer top
        .lineTo(r_min, 3.0)  # Inner top
        .close()
        .extrude(blade_thickness/2.0, both=True)
    )
    
    # Now intersect with a large cylinder to round the outer edge
    outer_limit = cq.Workplane("XY").circle(r_max).extrude(20, both=True)
    blade_final = sk.intersect(outer_limit)
    
    return blade_final

# 3. Create all blades and unite with hub
blades = cq.Workplane("XY")

# Parameters for the blade profile
r_inner = hub_diameter / 2.0 - 1.5
r_outer = 22.0
z_height_hub = hub_thickness
blade_thick = 2.5

# We construct a single blade geometry that is aligned with the X axis
# Profile viewed from the side (XZ plane)
# It flares out a bit like a bowtie or a fan blade
p1 = (r_inner, -3.0)
p2 = (r_outer, -7.0) # Tip is wider in Z
p3 = (r_outer, 7.0)
p4 = (r_inner, 3.0)

one_blade = (
    cq.Workplane("XZ")
    .moveTo(*p1)
    .lineTo(*p2)
    # Create an arc for the outer edge? Or straight? 
    # Image looks like the outer edge follows a cylinder curvature approx.
    # Straight line in profile means a cylinder in 3D when swept? No.
    # A straight line here means a flat edge. 
    # To get the rounded outer contour seen in the image, we intersect with a cylinder later 
    # OR we use a 3-point arc here if this represents the physical edge.
    # However, this is a 2D profile extruding in Y.
    # The outer edge of the generated solid will be flat.
    # The image shows the outer silhouette is curved.
    # Let's use an arc for the outer edge in the profile.
    .threePointArc((r_outer + 1.5, 0), p3) # Slight bulge outward
    .lineTo(*p4)
    .close()
    .extrude(blade_thick / 2.0, both=True) # Extrude symmetric to create thickness
)

# Rotate blades into position and fuse
for i in range(num_blades):
    angle = i * (360.0 / num_blades)
    # Rotate the blade around Z axis
    rotated_blade = one_blade.rotate((0,0,0), (0,0,1), angle)
    hub = hub.union(rotated_blade)

# 4. Final details
# The image shows a small chamfer or fillet at the blade roots?
# It's hard to see, but a boolean union usually leaves a sharp edge.
# We can add a small fillet if desired, but it might be computationally expensive or fail.
# Let's keep it clean.

result = hub
