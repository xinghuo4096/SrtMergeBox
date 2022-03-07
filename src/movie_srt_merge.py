'''
示例，合并srt到srt，合并srt到ass
'''
from Srt import merge_ass_tofile, merge_srt_tofile

merge_srt_tofile(first_subtitle_fname='indata/test_cn.srt',
                 second_subtitle_fname='indata/test_en.srt',
                 new_subtitle_fname='outdata/movie_new_srt.srt',
                 unalign_subtitle_fname='outdata/movie_new_srt.unalign.txt',
                 mark1='', mark2='')

merge_ass_tofile(first_subtitle_fname='indata/test_cn.srt',
                 second_subtitle_fname='indata/test_en.srt',
                 new_subtitle_fname='outdata/moviet_new_ass.ass',
                 unalign_subtitle_fname='outdata/movie_new_ass.unalgin.txt',
                 ass_template_fname='indata/test_ass_template_cn_en.txt',
                 mark1='', mark2='')
