# Mismo algoritmo, tres destinos: el tamaño del paso en el descenso del gradiente

Estado: aprobado
Fecha: 2026-10-28

## Pregunta principal
¿Por qué el mismo descenso del gradiente, desde el mismo punto, puede
converger despacio, converger rápido o escaparse al infinito?

## Objetivo didáctico
El espectador entiende que la tasa de aprendizaje η controla si el descenso
del gradiente converge, y que en f(x) = x² cada paso multiplica x por (1 − 2η),
de modo que converge si y solo si 0 < η < 1.

## Público y nivel previo
Personas interesadas en IA con conocimientos previos del tema.
Suposición (a confirmar): saben qué es una derivada como pendiente, han oído
hablar del descenso del gradiente y del término "tasa de aprendizaje", pero no
han analizado por qué un valor concreto converge o diverge.

## Formato
Vertical 9:16 · 45–50 s · tono directo y preciso, sin exageraciones.

## Gancho (0–3 s)
1. Tres puntos salen del mismo sitio en la misma parábola; solo cambia un
   número. Uno llega despacio, otro en un instante y otro sale disparado.
2. "Mismo algoritmo, mismo punto de partida, tres resultados distintos."

## Estructura por escenas
| # | Idea | Duración | Visual sugerido |
|---|------|----------|-----------------|
| 1 | Gancho: tres trayectorias desde x₀ = 1 | 0–4 s | Parábola, tres puntos de color etiquetados η = 0,1 / 0,4 / 1,2 |
| 2 | La regla: x ← x − η·f′(x); con f(x) = x², f′(x) = 2x | 4–13 s | Tangente en el punto, flecha del paso proporcional a la pendiente |
| 3 | η = 0,1: pasos cortos, converge despacio | 13–21 s | Puntos sucesivos 1 → 0,8 → 0,64…; contador de pasos |
| 4 | η = 0,4: converge en pocos pasos | 21–28 s | 1 → 0,2 → 0,04 → 0,008 |
| 5 | η = 1,2: salta al otro lado cada vez más lejos | 28–37 s | 1 → −1,4 → 1,96 → −2,74, la cámara se aleja |
| 6 | Por qué: cada paso multiplica x por (1 − 2η); converge si \|1 − 2η\| < 1, es decir 0 < η < 1 | 37–46 s | Ecuación con los tres factores 0,8 / 0,2 / −1,4 |
| 7 | Cierre: en IA η se ajusta; en problemas reales el límite no tiene una fórmula tan simple | 46–50 s | Texto breve |

## Afirmaciones a verificar
| # | Afirmación | Tipo | Cómo se verifica | Estado |
|---|------------|------|------------------|--------|
| 1 | La actualización del descenso del gradiente es x ← x − η·f′(x) | hecho | Fuente: Oyinlola (2023), freeCodeCamp: «b = a - γ Δ f(a)» | verificado (fuente divulgativa) |
| 2 | Para f(x) = x², x_{k+1} = (1 − 2η)·x_k | hecho | Cálculo: f′(x) = 2x ⇒ x − 2ηx | verificado (cálculo) |
| 3 | Converge a 0 si y solo si \|1 − 2η\| < 1 ⇔ 0 < η < 1 (con x₀ ≠ 0) | hecho | Cálculo: progresión geométrica de razón 1 − 2η | verificado (cálculo) |
| 4 | Con x₀ = 1: η = 0,1 necesita 21 pasos hasta \|x\| < 0,01; η = 0,4 necesita 3 | hecho | Ejecutado en borrador (scratchpad); repetir como test | verificado (ejecución preliminar) |
| 5 | Con η = 1,2 la secuencia es 1, −1,4, 1,96, −2,744… y diverge | hecho | Ejecutado en borrador; repetir como test | verificado (ejecución preliminar) |
| 6 | En el entrenamiento de modelos de IA, la tasa de aprendizaje es un hiperparámetro que hay que ajustar | hecho | Fuente: Oyinlola (2023): «importante elegir cuidadosamente la tasa de aprendizaje» | verificado (fuente divulgativa) |
| 7 | En problemas reales el valor límite de η no tiene una fórmula tan simple | hecho (cualitativo) | Fuente sobre funciones L-suaves (η < 2/L; aquí L = 2 ⇒ η < 1) | por verificar |
| 8 | Imagen de "tres destinos" | decisión creativa | — | — |

## Comprobaciones ejecutables propuestas
- `descenso_gradiente(df, x0, eta, n)` devuelve la trayectoria completa.
- Para f(x) = x² y η ∈ {0,1; 0,4; 0,9; 1,2}: x_k = (1 − 2η)^k · x₀ en cada paso
  (tolerancia numérica).
- Pasos hasta |x| < 0,01 con x₀ = 1: 21 para η = 0,1; 3 para η = 0,4.
- η = 1,2: |x_k| estrictamente creciente.
- Casos límite: η = 0 (no se mueve), η = 0,5 (llega a 0 en un paso),
  η = 1 (oscila entre 1 y −1 sin converger), x₀ = 0 (ya está en el mínimo).
- Correspondencia: la escena de Manim lee la trayectoria generada por la
  función probada; un test comprueba que los puntos animados son esos.

## Malentendidos a evitar
- "El gradiente apunta al mínimo": −f′ indica la dirección de descenso local,
  no la posición del mínimo. En 1D coincide en signo, pero no se debe
  generalizar en la narración.
- "Un paso más grande siempre es más rápido": el vídeo lo desmiente con η = 1,2.
- "Oscilar es divergir": η = 0,9 oscila y converge. No se muestra, pero la
  narración no debe equiparar "saltar al otro lado" con divergir; la
  divergencia es que el salto crece.
- "η = 0,5 es el valor ideal en general": solo es exacto en x²; no mencionarlo
  o aclararlo.
- "Siempre encuentra el mínimo global": fuera de alcance; no afirmarlo.

## Fuentes
- Oyinlola, S. (2023). «Descenso de gradiente: ejemplo de algoritmo de aprendizaje
  automático». freeCodeCamp en español (trad. A. Torres), 19-05-2023.
  https://www.freecodecamp.org/espanol/news/descenso-de-gradiente-ejemplo-de-algoritmo-de-aprendizaje-automaticod/
  Consultada 2026-10-28 (aportada por el usuario). Respalda las afirmaciones 1 y 6.
  No trata condiciones de convergencia (afirmación 7).
- Goodfellow, I., Bengio, Y. y Courville, A. (2016). *Deep Learning*. MIT Press.
  §4.3 (optimización basada en gradiente) y cap. 8. — por verificar sección exacta.
- Boyd, S. y Vandenberghe, L. (2004). *Convex Optimization*. Cambridge University
  Press. §9.3 (método del gradiente). — por verificar sección exacta.
- Cálculo propio de la recurrencia para f(x) = x² (afirmaciones 2–5).

## Supuestos
- Función de una variable, convexa y cuadrática: f(x) = x².
- Tasa de aprendizaje constante; gradiente exacto (no estocástico).
- Punto de partida x₀ = 1.
- El resultado 0 < η < 1 es exacto solo para esta función; no se presenta
  como regla general para redes neuronales.

## Decisiones creativas
- Comparar tres trayectorias en paralelo en lugar de una sola.
- Colores fijos por η en todo el vídeo.
- Valores 0,1 / 0,4 / 1,2 elegidos porque producen comportamientos
  claramente distintos en pocos pasos.
- No usar la analogía de "bajar una montaña con niebla" para no añadir
  elementos que no se verifican; la parábola ya es la montaña.

## Herramienta visual sugerida
Manim: es una gráfica 2D con puntos, tangentes y ecuaciones; no necesita 3D.

## Cuestiones sin verificar
- Afirmación 7 (límite de η en problemas reales): sin fuente. Reformular el
  cierre o verificarla con Boyd y Vandenberghe antes del guion.
- Las citas de la fuente se obtuvieron mediante una lectura automática de la
  página; conviene que el usuario las confirme a mano.
- Si el público conoce realmente la notación f′(x) o conviene decir "pendiente".
- Si 45–50 s es suficiente para la escena 6 sin acelerar la narración.
