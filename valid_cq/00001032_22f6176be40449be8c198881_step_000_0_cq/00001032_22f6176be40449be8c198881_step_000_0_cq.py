import cadquery as cq
import math

# The image depicts a mathematical surface, likely an immersion of the real projective plane
# known as "Boy's Surface" or a variation of a "Cross-Cap" or a specific parameterization of a torus-like 
# self-intersecting surface. However, looking closely at the curves, it strongly resembles
# the "Apple Surface" or a specific cyclide, but the most distinctive feature is the 
# self-intersection that looks like the "Jeener's Klein Surface" or a variation of a Klein bottle.

# Given the specific rounded lobe shape and the central pinch point, this appears to be a 
# "Roman Surface" or more likely a parametric "Cross Cap" or "Klein Bottle" representation 
# that has been thickened into a solid. 

# However, reproducing exact topological manifolds in CSG (Constructive Solid Geometry) 
# like CadQuery is extremely difficult as they are surface models, not solids.
# Instead, looking at the image as a mechanical part, it resembles a specific type of 
# toroidal shape or a revolve operation with a twist.

# Let's approximate this shape using a parametric surface generation approach
# or a carefully crafted Revolve/Sweep. The most straightforward mechanical interpretation
# that yields this specific visual is a "Self-Intersecting Torus" or a "Spindle Torus"
# where the inner radius is smaller than the tube radius, creating a "lemon" or "apple" shape inside.
# But the image has an asymmetry.

# A more accurate visual match for this specific render (often found in differential geometry catalogs) 
# is the "Cross-Cap" or a specific view of the "Klein Bottle".
# Since CadQuery works best with solids, let's create a parametric surface
# that mimics this topology using a `makeSplineApprox` or custom parametric face approach.

# Let's try to model it as a parametric surface. The specific shape looks very much like 
# the "Apple Surface" (a subset of Torus) or a "Cross-cap".
# Let's generate a parametric solid based on a toroidal coordinate system
# but distorted to match the visual.

# A robust way to create this organic shape in CadQuery is using a parametric function
# to define a face and then thickening it, or constructing it from splines.
# Given the limitations of pure CSG, let's build it as a "Apple" torus (Self-intersecting torus)
# which is visually very close.

def make_toroidal_apple(r_major, r_minor):
    """
    Creates a spindle torus (apple shape) where the minor radius is greater than the major radius.
    """
    # Create the profile: a circle centered at (r_major, 0, 0) with radius r_minor
    # We revolve this around the Z axis.
    
    # Since r_minor > r_major, the circle crosses the Z axis, creating the "dimple"
    # and the internal "lemon" shape.
    
    # CadQuery's revolve might complain about self-intersection if we do a full solid revolve
    # of a crossing profile.
    # So we construct it carefully.
    
    # Let's construct a wire for the circle
    # Center of tube is at x=r_major
    center = (r_major, 0, 0)
    
    # We need a Workplane to draw the circle on the XZ plane (which is the profile plane for a Z-axis revolve)
    # The default revolve uses the Y axis on the XY plane or similar.
    # Let's use standard CQ approach: Draw on XZ, revolve around Z.
    
    res = (
        cq.Workplane("XZ")
        .moveTo(r_major, 0)
        .circle(r_minor)
        .revolve(360, (0,0,0), (0,1,0)) # Revolve around Z (which is Y in the local XZ plane coordinate system? No.)
    )
    # In "XZ" plane: x is global X, y is global Z.
    # To revolve around global Z, we revolve around the local Y axis of the XZ plane.
    
    return res

# Dimensions
# Judging by the image, it's a "fat" torus where the hole has closed up completely and inverted.
# This happens when the Tube Radius > Major Radius.
# Major Radius (R): Distance from center to center of tube.
# Minor Radius (r): Radius of the tube.
# If r > R, it creates the dimpled apple shape.

R = 10.0  # Major radius
r = 15.0  # Minor radius (must be > R for the apple shape)

# However, the standard CadQuery `revolve` operation often validates for non-self-intersecting solids.
# A self-intersecting revolve often fails in the underlying OCCT kernel or produces a shape with internal voids.
# The image shows a perfect surface.
# Let's try a parametric surface approach using `makeSplineApprox` or building a shell if the simple revolve fails logic.

# Actually, the image looks remarkably like a Cross-Cap. 
# But let's look closer. It has a hole-like depression but no visible hole through it. 
# It has a continuous rim.
# This is characteristic of a standard torus where R < r.

# Let's try the direct revolve first. If that creates an invalid solid, we need a different strategy.
# Most CAD kernels handle spindle tori as valid solids (the union of the volume).

try:
    # Attempt simple revolve
    result = (
        cq.Workplane("XZ")
        .moveTo(R, 0)
        .circle(r)
        .revolve(360, (0,0,0), (0,1,0))
    )
except Exception:
    # If the kernel rejects the self-intersection, we model the outer shell.
    # The outer shell of a spindle torus is the union of the surface.
    # We can approximate this by revolving a half-arc that starts at the axis.
    
    # Calculate intersection of circle with Z axis.
    # Circle eq: (x - R)^2 + z^2 = r^2
    # At x=0: R^2 + z^2 = r^2 => z = +/- sqrt(r^2 - R^2)
    
    h_intersect = math.sqrt(r**2 - R**2)
    
    # We define an arc for the outer profile from (0, -h) to (x_max, 0) to (0, h)
    # The outer profile is the part of the circle where x >= 0.
    
    def get_x(z):
        # x = R + sqrt(r^2 - z^2)  (right side of tube)
        # x = R - sqrt(r^2 - z^2)  (left side, likely negative)
        # We want the max x profile.
        return R + math.sqrt(r**2 - z**2)
    
    # Actually, simpler: define 3 points for arc
    p_top = (0, h_intersect)
    p_side = (R + r, 0)
    p_bot = (0, -h_intersect)
    
    # But a simple 3-point arc won't match the circular curvature exactly.
    # We need the arc of the circle centered at (R,0) with radius r.
    # We only revolve the portion where x > 0.
    
    result = (
        cq.Workplane("XZ")
        .moveTo(0, -h_intersect)
        .radiusArc((0, h_intersect), -r) # Negative radius implies specific arc direction
        .close() # Close back to the Z axis
        .revolve(360, (0,0,0), (0,1,0))
    )

# The result variable is now defined. 
# To make it look exactly like the image (smooth shading),
# this Spindle Torus is the correct mathematical object.