import cadquery as cq

# --- Parameters ---
disk_diameter = 200.0
disk_thickness = 2.0
center_hole_diam = 6.0

# Pattern parameters
num_clusters = 10
pcd = 160.0  # Pitch Circle Diameter where clusters are located
cluster_hole_diam = 4.0
slot_length = 8.0
slot_width = 2.0
slot_offset = 9.0  # Distance from cluster center to slot center

# --- Geometry Construction ---

# 1. Create the base disk
result = (
    cq.Workplane("XY")
    .circle(disk_diameter / 2)
    .extrude(disk_thickness)
)

# 2. Cut the central hole
result = (
    result.faces(">Z")
    .workplane()
    .circle(center_hole_diam / 2)
    .cutThruAll()
)

# 3. Define the cutter tool for a single cluster
# We construct this at the origin (0,0). 
# It consists of a center pin and 4 slots arranged in an 'X' pattern.
def create_cluster_tool():
    # Length of the cutting tool (longer than plate thickness)
    tool_len = disk_thickness * 3
    
    # Create the center hole cutter
    tool = cq.Workplane("XY").circle(cluster_hole_diam / 2).extrude(tool_len)
    
    # Create one slot shape: a rectangle offset along the X-axis
    slot_base = (
        cq.Workplane("XY")
        .rect(slot_length, slot_width)
        .extrude(tool_len)
        .translate((slot_offset, 0, 0))
    )
    
    # Create the 4 slots by rotating the base slot
    # Angles 45, 135, 225, 315 create the 'X' shape relative to the cluster center
    for angle in [45, 135, 225, 315]:
        rotated_slot = slot_base.rotate((0, 0, 0), (0, 0, 1), angle)
        tool = tool.union(rotated_slot)
    
    # Position the tool in Z so it cuts through the plate (which is at Z=0..thickness)
    tool = tool.translate((0, 0, -disk_thickness))
    
    return tool

# Generate the single cluster tool
cluster_tool = create_cluster_tool()

# 4. Pattern the tool around the disk
# Get polar locations. polarArray handles the rotation of the local coordinate system,
# so the "X" pattern will rotate correctly around the disk.
locations = (
    cq.Workplane("XY")
    .polarArray(radius=pcd/2, startAngle=0, angle=360, count=num_clusters)
    .vals()
)

# Move the tool to each location
# .val() gets the underlying Shape, .moved(loc) applies the transformation
cutters = [cluster_tool.val().moved(loc) for loc in locations]

# Combine all cutters into a single compound for an efficient boolean operation
cutting_compound = cq.Compound.makeCompound(cutters)

# 5. Subtract the pattern from the base disk
result = result.cut(cutting_compound)