import cadquery as cq
import math

# --- Dimensions ---
width = 400.0
depth = 420.0
seat_height = 450.0
total_height = 850.0
leg_size = 40.0
seat_thickness = 25.0
apron_height = 50.0
apron_thickness = 20.0
back_tilt_angle = 12.0  # degrees

# --- Derived Parameters ---
leg_len_lower = seat_height - seat_thickness
# Calculate leg center positions (legs are at the corners)
x_leg_center = width / 2.0 - leg_size / 2.0
y_leg_front = -depth / 2.0 + leg_size / 2.0
y_leg_back = depth / 2.0 - leg_size / 2.0

# --- Geometry Construction ---

# 1. Seat
# Created as a box centered on XY, elevated to seat height
seat = (cq.Workplane("XY")
        .box(width, depth, seat_thickness)
        .translate((0, 0, seat_height - seat_thickness / 2.0)))

# 2. Front Legs
# Vertical legs extending from floor to bottom of seat
f_leg = (cq.Workplane("XY")
         .box(leg_size, leg_size, leg_len_lower)
         .translate((x_leg_center, y_leg_front, leg_len_lower / 2.0)))
front_legs = f_leg.union(f_leg.mirror("YZ"))

# 3. Back Legs (Lower Section)
# Vertical part under the seat
b_leg_lower = (cq.Workplane("XY")
               .box(leg_size, leg_size, leg_len_lower)
               .translate((x_leg_center, y_leg_back, leg_len_lower / 2.0)))
back_legs_lower = b_leg_lower.union(b_leg_lower.mirror("YZ"))

# 4. Backrest (Upper Leg Sections)
# These extend from the seat level up to total_height, tilted backwards
back_vertical_rise = total_height - leg_len_lower
upright_length = back_vertical_rise / math.cos(math.radians(back_tilt_angle))

upright = (cq.Workplane("XY")
           .box(leg_size, leg_size, upright_length)
           # Align bottom face to origin for rotation
           .translate((0, 0, upright_length / 2.0))
           # Rotate backwards
           .rotate((0, 0, 0), (1, 0, 0), back_tilt_angle)
           # Move to position on top of the lower rear leg
           .translate((x_leg_center, y_leg_back, leg_len_lower)))
back_uprights = upright.union(upright.mirror("YZ"))

# 5. Backrest Rails (Horizontal bars)
rail_height = 30.0
rail_gap = 15.0
rail_width_inner = width - 2 * leg_size

def create_angled_rail(offset_from_top_edge):
    """Creates a rail positioned relative to the top of the angled uprights."""
    dist_along_upright = upright_length - offset_from_top_edge
    
    # Calculate offsets based on the tilt angle
    y_offset = dist_along_upright * math.sin(math.radians(back_tilt_angle))
    z_offset = dist_along_upright * math.cos(math.radians(back_tilt_angle))
    
    return (cq.Workplane("XY")
            .box(rail_width_inner, leg_size, rail_height)
            .rotate((0, 0, 0), (1, 0, 0), back_tilt_angle)
            .translate((0, y_leg_back + y_offset, leg_len_lower + z_offset)))

# Top rail (aligned with top edge)
top_rail = create_angled_rail(rail_height / 2.0)
# Middle rail (below the top rail with a gap)
mid_rail = create_angled_rail(rail_height + rail_gap + rail_height / 2.0)

# 6. Aprons (Support frame under the seat)
# Front Apron
apron_front = (cq.Workplane("XY")
               .box(width - 2*leg_size, apron_thickness, apron_height)
               .translate((0, y_leg_front, leg_len_lower - apron_height / 2.0)))

# Back Apron
apron_back = (cq.Workplane("XY")
              .box(width - 2*leg_size, apron_thickness, apron_height)
              .translate((0, y_leg_back, leg_len_lower - apron_height / 2.0)))

# Side Aprons
apron_side = (cq.Workplane("XY")
              .box(apron_thickness, depth - 2*leg_size, apron_height)
              .translate((x_leg_center, 0, leg_len_lower - apron_height / 2.0)))
apron_sides = apron_side.union(apron_side.mirror("YZ"))

# --- Assembly ---
result = (seat
          .union(front_legs)
          .union(back_legs_lower)
          .union(back_uprights)
          .union(top_rail)
          .union(mid_rail)
          .union(apron_front)
          .union(apron_back)
          .union(apron_sides))