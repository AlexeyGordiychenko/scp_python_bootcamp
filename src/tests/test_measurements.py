from measurements import Measurements


def test_measurements_correct(monkeypatch):
    inputs = ["12", "60", "1", "8"]
    input_generator = (i for i in inputs)
    monkeypatch.setattr('builtins.input', lambda x: next(input_generator))
    measurements = Measurements()
    measurements.measure()
    assert measurements.respiration == [12]
    assert measurements.heart_rate == [60]
    assert measurements.blushing_level == [1]
    assert measurements.pupillary_dilation == [8]


def test_measurements_incorrect_respiration(monkeypatch):
    inputs_resp = ["1", "-1", "10", "lkj", "18", "111", "14"]
    inputs_other = ["60", "1", "8"]
    input_generator = (i for i in inputs_resp + inputs_other)
    monkeypatch.setattr('builtins.input', lambda x: next(input_generator))
    measurements = Measurements()
    measurements.measure()
    assert measurements.respiration == [14]
    assert measurements.heart_rate == [60]
    assert measurements.blushing_level == [1]
    assert measurements.pupillary_dilation == [8]


def test_measurements_incorrect_heart_rate(monkeypatch):
    inputs_before = ["16"]
    inputs_hr = ["wers", "33", "115", "-8", "333", "-66", "80"]
    inputs_after = ["1", "8"]
    input_generator = (i for i in inputs_before + inputs_hr + inputs_after)
    monkeypatch.setattr('builtins.input', lambda x: next(input_generator))
    measurements = Measurements()
    measurements.measure()
    assert measurements.respiration == [16]
    assert measurements.heart_rate == [80]
    assert measurements.blushing_level == [1]
    assert measurements.pupillary_dilation == [8]


def test_measurements_incorrect_blush(monkeypatch):
    inputs_before = ["16", "80"]
    inputs_blush = ["-1", "33", "115", "oiuxcv", "333", "-66", "5"]
    inputs_after = ["8"]
    input_generator = (i for i in inputs_before + inputs_blush + inputs_after)
    monkeypatch.setattr('builtins.input', lambda x: next(input_generator))
    measurements = Measurements()
    measurements.measure()
    assert measurements.respiration == [16]
    assert measurements.heart_rate == [80]
    assert measurements.blushing_level == [5]
    assert measurements.pupillary_dilation == [8]


def test_measurements_incorrect_pup(monkeypatch):
    inputs_before = ["16", "80", "5"]
    inputs_pup = [".,kjii", "12", "88", "oiuxcv", "-8", "66", "4"]
    input_generator = (i for i in inputs_before + inputs_pup)
    monkeypatch.setattr('builtins.input', lambda x: next(input_generator))
    measurements = Measurements()
    measurements.measure()
    assert measurements.respiration == [16]
    assert measurements.heart_rate == [80]
    assert measurements.blushing_level == [5]
    assert measurements.pupillary_dilation == [4]


def test_measurements_incorrect_all(monkeypatch):
    inputs_resp = ["1", "-1", "10", "lkj", "18", "111", "14"]
    inputs_hr = ["wers", "33", "115", "-8", "333", "-66", "80"]
    inputs_blush = ["-1", "33", "115", "oiuxcv", "333", "-66", "5"]
    inputs_pup = [".,kjii", "12", "88", "oiuxcv", "-8", "66", "4"]
    input_generator = (i for i in inputs_resp +
                       inputs_hr + inputs_blush + inputs_pup)
    monkeypatch.setattr('builtins.input', lambda x: next(input_generator))
    measurements = Measurements()
    measurements.measure()
    assert measurements.respiration == [14]
    assert measurements.heart_rate == [80]
    assert measurements.blushing_level == [5]
    assert measurements.pupillary_dilation == [4]
