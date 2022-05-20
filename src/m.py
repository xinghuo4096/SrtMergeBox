'''
调用的示例

'''
from Srt import merge_ass_tofile, Srt

merge_ass_tofile(first_subtitle_fname='z:/tests/a.cn.srt',
                 second_subtitle_fname='z:/tests/a.en.srt',
                 new_subtitle_fname='z:/tests/a.cnen.ass',
                 unalign_subtitle_fname='z:/tests/a.unalgin.txt',
                 ass_template_fname='indata/test_ass_template_cn_en.txt',
                 mark1='', mark2='', mini_time=Srt.MINI_MERGE_TIME, max_cnsubtitle=26)
