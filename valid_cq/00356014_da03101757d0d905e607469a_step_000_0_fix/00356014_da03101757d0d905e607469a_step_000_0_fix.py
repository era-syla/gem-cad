import cadquery as cq

# Define the profiles for lofting
profile1 = cq.Workplane("XY").ellipse(50, 25)
profile2 = profile1.workplane(offset=50).ellipse(100, 50)

# Loft between the profiles
result = profile1.add(profile2).loft()