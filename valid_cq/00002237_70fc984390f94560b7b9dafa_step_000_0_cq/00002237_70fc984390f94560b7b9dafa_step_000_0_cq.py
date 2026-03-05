import cadquery as cq

# Parametric definitions
center_sphere_radius = 10.0
center_sphere_height_ratio = 0.6  # How much of the sphere is visible (0.5 for hemisphere)

inner_ring_radius = 18.0
inner_ring_thickness = 1.0
inner_ring_height = 10.0
inner_ring_curvature_radius = 15.0 # Radius for the profile arc

outer_ring_radius = 35.0
outer_ring_thickness = 1.0
outer_ring_height = 12.0
outer_ring_curvature_radius = 40.0 # Radius for the profile arc

# 1. Create the central spherical cap
# We create a sphere and cut the bottom part
center_cap = (
    cq.Workplane("XY")
    .sphere(center_sphere_radius)
    .cut(
        cq.Workplane("XY")
        .rect(center_sphere_radius * 3, center_sphere_radius * 3)
        .extrude(-center_sphere_radius) # Cut below the XY plane
    )
)

# 2. Create the inner curved ring
# We will revolve a profile. The profile is an arc.
# The band seems to curve inward at the top.
# Let's define points for an arc.
# Start point: (inner_ring_radius, 0)
# End point: (inner_ring_radius - curl_in, height)
# We can use a 3-point arc or a radius arc.

def create_curved_ring(base_radius, thickness, height, curvature_offset):
    """
    Creates a ring that curves inwards/outwards using a revolve operation.
    base_radius: The radius at the base (z=0)
    thickness: Wall thickness
    height: Z height of the ring
    curvature_offset: How much the top radius differs from base radius (negative for inward curve)
    """
    
    # Define the outer profile
    # Point 1: Base outer edge
    p1 = (base_radius, 0)
    # Point 2: Top outer edge (curved in)
    p2 = (base_radius + curvature_offset, height)
    # Point 3: Midpoint control for the arc to give it some belly
    # A simple way is to define a midpoint that bulges out slightly
    p_mid = (base_radius + (curvature_offset/2) + 2.0, height/2)
    
    ring = (
        cq.Workplane("XZ")
        .moveTo(p1[0], p1[1])
        .threePointArc(p_mid, p2) # Outer curve
        .lineTo(p2[0] - thickness, p2[1]) # Top edge
        # Inner curve (approximate parallel)
        .threePointArc(
            (p_mid[0] - thickness, p_mid[1]), 
            (p1[0] - thickness, p1[1])
        )
        .close()
        .revolve()
    )
    return ring

# Creating the inner ring
# Looking at the image, the inner ring bulges outward like a slice of a sphere.
# So the radius at Z=0 and Z=top are smaller than the radius at Z=middle.
# Let's use a sphere slice approach for perfect spherical curvature which matches the image style better.

def create_spherical_band(sphere_radius, thickness, cut_z_bottom, cut_z_top):
    """
    Creates a band by intersecting two concentric spheres and slicing top/bottom.
    """
    outer_sphere = cq.Workplane("XY").sphere(sphere_radius)
    inner_sphere = cq.Workplane("XY").sphere(sphere_radius - thickness)
    hollow_sphere = outer_sphere.cut(inner_sphere)
    
    # Create a bounding box to keep only the slice we want
    # We want to keep between z=cut_z_bottom and z=cut_z_top
    # We do this by cutting away what we don't want
    
    # Cut top
    cut_top = (
        cq.Workplane("XY")
        .workplane(offset=cut_z_top)
        .rect(sphere_radius*3, sphere_radius*3)
        .extrude(sphere_radius * 2)
    )
    
    # Cut bottom
    cut_bottom = (
        cq.Workplane("XY")
        .workplane(offset=cut_z_bottom)
        .rect(sphere_radius*3, sphere_radius*3)
        .extrude(-sphere_radius * 2)
    )
    
    band = hollow_sphere.cut(cut_top).cut(cut_bottom)
    return band

# Adjusting parameters to visually match the image
# Inner ring looks like a slice of a sphere sitting on the ground
inner_band_radius_sphere = 20.0
inner_band = create_spherical_band(
    sphere_radius=inner_band_radius_sphere, 
    thickness=0.5, 
    cut_z_bottom=0, # Start at "ground"
    cut_z_top=12.0
)
# Move it so the bottom of the spherical slice sits at Z=0 if needed, 
# but slicing relative to center usually leaves it floating or centered.
# The sphere center is at (0,0,0). Slicing from 0 to 12 means it's the upper hemisphere slice.
# The image shows the rings sitting on a plane. The sphere cut keeps Z>0 parts.
# The previous logic works.

# Outer ring
# It looks taller and wider, also a spherical slice but less curved (larger radius sphere)
outer_band_radius_sphere = 50.0
outer_band = create_spherical_band(
    sphere_radius=outer_band_radius_sphere,
    thickness=0.5,
    cut_z_bottom=0, # Start at "ground"
    cut_z_top=15.0 # Taller than inner ring
)

# Combine geometry
result = center_cap.union(inner_band).union(outer_band)