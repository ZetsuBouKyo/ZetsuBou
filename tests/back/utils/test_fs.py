from back.utils.fs import alphanum_sorting


def test_alphanum_sorting():
    data = [
        (["z11", "z2"], ["z2", "z11"]),
        (
            ["12 sheets", "4 sheets", "48 sheets", "booklet"],
            ["4 sheets", "12 sheets", "48 sheets", "booklet"],
        ),
    ]
    for d in data:
        d[0].sort(key=alphanum_sorting)
        assert d[0] == d[1]
