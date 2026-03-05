import cadquery as cq

# --- Parametric Dimensions ---
outer_diameter = 50.0  # Main outer diameter
inner_diameter = 30.0  # Central through-hole diameter
height = 20.0          # Total height of the part

# Counterbore dimensions (the step on the top)
counterbore_diameter = 40.0  # Diameter of the wider opening at the top
counterbore_depth = 5.0      # Depth of the recess

# --- Modeling ---

# 1. Create the base cylinder
base = cq.Workplane("XY").circle(outer_diameter / 2.0).extrude(height)

# 2. Create the central through-hole
#    We cut a cylinder all the way through
result = base.faces(">Z").workplane().hole(inner_diameter)

# 3. Create the counterbore (recess)
#    We cut a larger hole to a specific depth from the top face
result = result.faces(">Z").workplane().cboreHole(inner_diameter, counterbore_diameter, counterbore_depth)

# Alternatively, using basic cut operations for clarity:
# 1. Base cylinder
# result = cq.Workplane("XY").circle(outer_diameter / 2.0).extrude(height)
# 2. Cut the counterbore first
# result = result.faces(">Z").workplane().circle(counterbore_diameter / 2.0).cutBlind(-counterbore_depth)
# 3. Cut the through hole
# result = result.faces(">Z").workplane().circle(inner_diameter / 2.0).cutThruAll()

# The cboreHole method combines the through hole and the counterbore, 
# but since the prompt image shows a simple ring with a step, let's ensure the logic holds.
# The `cboreHole` method assumes we are drilling into existing material.
# Let's rebuild it step-by-step for maximum robustness and clarity on the specific geometry.

# Revised approach:
# Create the profile and revolve it, or extrude and cut. Extrude and cut is often simpler to read.

result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(height)
    # Cut the main through hole
    .faces(">Z").workplane()
    .circle(inner_diameter / 2.0)
    .cutThruAll()
    # Cut the counterbore/step
    .faces(">Z").workplane()
    .circle(counterbore_diameter / 2.0)
    .cutBlind(-counterbore_depth)
)

# If running in an environment that visualizes 'result' automatically (like CQ-Editor), this is sufficient.