import cadquery as cq

# Define the dimensions of the boxes in the sequence (Length, Width, Height)
# Sequence matches the image from bottom-left to top-right
box_specs = [
    # Left Group
    (10, 6, 2),    # 1. Flat rectangular plate
    (3, 3, 3),     # 2. Smallest cube
    (4, 4, 4),     # 3. Small cube
    (5, 5, 5),     # 4. Medium cube (with slot feature)
    (14, 14, 14),  # 5. Largest cube
    
    # Right Group
    (5, 5, 7),     # 6. Tall small box
    (11, 9, 6),    # 7. Medium rectangular block
    (11, 7, 3),    # 8. Flat rectangular block
    (15, 11, 4)    # 9. Large flat end plate
]

# Define gaps between consecutive boxes
spacings = [
    3,    # Gap between 1-2
    2,    # Gap between 2-3
    2,    # Gap between 3-4
    2,    # Gap between 4-5
    30,   # Gap between 5-6 (Large separation between groups)
    2,    # Gap between 6-7
    3,    # Gap between 7-8
    3     # Gap between 8-9
]

solids = []
current_x = 0
current_y = 0

for i, (l, w, h) in enumerate(box_specs):
    # Calculate center position
    # Boxes are placed along the X=Y diagonal to achieve the stepped isometric layout
    cx = current_x + l / 2.0
    cy = current_y + w / 2.0
    cz = h / 2.0
    
    # Create the base box
    box = cq.Workplane("XY").box(l, w, h).translate((cx, cy, cz))
    
    # Add the detail feature visible on the 4th box (a small slot)
    if i == 3:
        # Cut a small rectangular slot on the visible face (assumed >Y or >X based on view)
        try:
            box = box.faces(">X").workplane().center(0, -1).rect(3, 1).cutBlind(-2)
        except Exception:
            pass # Fallback to solid if face selection fails
            
    solids.append(box)
    
    # Update position cursor for the next object
    if i < len(spacings):
        gap = spacings[i]
    else:
        gap = 0
        
    current_x += l + gap
    current_y += w + gap

# Combine all individual solids into a single CadQuery object
result = solids[0]
for s in solids[1:]:
    result = result.union(s)