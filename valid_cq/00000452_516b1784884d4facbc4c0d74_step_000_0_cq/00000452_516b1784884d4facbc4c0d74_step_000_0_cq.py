import cadquery as cq

# Parametric dimensions
bolt_length = 80.0     # Total length of the shaft
shaft_diameter = 6.0   # M6 roughly
head_height = 5.0      # Height of the hexagonal part
flange_height = 1.5    # Height of the flange washer
flange_diameter = 13.0 # Diameter of the flange
hex_size = 10.0        # Across flats for the hex head
thread_length = 20.0   # Length of the threaded portion at the tip
knurl_length = 30.0    # Approximate length of the "grip" or knurled-looking section
knurl_offset = 15.0    # Distance from head to start of knurl section (gap)

# Create the main shaft
# We'll create it centered on the origin, growing downwards
shaft = cq.Workplane("XY").circle(shaft_diameter / 2.0).extrude(-bolt_length)

# Create the Flange Head
# 1. The Hex Head
hex_head = (
    cq.Workplane("XY")
    .workplane(offset=flange_height) # Start on top of the flange
    .polygon(6, hex_size * 1.1547)   # 1.1547 factor converts flat-to-flat to diameter
    .extrude(head_height)
)

# 2. The Flange (Washer part)
flange = (
    cq.Workplane("XY")
    .circle(flange_diameter / 2.0)
    .extrude(flange_height)
)

# 3. Combine Head parts
head = flange.union(hex_head)

# Create the "Thread" Representation
# In CAD, modeling actual helical threads is computationally expensive and often bad practice.
# We usually represent threads by a slightly smaller cylinder or a cosmetic cut.
# However, the image shows distinct sections: 
# a smooth section near the head, a textured/knurled section, a smooth middle, and threads at the tip.
# Let's create visual cues for these sections using simple radius reductions or cuts.

# Thread section (at the tip)
# We represent threads as a cylinder slightly smaller than the major diameter to show the difference visually
thread_section = (
    cq.Workplane("XY")
    .workplane(offset=-(bolt_length - thread_length))
    .circle(shaft_diameter / 2.0 - 0.1) # Slightly smaller for visual distinction
    .extrude(-thread_length)
)

# Middle Knurled/Grip Section
# The image shows a section with horizontal ridges/knurling.
# We will represent this with a series of small circular cuts to mimic ridges.
grip_start = -knurl_offset
grip_end = -(knurl_offset + knurl_length)

# Instead of complex knurling, we'll create a slightly distinct cylinder for the section
grip_section = (
    cq.Workplane("XY")
    .workplane(offset=grip_start)
    .circle(shaft_diameter / 2.0 + 0.05) # Slightly larger or distinct
    .extrude(-(knurl_length))
)

# Combine everything
# Start with the head
result = head

# Add the main shaft
result = result.union(shaft)

# Simple filleting/chamfering for realism
# Chamfer the bottom tip of the shaft
result = result.faces("<Z").chamfer(0.5)

# Chamfer the top of the hex head
result = result.faces(">Z").chamfer(0.5)

# Fillet the connection between flange and shaft
# We need to select the edge at Z=0
try:
    result = result.edges(cq.selectors.NearestToPointSelector((shaft_diameter/2, 0, 0))).fillet(0.5)
except:
    # Fallback if specific edge selection is tricky, though Z=0 intersection is standard
    pass

# Create visual rings for the grip/threads to match the drawing style
# This creates a series of toroidal cuts to simulate the ribbed texture seen in the image
for i in range(15):
    z_pos = -20 - (i * 2.0) # Start 20mm down, spaced 2mm apart
    cutter = (
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .circle(shaft_diameter / 2.0 + 1.0) # Outer boundary
        .circle(shaft_diameter / 2.0 - 0.1) # Inner cut depth
        .extrude(0.2) # Thin slice
    )
    result = result.cut(cutter)

# Create visual rings for the tip threads
for i in range(10):
    z_pos = -(bolt_length - 2.0) + (i * 1.5)
    cutter = (
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .circle(shaft_diameter / 2.0 + 1.0)
        .circle(shaft_diameter / 2.0 - 0.2)
        .extrude(0.2)
    )
    result = result.cut(cutter)
    
# Final boolean cleanup to ensure solid
result = result.clean()