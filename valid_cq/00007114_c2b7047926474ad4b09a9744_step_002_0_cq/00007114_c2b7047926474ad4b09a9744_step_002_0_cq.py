import cadquery as cq

# Define parameters for the cylinders
# Based on visual estimation, there are 6 cylinders of varying sizes
# arranged in a staggered formation.

# Heights seem consistent or slightly varying. Let's use a standard height.
height = 20.0

# Cylinder definitions (x_pos, y_pos, radius)
# Coordinates are estimated based on the relative positions in the image
cylinders_data = [
    # Back row (largest one on left, medium on right)
    {"x": -25, "y": 25, "r": 18, "h": height},
    {"x": 25, "y": 20, "r": 14, "h": height},
    
    # Middle row
    {"x": -10, "y": -5, "r": 16, "h": height}, 
    {"x": 35, "y": -15, "r": 10, "h": height},
    
    # Front/Side row
    {"x": 10, "y": -35, "r": 12, "h": height},
    {"x": 55, "y": 5, "r": 8, "h": height},
]

# Create a list to hold the solid objects
solids = []

for data in cylinders_data:
    # Create a cylinder at the origin
    c = cq.Workplane("XY").circle(data["r"]).extrude(data["h"])
    # Translate it to its specific position
    c = c.translate((data["x"], data["y"], 0))
    solids.append(c)

# Combine all cylinders into a single compound object
# We start with the first one and union the rest
result = solids[0]
for i in range(1, len(solids)):
    result = result.union(solids[i])

# Alternatively, just leaving them as a compound if they don't touch
# But usually, a single "result" object is expected.
# Looking at the image, they might not be touching, so a Compound is safer than a Boolean Union if they are disjoint.
# However, if the goal is a single variable for display:
result = cq.Compound.makeCompound([s.val() for s in solids])

# Re-wrapping in a Workplane for consistency with standard CQ patterns
result = cq.Workplane("XY").newObject([result])