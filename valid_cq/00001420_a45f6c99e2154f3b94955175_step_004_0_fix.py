import cadquery as cq

# Aluminum extrusion profile - T-slot style
# The image shows three aluminum extrusion bars meeting at a junction
# - One vertical bar going up
# - Two horizontal bars going to the right (offset vertically)

# Extrusion cross-section size
size = 20  # 20mm x 20mm cross section
slot_depth = 4
slot_width = 6

def make_extrusion_profile():
    """Create a T-slot aluminum extrusion cross-section profile"""
    # Simple square profile with chamfered corners to approximate T-slot extrusion
    profile = (
        cq.Workplane("XY")
        .rect(size, size)
        .extrude(1)
    )
    return profile

def make_bar(length, axis='Z'):
    """Create an aluminum extrusion bar along specified axis"""
    bar = (
        cq.Workplane("XY")
        .rect(size, size)
        .extrude(length)
    )
    
    # Add corner chamfers to simulate T-slot profile
    bar = bar.edges("|Z").chamfer(2)
    
    if axis == 'X':
        bar = bar.rotate((0, 0, 0), (0, 1, 0), 90)
    elif axis == 'Y':
        bar = bar.rotate((0, 0, 0), (1, 0, 0), -90)
    
    return bar

# Lengths
vertical_length = 250
horizontal_length = 180

# Vertical bar (going up) - centered at origin
vertical_bar = (
    cq.Workplane("XY")
    .rect(size, size)
    .extrude(vertical_length)
    .translate((-size/2, -size/2, -vertical_length/2))
)
vertical_bar = vertical_bar.edges("|Z").chamfer(1.5)

# Upper horizontal bar (going to the right)
upper_horizontal = (
    cq.Workplane("XZ")
    .rect(size, size)
    .extrude(horizontal_length)
)
upper_horizontal = upper_horizontal.translate((0, -size/2, 20))
upper_horizontal = upper_horizontal.edges("|Y").chamfer(1.5)

# Lower horizontal bar (going to the right, offset down and forward)
lower_horizontal = (
    cq.Workplane("XZ")
    .rect(size, size)
    .extrude(horizontal_length)
)
lower_horizontal = lower_horizontal.translate((0, size/2, -20))
lower_horizontal = lower_horizontal.edges("|Y").chamfer(1.5)

# Combine all bars
result = (
    cq.Workplane("XY")
    .rect(size, size)
    .extrude(vertical_length)
)
result = result.edges("|Z").chamfer(1.5)
result = result.translate((-size/2, -size/2, -vertical_length + 60))

# Upper horizontal bar
uh = (
    cq.Workplane("XZ")
    .rect(size, size)
    .extrude(horizontal_length)
    .translate((0, -size/2, 20))
)
uh = uh.edges("|Y").chamfer(1.5)

# Lower horizontal bar  
lh = (
    cq.Workplane("XZ")
    .rect(size, size)
    .extrude(horizontal_length)
    .translate((0, size/2, 0))
)
lh = lh.edges("|Y").chamfer(1.5)

# Union all parts
result = result.union(uh).union(lh)