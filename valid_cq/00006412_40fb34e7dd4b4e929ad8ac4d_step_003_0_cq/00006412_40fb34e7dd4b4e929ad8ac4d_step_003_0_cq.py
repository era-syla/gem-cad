import cadquery as cq

# --- Parametric Dimensions ---
table_width = 80.0    # Width of the tabletop (X-axis)
table_depth = 50.0    # Depth of the tabletop (Y-axis)
table_height = 60.0   # Total height of the table (Z-axis)
top_thickness = 5.0   # Thickness of the tabletop slab
leg_width = 4.0       # Width of the square legs
leg_depth = 4.0       # Depth of the square legs

# --- Derived Calculations ---
leg_height = table_height - top_thickness
leg_offset_x = (table_width / 2) - (leg_width / 2)
leg_offset_y = (table_depth / 2) - (leg_depth / 2)

# --- Geometry Creation ---

# 1. Create the Table Top
# Start a sketch on the XY plane
table_top = (
    cq.Workplane("XY")
    .box(table_width, table_depth, top_thickness)
    .translate((0, 0, table_height - (top_thickness / 2))) # Move to the top position
)

# 2. Create the Legs
# Define the positions for the four legs relative to the center
leg_positions = [
    (leg_offset_x, leg_offset_y),
    (leg_offset_x, -leg_offset_y),
    (-leg_offset_x, leg_offset_y),
    (-leg_offset_x, -leg_offset_y)
]

# Create all legs in one operation
legs = (
    cq.Workplane("XY")
    .pushPoints(leg_positions)
    .rect(leg_width, leg_depth)
    .extrude(leg_height)
)

# 3. Combine Parts
# Union the top and the legs into a single solid
result = table_top.union(legs)

# Export or visualization would happen here normally
# For this script, 'result' holds the final geometry