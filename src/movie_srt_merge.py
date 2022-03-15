'''
示例，合并srt到srt，合并srt到ass
'''
import datetime
from Srt import merge_ass_tofile, merge_srt_tofile, Srt

merge_srt_tofile(first_subtitle_fname='indata/test_cn.srt',
                 second_subtitle_fname='indata/test_en.srt',
                 new_subtitle_fname='outdata/movie_new_srt.srt',
                 unalign_subtitle_fname='outdata/movie_new_srt.unalign.txt',
                 mark1='', mark2='', mini_time=Srt.MINI_MERGE_TIME)

merge_ass_tofile(first_subtitle_fname='indata/test_cn.srt',
                 second_subtitle_fname='indata/test_en.srt',
                 new_subtitle_fname='outdata/moviet_new_ass.ass',
                 unalign_subtitle_fname='outdata/movie_new_ass.unalgin.txt',
                 ass_template_fname='indata/test_ass_template_cn_en.txt',
                 mark1='', mark2='', mini_time=datetime.timedelta(microseconds=300*1000))

merge_srt_tofile(first_subtitle_fname='z:/tests/cn.srt',
                 second_subtitle_fname='z:/tests/en.srt',
                 new_subtitle_fname='z:/tests/new_srt.srt',
                 unalign_subtitle_fname='z:/tests/new_srt.unalign.txt',
                 mark1='', mark2='', mini_time=Srt.MINI_MERGE_TIME)

merge_ass_tofile(first_subtitle_fname='z:/tests/cn.srt',
                 second_subtitle_fname='z:/tests//en.srt',
                 new_subtitle_fname='z:/tests/new_ass.ass',
                 unalign_subtitle_fname='z:/tests/new_ass.unalgin.txt',
                 ass_template_fname='indata/test_ass_template_cn_en.txt',
                 mark1='', mark2='', mini_time=Srt.MINI_MERGE_TIME)

for i in range(1, 9):
    fname1 = f'd:/test/test2/test.S01E{i:02d}.1080p.WEB.H264'
    merge_ass_tofile(first_subtitle_fname=f'{fname1}.cn.srt',
                     second_subtitle_fname=f'{fname1}.en.srt',
                     new_subtitle_fname=f'{fname1}.ass',
                     unalign_subtitle_fname=f'{fname1}.unalgin.txt',
                     ass_template_fname='indata/test_ass_template_cn_en.txt',
                     mark1='', mark2='', mini_time=Srt.MINI_MERGE_TIME)
print()
