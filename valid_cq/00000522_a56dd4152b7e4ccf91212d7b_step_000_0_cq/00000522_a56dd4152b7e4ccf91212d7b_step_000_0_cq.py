import cadquery as cq

# Parameters
outer_diameter = 100.0
rim_width = 10.0
rim_thickness = 2.0
web_thickness = 2.0  # Thickness of the main disc face
hub_diameter = 20.0
hub_height = 15.0
bore_diameter = 10.0

# Rib parameters
num_ribs = 6
rib_thickness = 2.0
rib_height = 6.0  # Height of rib relative to the web surface
rib_start_offset = 2.0 # distance from hub center to start tapering or flat
inner_hub_reinforcement_dia = 28.0 # The slightly raised area around the central hub

# Main construction
# 1. Create the base web (the flat disc)
result = cq.Workplane("XY").circle(outer_diameter / 2.0).extrude(web_thickness)

# 2. Create the outer rim
# Create a ring on the circumference
rim = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .circle(outer_diameter / 2.0)
    .circle((outer_diameter / 2.0) - rim_thickness)
    .extrude(rim_width)
)
result = result.union(rim)

# 3. Create the central hub
hub = (
    cq.Workplane("XY")
    .workplane(offset=0) # Start from the back
    .circle(hub_diameter / 2.0)
    .extrude(hub_height)
)
result = result.union(hub)

# 4. Create the inner hub reinforcement (raised area around hub)
# This connects the ribs to the hub
reinforcement_height = 3.0 # Slightly higher than the web
hub_reinforcement = (
    cq.Workplane("XY")
    .workplane(offset=web_thickness)
    .circle(inner_hub_reinforcement_dia / 2.0)
    .extrude(reinforcement_height)
)
result = result.union(hub_reinforcement)

# 5. Create the ribs
# We create one rib and then rotate it
# The rib profile seems to be rectangular in cross-section, tapering or connecting hub to rim
def create_rib(angle):
    # Create a simple rectangular bar
    # Length needs to go from hub reinforcement to rim
    length = (outer_diameter/2.0) - rim_thickness
    
    rib = (
        cq.Workplane("XY")
        .workplane(offset=web_thickness) # Sit on top of the web
        .center(0, 0)
        .rect(length * 2, rib_thickness) # Make it long enough to cross center
        .extrude(rib_height)
    )
    
    # Cut the inner part to match the reinforcement diameter so it blends nicely
    # Actually, simpler to make a bar from center to edge, then cut the center
    
    rib_geometry = (
        cq.Workplane("XY")
        .workplane(offset=web_thickness)
        .transformed(rotate=cq.Vector(0, 0, angle))
        .center(length/2.0, 0) # Shift so one end is at center
        .box(length, rib_thickness, rib_height, centered=(True, True, False))
    )
    return rib_geometry

# Generate and union ribs
for i in range(num_ribs):
    angle = i * (360.0 / num_ribs)
    rib = create_rib(angle)
    result = result.union(rib)

# 6. Cut the center bore hole
result = result.faces(">Z").workplane().circle(bore_diameter / 2.0).cutThruAll()

# 7. Add the notches on the outer rim
# The image shows some rectangular cutouts/notches on the rim edge
num_notches = 3
notch_depth = 2.0
notch_width = 12.0

for i in range(num_notches):
    angle = i * (360.0 / num_notches) + 30 # Offset slightly from ribs if needed
    
    # We cut from the outside in
    notch_cutter = (
        cq.Workplane("XY")
        .workplane(offset=rim_width/2.0) # Center of rim height
        .transformed(rotate=cq.Vector(0, 0, angle))
        .center(outer_diameter/2.0, 0)
        .box(notch_depth * 2, notch_width, rim_width + 1.0) # Oversized to ensure cut
    )
    result = result.cut(notch_cutter)

# 8. Clean up center overlap
# The ribs overlapped the center hole and the reinforcement area. 
# Let's ensure the center bore is clean and the reinforcement shape is dominant.
# Re-cutting the bore is the safest way to clear rib debris.
result = result.faces(">Z").workplane().circle(bore_diameter / 2.0).cutThruAll()

# Fillets for realism (optional but makes it look like the image)
# Filleting the rib roots where they meet the web
try:
    # Select edges that are at the intersection of Z=web_thickness
    # This is often tricky in parametric CAD without specific edge selectors, 
    # omitting complex fillets to ensure stability of the script.
    pass 
except:
    pass