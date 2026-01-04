#ifdef GL_ES
    precision highp float;
#endif

varying vec2 tex_coord0;
uniform sampler2D texture0;
uniform float gray_scale;

void main (void)
{
    vec4 color = texture2D(texture0, tex_coord0);
    float gray = dot(color.rgb, vec3(0.299, 0.587, 0.114));
    gl_FragColor = vec4(mix(color.rgb, vec3(gray), gray_scale), color.a);
}
