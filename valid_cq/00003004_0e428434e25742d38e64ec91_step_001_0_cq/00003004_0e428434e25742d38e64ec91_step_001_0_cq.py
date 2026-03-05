import cadquery as cq

# --- Parameter Definitions ---
base_diameter = 20.0
base_height = 10.0

# The top is a spherical cap. 
# We can model this as a chamfer on a cylinder or as a sphere intersected/union with a cylinder.
# Looking at the image, it looks like a large chamfer or fillet. 
# Or more likely, a cylinder topped with a sphere, but the sphere diameter matches the cylinder.
# However, the transition point looks sharpish/tangent, suggesting a fillet or a dome.
# Let's check the profile: straight vertical sides, then curving inwards to a flat or rounded top.
# The top looks like a spherical dome, typical of a cap nut or a rivet head.
# Let's model it as a cylinder + a sphere, or a revolved profile.

# Method: Revolve a profile.
# It looks like a cylinder with a radius fillet on top, or a full hemispherical cap.
# Given the "shoulder" where the curve starts, it's not a full hemisphere starting from the base.
# It looks like a cylindrical section followed by a domed section.

total_height = 18.0
dome_height = total_height - base_height

# --- Geometry Construction ---

# Let's try a simple constructive solid geometry approach first:
# 1. Create a base cylinder.
# 2. Create a sphere for the top.
# 3. Intersect/Union appropriately or just use a fillet if the dome is small.

# Looking closely at the image:
# The transition from the cylindrical side to the top surface is not a simple fillet on a flat top.
# The top surface is fully curved.
# It looks like a "torispherical head" or just a cylinder topped with a spherical cap.
# The sphere's radius must be calculated such that it sits on the cylinder correctly.
# If the dome height is less than the radius (which it usually is for shallow domes), 
# we need to calculate the radius of the sphere based on the chord length (cylinder diameter) and the sagitta (dome height).

# Formula for radius R given chord c (diameter) and height h:
# R = (c^2 / 8h) + (h / 2)
c = base_diameter
h = dome_height # Let's assume the dome height is the remainder.

# If we assume standard proportions, let's just make parametric variables.
dome_radius = (c**2 / (8 * h)) + (h / 2)

# Alternative interpretation:
# It could just be a cylinder with a very large fillet on the top edge.
# If the fillet radius = base_diameter / 2, it becomes a full hemisphere.
# In the image, the top looks slightly flatter than a perfect hemisphere, 
# or the vertical walls are quite high relative to the diameter.

# Let's proceed with the Cylinder + Sphere Cap approach as it's the most robust way to make this shape.
# We create a cylinder, then cut a sphere or union a sphere.
# Wait, looking at the shading, it looks like a single solid piece.
# Let's create a profile and revolve it. It's cleaner.

def create_dome_pin():
    # Points for the profile
    # (0,0) -> (radius, 0) -> (radius, base_height) -> ... curve ... -> (0, total_height)
    
    radius = base_diameter / 2.0
    
    # We will construct this by:
    # 1. Extruding the base cylinder.
    # 2. Intersecting a sphere with a box to get the cap, then translating it?
    # No, simpler: Union a cylinder and a sphere section.
    
    # Solid 1: The Cylinder Base
    cyl = cq.Workplane("XY").circle(radius).extrude(base_height)
    
    # Solid 2: The Dome
    # We need a sphere that intersects the top circle of the cylinder.
    # The center of this sphere will be on the Z axis.
    # We need to determine the Z-height of the sphere center and its radius.
    # Let's assume the top is a spherical cap defined by a specific radius of curvature.
    # Often such parts have a radius approx equal to the diameter (1D bend) or similar.
    # Let's guess the radius of curvature is slightly larger than the cylinder radius (making it flatter than a hemisphere).
    
    # Parametric guess based on visual proportions:
    curvature_radius = base_diameter * 0.8  # slightly flatter than hemisphere (0.5 would be hemisphere)
    
    # Calculate the vertical offset (sagitta) of a sphere of this radius at the cylinder's width
    import math
    # R^2 = x^2 + (z - center_z)^2
    # At the edge: curvature_radius^2 = radius^2 + vertical_distance_from_center^2
    vertical_dist = math.sqrt(curvature_radius**2 - radius**2)
    
    # We want the sphere to touch the edge of the cylinder at (radius, base_height).
    # So the center of the sphere is at Z = base_height - vertical_dist
    sphere_center_z = base_height - vertical_dist
    
    # Create the sphere
    sphere = (
        cq.Workplane("XY")
        .workplane(offset=sphere_center_z)
        .sphere(curvature_radius)
    )
    
    # The final shape is the intersection of the sphere and the "infinite" upward extension of the cylinder?
    # Or just the union of the cylinder and the sphere, but the sphere bulges out at the sides if not careful.
    # If curvature_radius > radius (which it is), the sphere bulges WIDER than the cylinder below the intersection plane.
    # We need to cut the sides of the sphere to match the cylinder.
    
    # Let's combine:
    # 1. Create a Cylinder of full height to serve as the boundary.
    # 2. Create the Sphere positioned correctly.
    # 3. Intersect them.
    
    # Refined approach:
    # 1. Create a cylinder of radius R and height `base_height`.
    # 2. Create the cap.
    
    # Actually, looking at the image again:
    # The transition is sharp? No, it looks tangent continuous (G1).
    # If it is tangent continuous, the center of the sphere MUST lie on the plane of the top of the cylinder section? No.
    # If it's tangent, the sphere center is at the same Z level as the transition if the radius = cylinder radius.
    # If the radius is larger, the center is below.
    # If the transition shows a "crease" (sharp edge), it's just a cylinder and a sphere unioned.
    # The image shows a subtle line, suggesting a slight discontinuity in curvature or just the tessellation.
    # However, the silhouette is very smooth.
    # Let's assume it's a "button head" style shape.
    
    # Simplest valid code that produces this visual:
    # Cylinder + Fillet on top edge.
    # If the fillet radius is large, it creates a dome.
    # Let's try the fillet approach first as it's very "CadQuery" idiomatic.
    
    c = cq.Workplane("XY").circle(base_diameter/2).extrude(total_height)
    
    # We want to fillet the top edge.
    # To get a domed look that isn't a full hemisphere, we need a radius < base_diameter/2.
    # But if we want the top to be completely curved (no flat spot in the middle), 
    # we physically cannot do that with a standard constant-radius fillet unless it's a full hemisphere.
    # The image clearly has no flat spot on top. It is fully curved.
    
    # Therefore, this is a REVOLVED profile of an arc and a line.
    
    # Arc properties:
    # Starts at (radius, base_height)
    # Ends at (0, total_height)
    # Center must lie on Z-axis to be a surface of revolution.
    
    # Let's calculate the specific arc that passes through (r, h_base) and (0, h_total).
    p1 = (radius, base_height)
    p2 = (0, total_height)
    
    # We need an arc passing through p1 and p2, with the center on the Y-axis (which becomes Z in 3D).
    # Equation of circle: x^2 + (y-cy)^2 = R^2
    # Pass through (0, h_total): 0 + (h_total - cy)^2 = R^2  => R = |h_total - cy|
    # Pass through (r, h_base): r^2 + (h_base - cy)^2 = R^2
    
    # Substitute R:
    # r^2 + (h_base - cy)^2 = (h_total - cy)^2
    # r^2 + h_base^2 - 2*h_base*cy + cy^2 = h_total^2 - 2*h_total*cy + cy^2
    # r^2 + h_base^2 - h_total^2 = 2*cy*(h_base - h_total)
    # cy = (r^2 + h_base^2 - h_total^2) / (2 * (h_base - h_total))
    
    r = radius
    y1 = base_height
    y2 = total_height
    
    cy = (r**2 + y1**2 - y2**2) / (2 * (y1 - y2))
    R_arc = abs(y2 - cy)
    
    # Now we have the geometry.
    # Let's build the profile.
    
    res = (
        cq.Workplane("XZ")
        .lineTo(radius, 0)
        .lineTo(radius, base_height)
        .radiusArc((0, total_height), -R_arc) # Negative radius often indicates 'long' or 'short' way, or convexity. 
                                              # For radiusArc, we need a point and a radius. 
                                              # Direction is tricky.
        # Alternative: threePointArc
        # We know start (radius, base_height) and end (0, total_height).
        # We need a midpoint.
        # But CadQuery's 3-point arc is easiest.
        # Or even better: use the geometric construction variables we just calculated.
    )
    
    # Using the center point approach is clearer with primitives, but let's stick to sketching for precision.
    # Actually, simpler approach using primitives:
    # 1. Cylinder(h=base_height, r=radius)
    # 2. Sphere(r=R_arc) positioned at (0,0, cy)
    # 3. Intersect the sphere with a cylinder of infinite height (or just large height) to trim the sides?
    #    No, because the sphere center `cy` is calculated such that the sphere passes exactly through the corner edge.
    #    So we just need the intersection of [Sphere at cy] and [Cylinder of same radius].
    #    Wait, the sphere is usually wider than the cylinder (lower curvature).
    #    So: Intersection(Sphere, Cylinder).
    
    sphere_center = (0, 0, cy)
    sphere_radius = R_arc
    
    # 1. The base cylinder part (extending down)
    # We can model the whole thing as Intersection(Sphere, Cylinder) IF the sphere covers the bottom.
    # But the bottom is flat.
    
    # Final Plan:
    # Create Cylinder(r=radius, h=total_height)
    # Create Sphere(r=R_arc) at (0,0,cy)
    # Intersect them? 
    # If we intersect, we get the sphere cap on top, but the bottom of the sphere is curved. We want a flat bottom.
    
    # Final Final Plan:
    # 1. Create Cylinder(r=radius, h=base_height).
    # 2. Create the Sphere Cap.
    #    The Sphere Cap is: Sphere(R_arc) at (0,0,cy).
    #    We need to cut off everything below Z=base_height from this sphere.
    # 3. Union them.
    
    # Let's generate the code.
    
    cylinder_part = cq.Workplane("XY").circle(radius).extrude(base_height)
    
    # Create the sphere
    # Note: CadQuery primitives are centered.
    sphere_part = cq.Workplane("XY").workplane(offset=cy).sphere(sphere_radius)
    
    # Cut the bottom of the sphere off.
    # We can do this by intersecting with a box or cylinder that starts at base_height and goes up.
    cutter = cq.Workplane("XY").workplane(offset=base_height).circle(radius).extrude(total_height) 
    
    # Actually, if we just intersect the Sphere with a cylinder of radius `radius`, 
    # we get the "bullet" shape, but the bottom is rounded.
    # We need the bottom flat.
    
    # Robust method: Revolve. It handles all this logic in one operation.
    # Profile: (0,0) -> (r,0) -> (r, h_base) -> arc -> (0, h_total) -> close
    
    # Let's recalculate the midpoint for threePointArc to ensure it works flawlessly without complex math in the query.
    # Actually, `radiusArc` with a radius is supported.
    
    result_obj = (
        cq.Workplane("XY")
        .moveTo(0, 0)
        .lineTo(radius, 0)
        .lineTo(radius, base_height)
        .radiusArc((0, total_height), R_arc) # Note: curvature needs to be checked.
        .lineTo(0,0)
        .close()
        .revolve()
    )
    
    return result_obj

# Execute
result = create_dome_pin()