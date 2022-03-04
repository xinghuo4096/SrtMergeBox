
from Srt import merge_subtitle, merge_subtitle_tofile


def test_merge_subtitle():
    newsub, unalignsub = merge_subtitle(
        'tests/test_cn.srt', 'tests/test_en.srt')
    assert len(newsub) > 0
    assert len(unalignsub) > 0
    assert len(newsub) == 1165
    assert len(unalignsub) == 31


def test_merge_subtitle_tofile():
    merge_subtitle_tofile('tests/test_cn.srt', 'tests/test_en.srt',
                          'tests/test_new_subtitle.srt', 'tests/test_unalign_subtitle.srt')
    import os
    assert os.path.isfile('tests/test_new_subtitle.srt')
    assert os.path.isfile('tests/test_unalign_subtitle.srt')


# -----------main
def main():
    pass


if __name__ == '__main__':
    main()
