
import copy
import datetime
import re
import chardet


class Srt:
    SEPARATOR = '-->'
    ENCODING = ['utf-32', 'utf-16', 'utf-8',
                'UTF-8-SIG' 'cp1252', 'gb2312', 'gbk', 'big5']

    def __init__(self, sub_index, sub_time, sub_text) -> None:
        self.index = int(sub_index)

        self.start_time, self.end_time = self._split_time(sub_time)
        self.text = sub_text

    def __str__(self) -> str:
        temp = '{0}\n{1} {2} {3}\n{4}\n'.format(self.index, format_time(
            self.start_time), Srt.SEPARATOR, format_time(self.end_time), self.text)
        return temp

    def _split_time(self, strtime: str):
        t = strtime.split(self.SEPARATOR)
        tstrt = load_time(t[0])
        tend = load_time(t[1])
        return (tstrt, tend)


def detect_code(detect_str: str) -> tuple:
    s = chardet.detect(detect_str)
    str1 = ''
    if s['confidence'] > 0.9:
        str1 = detect_str.decode(s['encoding'], 'ignore')
    else:
        raise Exception(detect_str[0:10]+'... error.'+s['confidence'])
    return str1, s['encoding']


def load_time(srt_time: str) -> datetime.datetime:
    srt_time = srt_time.strip()
    t1 = datetime.datetime.strptime(srt_time, '%H:%M:%S,%f')
    return t1


def format_time(temp_time: datetime.datetime):
    timestr = '{h}:{m}:{s},{ss}'.format(
        h=temp_time.hour, m=temp_time.minute, s=temp_time.second, ss=temp_time.microsecond//1000)
    return timestr


def clear_srt(fname, srts, test='-test-'):
    for item in srts:
        assert isinstance(item, Srt)
        item.text = test + \
            str(item.index)+test+format_time(item.start_time) + \
            '-'+format_time(item.end_time)

    savelist = [str(x) for x in srts]

    savestr = '\n'.join(savelist)

    f1 = open(fname[:-3]+'txt', 'w', 100, 'utf-8')
    f1.write(savestr)
    f1.close()


def load_srt_fromfile(fname):

    f1 = open(fname, 'rb')
    str1 = f1.read()
    f1.close()

    srts = load_srt_from_str(str1)
    return srts


def load_srt_from_str(str1):
    re_srt_index = re.compile('^\d+$')

    subsrt = detect_code(str1)[0]
    subsrt = subsrt.replace('\r', '')
    sublines = [x.strip() for x in subsrt.split("\n") if x.strip()]
    srts = []

    can_gettext = True
    can_getsrt = True
    line_count = 0
    while can_getsrt:
        srtindex = int(sublines[line_count])
        line_count += 1

        srttime = sublines[line_count]
        line_count += 1

        textlist = []
        srttext = ''
        textlist.append(sublines[line_count])
        line_count += 1
        can_gettext = True
        while can_gettext:
            if (line_count) < len(sublines):
                if not re_srt_index.match(sublines[line_count]):
                    textlist.append(sublines[line_count])
                    line_count += 1
                else:
                    can_gettext = False
            else:
                can_gettext = False
                can_getsrt = False

        srttext = '\n'.join(textlist)
        s = Srt(srtindex, srttime, srttext)
        srts.append(s)

    srts.sort(key=by_start_time)
    reidnex(srts)
    return srts


def by_start_time(elem: Srt):
    return elem.start_time


def merge_subtitle(first_subtitle_fname='tests/test_cn.srt', second_subtitle_fname='tests/test_en.srt',  mark1='@@@@@@@-1', mark2='!!!!!!!-2'):
    '''
    返回: 
        新字幕,无法对齐内容
    - 中文
    1. 把两个字幕中的开始时间和结束时间一样部分合并,存入新字幕文件。
    2. 把没有合并的内容存储到一个新文件。
    3. 把第2步中没有合并的内容存储到另一个文件。
    - english
    1. merge the start time and end time parts of both subtitles into a new subtitle file.
    2. Store the content that is not merged into a new file.
    3. Store the content that was not merged in step 2 to another file.

    '''
    new_subtitle = []

    first_subtitle = load_srt_fromfile(first_subtitle_fname)
    second_subtitle = load_srt_fromfile(second_subtitle_fname)

    assert isinstance(first_subtitle, list)
    assert isinstance(second_subtitle, list)

    for item in first_subtitle:
        assert isinstance(item, Srt)
        temp = [x for x in second_subtitle if x.start_time ==
                item.start_time and x.end_time == item.end_time]
        if temp:
            for m in temp:
                item.text = item.text+'\n'+m.text

            new_subtitle.append(item)

            for m in temp:
                second_subtitle.remove(m)
        else:
            pass

    for item in new_subtitle:
        first_subtitle.remove(item)

    unalign_subtitle = []
    for item in first_subtitle:
        item.text = mark1+item.text
        unalign_subtitle.append(item)
        new_subtitle.append(item)

    for item in second_subtitle:
        item.text = mark2+item.text
        unalign_subtitle.append(item)
        new_subtitle.append(item)

    new_subtitle = copy.deepcopy(new_subtitle)
    new_subtitle.sort(key=by_start_time)
    reidnex(new_subtitle)

    unalign_subtitle = copy.deepcopy(unalign_subtitle)
    unalign_subtitle.sort(key=by_start_time)
    reidnex(unalign_subtitle)

    return new_subtitle, unalign_subtitle


def reidnex(subtitles):
    index_count = 1
    for item in subtitles:
        item.index = index_count
        index_count += 1


def save_subtitle(fname, subtitles: list):
    savelist = [str(x) for x in subtitles]
    savesrt = '\n'.join(savelist)
    f1 = open(fname, 'w', 1000, 'utf-8')
    f1.write(savesrt)
    f1.close()


def merge_subtitle_tofile(first_subtitle_fname='tests/test_cn.srt', second_subtitle_fname='tests/test_en.srt', new_subtitle_fname='tests/test_new.srt', unalign_subtitle_fname='tests/test_unalign.srt', mark1='@@@@@@@-1', mark2='!!!!!!!-2'):
    new_subtitle, unalign_subtitle = merge_subtitle(
        first_subtitle_fname, second_subtitle_fname, mark1, mark2)
    save_subtitle(new_subtitle_fname, new_subtitle)
    save_subtitle(unalign_subtitle_fname, unalign_subtitle)
