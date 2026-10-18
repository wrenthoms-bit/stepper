# Stepper

Smooth video in, stop-motion out.

Stepper re-times a clip to a stepped frame rate (12 drawings a second by
default) and holds each drawing across several output frames, the way
stop-motion and hand-drawn animation are shot "on twos". Camera wobble, tilt
and exposure flicker are added once per drawing and held, so it reads as a
camera that isn't quite seated in its mount rather than video noise.

Everything runs in the browser. Clips never leave your device.

## Use it

Open `index.html`, or the hosted copy once GitHub Pages is on. Drop clips in,
adjust, render, save.

- **Drawings per second**: 12 is classic stop-motion. Lower is choppier.
- **Holds**: Even, or Mixed (some drawings held a frame longer, like hand-shot work).
- **Output frame rate**: 24, 25 or 30. Match your edit timeline.
- **Camera wobble / Tilt wobble / Exposure flicker**: per-drawing, never in between.
- **Seed**: the same seed gives the same wobble every time.

Exports MP4: H.264 + AAC in Chrome, Edge and Safari; falls back to VP9/Opus in
browsers without H.264 encoding. Needs WebCodecs (Chrome/Edge, Safari 16.4+,
Firefox 130+).

## Host it on GitHub Pages

Settings → Pages → Source: *Deploy from a branch* → `main` / root → Save.
It's live at `https://wrenthoms-bit.github.io/stepper/` a minute later.

For `stepper.delrogue.com`: add a `CNAME` file containing `stepper.delrogue.com`,
then in Cloudflare DNS add a CNAME record `stepper` → `wrenthoms-bit.github.io`
(DNS only, grey cloud, until GitHub has issued the certificate).

## Files

- `index.html`: the whole app, one file.
- `stepper.fragment.html` + `build.py`: the same page in the Claude artifact
  format; `python3 build.py` regenerates `index.html` from it.
- `cli/stepper.py`: the original command-line version for batch work on a Mac.
  Needs Python 3 and ffmpeg (`brew install ffmpeg`, `pip3 install pillow`).
  `python3 cli/stepper.py in.mp4 out.mp4 --step 12 --wobble 2 --flicker 5`

Uses [mp4-muxer](https://github.com/Vanilagy/mp4-muxer) 5.1.5 (MIT) from jsDelivr.
