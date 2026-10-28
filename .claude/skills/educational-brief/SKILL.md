---
name: educational-brief
description: Genera el brief de un vídeo educativo vertical en español sobre física o algoritmos a partir de un tema o idea. Úsala cuando se proponga un tema nuevo de vídeo, se pida "un brief", "una idea de vídeo" o planificar un vídeo antes del guion. Es la primera etapa del flujo; no escribe guion ni código.
---

# Educational brief

Primera etapa del flujo de videolab. Convierte un tema en un brief que el usuario
aprueba antes de pasar a guion (`script-storyboard`).

## Entrada

Un tema o idea (p. ej. "caída libre", "búsqueda binaria"). Necesitas además
público, nivel previo y enfoque. Si falta alguno, pregunta antes de escribir;
no asumas valores por defecto. Si hay varios enfoques posibles, propón 2–3 con
ventajas e inconvenientes y deja elegir. Duración orientativa: 30–60 s.

## Salida

Escribe `videos/<slug>/brief.md` (slug en minúsculas con guiones, sin tildes) con
esta estructura:

```markdown
# <Título provisional>

Estado: pendiente de aprobación
Fecha: <AAAA-MM-DD>

## Pregunta principal
La única pregunta que responde el vídeo.

## Objetivo didáctico
Una frase: qué entiende el espectador al terminar.

## Público y nivel previo
Quién lo ve y qué se supone que ya sabe. Marca lo que sea suposición.

## Formato
Vertical 9:16 · duración objetivo · tono.

## Gancho (0–3 s)
Pregunta, paradoja o imagen inicial. 1–2 alternativas.

## Estructura por escenas
| # | Idea | Duración | Visual sugerido |
|---|------|----------|-----------------|

## Afirmaciones a verificar
Toda afirmación que aparecerá en narración o pantalla.
| # | Afirmación | Tipo | Cómo se verifica | Estado |
|---|------------|------|------------------|--------|
Tipo: hecho · analogía · decisión creativa.
Cómo se verifica: fuente concreta, test ejecutable o cálculo.
Estado: verificado · por verificar.

## Comprobaciones ejecutables propuestas
Tests que el código debe pasar antes de animar (resultados esperados,
casos límite, correspondencia entre pasos visualizados y algoritmo).

## Malentendidos a evitar
Errores conceptuales típicos sobre el tema y cómo no reforzarlos.

## Fuentes
Referencias verificables (libro, artículo, documentación). Marca como
"por verificar" lo que no hayas comprobado. Nunca inventes referencias.

## Supuestos
Simplificaciones físicas o algorítmicas (sin rozamiento, n potencia de 2…).

## Decisiones creativas
Elecciones de estilo, metáforas y ritmo, separadas de lo factual.

## Herramienta visual sugerida
Manim, Blender o mixto, con una línea de justificación.

## Cuestiones sin verificar
Lista explícita de lo pendiente de comprobar antes de aprobar el guion.
```

## Reglas

- Mantén separadas fuentes, supuestos y decisiones creativas.
- Una afirmación solo es "verificado" si se ha comprobado con una fuente
  consultada, un cálculo o un test ejecutado; la opinión de un modelo no basta.
- No descargues recursos ni consultes servicios de pago.
- No avances a guion: termina mostrando un resumen del brief y pidiendo
  aprobación. Al aprobarse, cambia `Estado:` a `aprobado`.
- Si el brief ya existe, propón los cambios antes de sobrescribirlo.
