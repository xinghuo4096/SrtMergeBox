'''
示例，合并srt到srt，合并srt到ass
'''
from Srt import merge_ass_tofile, merge_srt_tofile

merge_srt_tofile(first_subtitle_fname='indata/test_cn.srt',
                 second_subtitle_fname='indata/test_en.srt',
                 new_subtitle_fname='outdata/test_new_srt1.srt',
                 unalign_subtitle_fname='outdata/test_new_srt1_unalign.srt',
                 mark1='', mark2='')

merge_ass_tofile(first_subtitle_fname='indata/test_cn.srt',
                 second_subtitle_fname='indata/test_en.srt',
                 new_subtitle_fname='outdata/test_new_ass3.ass',
                 unalign_subtitle_fname='outdata/test_new_ass3_unalgin.txt',
                 ass_template_fname='indata/test_ass_template_cn_en.txt',
                 mark1='', mark2='')
