# pixel-brand-video

**English** | [繁體中文](README.zh-TW.md)

**Create 8-bit pixel-style brand videos with Claude Code: visuals, music, sound effects, mixing, and a license log in one workflow.**

[![Sample video](https://img.youtube.com/vi/7YiMerqztfY/hqdefault.jpg)](https://youtu.be/7YiMerqztfY)

▶ [Watch the sample video on YouTube](https://youtu.be/7YiMerqztfY)

![preview](docs/preview.jpg)

## What is this?

A [Claude Code](https://claude.com/claude-code) **Skill**: a ready-made workflow made of instructions, a template, and scripts.

Once it is installed, tell Claude your topic, brand, and key messages. It will:

1. Use [HyperFrames](https://hyperframes.heygen.com) (HTML → MP4) to turn the 30-second pixel-style template into your own brand video.
2. Pick BGM and sound effects from [Mixkit](https://mixkit.co) (free license), sync them to the picture, mix, and master.
3. Write a `LICENSES.md` file for every asset used, then run automatic QA on duration, loudness, peak level, and the ending fade-out.

## What's inside

```text
pixel-brand-video/
├── SKILL.md                          # The full workflow for Claude
├── assets/
│   ├── template/index.html           # 30-second 16:9 template (search "EDIT:" to change text and colors)
│   ├── placeholders/                 # Placeholder logo, mascot, and pixelated logo steps
│   └── audio-pipeline/build_mix.py   # SFX cue sheet + mixing script, generates the FFmpeg command
├── scripts/
│   ├── fetch_mixkit.py               # List and download Mixkit music and sound effects
│   ├── estimate_bpm.py               # Estimate BPM and first beat, find the drop
│   └── pixelate_logo.py              # Logo → 3-step pixel version for the 8-bit ending
└── references/                       # Licensing notes, mixing notes, license log template
```

## Requirements

- [Claude Code](https://claude.com/claude-code)
- Node.js 22 or later
- [FFmpeg](https://ffmpeg.org)
- Python 3, plus two packages:

```bash
pip install pillow numpy
```

- Recommended: also install the HyperFrames skills:

```bash
npx hyperframes skills
```

## Installation

Copy the `pixel-brand-video` folder into your Claude Code skills directory, then restart Claude Code.

| Scope | Location |
|---|---|
| All projects (personal) | `~/.claude/skills/pixel-brand-video/` (Windows: `C:\Users\<you>\.claude\skills\pixel-brand-video\`) |
| One project only | `<project>/.claude/skills/pixel-brand-video/` |

```bash
git clone https://github.com/thedes13/pixel-brand-video.git
cp -r pixel-brand-video/pixel-brand-video ~/.claude/skills/
```

## Usage

Tell Claude what you want. For example:

> Use pixel-brand-video to make a 30-second video. The brand is "XX Tech", the logo is `logo.png`, and the topic is "E-commerce website redesign". Three key points: speed, SEO, and payment integration. Add music and sound effects, and finish everything without asking me.

- No mascot? Say "no mascot".
- Want your own colors? Give it 3 to 5 brand colors.

## Licensing (important)

- **Code, template, and placeholder images in this repository: [MIT License](LICENSE).**
- **This repository contains no music or sound-effect files.** You download them yourself from Mixkit with `scripts/fetch_mixkit.py`, and they stay under the [Mixkit license](https://mixkit.co/license/):
  - Free for commercial use, no attribution required.
  - BGM cannot be used for TV, radio, or games, and cannot be registered with Content ID.
  - Sound effects cannot be redistributed on their own.
  - Details: [`pixel-brand-video/references/licensing.md`](pixel-brand-video/references/licensing.md).
- The visuals and brand assets in videos you make with the template belong to you. You are responsible for making sure the logos, fonts, images, and any other third-party assets you use are properly licensed.
- The licensing notes here are a reminder for users and are not legal advice. Mixkit's terms can change, so check the official site.

## Known limitations

- The template is 16:9 and 30 seconds. For 9:16 or another length, the layout and timeline need to be adjusted (Claude can do that for you).
- Claude cannot listen to the finished video. Audio QA relies on loudness, peak level, spectrum, and alignment with the picture. Listen with headphones before you publish.

---

Made and shared by 益盛科技 / ES Design ([des13.com](https://des13.com)).
