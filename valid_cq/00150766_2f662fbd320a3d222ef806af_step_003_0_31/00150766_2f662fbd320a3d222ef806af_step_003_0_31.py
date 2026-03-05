import cadquery as cq
import math

# --- Parameters ---
dx = 50.0                # Distance between left and right motors
dy = 65.0                # Distance between front and rear motors
duct_out_r = 20.0        # Duct outer radius
duct_in_r = 18.5         # Duct inner radius
duct_h = 12.0            # Duct height
plate_h = 2.5            # Main plate thickness
hub_out_r = 4.0          # Motor hub outer radius
hub_in_r = 1.5           # Motor hub hole radius
hub_h = 7.0              # Motor hub height
strut_w = 1.5            # Strut width
fc_mount = 25.5          # Standard FC mounting hole spacing
hex_d = 4.5              # Honeycomb hex diameter
hex_gap = 1.2            # Honeycomb wall thickness

motor_pts = [(dx/2, dy/2), (-dx/2, dy/2), (dx/2, -dy/2), (-dx/2, -dy/2)]
fc_pts = [(fc_mount/2, fc_mount/2), (-fc_mount/2, fc_mount/2), (fc_mount/2, -fc_mount/2), (-fc_mount/2, -fc_mount/2)]

# --- 1. Base Plate & Duct Outers ---
# Build each piece as a solid, then union
base_center = cq.Workplane("XY").rect(30, dy).extrude(plate_h)
base_arms_f = cq.Workplane("XY").center(0, dy/2).rect(dx, 24).extrude(plate_h)
base_arms_r = cq.Workplane("XY").center(0, -dy/2).rect(dx, 24).extrude(plate_h)
base_ducts = cq.Workplane("XY").pushPoints(motor_pts).circle(duct_out_r).extrude(plate_h)
base = base_center.union(base_arms_f).union(base_arms_r).union(base_ducts)

# Add full solid duct cylinders (to be hollowed out)
body = base.union(cq.Workplane("XY").pushPoints(motor_pts).circle(duct_out_r).extrude(duct_h))

# --- 2. Cut Duct Inners ---
# Clear out the centers of the ducts entirely
body = body.cut(cq.Workplane("XY").workplane(offset=-5)
                .pushPoints(motor_pts).circle(duct_in_r).extrude(duct_h + 10))

# --- 3. Motor Hubs & Struts ---
body = body.union(cq.Workplane("XY").pushPoints(motor_pts).circle(hub_out_r).extrude(hub_h))

# Create a 3-spoke pattern for the struts
spoke_len = duct_in_r + 0.5 # Extend slightly into duct wall
spoke = cq.Workplane("XY").rect(spoke_len, strut_w, centered=(False, True, False)).extrude(plate_h)
spokes = (spoke
          .union(spoke.rotate((0,0,0), (0,0,1), 120))
          .union(spoke.rotate((0,0,0), (0,0,1), 240))
          .rotate((0,0,0), (0,0,1), 45)) # Offset rotation for aesthetics

# Apply struts to all 4 motor hubs
for p in motor_pts:
    body = body.union(spokes.translate((p[0], p[1], 0)))

# --- 4. Central Features ---
# FC Mounting Pads
body = body.union(cq.Workplane("XY").pushPoints(fc_pts).circle(3.5).extrude(plate_h))

# Generate Honeycomb Pattern
hex_pts = []
R = hex_d / 2.0
W = 1.73205 * R
pitch_x = W + hex_gap
pitch_y = 1.5 * R + hex_gap * 0.86602

for i in range(-8, 9):
    for j in range(-12, 13):
        hx = i * pitch_x
        if j % 2 != 0:
            hx += pitch_x / 2
        hy = j * pitch_y

        # Bounding constraints for hex pattern (avoid edges and pads)
        if abs(hx) < 14.0 and abs(hy) < (dy/2 - 6.0):
            avoid = False
            for fx, fy in fc_pts:
                if math.hypot(hx - fx, hy - fy) < 5.0:
                    avoid = True
                    break
            if not avoid:
                hex_pts.append((hx, hy))

# --- 5. Apply All Cuts ---
cutter_base = cq.Workplane("XY").workplane(offset=-5)
cut_depth = duct_h + 10

# Honeycomb cut
if hex_pts:
    body = body.cut(cutter_base.pushPoints(hex_pts).polygon(6, hex_d).extrude(cut_depth))

# Hub holes
body = body.cut(cutter_base.pushPoints(motor_pts).circle(hub_in_r).extrude(cut_depth))

# FC mounting holes
body = body.cut(cutter_base.pushPoints(fc_pts).circle(1.0).extrude(cut_depth))

# Side utility/zip-tie holes at the waist
body = body.cut(cutter_base.pushPoints([(12.5, 0), (-12.5, 0)]).circle(0.8).extrude(cut_depth))

# --- 6. Fillets ---
try:
    # Fillet the highest edges (+Z) to round off the duct lips
    body = body.edges("+Z").fillet(0.7)
except:
    pass

# Export final geometry
result = body