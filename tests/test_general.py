import pytest
from pambox import general
from scipy.io import wavfile
import numpy as np
import scipy.io as sio


@pytest.fixture
def speech_raw():
    x = wavfile.read("test_files/test_speech_raw_22050.wav")[1]
    return x / 2. ** 15


@pytest.fixture
def noise_raw():
    x = wavfile.read("test_files/test_noise_raw_22050.wav")[1]
    return x / 2. ** 15


@pytest.fixture
def mix_0dB():
    x = wavfile.read("test_files/test_mix_0dB_22050.wav")[1]
    return x / 2. ** 15


@pytest.fixture
def noise_65dB():
    x_65 = wavfile.read("test_files/test_noise_65dB_22050.wav")[1]
    return x_65 / 2. ** 15


def test_set_level(noise_raw, noise_65dB):
    x65 = general.setdbspl(noise_raw, 65)
    np.testing.assert_allclose(x65, noise_65dB, atol=1e-4)


def test_mix_speech_and_noise_0dB(speech_raw, noise_raw, mix_0dB):
    speech65 = general.setdbspl(speech_raw, 65)
    noise65 = general.setdbspl(noise_raw, 65)
    mixed = speech65 + noise65
    np.testing.assert_allclose(mixed, mix_0dB, atol=1e-4)


def test_envelope_extraction():
    mat = sio.loadmat("./test_files/test_envelope.mat")
    x = mat['signal'][0]
    target = mat['envelope'][0]
    envelope = general.hilbert_envelope(x)
    np.testing.assert_allclose(envelope, target, atol=1e-3)


# Can't be done programmatically, because the exact third-octave spacing is not
# exactly the same as the one commonly used.
@pytest.mark.xfail
def test_third_oct_center_freq_bet_63_12500_hz():
    """Test returns correct center frequencies for third-octave filters

    Between 63 and 12500 Hz.

    """
    midfreq = (63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000,
               1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000)
    assert noctave_center_freq(63, 12500, width=3) == midfreq