#!/usr/bin/env python3
"""
stepper.py - turn smooth video into stepped stop-motion.

  python3 stepper.py in.mp4 out.mp4 [--step 12] [--wobble 2] [--flicker 5]

Nearest-frame sampling only. Never blends. Wobble/flicker are generated once
per SAMPLED frame and held for its whole duration - that's what makes it read
as a camera not seated properly in its mount, rather than video noise.
"""
import argparse, os, random, shutil, subprocess, sys, tempfile
from PIL import Image, ImageEnhance

def run(cmd):
    subprocess.run(cmd, check=True, capture_output=True)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("src"); p.add_argument("dst")
    p.add_argument("--step", type=int, default=12, help="stepped frame rate")
    p.add_argument("--wobble", type=float, default=2.0, help="register wobble, px")
    p.add_argument("--flicker", type=float, default=5.0, help="exposure flicker, %%")
    p.add_argument("--seed", type=int, default=None)
    a = p.parse_args()
    if a.seed is not None: random.seed(a.seed)

    tmp = tempfile.mkdtemp(prefix="stepper_")
    raw, out = os.path.join(tmp, "raw"), os.path.join(tmp, "out")
    os.makedirs(raw); os.makedirs(out)
    try:
        # 1. sample at the step rate. fps filter = nearest frame, no blending.
        run(["ffmpeg","-v","error","-i",a.src,"-vf",f"fps={a.step}",
             os.path.join(raw,"f_%05d.png")])

        frames = sorted(os.listdir(raw))
        if not frames: sys.exit("no frames extracted")

        for fn in frames:
            im = Image.open(os.path.join(raw, fn)).convert("RGB")
            w, h = im.size
            if a.wobble > 0:
                # overscan so the wobble never exposes an empty edge
                im = im.resize((int(w*1.02), int(h*1.02)), Image.LANCZOS)
                im = im.rotate(random.uniform(-0.3, 0.3), resample=Image.BICUBIC)
                ow, oh = im.size
                cx = (ow-w)//2 + int(random.uniform(-a.wobble, a.wobble))
                cy = (oh-h)//2 + int(random.uniform(-a.wobble, a.wobble))
                cx = max(0, min(cx, ow-w)); cy = max(0, min(cy, oh-h))
                im = im.crop((cx, cy, cx+w, cy+h))
            if a.flicker > 0:
                im = ImageEnhance.Brightness(im).enhance(
                    1.0 + random.uniform(-a.flicker, a.flicker)/100.0)
            im.save(os.path.join(out, fn))

        # 2. reassemble at the step rate, doubled into a 24fps container.
        #    each sampled frame is held - the motion is stepped, playback is smooth.
        run(["ffmpeg","-v","error","-y","-framerate",str(a.step),
             "-i",os.path.join(out,"f_%05d.png"),
             "-i",a.src,"-map","0:v","-map","1:a?","-c:a","copy",
             "-r","24","-c:v","libx264","-crf","18","-pix_fmt","yuv420p", a.dst])
        print(f"{a.dst}  ({len(frames)} sampled frames @ {a.step}fps)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    main()
