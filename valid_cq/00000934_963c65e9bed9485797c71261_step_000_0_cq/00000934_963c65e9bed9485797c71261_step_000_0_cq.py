import cadquery as cq

# Parametric dimensions
total_length = 50.0  # Estimated total length
main_diameter = 10.0  # Main diameter of the shaft sections
groove_diameter = 6.0  # Diameter inside the grooves
groove_width = 3.0    # Width of the grooves
head_length = 8.0     # Length of the first large section (the "head")
mid_land_width = 3.0  # Width of the section between grooves
main_body_length = total_length - head_length - (2 * groove_width) - mid_land_width

# Construction logic:
# We will build this by revolving a profile or by stacking cylinders.
# Stacking cylinders is often more readable for simple turned parts in CadQuery.

# 1. Create the "Head" (the leftmost section in the image)
head = cq.Workplane("XY").circle(main_diameter / 2).extrude(head_length)

# 2. Create the first Groove
groove1 = head.faces(">Z").workplane().circle(groove_diameter / 2).extrude(groove_width)

# 3. Create the middle land (the ring between grooves)
mid_land = groove1.faces(">Z").workplane().circle(main_diameter / 2).extrude(mid_land_width)

# 4. Create the second Groove
groove2 = mid_land.faces(">Z").workplane().circle(groove_diameter / 2).extrude(groove_width)

# 5. Create the main body (the long section on the right)
body = groove2.faces(">Z").workplane().circle(main_diameter / 2).extrude(main_body_length)

# Combine into result
result = body

# Alternative single-operation method (more robust):
# Define points for a revolution
# (0,0) -> (R_main, 0) -> (R_main, L_head) -> (R_groove, L_head) 
# -> (R_groove, L_head+W_groove) -> (R_main, L_head+W_groove) ... etc
# But simple extrusion stacking is perfectly valid for this geometry.

if __name__ == "__main__":
    # If running in an environment that supports show_object (like CQ-Editor), display it
    try:
        show_object(result)
    except NameError:
        pass