import cadquery as cq

# Main body dimensions
body_w = 60
body_d = 50
body_h = 25

# Create main rectangular body
body = cq.Workplane("XY").box(body_w, body_d, body_h)

# Create mounting tabs (flanges) on the left side
tab_w = 12
tab_d = 14
tab_h = 4
tab_hole_r = 2.5

# Bottom-left mounting tab
tab1 = (cq.Workplane("XY")
    .box(tab_w, tab_d, tab_h)
    .translate((-body_w/2 - tab_w/2 + 2, -body_d/2 + tab_d/2, -body_h/2 + tab_h/2))
)

# Top-left mounting tab
tab2 = (cq.Workplane("XY")
    .box(tab_w, tab_d, tab_h)
    .translate((-body_w/2 - tab_w/2 + 2, body_d/2 - tab_d/2, -body_h/2 + tab_h/2))
)

# Combine body with tabs
result = body.union(tab1).union(tab2)

# Add holes to mounting tabs
result = (result
    .faces("<Z")
    .workplane()
    .pushPoints([
        (-body_w/2 - tab_w/2 + 2 + 1, -body_d/2 + tab_d/2),
        (-body_w/2 - tab_w/2 + 2 + 1, body_d/2 - tab_d/2),
    ])
    .circle(tab_hole_r)
    .cutThruAll()
)

# Create terminal block on top-front of body
# 4 terminal connectors along the front-top edge
num_terminals = 4
term_w = 10
term_d = 10
term_h = 12
term_spacing = term_w + 2
term_start_x = -(num_terminals * term_spacing - 2) / 2 + term_w/2

terminal_block = cq.Workplane("XY").box(
    num_terminals * term_spacing - 2,
    term_d,
    term_h
).translate((
    term_start_x - term_w/2 + (num_terminals * term_spacing - 2)/2 - (num_terminals * term_spacing - 2)/2,
    -body_d/2 + term_d/2,
    body_h/2 + term_h/2
))

result = result.union(terminal_block)

# Add individual terminal separators/ribs
for i in range(num_terminals - 1):
    rib_x = term_start_x + i * term_spacing + term_w/2 + 1 - (num_terminals * term_spacing - 2)/2 + (num_terminals * term_spacing - 2)/2
    rib = cq.Workplane("XY").box(1.5, term_d + 1, term_h + 2).translate((
        rib_x,
        -body_d/2 + term_d/2,
        body_h/2 + term_h/2
    ))
    result = result.union(rib)

# Add screw holes in terminal block (top surface)
for i in range(num_terminals):
    screw_x = -((num_terminals - 1) * term_spacing) / 2 + i * term_spacing
    result = (result
        .faces(">Z")
        .workplane()
        .pushPoints([(screw_x, -body_d/2 + term_d/2 - body_h/2 - term_h/2 + body_h/2 + term_h/2 - body_h/2 - term_h/2)])
        .circle(2)
        .cutBlind(-5)
    )

# Slight chamfer on body edges
try:
    result = result.edges("|Z").chamfer(1.5)
except:
    pass