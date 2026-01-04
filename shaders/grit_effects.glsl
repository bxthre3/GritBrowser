#ifdef GL_ES
    precision highp float;
#endif

varying vec2 tex_coord0;
uniform sampler2D texture0;
uniform float grayscale_amount;
uniform float blue_light_filter;
uniform float zen_mode;

void main (void)
{
    vec4 color = texture2D(texture0, tex_coord0);
    
    // Grayscale calculation
    float gray = dot(color.rgb, vec3(0.299, 0.587, 0.114));
    vec3 gray_color = mix(color.rgb, vec3(gray), grayscale_amount);
    
    // Blue light filter (warmth)
    vec3 warm_color = gray_color;
    warm_color.r *= 1.0;
    warm_color.g *= 0.9;
    warm_color.b *= 0.7;
    vec3 final_color = mix(gray_color, warm_color, blue_light_filter);
    
    // Zen Mode: Blackout non-essential (simulated by darkening)
    final_color = mix(final_color, vec3(0.05), zen_mode * 0.9);
    
    gl_FragColor = vec4(final_color, color.a);
}
