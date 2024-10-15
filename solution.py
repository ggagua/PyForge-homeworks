import numpy as np
from scipy.io import wavfile
import re


class SoundWaveFactory:
    SAMPLING_RATE = 44100  # like 44.1 KHz
    DURATION_SECONDS = 5
    SOUND_ARRAY_LEN = SAMPLING_RATE * DURATION_SECONDS
    MAX_AMPLITUDE = 2 ** 13

    NOTES = {
        '0': 0, 'e0': 20.60172, 'f0': 21.82676, 'f#0': 23.12465, 'g0': 24.49971, 'g#0': 25.95654, 'a0': 27.50000, 'a#0': 29.13524,
        'b0': 30.86771, 'c0': 32.70320, 'c#0': 34.64783, 'd0': 36.70810, 'd#0': 38.89087,
        'e1': 41.20344, 'f1': 43.65353, 'f#1': 46.24930, 'g1': 48.99943, 'g#1': 51.91309, 'a1': 55.00000, 'a#1': 58.27047,
        'b1': 61.73541, 'c1': 65.40639, 'c#1': 69.29566, 'd1': 73.41619, 'd#1': 77.78175,
        'e2': 82.40689, 'f2': 87.30706, 'f#2': 92.49861, 'g2': 97.99886, 'g#2': 103.8262, 'a2': 110.0000, 'a#2': 116.5409,
        'b2': 123.4708, 'c2': 130.8128, 'c#2': 138.5913, 'd2': 146.8324, 'd#2': 155.5635,
        'e3': 164.8138, 'f3': 174.6141, 'f#3': 184.9972, 'g3': 195.9977, 'g#3': 207.6523, 'a3': 220.0000, 'a#3': 233.0819,
        'b3': 246.9417, 'c3': 261.6256, 'c#3': 277.1826, 'd3': 293.6648, 'd#3': 311.1270,
        'e4': 329.6276, 'f4': 349.2282, 'f#4': 369.9944, 'g4': 391.9954, 'g#4': 415.3047, 'a4': 440.0000, 'a#4': 466.1638,
        'b4': 493.8833, 'c4': 523.2511, 'c#4': 554.3653, 'd4': 587.3295, 'd#4': 622.2540,
        'e5': 659.2551, 'f5': 698.4565, 'f#5': 739.9888, 'g5': 783.9909, 'g#5': 830.6094, 'a5': 880.0000, 'a#5': 932.3275,
        'b5': 987.7666, 'c5': 1046.502, 'c#5': 1108.731, 'd5': 1174.659, 'd#5': 1244.508,
        'e6': 1318.510, 'f6': 1396.913, 'f#6': 1479.978, 'g6': 1567.982, 'g#6': 1661.219, 'a6': 1760.000, 'a#6': 1864.655,
        'b6': 1975.533, 'c6': 2093.005, 'c#6': 2217.461, 'd6': 2349.318, 'd#6': 2489.016,
        'e7': 2637.020, 'f7': 2793.826, 'f#7': 2959.955, 'g7': 3135.963, 'g#7': 3322.438, 'a7': 3520.000, 'a#7': 3729.310,
        'b7': 3951.066, 'c7': 4186.009, 'c#7': 4434.922, 'd7': 4698.636, 'd#7': 4978.032,
    }

    def __init__(self):
        self.notes = []

    @staticmethod
    def get_normed_sin(timeline, frequency):
        """Calculate the normalized sine wave for a given timeline and frequency.

        Args:
            timeline (np.ndarray): The time points at which to calculate the sine wave.
            frequency (float): The frequency of the sine wave.

        Returns:
            np.ndarray: The normalized sine wave values.
        """
        return SoundWaveFactory.MAX_AMPLITUDE * np.sin(2 * np.pi * frequency * timeline)

    @staticmethod
    def get_soundwave(timeline, note):
        """Generate a sound wave based on the given note.

        Args:
            timeline (np.ndarray): The time points for the sound wave.
            note (str): The musical note to generate.

        Returns:
            np.ndarray: The sound wave corresponding to the specified note.
        """
        return SoundWaveFactory.get_normed_sin(timeline, SoundWaveFactory.NOTES[note])

    @staticmethod
    def create_note(note="a4", duration=DURATION_SECONDS):
        """Create a sound wave for a specific note and duration.

        Args:
            note (str): The musical note to create.
            duration (float): The duration of the note in seconds.

        Returns:
            np.ndarray: The sound wave for the specified note and duration.
        """
        timeline = np.linspace(0, duration, num=SoundWaveFactory.SOUND_ARRAY_LEN)
        sound_wave = SoundWaveFactory.get_soundwave(timeline, note).astype(np.int16)
        return sound_wave

    def save_wave(self, wave, name, file_type='txt'):
        """Save the generated sound wave to a file in the specified format.

        Args:
            wave (np.ndarray): The sound wave to save.
            name (str): The name of the file to save the wave to.
            file_type (str): The type of file ('WAV' or 'txt').

        Raises:
            ValueError: If the specified file type is not supported.
        """
        if file_type == 'WAV':
            wavfile.write(name, SoundWaveFactory.SAMPLING_RATE, wave)
        else:
            np.savetxt(name, wave)

    @staticmethod
    def read_wave_from_txt(file_path):
        """Read a sound wave from a text file.

        Args:
            file_path (str): The path to the text file containing the wave data.

        Returns:
            np.ndarray: The sound wave read from the file.
        """
        return np.loadtxt(file_path)

    @staticmethod
    def print_wave_details(wave):
        """Print details about the sound wave, including its length and amplitude.

        Args:
            wave (np.ndarray): The sound wave for which to print details.
        """
        print(f"Wave Details:\nLength: {len(wave)}\nMax Amplitude: {np.max(wave)}\nMin Amplitude: {np.min(wave)}")

    @staticmethod
    def normalize_sound_waves(waves):
        """Normalize a list of sound waves to the same length and amplitude.

        Args:
            waves (list of np.ndarray): The list of sound waves to normalize.

        Returns:
            np.ndarray: An array of normalized sound waves.
        """
        min_length = min(len(wave) for wave in waves)
        normalized_waves = []
        for wave in waves:
            normalized_wave = wave[:min_length] / np.max(np.abs(wave))  # Normalize amplitude
            normalized_waves.append(normalized_wave)
        return np.array(normalized_waves)

    @staticmethod
    def convert_wave_type(wave, wave_type='triangular'):
        """Convert the sound wave to a specified wave type (triangular or square).

        Args:
            wave (np.ndarray): The sound wave to convert.
            wave_type (str): The type of wave to convert to ('triangular' or 'square').

        Returns:
            np.ndarray: The converted sound wave.

        Raises:
            ValueError: If the specified wave type is unsupported.
        """
        x = np.linspace(0, 1, len(wave))
        if wave_type == 'triangular':
            return (2 * np.abs(2 * (x - np.floor(x + 0.5))) - 1) * SoundWaveFactory.MAX_AMPLITUDE
        elif wave_type == 'square':
            return np.sign(wave) * SoundWaveFactory.MAX_AMPLITUDE
        else:
            raise ValueError("Unsupported wave type. Choose 'triangular' or 'square'.")

    @staticmethod
    def apply_adsr(wave, attack=0.1, decay=0.1, sustain=0.7, release=0.1):
        """Apply an ADSR (Attack, Decay, Sustain, Release) envelope to the sound wave.

        Args:
            wave (np.ndarray): The sound wave to modify.
            attack (float): The duration of the attack phase.
            decay (float): The duration of the decay phase.
            sustain (float): The sustain level after decay.
            release (float): The duration of the release phase.

        Returns:
            np.ndarray: The sound wave after applying the ADSR envelope.
        """
        total_length = len(wave)
        attack_length = int(total_length * attack)
        decay_length = int(total_length * decay)
        release_length = int(total_length * release)

        envelope = np.zeros(total_length)
        envelope[:attack_length] = np.linspace(0, 1, attack_length)
        envelope[attack_length:attack_length + decay_length] = np.linspace(1, sustain, decay_length)
        envelope[-release_length:] = np.linspace(sustain, 0, release_length)

        return wave * envelope

    @staticmethod
    def combine_waves(waves):
        """Combine multiple sound waves into a single wave.

        Args:
            waves (list of np.ndarray): The sound waves to combine.

        Returns:
            np.ndarray: The combined sound wave.
        """
        return np.sum(waves, axis=0)

    @staticmethod
    def generate_melody(melody_str):
        """Generate a melody from a string representation of notes and their durations.

        Args:
            melody_str (str): A string containing notes and optional durations.

        Returns:
            np.ndarray: The combined sound wave for the generated melody.
        """
        notes_with_duration = re.findall(r'([a-g][#]?\d)(\s\d*\.?\d*s)?', melody_str)
        combined_wave = None
        for note, duration in notes_with_duration:
            duration = float(duration[:-1]) if duration else SoundWaveFactory.DURATION_SECONDS
            wave = SoundWaveFactory.create_note(note, duration)
            combined_wave = wave if combined_wave is None else combined_wave + wave
        return combined_wave


if __name__ == "__main__":
    factory = SoundWaveFactory()
    a4_wave = factory.create_note()
    factory.save_wave(a4_wave, 'a4_sin.txt')