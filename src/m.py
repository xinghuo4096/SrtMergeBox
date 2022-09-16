'''
调用的示例

'''
from Srt import merge_ass_tofile, Srt


def mymian():
    '''
    单个处理
    '''
    fname = 'z:/tests/a/test_moveie'

    merge_ass_tofile(first_subtitle_fname=f'{fname}.cn.srt',
                     second_subtitle_fname=f'{fname}.en.3.srt',
                     new_subtitle_fname=f'{fname}.cnen.ass',
                     unalign_subtitle_fname=f'{fname}.unalgin.txt',
                     ass_template_fname='indata/ass_template_cn_en_1280.txt',
                     ass_head_fname='indata/ass_info_head_cn_en_1280.txt',
                     mark1='',
                     mark2='',
                     mini_time=Srt.MINI_MERGE_TIME,
                     max_cnsubtitle=26)


def mymain_batch():
    '''
    批处理
    '''
    for i in range(1, 9):
        fname = f'z:/tests/a/test_moveie.S01E{i:0>2}'
        merge_ass_tofile(
            first_subtitle_fname=f'{fname}.cn.srt',
            second_subtitle_fname=f'{fname}.en.srt',
            new_subtitle_fname=f'{fname}.cnen.ass',
            unalign_subtitle_fname='{fname}.unalgin.txt',
            ass_template_fname='indata/test_ass_template_cn_en.txt',
            ass_head_fname='indata/ass_head_cn_en.txt',
            mark1='',
            mark2='',
            mini_time=Srt.MINI_MERGE_TIME,
            max_cnsubtitle=26)


mymian()
