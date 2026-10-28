"""Renderiza un vídeo a partir de videos/<slug>/video.toml.

Uso:
    uv run python scripts/render.py <slug> [--calidad borrador|final]

Pasos: escenas con Manim -> audio -> montaje y subtítulos con FFmpeg
-> verificación con ffprobe -> manifest.json.

No reintenta: ante un error lo registra en render/render.log y termina
con código distinto de cero.
"""

import argparse
import datetime
import hashlib
import json
import platform
import subprocess
import sys
import tomllib
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def sha256(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def primera_linea(cmd: list[str]) -> str:
    salida = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return salida.stdout.splitlines()[0].strip()


def commit_git() -> dict:
    try:
        commit = primera_linea(["git", "rev-parse", "HEAD"])
    except subprocess.CalledProcessError:
        commit = None  # repositorio sin commits
    cambios = subprocess.run(
        ["git", "status", "--porcelain"], cwd=RAIZ, capture_output=True, text=True
    ).stdout.strip()
    return {"commit": commit, "cambios_sin_commit": bool(cambios)}


class Registro:
    def __init__(self, ruta: Path):
        self.ruta = ruta
        self.ruta.parent.mkdir(parents=True, exist_ok=True)

    def __call__(self, mensaje: str):
        linea = f"{datetime.datetime.now().isoformat(timespec='seconds')} {mensaje}"
        print(linea)
        with self.ruta.open("a", encoding="utf-8") as f:
            f.write(linea + "\n")


def ejecutar(cmd: list[str], log: Registro, cwd: Path | None = None):
    log("$ " + " ".join(cmd))
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        log(f"ERROR (código {res.returncode}):\n{res.stderr[-3000:]}")
        sys.exit(1)


def sondear(video: Path) -> dict:
    salida = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "stream=codec_type,width,height,r_frame_rate:format=duration",
         "-of", "json", str(video)],
        capture_output=True, text=True, check=True,
    )
    datos = json.loads(salida.stdout)
    v = next(s for s in datos["streams"] if s["codec_type"] == "video")
    return {
        "ancho": v["width"],
        "alto": v["height"],
        "fps": v["r_frame_rate"],
        "duracion_s": float(datos["format"]["duration"]),
        "tiene_audio": any(s["codec_type"] == "audio" for s in datos["streams"]),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    parser.add_argument("--calidad", choices=["borrador", "final"], default="borrador")
    args = parser.parse_args()

    dir_video = RAIZ / "videos" / args.slug
    spec = tomllib.loads((dir_video / "video.toml").read_text(encoding="utf-8"))
    calidad = spec["calidad"][args.calidad]
    dir_render = dir_video / "render" / args.calidad
    dir_render.mkdir(parents=True, exist_ok=True)
    log = Registro(dir_video / "render" / "render.log")
    log(f"--- render {args.slug} ({args.calidad})")

    # 1. Escenas
    clips = []
    for escena in spec["escenas"]:
        if escena["motor"] != "manim":
            log(f"ERROR: motor no soportado: {escena['motor']}")
            sys.exit(1)
        ejecutar([
            sys.executable, "-m", "manim", "render",
            str(dir_video / escena["archivo"]), escena["clase"],
            "--resolution", f"{calidad['ancho']},{calidad['alto']}",
            "--fps", str(calidad["fps"]),
            "--media_dir", str(dir_render / "manim"),
            "--output_file", escena["id"],
            "--disable_caching", "--progress_bar", "none",
        ], log)
        clip = next((dir_render / "manim" / "videos").rglob(f"{escena['id']}.mp4"))
        clips.append(clip)

    if len(clips) != 1:
        log("ERROR: el montaje de varias escenas aún no está implementado")
        sys.exit(1)

    # 2. Audio
    audio = dir_render / "audio.wav"
    a = spec["audio"]
    ejecutar([
        "ffmpeg", "-y", "-hide_banner", "-f", "lavfi",
        "-i", f"sine=frequency={a['frecuencia_hz']}:duration={spec['formato']['duracion_s']}",
        "-af", f"volume={a['volumen']}", str(audio),
    ], log)

    # 3. Montaje + subtítulos. FFmpeg se ejecuta dentro de la carpeta del vídeo
    # para pasar el .srt con ruta relativa y evitar el escapado de rutas de
    # Windows (dos puntos, espacios, tildes) en el filtro subtitles.
    sub = spec["subtitulos"]
    final = dir_render / f"{args.slug}.mp4"
    ejecutar([
        "ffmpeg", "-y", "-hide_banner", "-i", str(clips[0]), "-i", str(audio),
        "-vf", f"subtitles={sub['archivo']}:force_style='{sub['estilo']}'",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
        "-map", "0:v:0", "-map", "1:a:0", "-shortest", str(final),
    ], log, cwd=dir_video)

    # 4. Verificación
    medido = sondear(final)
    esperado_s = spec["formato"]["duracion_s"]
    comprobaciones = {
        "resolucion": (medido["ancho"], medido["alto"]) == (calidad["ancho"], calidad["alto"]),
        "duracion": abs(medido["duracion_s"] - esperado_s) <= spec["formato"]["tolerancia_s"],
        "audio": medido["tiene_audio"],
    }

    # 5. Manifiesto
    entradas = [dir_video / "video.toml", dir_video / sub["archivo"], RAIZ / "uv.lock",
                Path(__file__)] + [dir_video / e["archivo"] for e in spec["escenas"]]
    manifiesto = {
        "fecha": datetime.datetime.now().isoformat(timespec="seconds"),
        "slug": args.slug,
        "calidad": args.calidad,
        "parametros": calidad,
        "git": commit_git(),
        "versiones": {
            "python": platform.python_version(),
            "manim": primera_linea([sys.executable, "-m", "manim", "--version"]),
            "ffmpeg": primera_linea(["ffmpeg", "-version"]),
            "so": platform.platform(),
        },
        "entradas": {str(p.relative_to(RAIZ).as_posix()): sha256(p) for p in entradas},
        "salida": {"archivo": final.relative_to(RAIZ).as_posix(), "sha256": sha256(final)},
        "medido": medido,
        "comprobaciones": comprobaciones,
    }
    (dir_video / f"manifest-{args.calidad}.json").write_text(
        json.dumps(manifiesto, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    log(f"comprobaciones: {comprobaciones}")
    if not all(comprobaciones.values()):
        log("ERROR: alguna comprobación ha fallado")
        sys.exit(1)
    log(f"OK -> {final}")


if __name__ == "__main__":
    main()
