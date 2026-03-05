import cadquery as cq

# Parametric dimensions for a typical SMD chip resistor (e.g., 1206 or similar)
# All dimensions in mm
length = 3.2  # Total length
width = 1.6   # Total width
height = 0.55 # Thickness
terminal_length = 0.5 # Length of the metal terminals at each end

# Calculate body dimensions
# The black part is slightly shorter than the total length in reality, 
# but often modeled as the full length with terminals on top/bottom/ends.
# Looking at the image, it looks like a central black body with metal caps at the ends.
# Let's model it as a central body and two end caps.

body_length = length - (2 * terminal_length)

# Create the main central body (the black part)
# We start by centering the workplane
main_body = (cq.Workplane("XY")
             .box(length, width, height)
            )

# Create the terminals
# In a realistic model, terminals might wrap around. 
# However, the image shows a simplified blocky look.
# Let's create the two end sections to represent terminals.
# We can do this by creating a full block and then assigning colors, 
# or creating separate solids if we wanted a multi-body object.
# But CadQuery usually returns a single "result" solid.
# The prompt asks for geometry. 
# The image shows the terminals slightly protruding or just distinct at the ends.
# A common way to model this simple shape is just a box.
# But to distinguish the terminals as shown in the image (grey ends), 
# let's make the geometry represent the physical structure: 
# A ceramic core with metal ends.

# Let's construct it as a union of 3 parts to be precise, 
# although a single box is the bounding volume.
# Let's make the "terminals" slightly larger or just distinct segments?
# Actually, looking closely at the image, it's a flat rectangular prism. 
# The visual distinction is material/color.
# Since I can only provide geometry, the best geometric representation is the single solid block 
# representing the component's envelope.
# However, sometimes users want the separate bodies to represent the assembly.
# Let's create a single unioned solid that represents the entire component.

# Re-evaluating the image:
# It looks like a standard rectangular prism.
# The "terminals" are just the ends of the prism.
# The request asks for the "final geometry".
# Simple geometry: Just a box.
# Slightly detailed geometry: A central body and two end caps.

# Let's produce the detailed geometry where the terminals are separate entities fused together
# or just a single block if that's what represents the component best.
# Most CAD models for ECAD are just the bounding box or the body + leads.
# Given the "expert" persona, I will model it as a single solid (the physical chip)
# but I will construct it in a way that dimensions are clear.

# Let's build the central body and two end caps to mimic the structure, 
# even if they fuse into one block, it allows for easier material assignment later if supported.
# But standard STL/STEP export is one mesh.

# Let's stick to the simplest accurate representation: A rectangular box.
# Wait, looking very closely at the crop, the grey terminals seem to be slightly slightly thinner (z-height)
# or maybe it's just the rendering. No, usually terminals are slightly thicker due to solder plating.
# But often modeled as flush.
# The image shows the grey parts at the very ends.

# Let's provide a script that generates the full component shape.
# I will create a central body and two terminals, then union them.
# This is "good practice" for parametric modeling of multi-material parts.

# Component Dimensions (based on standard 1206 Imperial / 3216 Metric)
L = 3.20
W = 1.60
T = 0.55
# Terminal length (metallization)
t_len = 0.50

# Create the main ceramic body
# The body sits in the middle
ceramic_len = L - 2*t_len
ceramic_body = cq.Workplane("XY").box(ceramic_len, W, T)

# Create Terminal 1 (Left)
# Position: -L/2 + t_len/2
term1 = cq.Workplane("XY").center(-L/2 + t_len/2, 0).box(t_len, W, T)

# Create Terminal 2 (Right)
# Position: L/2 - t_len/2
term2 = cq.Workplane("XY").center(L/2 - t_len/2, 0).box(t_len, W, T)

# Combine them into one object
result = ceramic_body.union(term1).union(term2)

# If the user wants just the code:

import cadquery as cq

# Dimensions for a standard SMD Chip Resistor (e.g., 1206 package)
total_length = 3.2
total_width = 1.6
thickness = 0.6
terminal_length = 0.5

# Create the central body (substrate)
# The central body length is total length minus the two terminals
body_length = total_length - (2 * terminal_length)

# Create the center part
center_body = cq.Workplane("XY").box(body_length, total_width, thickness)

# Create the left terminal
# We shift the workplane center to the left
left_terminal = (cq.Workplane("XY")
                 .center(-(total_length/2) + (terminal_length/2), 0)
                 .box(terminal_length, total_width, thickness))

# Create the right terminal
# We shift the workplane center to the right
right_terminal = (cq.Workplane("XY")
                  .center((total_length/2) - (terminal_length/2), 0)
                  .box(terminal_length, total_width, thickness))

# Combine all parts into a single solid object
result = center_body.union(left_terminal).union(right_terminal)

# Note: While geometrically this results in a simple box of size 3.2x1.6x0.6,
# constructing it this way allows for future modification (e.g., making terminals thicker)
# and clearly defines the parametric relationships of the component parts.