'''
字幕合并测试用例
'''
import os
from Srt import (merge_ass_tofile,
                 merge_srt_tofile, merge_srt_tostr)


def test_merge_srt_tostr():
    '''
    合并到list
    '''
    newsub, unalignsub = merge_srt_tostr('indata/test_cn.srt',
                                         'indata/test_en.srt')
    assert len(newsub) > 0
    assert len(unalignsub) > 0
    assert len(newsub) == 1165
    assert len(unalignsub) == 31


def test_merge_srt_tofile():
    '''
    测试合并到srt
    '''
    merge_srt_tofile('indata/test_cn.srt', 'indata/test_en.srt',
                     'outdata/test_merge_srt_tofile.srt',
                     'outdata/test_merge_srt_tofile.unalign.srt')
    assert os.path.isfile('outdata/test_merge_srt_tofile.srt')
    assert os.path.isfile('outdata/test_merge_srt_tofile.unalign.srt')


def test_merge_ass_tofile():
    '''
    测试合并到ass
    '''

    file1 = 'outdata/test_new.ass'
    file2 = 'outdata/test_ass_unalign.txt'

    file3 = 'outdata/test_merge_ass_tofile2.ass'
    file4 = 'outdata/test_merge_ass_tofile2.unalign.txt'

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
    '''
    main用于调试
    '''
    test_merge_srt_tofile()


if __name__ == '__main__':
    main()
