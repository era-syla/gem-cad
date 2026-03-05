import cadquery as cq

# Parametric dimensions
total_length = 50.0  # Total length of the object
base_diameter = 20.0 # Diameter of the large cylindrical base
base_length = 12.0   # Length of the large cylindrical base
taper_length = 38.0  # Length of the tapered section
tip_diameter = 4.0   # Diameter at the very tip
mid_diameter = 10.0  # Diameter where the taper meets the base (smaller than base_diameter to create a step)
step_chamfer = 1.0   # Chamfer/fillet size at the transition

# The part consists of a large cylinder base and a long tapered cone.
# We will construct this by revolving a profile or lofting.
# A simple loft or stack of primitives works well here.

# Create the base cylinder
base = cq.Workplane("XY").circle(base_diameter / 2).extrude(base_length)

# Create the tapered section
# We'll create it on the face of the base cylinder.
# Looking at the image, there seems to be a slight step-down or a specific radius
# before the taper starts, or the taper starts directly from a smaller diameter
# centered on the base.

taper = (
    base.faces(">Z")
    .workplane()
    .circle(mid_diameter / 2)
    .workplane(offset=taper_length)
    .circle(tip_diameter / 2)
    .loft(combine=True)
)

# Refinement: The image shows segmented lines on the cone. This usually implies
# a specific manufacturing step or just a visual artifact of the tessellation.
# However, assuming it's a smooth cone, the loft is correct.
# There is a fillet or chamfer at the transition between the base and the taper.
# Let's add a small fillet at the base of the taper where it meets the cylinder face.
# Because of the loft, we need to select the edge carefully.

# Let's refine the approach to ensure robust edge selection.
# Method 2: Constructing the profile and revolving it is often cleaner for turned parts.

# Re-evaluating the shape based on the "ribs" or lines on the cone.
# The lines look like they might be segments of a cone. 
# However, standard representation usually implies a smooth cone.
# Let's stick to the smooth geometry representation as standard CAD.

# Profile Points (in X, Z plane, assuming rotation around Z axis)
# 1. (0, 0) - Center bottom
# 2. (base_radius, 0) - Outer bottom edge
# 3. (base_radius, base_length) - Outer top edge of base
# 4. (mid_radius, base_length) - Step in
# 5. (tip_radius, total_length) - Tip edge
# 6. (0, total_length) - Center tip
# 7. Close to (0,0)

base_radius = base_diameter / 2
mid_radius = mid_diameter / 2
tip_radius = tip_diameter / 2

# Using a revolution operation for a cleaner "turned part" geometry
result = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),
        (base_radius, 0),
        (base_radius, base_length),
        (mid_radius, base_length),
        (tip_radius, base_length + taper_length),
        (0, base_length + taper_length),
        (0, 0)
    ])
    .close()
    .revolve()
)

# Optional: Add the fillet at the transition step if desired, though the image
# shows a relatively sharp step or a very small radius.
# The image shows the transition is slightly rounded.
try:
    # Select the edge at the step down. 
    # It is the circle at Z = base_length with radius = mid_radius
    result = result.edges(cq.selectors.RadiusNthSelector(1)).fillet(1.0)
except:
    # If selection fails (sometimes dependent on kernel), return un-filleted
    pass

# The tip in the image looks slightly rounded/filleted as well.
try:
    result = result.edges(">Z").fillet(0.5)
except:
    pass