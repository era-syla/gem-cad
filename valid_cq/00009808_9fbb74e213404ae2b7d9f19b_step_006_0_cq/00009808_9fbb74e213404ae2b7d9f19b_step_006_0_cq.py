import cadquery as cq

# Parametric dimensions
outer_diameter = 40.0
total_height = 20.0
rim_thickness = 2.0
base_thickness = 2.0

# Central hub dimensions
hub_outer_diameter = 18.0
hub_inner_diameter = 12.0
hub_height = 18.0  # Slightly less than total height to be recessed or same? Looks flush or slightly proud. Let's make it equal for now.

# Shaft cutout (D-shaft or notched)
# The image shows a specific notch pattern on the hub.
# It looks like a slot cut across the hub face.
slot_width = 4.0
slot_depth = 5.0

# Ribs/Spokes
num_ribs = 6
rib_thickness = 1.0

# Construction

# 1. Create the main cup/cylinder body
# We start with the solid outer cylinder
main_body = cq.Workplane("XY").circle(outer_diameter / 2).extrude(total_height)

# 2. Hollow out the main body to create the cup shape
# We shell it, leaving the bottom face (at Z=0) open? No, based on the image, the "top" is the open side we see.
# Let's re-orient. Let's say the closed face is at Z=0 and we extrude up.
# Actually, the image shows a closed back face (implied) and an open front face.
# Let's create the shell by removing material from the top.
# Inner diameter = outer - 2*rim_thickness
inner_diameter = outer_diameter - (2 * rim_thickness)
interior_cut = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .circle(inner_diameter / 2)
    .extrude(total_height - base_thickness, combine=False)
)

main_body = main_body.cut(interior_cut)

# 3. Create the central hub
# The hub rises from the base thickness up to the top.
hub = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .circle(hub_outer_diameter / 2)
    .circle(hub_inner_diameter / 2) # Hollow center
    .extrude(hub_height - base_thickness)
)

# 4. Create the notch on the hub
# The notch is cut into the top of the hub.
notch = (
    cq.Workplane("XY")
    .workplane(offset=hub_height - slot_depth)
    .rect(hub_outer_diameter * 1.5, slot_width) # Make rectangle wide enough to cut through
    .extrude(slot_depth, combine=False)
)

hub = hub.cut(notch)

# 5. Create the internal ribs
# Ribs connect the hub to the outer rim.
# They sit on the base and go up some distance (looks like halfway or full height - rim offset).
# In the image, the ribs look recessed from the top rim.
rib_height = (total_height - base_thickness) * 0.6 

ribs = cq.Workplane("XY").workplane(offset=base_thickness)

for i in range(num_ribs):
    angle = i * (360.0 / num_ribs)
    # Create a thin rectangle radiating from center
    # Length needs to bridge the gap between hub and outer rim
    rib = (
        cq.Workplane("XY")
        .workplane(offset=base_thickness)
        .transformed(rotate=cq.Vector(0, 0, angle))
        .center(outer_diameter/4, 0) # Rough centering
        .rect(outer_diameter/2, rib_thickness) # Long enough to intersect both
        .extrude(rib_height, combine=False)
    )
    # Intersect the rib with the annular space between hub and rim to trim it cleanly
    # Define the annular volume
    annulus = (
        cq.Workplane("XY")
        .workplane(offset=base_thickness)
        .circle(inner_diameter / 2)
        .circle(hub_outer_diameter / 2)
        .extrude(rib_height, combine=False)
    )
    
    clean_rib = rib.intersect(annulus)
    if i == 0:
        all_ribs = clean_rib
    else:
        all_ribs = all_ribs.union(clean_rib)

# 6. Combine all parts
result = main_body.union(hub).union(all_ribs)

# 7. Add the subtle lip on the outer rim if visible
# The image shows a slight flange or wider rim at the very top.
# Let's add a small ring at the top.
lip_width = 1.0
lip_height = 1.5
lip = (
    cq.Workplane("XY")
    .workplane(offset=total_height - lip_height)
    .circle((outer_diameter / 2) + lip_width)
    .circle(outer_diameter / 2)
    .extrude(lip_height)
)

result = result.union(lip)

# Apply a fillet to the bottom edge for a nicer look (optional but common)
try:
    result = result.edges("|Z").filterByPosition(lambda p: p.z < 0.1).fillet(1.0)
except:
    pass # If selection fails, skip fillet