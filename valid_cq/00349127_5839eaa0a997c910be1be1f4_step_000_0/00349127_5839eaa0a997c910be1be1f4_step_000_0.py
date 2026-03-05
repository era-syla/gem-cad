import cadquery as cq

# Parametric Dimensions
length = 400.0
beam = 160.0    # Width at widest point
height = 60.0   # Height of gunwale
thickness = 4.0 # Hull thickness

# Helper function to create cross-section profiles
def create_profile(workplane, offset, bottom_w, top_w, h_val, raked_bottom=0):
    """
    Creates a trapezoidal profile for the hull.
    offset: Position along the length (X axis)
    bottom_w: Width of the flat bottom
    top_w: Width at the gunwale
    h_val: Height at this section
    raked_bottom: Vertical offset for the bottom (rake at bow)
    """
    pts = [
        (-bottom_w / 2, raked_bottom),  # Bottom Left
        (-top_w / 2, h_val),            # Top Left
        (top_w / 2, h_val),             # Top Right
        (bottom_w / 2, raked_bottom)    # Bottom Right
    ]
    return workplane.workplane(offset=offset).polyline(pts).close()

# 1. Define the Hull Geometry
# We use the YZ plane and loft along the X axis.
wp = cq.Workplane("YZ")

# Transom Profile (Rear) - X = 0
# Slightly narrower than midship, standard height
transom = create_profile(wp, 0, beam * 0.6, beam * 0.85, height)

# Midship Profile - X = ~60% of length
# Widest point, slightly higher sheer line
midship = create_profile(wp, length * 0.6, beam * 0.7, beam, height * 1.05)

# Bow Profile - X = Length
# Comes to a point (very narrow width), bottom rakes up significantly
bow = create_profile(wp, length, 0.1, 0.1, height * 1.15, raked_bottom=height * 0.6)

# Create the solid hull shape
hull_solid = transom.add(midship).add(bow).loft()

# 2. Create the Open Boat (Shelling)
# Shell inwards, removing the top face (faces with normal pointing +Z)
# We accept faces where the Z component of the normal is positive and dominant
hull_shelled = hull_solid.faces("+Z").shell(-thickness)

# 3. Modeling Internal Components
# Strategy: Create blocks and intersect them with the original solid hull 
# to ensure they fit perfectly against the curved bottom/sides.

# -- Rear Bench --
bench_length = length * 0.15
bench_height = height * 0.6
bench_block = (
    cq.Workplane("XY")
    .box(bench_length, beam * 1.2, bench_height) # Oversized width
    .translate((bench_length/2 + thickness, 0, bench_height/2))
)
rear_bench = hull_solid.intersect(bench_block)

# -- Front Casting Deck --
deck_length = length * 0.25
deck_height = height * 0.8
deck_pos_x = length - deck_length
deck_block = (
    cq.Workplane("XY")
    .box(deck_length, beam * 1.2, deck_height)
    .translate((deck_pos_x + deck_length/2, 0, deck_height/2))
)
front_deck = hull_solid.intersect(deck_block)
# Flatten the top of the deck (since the hull sheer line curves up)
front_deck = front_deck.cut(
    cq.Workplane("XY")
    .workplane(offset=deck_height)
    .box(length, beam*2, height)
    .translate((length/2, 0, height/2))
)

# -- Side Console / Seat --
# Located on the starboard side (right side looking forward, so -Y in YZ plane logic? 
# Let's place it at +Y for visibility)
console_len = length * 0.15
console_width = beam * 0.35
console_height = height * 0.85
console_x = length * 0.55
console_y = beam * 0.25

console_block = (
    cq.Workplane("XY")
    .box(console_len, console_width, height * 1.2) # Oversized height for initial intersection
    .translate((console_x, console_y, height/2))
)
# Fit to hull
console = hull_solid.intersect(console_block)
# Cut to correct height
console = console.cut(
    cq.Workplane("XY")
    .workplane(offset=console_height)
    .box(length, beam, height)
    .translate((length/2, 0, height/2))
)

# Add the "Shelf" cutout in the console
# Cut a box out of the inner face of the console
shelf_cutout = (
    cq.Workplane("XY")
    .box(console_len * 0.8, console_width, console_height * 0.4)
    .translate((console_x, console_y - thickness, console_height * 0.6))
)
console = console.cut(shelf_cutout)

# 4. Combine all parts
result = hull_shelled.union(rear_bench).union(front_deck).union(console)