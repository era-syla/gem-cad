import cadquery as cq

# Create a terminal block / connector strip with multiple slots
# The image shows a row of 8 terminal block connectors

def make_single_terminal(width=8, depth=10, height=14):
    """Create a single terminal block unit"""
    
    # Main body
    body = (
        cq.Workplane("XY")
        .box(width, depth, height)
    )
    
    # Add top flange/cap that overhangs slightly
    flange_height = 2
    flange_overhang = 2
    top_flange = (
        cq.Workplane("XY")
        .box(width + flange_overhang * 2, depth + flange_overhang * 2, flange_height)
        .translate((0, 0, height / 2 + flange_height / 2))
    )
    
    # Combine body and flange
    terminal = body.union(top_flange)
    
    # Cut a slot/groove from the front for wire entry
    slot_w = width * 0.5
    slot_d = depth * 0.6
    slot_h = height * 0.5
    
    slot = (
        cq.Workplane("XY")
        .box(slot_w, slot_d, slot_h)
        .translate((0, depth * 0.2, -height * 0.1))
    )
    
    terminal = terminal.cut(slot)
    
    # Add screw channel grooves on top
    groove_w = width * 0.25
    groove_d = depth * 0.3
    groove_h = flange_height + 0.5
    
    groove1 = (
        cq.Workplane("XY")
        .box(groove_w, groove_d, groove_h)
        .translate((-width * 0.2, 0, height / 2 + flange_height / 2 + groove_h / 2 - 0.5))
    )
    groove2 = (
        cq.Workplane("XY")
        .box(groove_w, groove_d, groove_h)
        .translate((width * 0.2, 0, height / 2 + flange_height / 2 + groove_h / 2 - 0.5))
    )
    
    terminal = terminal.union(groove1).union(groove2)
    
    # Cut side grooves between terminals
    side_groove_w = 1.0
    side_groove_h = height * 0.8
    side_groove_d = depth * 0.8
    
    return terminal

# Number of terminals in the strip
n_terminals = 8
terminal_width = 8
spacing = terminal_width

# Build the full strip
result = None

for i in range(n_terminals):
    x_pos = i * spacing - (n_terminals - 1) * spacing / 2
    
    # Main terminal body
    body = (
        cq.Workplane("XY")
        .box(terminal_width - 0.5, 10, 14)
        .translate((x_pos, 0, 0))
    )
    
    # Top flange
    flange = (
        cq.Workplane("XY")
        .box(terminal_width + 1, 12, 2)
        .translate((x_pos, 0, 8))
    )
    
    # Wire entry slot cut
    slot = (
        cq.Workplane("XY")
        .box(4, 6, 7)
        .translate((x_pos, 1, -1.5))
    )
    
    # Screw post bumps on top
    bump1 = (
        cq.Workplane("XY")
        .box(1.5, 3, 3)
        .translate((x_pos - 2, 0, 10))
    )
    bump2 = (
        cq.Workplane("XY")
        .box(1.5, 3, 3)
        .translate((x_pos + 2, 0, 10))
    )
    
    # Combine terminal parts
    term = body.union(flange).cut(slot).union(bump1).union(bump2)
    
    # Add separator ridge between terminals
    if i < n_terminals - 1:
        ridge = (
            cq.Workplane("XY")
            .box(0.8, 10, 14)
            .translate((x_pos + spacing / 2, 0, 0))
        )
        term = term.union(ridge)
    
    if result is None:
        result = term
    else:
        result = result.union(term)

# Add base rail running the full length
base_length = n_terminals * terminal_width + 2
base = (
    cq.Workplane("XY")
    .box(base_length, 10, 1.5)
    .translate((0, 0, -7.75))
)

result = result.union(base)