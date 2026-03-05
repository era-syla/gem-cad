import cadquery as cq

# Parametric dimensions
dome_radius = 10.0      # Radius of the hemispherical top
cylinder_length = 15.0  # Length of the middle cylindrical section
base_radius = 12.0      # Radius of the base flange
base_thickness = 5.0    # Thickness of the base flange

# 1. Create the hemispherical dome
# We create a sphere and then will cut it or unite it. 
# Alternatively, we can revolve a profile. Let's build up from primitives.
# A sphere at the origin.
dome = cq.Workplane("XY").sphere(dome_radius)

# We need a hemisphere. A simple way is to cut the sphere in half.
# The sphere is centered at (0,0,0). Let's cut off the bottom half (Z < 0).
# But looking at the orientation, let's align the axis along Z.
# Let's start with the base and work up, or create separate parts and union them.

# Method: Stack cylinders and a sphere, then union.
# Center of the dome will be at Z = cylinder_length + base_thickness
# But the dome is a hemisphere, so its base is at that Z height.

# Let's define the parts based on a common axis (Z-axis).

# Base Flange
# Cylinder starting at Z=0, height=base_thickness
base = cq.Workplane("XY").circle(base_radius).extrude(base_thickness)

# Middle Cylinder
# Cylinder starting at top of base, height=cylinder_length
# We create a new workplane on the top face of the base
middle_cylinder = base.faces(">Z").workplane().circle(dome_radius).extrude(cylinder_length)

# Dome
# The dome sits on top of the middle cylinder.
# We can create a sphere centered at the top face of the middle cylinder
# and then intersect it with a box or just rely on the union if the sphere is positioned correctly.
# If we position a sphere of radius R at center (0,0, Z_top), the bottom half of the sphere overlaps
# the cylinder. We want a hemisphere *on top*.
# So the center of the sphere should be at Z_top.
# But we only want the top half.
# An easier way to make a perfect dome on a cylinder in CadQuery is to revolve a profile or 
# create a sphere and cut it.

# Let's try the revolve approach for the whole shape, or just the tip.
# Actually, constructing with primitives is often robust.

# Let's create the full sphere centered at the top of the cylinder.
# Current Z height = base_thickness + cylinder_length
total_cylinder_height = base_thickness + cylinder_length
sphere_center = (0, 0, total_cylinder_height)

# Create a full sphere
full_sphere = cq.Workplane("XY").center(0, 0).workplane(offset=total_cylinder_height).sphere(dome_radius)

# We need to cut the bottom half of the sphere so it doesn't protrude inside the cylinder 
# (though visually it doesn't matter for a solid union, it's cleaner).
# Actually, simply unioning the sphere centered at the end of the cylinder results in a dome 
# cap + an internal overlap. Since we want a single solid, union is fine.
# The sphere's bottom hemisphere will be inside the cylinder of the same radius. 
# This works perfectly.

# Combine the parts
result = middle_cylinder.union(full_sphere)

# Alternative Approach (Revolve):
# This creates a very clean geometry without internal faces.
# Profile:
# 1. Start at (0, 0)
# 2. Line to (base_radius, 0)
# 3. Line up to (base_radius, base_thickness)
# 4. Line left to (dome_radius, base_thickness)
# 5. Line up to (dome_radius, base_thickness + cylinder_length)
# 6. Arc to (0, base_thickness + cylinder_length + dome_radius)
# 7. Close back to (0,0)

pts = [
    (0, 0),
    (base_radius, 0),
    (base_radius, base_thickness),
    (dome_radius, base_thickness),
    (dome_radius, base_thickness + cylinder_length)
]

# Create the profile and revolve it
# The arc needs to go from the last point to the tip.
# The tip is at (0, base_thickness + cylinder_length + dome_radius)
# The center of the arc is (0, base_thickness + cylinder_length)

result = (cq.Workplane("XZ")
          .polyline(pts)
          .threePointArc(
              (dome_radius * 0.7071, base_thickness + cylinder_length + dome_radius * 0.7071), # Approximate point on arc
              (0, base_thickness + cylinder_length + dome_radius) # End point
          ) 
          # Actually, threePointArc is tricky with exact geometric constraints. 
          # radiusArc is better if we know the radius.
          # Or simply building the solid with primitives as planned first is safer for "exact" simple shapes.
          )

# Let's stick to the primitive construction which is less prone to arc calculation errors.
# Re-implementing the primitive stack cleanly:

# 1. Base Cylinder
base = cq.Workplane("XY").circle(base_radius).extrude(base_thickness)

# 2. Main Body Cylinder (on top of base)
body = base.faces(">Z").workplane().circle(dome_radius).extrude(cylinder_length)

# 3. Dome (Sphere centered at the top of the body)
# We use a sphere centered at the top face.
# Because the body cylinder has radius = dome_radius, the sphere matches perfectly.
# The bottom half of the sphere is buried inside the body, which is fine for a union.
dome = body.faces(">Z").workplane().sphere(dome_radius)

# Combine everything
result = body.union(dome)

# Export or visualization would happen here, but only the code is requested.