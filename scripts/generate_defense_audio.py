"""Synthesize an original quiet, breathy Mourning Flesh moan. No sampled voices."""
from pathlib import Path
import math
import random
import struct
import wave

ROOT = Path(__file__).resolve().parents[1]


def main():
    rate, duration = 22050, 2.1
    randomizer = random.Random(714)
    samples, phase = [], 0.0
    for i in range(int(rate * duration)):
        t = i / rate
        frequency = 105 - 25 * t / duration + 4 * math.sin(2 * math.pi * 4.5 * t)
        phase += 2 * math.pi * frequency / rate
        voice = 0.0
        for harmonic in range(1, 16):
            f = harmonic * frequency
            formant = math.exp(-((f - 430) / 150) ** 2) + .45 * math.exp(-((f - 1000) / 250) ** 2)
            voice += math.sin(harmonic * phase) * formant / harmonic
        envelope = math.sin(math.pi * t / duration) ** 1.6
        samples.append((voice + randomizer.uniform(-.035, .035)) * envelope)
    peak = max(abs(v) for v in samples)
    output = ROOT / 'mods/sevenfall/audio/sf-mourning.wav'
    output.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output), 'wb') as stream:
        stream.setnchannels(1)
        stream.setsampwidth(2)
        stream.setframerate(rate)
        stream.writeframes(b''.join(struct.pack('<h', round(v / peak * 6500)) for v in samples))
    print(output)


if __name__ == '__main__':
    main()
