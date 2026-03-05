import cadquery as cq

# --- Parameters ---
# Dimensions estimated from the image proportions
unit_size = 15.0          # The width of a tab or a gap
thickness = 5.0           # Thickness of the plate
tab_protrusion = 5.0      # How far the tabs stick out from the base

# Number of tabs on each side based on image features
# Long side has 3 tabs visible with gaps at corners -> Gap-Tab-Gap-Tab-Gap-Tab-Gap
n_tabs_long = 3
# Short side has 1 tab visible with gaps at corners -> Gap-Tab-Gap
n_tabs_short = 1

# Calculate base dimensions based on the pattern of tabs and gaps
# Total segments = 2 * n_tabs + 1 (assuming alternating gap/tab starting with gap)
base_length = (2 * n_tabs_long + 1) * unit_size
base_width = (2 * n_tabs_short + 1) * unit_size

# --- Modeling ---

# 1. Create the central base plate (the inner rectangle defined by the corner gaps)
result = cq.Workplane("XY").box(base_length, base_width, thickness)

# 2. Define geometry for a single tab on the long edge
# Dimensions: Width=unit_size, Depth=tab_protrusion, Height=thickness
long_tab = cq.Workplane("XY").box(unit_size, tab_protrusion, thickness)

# 3. Add tabs to the long sides (Top and Bottom / +/- Y)
for i in range(n_tabs_long):
    # Tabs are at odd indices (1, 3, 5...) in the segment sequence
    segment_index = 1 + (i * 2)
    
    # Calculate X position relative to the center of the plate
    # Start at left edge (-L/2), add offset to center of the specific segment
    x_pos = -base_length / 2.0 + (segment_index + 0.5) * unit_size
    
    # Calculate Y positions (center of the protruding tab)
    y_pos_top = (base_width + tab_protrusion) / 2.0
    y_pos_bottom = -(base_width + tab_protrusion) / 2.0
    
    # Union the tabs to the base
    result = result.union(long_tab.translate((x_pos, y_pos_top, 0)))
    result = result.union(long_tab.translate((x_pos, y_pos_bottom, 0)))

# 4. Define geometry for a single tab on the short edge
# Dimensions: Depth=tab_protrusion, Width=unit_size, Height=thickness
short_tab = cq.Workplane("XY").box(tab_protrusion, unit_size, thickness)

# 5. Add tabs to the short sides (Left and Right / +/- X)
for i in range(n_tabs_short):
    segment_index = 1 + (i * 2)
    
    # Calculate Y position relative to center
    y_pos = -base_width / 2.0 + (segment_index + 0.5) * unit_size
    
    # Calculate X positions
    x_pos_right = (base_length + tab_protrusion) / 2.0
    x_pos_left = -(base_length + tab_protrusion) / 2.0
    
    # Union the tabs to the base
    result = result.union(short_tab.translate((x_pos_right, y_pos, 0)))
    result = result.union(short_tab.translate((x_pos_left, y_pos, 0)))

# result now contains the final geometry