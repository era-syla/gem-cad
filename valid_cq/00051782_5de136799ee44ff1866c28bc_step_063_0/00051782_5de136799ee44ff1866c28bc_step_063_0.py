import cadquery as cq

# -- Parameters --
shaft_diam = 3.0      # Diameter of the cylindrical shaft
head_diam = 6.0       # Diameter of the head
head_height = 4.0     # Height of the head
tab_visible_len = 7.0 # Length of the connecting tab (gap between heads)
tab_width = 3.6       # Width of the tab
tab_thickness = 1.8   # Thickness of the tab
text_size = 2.2       # Size of the text
text_height = 0.5     # Emboss height
spacing = 13.0        # Center-to-center spacing (3mm radius + 7mm gap + 3mm radius = 13mm)

# Pin configurations: (Shaft Length, Label)
configs = [
    (25.0, "3-25"),
    (20.0, "3-20"),
    (15.0, "3-15"),
    (10.0, "3-10")
]

pins = []

for i, (length, label) in enumerate(configs):
    # 1. Create the Shaft (extending downwards from Z=0)
    shaft = cq.Workplane("XY").circle(shaft_diam / 2.0).extrude(-length)
    
    # 2. Create the Head (extending upwards from Z=0)
    head = cq.Workplane("XY").circle(head_diam / 2.0).extrude(head_height)
    
    # 3. Create the Tab
    # We position the tab extending along the X-axis from the head.
    # Overlap ensures solid union with the head.
    overlap = 1.0
    box_len = tab_visible_len + overlap
    
    # Calculate geometric center for the box to place it correctly
    # Start X relative to center: head_radius - overlap
    start_x = (head_diam / 2.0) - overlap
    center_x = start_x + (box_len / 2.0)
    
    # Z-level: Flush with the top of the head
    center_z = head_height - (tab_thickness / 2.0)
    
    tab = (cq.Workplane("XY")
           .workplane(offset=center_z)
           .center(center_x, 0)
           .box(box_len, tab_width, tab_thickness))
    
    # 4. Create the Text
    # Centered on the visible portion of the tab
    text_center_x = (head_diam / 2.0) + (tab_visible_len / 2.0)
    
    text_obj = (cq.Workplane("XY")
                .workplane(offset=head_height)
                .center(text_center_x, 0)
                .text(label, text_size, text_height))
    
    # Union parts for this pin
    pin = shaft.union(head).union(tab).union(text_obj)
    
    # Translate to correct position in the row
    pin = pin.translate((i * spacing, 0, 0))
    pins.append(pin)

# Combine all pins into a single object
result = pins[0]
for p in pins[1:]:
    result = result.union(p)