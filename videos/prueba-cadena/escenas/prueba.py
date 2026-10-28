"""Escena de prueba: texto y una forma en movimiento durante 5 s exactos."""

from manim import BLUE, DOWN, UP, Circle, FadeOut, Scene, Text, Write, config

# Marco vertical 9:16 en unidades de Manim; la resolución en píxeles
# la fija scripts/render.py según la calidad.
config.frame_width = 9
config.frame_height = 16


class Prueba(Scene):
    def construct(self):
        titulo = Text("Prueba de la cadena", font_size=60).to_edge(UP, buff=2)
        circulo = Circle(radius=1, color=BLUE, fill_opacity=0.6).shift(UP * 2)

        self.play(Write(titulo), run_time=1)
        self.play(circulo.animate.shift(DOWN * 4), run_time=3)
        self.play(FadeOut(titulo, circulo), run_time=1)
