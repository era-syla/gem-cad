import cadquery as cq

# Parametric dimensions for a brilliant-cut style diamond shape
# These parameters control the proportions of the gem
girdle_diameter = 10.0  # The diameter at the widest part (the girdle)
table_width = 6.0       # The width of the flat top face (the table)
crown_height = 2.0      # The height of the top section (crown) above the girdle
pavilion_depth = 5.0    # The depth of the bottom section (pavilion) below the girdle
num_sides = 8           # Number of sides for the main polygon (octagon is standardish)

# Create the workplane
# We will construct the profile of the gem and revolve it or loft it.
# However, a faceted gem is best created by defining cross-sections or using lofting between polygons.
# A simpler approach that yields the "low poly" look in the image is to loft from a point to a polygon to a smaller polygon.

# Strategy:
# 1. Create the girdle: A regular polygon at Z = 0
# 2. Create the table: A smaller regular polygon at Z = crown_height
# 3. Create the culet (bottom tip): A point (or tiny polygon) at Z = -pavilion_depth
# 4. Loft the sections together.

# Create the Girdle (middle widest part)
# We use circumscribed=True to make the diameter correspond to the outer points
girdle_wire = cq.Workplane("XY").polygon(num_sides, girdle_diameter).wire()

# Create the Table (top flat face)
# We offset this in Z by the crown height
table_wire = cq.Workplane("XY").workplane(offset=crown_height).polygon(num_sides, table_width).wire()

# Create the Pavilion tip (bottom point)
# We simulate a point by making a very tiny polygon at the bottom depth
# In a real diamond, this is the culet.
culet_wire = cq.Workplane("XY").workplane(offset=-pavilion_depth).polygon(num_sides, 0.01).wire()

# Construct the Crown (Top part)
# Loft from girdle to table
crown = cq.Workplane("XY").add(girdle_wire).add(table_wire).toPending().loft()

# Construct the Pavilion (Bottom part)
# Loft from girdle to culet
pavilion = cq.Workplane("XY").add(culet_wire).add(girdle_wire).toPending().loft()

# Combine them into a single solid
result = crown.union(pavilion)

# Optional: Rotate for better viewing angle similar to the image
# result = result.rotate((0,0,0), (1,0,0), -20).rotate((0,0,0), (0,0,1), 45)