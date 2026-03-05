import cadquery as cq

# Parametric dimensions
outer_diameter = 50.0
thickness = 15.0

# The inner geometry appears to be stepped. 
# It looks like two different inner diameters meeting in the middle, 
# or a counterbore from one side.
# Let's assume a symmetrical design or a simple counterbore based on the visual.
# Looking at the shadow inside, there seems to be a ridge.
# Let's model it as a ring with a smaller inner ridge (or two larger counterbores).
# However, the most standard interpretation of this visual is a simple bushing or spacer
# with a stepped internal diameter. Let's assume a central smaller diameter and wider 
# diameters on the sides, or a simple counterbore.
# 
# Re-evaluating the image: It looks like a single continuous outer cylinder. 
# The inside has a rim or step. It looks like the hole gets smaller in the middle.
# Let's model it as:
# 1. Main cylinder
# 2. A through hole
# 3. A counterbore or a larger hole on one or both sides. 
# Let's go with a central rib design (smaller diameter in center, larger on outsides)
# or a simple counterbore. The shadow suggests a single step.
# Let's try a counterbored hole from one side.
# Wait, looking at the bottom inner surface, I see a line in the middle. 
# This suggests symmetry: a central smaller ring with counterbores on both sides.

inner_diameter_small = 30.0  # The smallest ID in the middle
inner_diameter_large = 38.0  # The larger ID at the faces
counterbore_depth = 4.0      # Depth of the larger ID sections from each face

# Create the main outer cylinder
result = cq.Workplane("XY").circle(outer_diameter / 2).extrude(thickness)

# Create the through hole (smallest diameter)
result = result.faces(">Z").workplane().hole(inner_diameter_small)

# Create the counterbores on both sides to form the stepped internal profile
# Top counterbore
result = result.faces(">Z").workplane().cboreHole(inner_diameter_small, inner_diameter_large, counterbore_depth)

# Bottom counterbore (to match the symmetrical look of the internal line)
# We need to flip to the bottom face
result = result.faces("<Z").workplane().cboreHole(inner_diameter_small, inner_diameter_large, counterbore_depth)

# Alternatively, using a revolution profile is cleaner for this specific shape
# Profile: A rectangle for the main body, minus the internal cutouts.
# Let's stick to the boolean/hole operations above as they are very readable, 
# but let's refine the "line in the middle" observation.
# If I use cboreHole on both sides, the "line" is the edge where the small diameter starts.
# If the small diameter is just a thin ridge in the middle, we construct it that way.

# Revised Approach: Construct via 2D profile and revolve. This is often more robust.
# Axis of revolution is Y-axis (or Z-axis depending on orientation). 
# Let's define the cross-section on the XZ plane and revolve around Z.

# Dimensions
od = 50.0
id_narrow = 35.0  # Middle restriction
id_wide = 42.0    # Outer openings
h = 15.0          # Total height
rim_h = 3.0       # Height of the inner narrow band

# Create the profile
# We will draw the right-half cross section and revolve it
# Points for the cross section (clockwise or counter-clockwise):
# 1. (od/2, -h/2) - Bottom Outer
# 2. (od/2, h/2)  - Top Outer
# 3. (id_wide/2, h/2) - Top Inner Start
# 4. (id_wide/2, rim_h/2) - Top Step Corner
# 5. (id_narrow/2, rim_h/2) - Inner Ridge Top
# 6. (id_narrow/2, -rim_h/2) - Inner Ridge Bottom
# 7. (id_wide/2, -rim_h/2) - Bottom Step Corner
# 8. (id_wide/2, -h/2) - Bottom Inner Start
# Close back to 1.

# Re-evaluating the image: The step looks simpler. It looks like a simple counterbore 
# resulting in two distinct inner diameters. The line in the shadow suggests the transition.
# Let's assume a simple stepped bushing: Wide opening on top, narrowing down below (or vice versa).
# However, often these generic CAD icons represent a symmetrical part. 
# I will implement the symmetrical "inner ridge" design as it fits the "line in the middle" visual best.

profile_pts = [
    (od / 2, -h / 2),
    (od / 2, h / 2),
    (id_wide / 2, h / 2),
    (id_wide / 2, rim_h / 2),
    (id_narrow / 2, rim_h / 2),
    (id_narrow / 2, -rim_h / 2),
    (id_wide / 2, -rim_h / 2),
    (id_wide / 2, -h / 2)
]

# Generate the solid
result = (cq.Workplane("XZ")
          .polyline(profile_pts)
          .close()
          .revolve(360, (0, 0, 0), (0, 1, 0)) # Revolve around Y axis in this sketch plane to get Z-up orientation roughly
          )

# Re-orient to match standard "Z-up" cylinder default if needed, 
# but the revolve creates it lying down or standing up depending on axis.
# Let's use standard Workplane logic for a standing cylinder to match the image perspective.
# Image perspective is roughly isometric.

result = cq.Workplane("XY").circle(outer_diameter/2).extrude(thickness)

# Let's apply cuts to make the internal shape.
# Cut the main hole
result = result.cut(cq.Workplane("XY").circle(inner_diameter_small/2).extrude(thickness))

# Cut the top counterbore
result = result.cut(
    cq.Workplane("XY")
    .workplane(offset=thickness - counterbore_depth)
    .circle(inner_diameter_large/2)
    .extrude(counterbore_depth)
)

# Cut the bottom counterbore
result = result.cut(
    cq.Workplane("XY")
    .workplane(offset=0)
    .circle(inner_diameter_large/2)
    .extrude(counterbore_depth)
)