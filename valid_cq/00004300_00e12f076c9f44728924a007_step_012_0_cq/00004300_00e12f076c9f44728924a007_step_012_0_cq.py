import cadquery as cq

# --- Parametric Dimensions ---
panel_width = 300.0   # Width of the panel
panel_height = 500.0  # Height of the panel
panel_thickness = 40.0 # Total thickness of the panel

# Joint details (Tongue and Groove / Ship Lap style)
joint_depth = 15.0     # How deep the cutout goes into the edge
joint_width = 15.0     # The width of the joint step (vertical/horizontal overlap)
groove_width = 5.0    # Width of any small separation groove, if visible (visual gap)

# The image shows a specific profile:
# - A main body.
# - The top edge has a step cutout on the front face.
# - The bottom edge has a step cutout on the back face (implied by typical cladding, to interlock).
# - The left edge has a complex profile: a vertical groove and a tongue.
# - The right edge seems to be a simple tongue or flat edge, likely meant to mate with the left.

# Let's simplify the interpretation based on the single view:
# It looks like a standard wall panel with a shiplap or tongue-and-groove system on all four sides.
# Top: Recessed ledge on the back (or front, depending on orientation). Let's assume the visible face is the front.
# The top shows a step down on the back side.
# The bottom shows a step up on the front side (to mate with the panel below).
# Left side: Shows a vertical groove/channel.

# Revised Strategy:
# 1. Create the base block.
# 2. Cut a rabbet (step) along the top edge on the back side.
# 3. Cut a rabbet along the bottom edge on the front side.
# 4. Cut a rabbet along the right edge on the back side.
# 5. Cut a rabbet along the left edge on the front side.
# Looking closely at the left edge in the image: It actually has a double step or a groove.
# There is a thin vertical strip, then a groove, then the main panel face. This suggests a specific interlocking profile.

# Detailed Profile Construction:
# Let's define the cross-section and extrude it, then apply top/bottom cuts. This is usually cleaner for panels.

# Profile (Top-down view of the horizontal cross-section):
# Front face is at y=0. Back face is at y=thickness.
# Let's say Left is x=0, Right is x=width.

# Left Edge Geometry (based on image):
# - It seems to have a "tongue" protruding from the middle/back.
# - There is a "reveal" or groove on the front face.
# Right Edge Geometry:
# - Likely the inverse to mate.

# Let's try a simpler approach that matches the visual blockiness:
# 1. Base Box.
# 2. Subtract from Top-Back.
# 3. Subtract from Bottom-Front.
# 4. Subtract from Right-Back.
# 5. Subtract from Left-Front, but leave a tongue.

# --- Dimensions ---
H = 600.0
W = 400.0
T = 30.0

# Lap joint dimensions
lap_w = 20.0  # Width of the overlap on sides
lap_h = 20.0  # Height of the overlap on top/bottom
lap_d = T / 2.0 # Depth is half thickness

# Left side groove detail
groove_w = 5.0
groove_d = 5.0

# --- Geometry Construction ---

# 1. Start with the main solid block
# Origin at bottom-left-back corner
result = cq.Workplane("XY").box(W, H, T, centered=(True, True, True))

# 2. Create the Top Edge Joint (Rabbet on the back side)
# Removing material from the top-back
# Select top face, select back edge
result = (result
          .faces(">Y") # Top face
          .workplane()
          .rect(W + 10, lap_d * 2) # Rectangle covering width and half thickness
          .cutBlind(-lap_h) # Cut down
          )

# Note on centering: box(centered=True) puts origin at center of mass. 
# Let's shift logic to specific edges for clarity.

# Let's restart with corners more explicitly to match the image features.
# The image shows:
# - Top Edge: A step down on the back half.
# - Left Edge: A step down on the front half, PLUS a small groove.
# - Bottom Edge: (Inferred) A step up on the front half.
# - Right Edge: (Inferred) A step up on the back half.

# Re-defining using a sketch/profile extrusion might be overkill. Boolean ops on a box are easiest.

# Re-initialize parameters based on visual estimation
height = 80.0
width = 50.0
thick = 4.0
step_depth = thick / 2.0
step_width = 3.0 # The margin around the edge

result = cq.Workplane("XY").box(width, height, thick)

# --- Top Edge Feature ---
# Cut away the back half of the top edge
# Create a cutter box
cutter_top = (cq.Workplane("XY")
              .workplane(offset=height/2 - step_width/2)
              .moveTo(0, 0)
              .box(width + 2, step_width, step_depth, centered=(True, True, False)))
# Move cutter to the back face (negative Z relative to center if thick is Z)
# Wait, box default aligns Z. Let's look at coordinate system.
# box(w, h, t): Z is thickness.
# We want to remove material from Z < 0 (back) at Y > (height/2 - step).

result = (result
          .faces(">Y") # Select top face
          .workplane(centerOption="CenterOfMass")
          .moveTo(0, -step_depth/2) # Move to back half
          .rect(width + 1.0, step_depth) # Rectangle width of panel, depth of half thickness
          .cutBlind(-step_width) # Cut downwards
          )

# --- Bottom Edge Feature ---
# Cut away the front half of the bottom edge (so it laps with a panel below)
result = (result
          .faces("<Y") # Select bottom face
          .workplane(centerOption="CenterOfMass")
          .moveTo(0, step_depth/2) # Move to front half
          .rect(width + 1.0, step_depth)
          .cutBlind(-step_width) # Cut upwards
          )

# --- Left Edge Feature (The complex one in the image) ---
# The image shows the left side (or right, depending on view) has a vertical channel.
# Let's assume the left side of the image is the "Left Edge".
# It has a step cut out of the front face, similar to a shiplap.
# AND it looks like there might be a small groove inside that step.

# 1. Main shiplap cut on Left (Front side removed)
result = (result
          .faces("<X") # Left face
          .workplane(centerOption="CenterOfMass")
          .moveTo(step_depth/2, 0) # Move to front half
          .rect(step_depth, height + 1.0) # Rectangle thickness/2 x height
          .cutBlind(-step_width) # Cut inward
          )

# 2. Vertical Groove detail on the Left Edge
# Looking at the image, there is a distinct shadow line vertically near the edge.
# It looks like a small stress-relief or capillary break groove.
# Let's add a small groove on the stepped face we just created.
# We need to select the face created by the previous cut. It faces <X.
# It's located at x = -width/2 + step_width.

result = (result
          .faces("<X") # Select all left-facing faces
          .workplane(centerOption="CenterOfMass")
          # Filter faces to find the one that is recessed
          )

# To avoid complex selectors, let's just make a cutter relative to the main block.
# Groove parameters
groove_w = 0.5
groove_d = 0.5

# Position: On the "tongue" that remains on the back, or on the ledge?
# The image shows the groove is on the main front face, parallel to the edge?
# No, it looks like it's ON the side lap joint.
# Let's just cut a small vertical slot near the left edge on the front face to simulate that detail line.
cutter_groove = (cq.Workplane("XY")
                 .box(groove_w, height + 2.0, groove_d, centered=(True, True, False)))

# Move cutter to position: Left side, Front face
# X = -width/2 + step_width + padding
# Z = thick/2
groove_x_pos = -width/2 + step_width + 0.5
groove_z_pos = thick/2 - groove_d

result = result.cut(
    cutter_groove.translate((groove_x_pos, 0, thick/2 - groove_d))
)

# --- Right Edge Feature ---
# Standard shiplap: Remove back half
result = (result
          .faces(">X") # Right face
          .workplane(centerOption="CenterOfMass")
          .moveTo(-step_depth/2, 0) # Move to back half
          .rect(step_depth, height + 1.0)
          .cutBlind(-step_width) # Cut inward
          )

# --- Final Refinement to match Image ---
# The image specifically shows the Top-Left corner.
# There is a horizontal step at the top.
# There is a vertical feature on the left.
# The vertical feature on the left seems to go ALL the way up, intersecting the top step.
# The current boolean order handles this intersection naturally.

# Let's adjust dimensions to be more proportional to the image.
# Image is tall.
panel_h = 100.0
panel_w = 60.0
panel_t = 5.0
lap_size = 4.0 # Size of the ledge
lap_thick = panel_t / 2.0

# Re-building purely
result = cq.Workplane("XY").box(panel_w, panel_h, panel_t)

# Top Rabbet (Remove Top-Back)
# Select Top Face
# Draw Rect on Back half
# Extrude Cut Down
result = (result
          .faces(">Y")
          .workplane(centerOption="CenterOfMass")
          .moveTo(0, -panel_t/4) # Shift Y center to back half of thickness (Since we are looking at top face, Z is Up, Y is Back... wait local coords)
          # Global Y is Up. Global Z is Thick. 
          # Top Face is Plane(normal=(0,1,0)). Local X is Global X. Local Y is Global Z (Back).
          # We want to cut the "Back" part of the panel thickness.
          # In Global, Back is -Z (if Front is +Z). Or usually Z is up.
          # Let's stick to: Z is thickness. Y is height. X is width.
          # Top Face is at Y = h/2.
          # Workplane on Top Face: Origin at center of face.
          # Local X aligned with Global X.
          # Local Y aligned with Global Z? Or -Z? Standard is projected Z axis.
          # Let's use boolean cuts with explicit boxes to be 100% sure of orientation.
          )

# Reset for explicit boolean approach
R = cq.Workplane("XY").box(panel_w, panel_h, panel_t)

# Top Cut (Back side)
# Box overlap: Width=Full, Height=lap_size, Thick=Half (Back)
top_cutter = (cq.Workplane("XY")
              .box(panel_w + 10, lap_size, lap_thick, centered=(True, False, False))
              .translate((0, panel_h/2 - lap_size, -panel_t/2))
             )
R = R.cut(top_cutter)

# Bottom Cut (Front side)
# Box overlap: Width=Full, Height=lap_size, Thick=Half (Front)
bottom_cutter = (cq.Workplane("XY")
                 .box(panel_w + 10, lap_size, lap_thick, centered=(True, False, False))
                 .translate((0, -panel_h/2, 0)) # Z=0 to Z=thick/2
                )
R = R.cut(bottom_cutter)

# Left Cut (Front side - vertical lap)
# The image shows the left side has the cut on the FRONT (visible) side.
left_cutter = (cq.Workplane("XY")
               .box(lap_size, panel_h + 10, lap_thick, centered=(False, True, False))
               .translate((-panel_w/2, 0, 0)) # Left side, Front half (Z>0)
              )
R = R.cut(left_cutter)

# Right Cut (Back side - vertical lap)
right_cutter = (cq.Workplane("XY")
                .box(lap_size, panel_h + 10, lap_thick, centered=(False, True, False))
                .translate((panel_w/2 - lap_size, 0, -panel_t/2)) # Right side, Back half
               )
R = R.cut(right_cutter)


# Adding the "Groove" detail on the left
# Looking at the image, there is a thin groove inside the left lap area.
# It runs vertically.
groove_width = 1.0
groove_depth = 1.0
groove_cutter = (cq.Workplane("XY")
                 .box(groove_width, panel_h + 10, groove_depth, centered=(True, True, False))
                 .translate((-panel_w/2 + lap_size + groove_width, 0, 0)) # Just inboard of the lap
                )
# Actually, looking at the image, the groove seems to be ON the lap surface or defining the start of the lap.
# Let's put a small V-groove or rectangular groove right at the shoulder of the left lap.
# Position: X = -panel_w/2 + lap_size.
groove_cutter = (cq.Workplane("XY")
                 .box(groove_width, panel_h + 10, groove_depth, centered=(True, True, False))
                 .translate((-panel_w/2 + lap_size, 0, lap_thick - groove_depth))
                )
# This cuts into the remaining thickness of the lap area? No, the lap area is already cut away.
# The groove is likely on the full-thickness part, right next to the step.
groove_cutter = (cq.Workplane("XY")
                 .box(groove_width, panel_h + 10, groove_depth, centered=(True, True, False))
                 .translate((-panel_w/2 + lap_size + groove_width/2, 0, panel_t/2 - groove_depth))
                )

R = R.cut(groove_cutter)

result = R