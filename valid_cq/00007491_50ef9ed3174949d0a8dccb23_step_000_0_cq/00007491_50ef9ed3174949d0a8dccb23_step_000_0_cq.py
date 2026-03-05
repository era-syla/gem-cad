import cadquery as cq

# --- Parametric Definitions ---
table_width = 800.0   # Total width of the table
table_depth = 1200.0  # Total length/depth of the table
table_height = 750.0  # Total height of the table

# Leg parameters
leg_size = 50.0       # Square profile size of the legs

# Frame parameters
frame_height = 60.0   # Height of the apron/frame connecting legs
frame_thickness = 20.0 # Thickness of the frame material (optional refinement, usually frame is flush with legs)

# Top parameters
slat_count = 6        # Number of slats on top
slat_thickness = 25.0 # Thickness of the table top slats
gap_width = 5.0       # Gap between slats

# Derived calculations for slats
total_slat_width = table_width - (2 * 0) # Assuming slats cover full width
individual_slat_width = (table_width - (gap_width * (slat_count - 1))) / slat_count


# --- Geometry Construction ---

# 1. Create the Legs
# We create one leg and mirror it to form the four legs
leg = (
    cq.Workplane("XY")
    .rect(leg_size, leg_size)
    .extrude(table_height - slat_thickness)
    .translate((table_width/2 - leg_size/2, table_depth/2 - leg_size/2, 0))
)

# Create the set of 4 legs
legs = (
    leg
    .union(leg.mirror("YZ"))
    .union(leg.mirror("XZ").union(leg.mirror("YZ").mirror("XZ")))
)


# 2. Create the Frame (Apron)
# Connects the legs just below the top
frame_length_x = table_width - 2 * leg_size
frame_length_y = table_depth - 2 * leg_size

# Side aprons (running along Depth)
side_apron = (
    cq.Workplane("XY")
    .rect(leg_size, frame_length_y) # Assuming frame is flush with leg thickness
    .extrude(frame_height)
    .translate((
        table_width/2 - leg_size/2, 
        0, 
        table_height - slat_thickness - frame_height
    ))
)
side_aprons = side_apron.union(side_apron.mirror("YZ"))

# End aprons (running along Width)
end_apron = (
    cq.Workplane("XY")
    .rect(frame_length_x, leg_size)
    .extrude(frame_height)
    .translate((
        0,
        table_depth/2 - leg_size/2,
        table_height - slat_thickness - frame_height
    ))
)
end_aprons = end_apron.union(end_apron.mirror("XZ"))

frame = side_aprons.union(end_aprons)


# 3. Create the Slat Top
# We create a single slat centered, then array/distribute it
base_slat = (
    cq.Workplane("XY")
    .rect(individual_slat_width, table_depth)
    .extrude(slat_thickness)
    .translate((0, 0, table_height - slat_thickness))
)

# Create a list of offsets for the slats
# Center of the table is 0. Slats are distributed along the X axis (Width)
start_x = -((table_width - individual_slat_width) / 2)
offsets = []
for i in range(slat_count):
    offsets.append((start_x + i * (individual_slat_width + gap_width), 0, 0))

# While CadQuery doesn't have a simple "linear array of solids" function in one line for independent bodies,
# we can iterate and union.
top = base_slat.translate(offsets[0]) # Start with first position
for i in range(1, slat_count):
    # We recreate the base slat for each position to ensure clean union
    next_slat = base_slat.translate(offsets[i])
    top = top.union(next_slat)


# --- Combine All Parts ---
result = legs.union(frame).union(top)

# Export or Display (if running in an environment that supports it)
# cq.exporters.export(result, "table.step")