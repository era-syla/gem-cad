import cadquery as cq

# --- Parametric Dimensions ---
# Shaft dimensions
shaft_diameter = 6.0
shaft_length = 18.0

# Head dimensions
head_diameter = 12.0
head_height = 3.0  # The cylindrical part of the head
dome_height = 2.0  # The height of the rounded top part

# Chamfer at the end of the shaft
chamfer_size = 0.5

# --- Modeling ---

# 1. Create the Shaft
# We start with a cylinder for the main body
shaft = cq.Workplane("XY").circle(shaft_diameter / 2.0).extrude(shaft_length)

# 2. Create the Head
# We create a new workplane at the start of the shaft (Z=0)
# Note: By default, extrude goes in the positive Z direction. 
# We want the head at the bottom (or we can just add it on top and rotate).
# Let's add the head at the base (Z=0) going in the negative Z direction to keep Z=0 as the mating surface.
head_cylinder = (
    cq.Workplane("XY")
    .circle(head_diameter / 2.0)
    .extrude(-head_height)
)

# 3. Create the Dome
# The dome sits on top of the head cylinder (which is at Z = -head_height)
# We can approximate the dome using a sphere intersected with a box or a revolved arc.
# A simple way for a button head is to create a sphere and union it.
# The sphere needs to be positioned correctly.
# Let's calculate the radius of a sphere that satisfies the width (head_diameter) and height (dome_height).
# R^2 = (d/2)^2 + (R-h)^2
# R^2 = (d/2)^2 + R^2 - 2Rh + h^2
# 2Rh = (d/2)^2 + h^2
# R = ((d/2)^2 + h^2) / (2h)
dome_radius = ((head_diameter / 2.0)**2 + dome_height**2) / (2 * dome_height)

# Center of the sphere needs to be shifted so the top of the dome is at -head_height - dome_height
# Actually, let's look at the image again. The dome is on the "outside" face of the head.
# If the shaft goes from 0 to +18, the head cylinder is from 0 to -3.
# The dome should be attached to the face at -3 and bulge further negative.
dome_sphere_center_z = -head_height - dome_radius + dome_height

dome = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, 0, dome_sphere_center_z))
    .sphere(dome_radius)
)

# Cut the sphere to only keep the cap we want. 
# A sphere creates a full solid. We only want the part below Z = -head_height.
# Actually, since we will union it, the overlapping part inside the head doesn't matter much visually,
# but for clean geometry, it's often better to just union.
# However, a huge sphere might protrude out the sides of the cylinder if R > head_diameter/2 (which it is).
# Wait, if R is calculated from the chord, the width of the sphere at height h is exactly head_diameter.
# So simply unioning the sphere is fine, provided we cut off the top part if it protrudes into the shaft area?
# No, the sphere is on the *back* of the head. The shaft is on the *front*.
# So we need the sphere part that is < -head_height.
# We can intersect the sphere with a large box or cylinder that defines the valid volume, 
# or simpler: create the head profile and revolve it.

# Let's try the Revolve approach for the head to ensure it's clean.
# We will revolve a profile around the Z axis.
# Profile:
# 1. Start at shaft radius, Z=0
# 2. Line to head radius, Z=0
# 3. Line to head radius, Z = -head_height
# 4. Arc to (0, -head_height - dome_height) 
#    OR just a 3-point arc from (head_r, -head_h) to (-head_r, -head_h) via (0, -head_h-dome_h) ?? No, profile is 2D.
#    Arc from (head_radius, -head_height) to (0, -total_head_height)
# 5. Close to (0,0) - wait, shaft is solid.

# Let's stick to the boolean composition, it's often easier to read.
# 1. Shaft (0 to length)
# 2. Head Cylinder (0 to -head_height)
# 3. Dome (cap on -head_height face)

part = shaft.union(head_cylinder)

# Create the dome as a separate solid to union
# Position sphere such that its 'top' (relative to its own center) sticks out by dome_height from the back face.
# Back face is at Z = -head_height.
# We want the sphere surface to reach Z = -head_height - dome_height.
# Sphere center Z = (-head_height - dome_height) + dome_radius.
# Wait, standard sphere is centered at origin.
# Z_center = -head_height - dome_height + dome_radius
# This sphere will be valid.
dome_solid = cq.Solid.makeSphere(dome_radius, cq.Vector(0, 0, -head_height - dome_height + dome_radius))

# We need to trim this sphere so it doesn't bulge wider than the cylinder (it shouldn't based on math)
# and doesn't stick into the shaft area (it overlaps the head cylinder, which is fine).
# But wait, does the sphere bulge *out* past the cylinder walls?
# R > d/2. The sphere is wider than the head diameter at its equator.
# We only want the "cap".
# The cap is defined by the plane at Z = -head_height.
# So we intersect the sphere with a half-space or a large box below Z = -head_height.
# Actually, the image shows a continuous curvature, or maybe a fillet.
# Let's assume standard rivet geometry: Button Head.
# Button heads usually have a spherical cap.
# The "equator" of the sphere often matches the head diameter if it's a full hemisphere,
# but for shallower heads, the sphere is larger and sliced.
# If we calculated R based on width and height, the width at the slice plane is exactly head_diameter.
# So the sphere will not protrude radially beyond the cylinder *at the intersection plane*.
# But since it's a sphere, and we are taking the "tip" of it, the widest part we keep is the intersection plane.
# So it won't be wider than head_diameter anywhere else in the kept volume.
# So a simple union is safe.

result = part.union(dome_solid)

# 4. Apply Chamfer to the shaft end
# The shaft end is the face at Z = shaft_length
result = result.faces(">Z").chamfer(chamfer_size)

# 5. Apply Fillet between shaft and head?
# The image shows a sharp transition or maybe a very small fillet.
# Standard rivets often have a small radius under the head.
# Let's add a small fillet for realism.
try:
    result = result.faces("Z=0").edges().fillet(0.5)
except:
    # If selection fails (sometimes topology naming can be tricky), skip it
    pass

# Ensure result is returned
result = result