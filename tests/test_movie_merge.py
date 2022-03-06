from ast import match_case
import datetime
from Srt import Srt, detect_code, load_srt_fromfile, merge_ass_tofile, merge_srt_tostr, merge_srt_tofile, merge_to_ass_str


def test_merge_subtitle():
    newsub, unalignsub = merge_srt_tostr('indata/test_cn.srt',
                                         'indata/test_en.srt')
    assert len(newsub) > 0
    assert len(unalignsub) > 0
    assert len(newsub) == 1165
    assert len(unalignsub) == 31


def test_merge_srt_tofile():
    merge_srt_tofile('indata/test_cn.srt', 'indata/test_en.srt',
                     'outdata/test_new_subtitle.srt',
                     'outdata/test_unalign_subtitle.srt')
    import os
    assert os.path.isfile('outdata/test_new_subtitle.srt')
    assert os.path.isfile('outdata/test_unalign_subtitle.srt')


def test_merge_ass_tofile():

    import os
    file1 = 'outdata/test_new.ass'
    file2 = 'outdata/test_ass_unalign.txt'

    file3 = 'outdata/test_new2.ass'
    file4 = 'outdata/test_ass_unalign2.txt'

    if os.path.isfile(file1):
        os.remove(file1)
    if os.path.isfile(file2):
        os.remove(file2)
    if os.path.isfile(file3):
        os.remove(file3)
    if os.path.isfile(file4):
        os.remove(file4)

    merge_ass_tofile()

    assert os.path.isfile(file1)
    assert os.path.isfile(file2)
    assert not os.path.isfile(file3)
    assert not os.path.isfile(file4)

    merge_ass_tofile(first_subtitle_fname='indata/test_cn.srt', 
                     second_subtitle_fname='indata/test_en.srt',
                     new_subtitle_fname=file3, 
                     unalign_subtitle_fname=file4, 
                     mark1='', mark2='')

    assert os.path.isfile(file1)
    assert os.path.isfile(file2)
    assert os.path.isfile(file3)
    assert os.path.isfile(file4)


# -----------main
def main():
    test_merge_ass_tofile()


if __name__ == '__main__':
    main()
