import cadquery as cq

# Parametric dimensions
pipe_length = 200.0       # Total length of the pipe
pipe_od = 50.0            # Outer diameter of the main pipe body
wall_thickness = 3.0      # Thickness of the pipe wall

# Socket (bell end) dimensions
socket_length = 40.0      # Length of the flared socket section
socket_od_start = pipe_od # Outer diameter where socket starts (matches pipe)
socket_od_end = 60.0      # Outer diameter at the widest part of the socket
lip_length = 5.0          # Length of the small lip at the very end
lip_od = 64.0             # Outer diameter of the lip

# Derived dimensions
pipe_id = pipe_od - (2 * wall_thickness)
main_body_length = pipe_length - socket_length - lip_length

# 1. Create the main straight pipe body
# We create a solid cylinder first
main_body = cq.Workplane("XY").circle(pipe_od / 2.0).extrude(main_body_length)

# 2. Create the flared socket section
# This connects the main body to the lip. It's a conical frustum (loft)
# We start at the end of the main body
socket_face = main_body.faces(">Z")

# We create a new workplane at the end of the main body for the socket start
# And another sketch plane offset by the socket length for the socket end
socket_solid = (
    socket_face.workplane()
    .circle(socket_od_start / 2.0)
    .workplane(offset=socket_length)
    .circle(socket_od_end / 2.0)
    .loft(combine=True)
)

# 3. Create the end lip
# This is a short cylinder at the end of the socket
lip_solid = (
    socket_solid.faces(">Z")
    .workplane()
    .circle(lip_od / 2.0)
    .extrude(lip_length, combine=True)
)

# 4. Hollow out the entire shape to create the pipe
# We select the faces at both ends (Z min and Z max) to define the through-hole
# Since we combined everything into one object (lip_solid), we use that.
# Shelling with a negative thickness removes material from the inside.
# Alternatively, we could bore it out, but shell is cleaner for uniform thickness 
# following the flared contour. However, standard pipes often have a straight bore
# or a bore that follows the outer contour. The image suggests the inner wall follows 
# the outer shape (constant wall thickness).

result = lip_solid.faces("<Z").shell(-wall_thickness)

# If the shell operation fails or produces unexpected geometry on complex lofts, 
# a boolean subtraction of a scaled inner shape is another approach. 
# But for this simple loft, shell usually works well. 
# Let's ensure the ends are open. The 'shell' command in CadQuery with a face list
# keeps those faces open. If we just pass a thickness, it shells the whole solid (hollow inside).
# To make a pipe, we need to remove the end faces.

result = lip_solid.faces("<Z or >Z").shell(-wall_thickness)