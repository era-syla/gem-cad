import cadquery as cq
import math

# ==========================================
# Parameters and Dimensions
# ==========================================

# Wedge (Left Part)
wedge_depth = 60.0    # X direction length
wedge_width = 80.0    # Y direction width
wedge_h_front = 75.0  # Height at the front face
wedge_h_back = 30.0   # Height at the back

# Plate (Right Part)
plate_depth = 60.0    # X direction
plate_width = 100.0   # Y direction
plate_height = 25.0   # Z direction
gap = 40.0            # Gap between wedge and plate

# Dovetail Geometry
dt_opening = 10.0     # Width of slot opening at surface
dt_height = 6.0       # Depth of slot
dt_angle = 60.0       # Dovetail angle in degrees
dt_spacing = 30.0     # Distance between slot centers (Y axis)

# Gib (Key)
gib_length = 35.0

# ==========================================
# Helper Functions
# ==========================================

def get_dovetail_profile(center_y, bottom_z, w, h, angle):
    """
    Returns a list of points for a dovetail cutout profile (trapezoid).
    w: opening width at bottom
    h: height of cut
    angle: angle of the dovetail cut
    """
    rad = math.radians(angle)
    offset = h / math.tan(rad)
    
    # Points defining the trapezoid (material to be removed)
    # The shape widens as it goes up (undercut)
    p1 = (center_y - w/2, bottom_z)
    p2 = (center_y - w/2 - offset, bottom_z + h)
    p3 = (center_y + w/2 + offset, bottom_z + h)
    p4 = (center_y + w/2, bottom_z)
    
    return [p1, p2, p3, p4]

# ==========================================
# Part 1: Wedge Block
# ==========================================

# 1. Create Base Block (positioned -X direction relative to origin)
# Origin is centered in Y, bottom at Z=0, Front face at X=0
wedge = (cq.Workplane("XY")
         .box(wedge_depth, wedge_width, wedge_h_front, centered=False)
         .translate((-wedge_depth, -wedge_width/2, 0))
         )

# 2. Cut Slope
# Cutting tool defined on XZ plane to slice off the top
# Slope goes from h_front at X=0 to h_back at X=-wedge_depth
slope_profile = (cq.Workplane("XZ")
                 .moveTo(0, wedge_h_front)
                 .lineTo(-wedge_depth, wedge_h_back)
                 .lineTo(-wedge_depth, wedge_h_front + 10)
                 .lineTo(0, wedge_h_front + 10)
                 .close()
                 .extrude(wedge_width + 10, both=True) # Cut across all Y
                 )
wedge = wedge.cut(slope_profile)

# 3. Cut Dovetail Slots on Bottom
# Slots run along X axis. Profile is visible on the YZ plane (Front Face).
pts_dt1 = get_dovetail_profile(-dt_spacing/2, 0, dt_opening, dt_height, dt_angle)
pts_dt2 = get_dovetail_profile(dt_spacing/2, 0, dt_opening, dt_height, dt_angle)

dt_cutter_wedge = (cq.Workplane("YZ")
                   .workplane(offset=0) # At X=0 face
                   .polyline(pts_dt1).close()
                   .polyline(pts_dt2).close()
                   .extrude(-wedge_depth) # Cut into the block (-X direction)
                   )
wedge = wedge.cut(dt_cutter_wedge)

# 4. Add Side Features (Vertical Rib/Step)
# Cut a relief on the right side (+Y) to create a stepped flange appearance
step_width = 5.0
step_cut = (cq.Workplane("XY")
            .box(wedge_depth, 10, wedge_h_front, centered=False)
            .translate((-wedge_depth, wedge_width/2 - step_width, 10))
            )
# wedge = wedge.cut(step_cut) # (Optional refinement based on image)


# ==========================================
# Part 2: Mounting Plate
# ==========================================

# 1. Create Base Block
# Positioned at X = gap
plate = (cq.Workplane("XY")
         .box(plate_depth, plate_width, plate_height, centered=False)
         .translate((gap, -plate_width/2, 0))
         )

# 2. Cut Dovetail Slots on Face facing Wedge
# Profile same as wedge, extruded into the plate (+X)
dt_cutter_plate = (cq.Workplane("YZ")
                   .workplane(offset=gap) # Start at front face of plate
                   .polyline(pts_dt1).close()
                   .polyline(pts_dt2).close()
                   .extrude(plate_depth)
                   )
plate = plate.cut(dt_cutter_plate)

# 3. Add Top Mounting Holes (Counterbored)
plate = (plate.faces(">Z").workplane()
         .rect(plate_depth - 15, plate_width - 15, forConstruction=True)
         .vertices()
         .cboreHole(6.5, 11.0, 7.0)
         )

# 4. Add Adjustment Holes on Front Face
# Face normal is -X. 
plate = (plate.faces("<X").workplane()
         .center(0, 5) # Shift up in Z (Local Y)
         .rarray(25, 1, 3, 1) # Array along global Y (Local X)
         .hole(5.0, depth=25.0)
         )


# ==========================================
# Part 3: Gib Key
# ==========================================

# Fits into one of the dovetail slots
# Located in the gap, partially inserted
gib = (cq.Workplane("YZ")
       .polyline(pts_dt2).close() # Use profile of the right slot
       .extrude(gib_length)
       )

# Add a hole in the gib
gib = (gib.faces(">Z").workplane()
       .center(0, 0)
       .hole(3.5)
       )

# Position the Gib
# Move it into the gap area
gib = gib.translate((gap - 15, 0, 0))


# ==========================================
# Final Assembly
# ==========================================

result = wedge.union(plate).union(gib)