#version 410 core

in vec2 texcoords;

uniform sampler2D source;

out vec4 color;

void main()
{
    color = texture(source, vec2(texcoords.x, 1.0 - texcoords.y));
}