import os
import screwdriver


def test_upload(capfd):
    audio_dir = 'audio'
    files = os.listdir(os.path.join(os.path.dirname(__file__), audio_dir))
    for file in files:
        screwdriver.upload_file(os.path.join(audio_dir, file))
        output = capfd.readouterr()
        if file.startswith('26921'):
            assert output.out == "Non-audio file detected\n"
        else:
            assert output.out == "Upload successfully\n"


def test_upload_non_existent(capfd):
    screwdriver.upload_file('nonexistent_file')
    output = capfd.readouterr()
    assert output.out == "File does not exist\n"


def test_list(capfd):
    screwdriver.list_files()
    output = capfd.readouterr()
    assert output.out.splitlines() == sorted(os.listdir(
        os.path.join(os.path.dirname(__file__), 'uploads')))
