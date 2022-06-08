import os

from src.utils import lookFiles, loadPath


def pytest_configure():
    os.system("python3 src/convert.py")
    return True


def test_getMinFiles():
    assert pytest_configure()
    for root, file in lookFiles(loadPath):
        print(os.path.join(root, file), end=" - ")
        assert ".min" in file
