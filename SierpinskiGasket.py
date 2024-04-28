import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import *
import ctypes

# Vertex shader source code
vertex_shader_source = """
#version 330 core
in vec2 position;  // Input attribute for vertex position
void main()
{
    gl_Position = vec4(position, 0.0, 1.0);  // Set the position of the vertex
}
"""

# Fragment shader source code
fragment_shader_source = """
#version 330 core
out vec4 color;  // Output attribute for fragment color
void main()
{
    color = vec4(1.0, 0.0, 0.0, 0.2);  // Set the color of the fragment to red
}
"""

class SierpinskiGasket:
    def __init__(self):
        pass

    def draw_triangle(self, v1, v2, v3):
        glBegin(GL_TRIANGLES)  # Begin drawing triangles
        glVertex2fv(v1)  # Define the first vertex of the triangle
        glVertex2fv(v2)  # Define the second vertex of the triangle
        glVertex2fv(v3)  # Define the third vertex of the triangle
        glEnd()  # End drawing triangles

    def divide_triangle(self, v1, v2, v3, depth):
        if depth == 0:  # Base case: stop recursion if depth is 0
            self.draw_triangle(v1, v2, v3)  # Draw the triangle
            return
        # Calculate midpoints of triangle edges
        v12 = [(v1[0] + v2[0]) / 2, (v1[1] + v2[1]) / 2]
        v23 = [(v2[0] + v3[0]) / 2, (v2[1] + v3[1]) / 2]
        v31 = [(v3[0] + v1[0]) / 2, (v3[1] + v1[1]) / 2]
        # Recursively divide the triangle into smaller triangles
        self.divide_triangle(v1, v12, v31, depth - 1)
        self.divide_triangle(v12, v2, v23, depth - 1)
        self.divide_triangle(v31, v23, v3, depth - 1)

    def draw_gasket(self):
        vertices = [  # Define the vertices of the initial triangle
            (-1.0, -1.0),  # Define the first vertex of the initial triangle
            (0.0, 1.0),    # Define the second vertex of the initial triangle
            (1.0, -1.0)    # Define the third vertex of the initial triangle
        ]

        # Compile vertex shader from the provided source code
        vertex_shader = compileShader(vertex_shader_source, GL_VERTEX_SHADER)

        # Compile fragment shader from the provided source code
        fragment_shader = compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)

        # Create a shader program object
        shader_program = glCreateProgram()

        # Attach the compiled vertex shader to the shader program
        glAttachShader(shader_program, vertex_shader)

        # Attach the compiled fragment shader to the shader program
        glAttachShader(shader_program, fragment_shader)

        # Link the shader program, which combines the shaders into a single executable program
        glLinkProgram(shader_program)

        # Use the shader program for rendering
        glUseProgram(shader_program)


        running = True
        while running:  # Main loop for rendering
            for event in pygame.event.get():  # Check for events
                if event.type == pygame.QUIT:  # If the window is closed, quit the application
                    running = False

            glClear(GL_COLOR_BUFFER_BIT)  # Clear the color buffer
            for i in range(3):  # Iterate over each vertex of the initial triangle
                glLoadIdentity()  # Reset the modelview matrix
                glTranslatef(vertices[i][0], vertices[i][1], 0.0)  # Translate to the position of the current vertex
                # Divide the triangle into smaller triangles and draw the Sierpinski Gasket
                self.divide_triangle(vertices[i], vertices[(i + 1) % 3], vertices[(i + 2) % 3], depth=5)

            pygame.display.flip()  # Swap buffers to display the rendered frame


if __name__ == "__main__":  # Entry point of the program
    pygame.init()  # Initialize pygame
    pygame.display.set_caption('Sierpinski Gasket')
    display = (900, 600)  # Set the size of the display window
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)  # Create a window
    gasket = SierpinskiGasket()
    gasket.draw_gasket()
