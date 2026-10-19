# -*- coding: utf-8 -*-
"""Synthesised UI sound effects for Kayla's Grammar Lab (48 kHz mono, numpy). Soft, sparkly, not harsh."""
import numpy as np, soundfile as sf, os
SR = 48000
OUT = "/home/ubuntu/kslo_grammar/audio/sfx"
os.makedirs(OUT, exist_ok=True)


def env(n, a=0.005, r=0.2):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / r)
    return e


def tone(f, d, a=0.004, r=0.15, harm=(1, 0.3, 0.1)):
    n = int(d * SR); t = np.arange(n) / SR
    y = sum(h * np.sin(2 * np.pi * f * (k + 1) * t) for k, h in enumerate(harm))
    return y * env(n, a, r)


def mix(parts, d):
    y = np.zeros(int(d * SR))
    for t0, x in parts:
        i = int(t0 * SR); y[i:i + len(x)] += x[:len(y) - i]
    return y


def norm(y, peak=0.7):
    return y / (np.abs(y).max() + 1e-9) * peak


def save(name, y, peak=0.7):
    sf.write(f"{OUT}/{name}.wav", norm(y, peak).astype(np.float32), SR)


def noise(d, lp=None):
    n = int(d * SR); x = np.random.default_rng(1).standard_normal(n)
    if lp:
        k = int(SR / lp); x = np.convolve(x, np.ones(k) / k, "same")
    return x


# pop: short bubbly blip with pitch drop
n = int(0.12 * SR); t = np.arange(n) / SR
f = 900 * np.exp(-t * 18) + 380
save("pop", np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.04), 0.55)
# whoosh: filtered noise swell
d = 0.45; x = noise(d, 2500); n = len(x); t = np.arange(n) / SR
save("whoosh", x * np.sin(np.pi * t / d) ** 2, 0.35)
# sparkle: quick rising bell arpeggio (F major)
notes = [698.5, 880, 1046.5, 1396.9]
save("sparkle", mix([(i * 0.055, tone(fq, 0.5, 0.002, 0.18, (1, 0.25, 0.08))) for i, fq in enumerate(notes)], 0.8), 0.5)
# chime / XP level-up: bright bell chord + shimmer
ch = mix([(0, tone(698.5, 1.2, 0.003, 0.5)), (0.06, tone(880, 1.2, 0.003, 0.5)), (0.12, tone(1046.5, 1.2, 0.003, 0.5)),
          (0.18, tone(1396.9, 1.2, 0.003, 0.6, (1, 0.2)))], 1.6)
save("levelup", ch, 0.6)
# tick (countdown)
save("tick", tone(1500, 0.08, 0.001, 0.02, (1, 0.5, 0.2)), 0.45)
# correct: two-note ding up
save("correct", mix([(0, tone(1046.5, 0.5, 0.002, 0.18)), (0.1, tone(1568, 0.7, 0.002, 0.3))], 0.9), 0.55)
# buzzer: soft cartoon "nope" (two low square-ish tones)
def sq(fq, d):
    n = int(d * SR); t = np.arange(n) / SR
    return np.tanh(3 * np.sin(2 * np.pi * fq * t)) * env(n, 0.005, d / 2)
save("buzz", mix([(0, sq(220, 0.18)), (0.2, sq(185, 0.3))], 0.55), 0.4)
# click (UI snap)
save("click", tone(2400, 0.04, 0.0005, 0.01, (1, 0.4)), 0.35)
# glitch: short digital stutter for wipes
g = noise(0.25, 6000) * (np.sign(np.sin(2 * np.pi * 30 * np.arange(int(0.25 * SR)) / SR)) > 0)
save("glitch", g * env(len(g), 0.002, 0.12), 0.3)
# sting: logo hit (sub thump + chord)
n = int(1.2 * SR); t = np.arange(n) / SR
thump = np.sin(2 * np.pi * (60 + 80 * np.exp(-t * 20)) * t) * np.exp(-t * 6)
save("sting", thump * 0.8 + mix([(0, tone(349.2, 1.2, 0.002, 0.6)), (0, tone(523.3, 1.2, 0.002, 0.6)),
                                  (0, tone(698.5, 1.2, 0.002, 0.6))], 1.2), 0.6)
print(sorted(os.listdir(OUT)))
