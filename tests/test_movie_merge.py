from ast import match_case
import datetime
from Srt import Srt, detect_code, load_srt_fromfile, merge_to_srt, merge_srt_tofile


def test_merge_subtitle():
    newsub, unalignsub = merge_to_srt('tests/test_cn.srt', 'tests/test_en.srt')
    assert len(newsub) > 0
    assert len(unalignsub) > 0
    assert len(newsub) == 1165
    assert len(unalignsub) == 31


def test_merge_subtitle_tofile():
    merge_srt_tofile('tests/test_cn.srt', 'tests/test_en.srt',
                     'outdata/test_new_subtitle.srt',
                     'outdata/test_unalign_subtitle.srt')
    import os
    assert os.path.isfile('outdata/test_new_subtitle.srt')
    assert os.path.isfile('outdata/test_unalign_subtitle.srt')


def test_merge_ass_tofile():

    ass_template = 'tests/test_ass_template_cn_en.txt'
    f1 = open(ass_template, 'rb')
    str1 = f1.read()
    f1.close()

    str1 = detect_code(str1)[0]
    assert isinstance(str1, str)

    str1 = str1.replace('\r', '')

    ass_info_style = str1[str1.find('[Script Info]'):str1.find('[Events]')]

    ass_text = str1[str1.find('Dialogue'
                              ):str1.find('{language2_subtitle_text}') + 25]

    ass_info_style = ass_info_style.replace('{softname}', 'srt mergen box')
    ass_info_style = ass_info_style.replace('{softurl}', 'xinghuo4096')
    ass_info_style = ass_info_style.replace('{title}', 'title')
    ass_info_style = ass_info_style.replace('{Original_file}', 'srt')
    ass_info_style = ass_info_style.replace('{update_name}', 'npc')
    ass_info_style = ass_info_style.replace('{update_detial}',
                                            str(datetime.datetime.now()))

    srts = load_srt_fromfile('tests/test_cn.srt')
    texts = []
    text = ''
    for item in srts:
        assert isinstance(item, Srt)
        text = ass_text

        text = text.replace('{start_time}',
                            format_subtitle_ass(item.start_time))
        text = text.replace('{end_time}', format_subtitle_ass(item.end_time))
        languages=item.text.split('\n')
        match len(languages):
            case 1:
                text = text.replace('{language1_subtitle_text}', languages[0])
                text = text[:text.find(r'\N{\fn')]
            case 2:
                text = text.replace('{language1_subtitle_text}', languages[0])
                text = text.replace('{language2_subtitle_text}', languages[1])   
            case _:
                text = text.replace('{language1_subtitle_text}', languages[:-1])
                text = text.replace('{language2_subtitle_text}', ''.joing(languages[-1]))   
 
            
        
        texts.append(text)
    ass = ass_info_style + '\n'.join(texts)

    savesrt = ass
    fname = 'outdata/test.txt'
    f1 = open(fname, 'w', 1000, 'utf-8')
    f1.write(savesrt)
    f1.close()
    print()


def format_subtitle_ass(t_time):
    str.format
    return '{0:1d}:{1:0>2d}:{2:0>2d}.{3:0>2d}'.format(
        t_time.hour, t_time.minute, t_time.second, t_time.microsecond // 10000)


# -----------main
def main():
    test_merge_ass_tofile()


if __name__ == '__main__':
    main()
