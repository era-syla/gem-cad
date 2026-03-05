import cadquery as cq

# Overall keyboard dimensions
kbd_width = 160
kbd_depth = 60
kbd_height = 4
border = 3
recess_depth = 1.5

# Key dimensions
key_w = 12
key_h = 8
key_thickness = 1.5
key_gap = 2.5

# Start with base plate
result = cq.Workplane("XY").rect(kbd_width, kbd_depth).extrude(kbd_height)

# Add raised border rim by cutting inner recess
inner_w = kbd_width - 2 * border
inner_d = kbd_depth - 2 * border

result = (result
    .faces(">Z")
    .workplane()
    .rect(inner_w, inner_d)
    .cutBlind(-recess_depth)
)

# Function to add a key at position (x, y) relative to center of keyboard top
def add_key(wp, x, y, w=key_w, h=key_h):
    return (wp
        .workplane(offset=0)
        .center(x, y)
        .rect(w, h)
        .extrude(key_thickness)
        .center(-x, -y)
    )

# Work on the recessed face
key_surface = result.faces(">Z").workplane()

# Define key layout - rows of keys
# Row positions (y from center)
row_y = [15, 7, -1, -9]  # 4 rows

# Number of keys per row
keys_per_row = [7, 7, 7, 7]

# Starting x positions
start_x = -(kbd_width/2) + border + key_gap + key_w/2 - 5

# Build keys as separate solid and union
keys_solid = None

col_spacing = key_w + key_gap
row_spacing = key_h + key_gap

# Row 1 - function/special keys area (top)
# Small keys at top left
top_row_y = 22

# Add a couple special keys top-left
for i in range(2):
    x = start_x + i * (key_w * 0.7 + key_gap)
    y = top_row_y
    kw = key_w * 0.7
    kh = key_h * 0.7
    box = (cq.Workplane("XY")
           .transformed(offset=cq.Vector(x, y, kbd_height - recess_depth))
           .rect(kw, kh)
           .extrude(key_thickness))
    if keys_solid is None:
        keys_solid = box
    else:
        keys_solid = keys_solid.union(box)

# Main key area - 4 rows x 7-8 columns
num_rows = 4
num_cols = 8

for row in range(num_rows):
    y = 14 - row * (key_h + key_gap)
    for col in range(num_cols):
        x = start_x + col * (key_w + key_gap)
        # Skip if out of bounds
        if x + key_w/2 > kbd_width/2 - border - 2:
            continue
        box = (cq.Workplane("XY")
               .transformed(offset=cq.Vector(x, y, kbd_height - recess_depth))
               .rect(key_w, key_h)
               .extrude(key_thickness))
        if keys_solid is None:
            keys_solid = box
        else:
            keys_solid = keys_solid.union(box)

# Add a wider space-bar like key at bottom
wide_key = (cq.Workplane("XY")
            .transformed(offset=cq.Vector(start_x + 3 * (key_w + key_gap), 
                                          14 - 4 * (key_h + key_gap), 
                                          kbd_height - recess_depth))
            .rect(key_w * 3 + key_gap * 2, key_h)
            .extrude(key_thickness))
if keys_solid is None:
    keys_solid = wide_key
else:
    keys_solid = keys_solid.union(wide_key)

# Union keys with base
if keys_solid is not None:
    result = result.union(keys_solid)