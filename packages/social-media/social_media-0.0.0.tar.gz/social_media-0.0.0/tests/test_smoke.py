import inspect

import social_media


def test_smoke() -> None:
    assert inspect.ismodule(social_media)
