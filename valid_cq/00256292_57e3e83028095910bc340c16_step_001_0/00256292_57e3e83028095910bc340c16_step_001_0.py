import cadquery as cq

# Parametric dimensions based on visual estimation
length = 100.0        # Center-to-center distance
boss_od = 30.0        # Outer diameter of the bosses
boss_id = 12.0        # Diameter of the through holes
boss_height = 15.0    # Thickness of the bosses
arm_width = 20.0      # Width of the connecting beam
arm_thickness = 8.0   # Thickness of the connecting beam

# 1. Create the two cylindrical bosses at the ends
bosses = (
    cq.Workplane("XY")
    .pushPoints([(-length / 2.0, 0), (length / 2.0, 0)])
    .circle(boss_od / 2.0)
    .extrude(boss_height)
)

# 2. Create the connecting arm
# Calculate the Z-offset to center the arm vertically relative to the bosses
z_offset = (boss_height - arm_thickness) / 2.0

# Create the arm geometry
# A rectangle of length 'length' centered at origin will extend exactly to the 
# centers of the bosses, ensuring a clean union with the solid cylinders.
arm = (
    cq.Workplane("XY")
    .workplane(offset=z_offset)
    .rect(length, arm_width)
    .extrude(arm_thickness)
)

# 3. Combine the bosses and the arm into one solid
body = bosses.union(arm)

# 4. Cut the through holes in the bosses
result = (
    body
    .faces(">Z")
    .workplane()
    .pushPoints([(-length / 2.0, 0), (length / 2.0, 0)])
    .circle(boss_id / 2.0)
    .cutThruAll()
)