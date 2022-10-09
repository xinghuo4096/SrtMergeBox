"""
    字幕文件Srt使用的类和工具
"""
import copy
import datetime
import re
import math

import chardet


class Srt:
    """
    字幕srt的基本类，包含数据
    """

    SEPARATOR = "-->"
    ENCODING = [
        "utf-32",
        "utf-16",
        "utf-8",
        "UTF-8-SIG" "cp1252",
        "gb2312",
        "gbk",
        "big5",
    ]
    RE_TIME = re.compile("[:,]")

    MINI_MERGE_TIME = datetime.timedelta(microseconds=500 * 1000)
    """
    把两个字幕合并的最短时间，500ms。
    500*1000 microsecond
    Returns:
        _type_: _description_
    """
    CHINESE_SUBTITLE_LENGTH = 22
    """
    中文字幕一行最多字符默认22个
    """

    def __init__(self, sub_index, sub_time, sub_text) -> None:
        self.index = int(sub_index)

        self.start_time, self.end_time = self._split_time(sub_time)
        self.text = sub_text

    def __str__(self) -> str:
        temp = "{0}\n{1} {2} {3}\n{4}\n".format(
            self.index,
            format_time(self.start_time),
            Srt.SEPARATOR,
            format_time(self.end_time),
            self.text,
        )
        return temp

    def _split_time(self, strtime: str):
        tm1 = strtime.split(self.SEPARATOR)
        tstrt = load_time(tm1[0])
        tend = load_time(tm1[1])
        return (tstrt, tend)


def detect_code(detect_str="", confidence=0.51) -> tuple:
    """
    检测byte数组的detect_str的编码，并且返回解码后的字符串和编码名称

    _extended_summary_

    Args:
        detect_str (str): byte数组的detect_str
        confidence 字符编码可信度，设的太高容易出错，默认改为0.51

    Raises:
        Exception: _description_

    Returns:
        tuple: 解码后字符串，编码名称
    """
    stemp = chardet.detect(detect_str)
    str1 = ""
    if stemp["confidence"] > confidence:
        str1 = detect_str.decode(stemp["encoding"], "ignore")
    else:
        raise Exception(detect_str[0:10] + "... error." + stemp["confidence"])
    return str1, stemp["encoding"]


def load_time(srt_time: str) -> datetime.datetime:
    """
    '%H:%M:%S,%f'字符串转换为datetime
    '00:00:33,46'
    '00:00:33,046'
    应该是一样的时间。

    Args:
        srt_time (str): 时间字符串

    Returns:
        datetime.datetime: 时间
    """

    srt_time = srt_time.strip()
    stime = Srt.RE_TIME.split(srt_time)

    tm1 = datetime.datetime(
        year=2022,
        month=1,
        day=1,
        hour=int(stime[0]),
        minute=int(stime[1]),
        second=int(stime[2]),
        microsecond=int(stime[3]) * 1000,
    )
    return tm1


def format_time(temp_time: datetime.datetime):
    """
    格式化时间为srt格式

    _extended_summary_

    Args:
        temp_time (datetime.datetime): 时间

    Returns:
        _type_: 格式化后的srt时间
    """
    timestr = "{h}:{m}:{s},{ss}".format(
        h=temp_time.hour,
        m=temp_time.minute,
        s=temp_time.second,
        ss=temp_time.microsecond // 1000,
    )
    return timestr


def clear_srt(fname, srts, test="-test-"):
    """
    清除srt字幕里的字幕文本，替换为类似test的标记。

    Args:
        fname (_type_): 清除后保存的文件名
        srts (_type_): 待清除的Srt列表
        test (str, optional): 替换字幕文本的标记。 Defaults to '-test-'.
    """
    for item in srts:
        assert isinstance(item, Srt)
        item.text = (
            test
            + str(item.index)
            + test
            + format_time(item.start_time)
            + "-"
            + format_time(item.end_time)
        )

    savelist = [str(x) for x in srts]

    savestr = "\n".join(savelist)

    file1 = open(file=fname[:-3] + "txt", mode="w", buffering=1000, encoding="utf-8")
    file1.write(savestr)
    file1.close()


def load_srt_fromfile(fname):
    """
    从文件加载srt文件

    Args:
        fname (_type_): file name

    Returns:
        _type_: Srt list
    """

    file1 = open(fname, "rb")
    str1 = file1.read()
    file1.close()

    srts = load_srt_from_str(str1)
    return srts


def check_srt(str1):
    """
    1. 字符串包含换行。

    _extended_summary_

    Args:
        str1 (_type_): _description_
    """
    str1 = len(str1)


def clear_before_srt(str1) -> str:
    """
    1. 清除文件里的回车`\\r`

    Returns:
        str: str
    """
    subsrt = str1.replace("\r", "")
    return subsrt


def clear_nfsubtitle_before_srt(str1) -> str:
    """
    清除类似NF字幕里，字幕中标识方向的html字符&lrm;&rlm;

    <p>&lrm;' 5 times on the page.</p>
    <p>&rlm;' 5 times on the page.</p>

    Args:
        str1 (_type_): _description_

    Returns:
        str: _description_
    """
    subsrt = str1.replace("&lrm;", "").replace("&rlm;", "")
    return subsrt


def clear_after_srt(srt: Srt) -> str:
    """
    1.把一个字幕块里的字幕变为一行。
        比如：
       ` Dad.`

       ` Yeah?`

        这样的字幕变为 ` Dad.  Yeah?`

    Args:
        str1 (_type_): str

    Returns:
        str: str
    """
    srt.text = srt.text.replace("\n", " ")


def load_srt_from_str(str1):
    """
    从字符串加载Srt字幕。
    先做编码转换detect_code，然后做检查check_srt，接着清除特殊字符clear_before_srt，转换为Srt，再清除做格式变化clear_after_srt

    Args:
        str1 (_type_): 字符串可以是 byte类型的，会做编码转换。

    Returns:
        _type_: Srt list
    """
    re_srt_index = re.compile(r"^\d+$")
    subsrt = detect_code(str1)[0]

    check_srt(subsrt)

    subsrt = clear_before_srt(subsrt)
    subsrt = clear_nfsubtitle_before_srt(subsrt)

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
        srttext = ""
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

        srttext = "\n".join(textlist)
        srt1 = Srt(srtindex, srttime, srttext)

        clear_after_srt(srt1)

        srts.append(srt1)

    srts.sort(key=by_start_time)
    reidnex(srts)
    return srts


def by_start_time(elem: Srt):
    """
    用start_time排序，排序方法用。

    Args:
        elem (Srt): _description_

    Returns:
        _type_: _description_
    """
    return elem.start_time


def merge_srt_tostr(
    first_subtitle_fname="indata/test_cn.srt",
    second_subtitle_fname="indata/test_en.srt",
    mark1="@@@@@@@-1",
    mark2="!!!!!!!-2",
    mini_time=Srt.MINI_MERGE_TIME,
):
    """
    - 中文
    1.合并

        把两个字幕中的‘开始时间’和‘结束时间’一样部分合并,存入新字幕文件。

        把两个字幕中的‘开始时间’一样的部分合并,取两者最晚的‘结束时间’，存入新字幕。

        把两个‘开始时间’绝对值相差‘mini_time’ 的字幕合并，取两者最晚的‘结束时间’，存入新字幕。

    2. 把没有合并的内容存储到一个新文件。
    3. 把第2步中没有合并的内容存储到另一个文件。
    - english
    1.Merge

        Merge the parts of both subtitles with the same 'start time' and 'end time' into a new subtitle file.

        Merge the parts of both subtitles with the same 'start time', and take the latest 'end time' of both and store it in the new subtitle file.

        Merge the two subtitles with the absolute difference of 'start time' and 'min time', and take the latest 'end time' of both, and store them in the new subtitle file.

    2. Store the content that is not merged into a new file.
    3. Store the content that was not merged in step 2 to another file.

    Args:
        first_subtitle_fname (str, optional): 字幕1 Defaults to 'indata/test_cn.srt'.
        second_subtitle_fname (str, optional): 字幕2 Defaults to 'indata/test_en.srt'.
        mark1 (str, optional): _description_. 字幕1字幕无法对齐时标记 to '@@@@@@@-1'.
        mark2 (str, optional): _description_. 字幕2字幕无法对齐时标记 to '!!!!!!!-2'.
        mini_time (timedelta, optional): 当字幕1和字幕的开始时间差在mini_time内，两字幕可以合并
        Defaults to Srt.MINI_MERGE_TIME=500*1000μs(microsecond)=500ms。
    返回:
        新字幕,无法对齐内容。
        new_subtitle, unalign_subtitle
    """
    new_subtitle = []

    first_subtitle = load_srt_fromfile(first_subtitle_fname)
    second_subtitle = load_srt_fromfile(second_subtitle_fname)

    for item in first_subtitle:
        assert isinstance(item, Srt)
        item.text = item.text.replace("\n", " ")

    for item in second_subtitle:
        assert isinstance(item, Srt)
        item.text = item.text.replace("\n", " ")

    assert isinstance(first_subtitle, list)
    assert isinstance(second_subtitle, list)

    for item in first_subtitle:
        assert isinstance(item, Srt)
        start_eq_end = [
            x
            for x in second_subtitle
            if x.start_time == item.start_time and x.end_time == item.end_time
        ]
        if start_eq_end:
            for item2 in start_eq_end:
                item.text = item.text + "\n" + item2.text

            new_subtitle.append(item)

            for item2 in start_eq_end:
                second_subtitle.remove(item2)
        else:
            pass

    # strat_eq  end_not_eq
    for item in first_subtitle:
        assert isinstance(item, Srt)
        start_eq_end_noteq = [
            x
            for x in second_subtitle
            if x.start_time == item.start_time and x.end_time != item.end_time
        ]
        if start_eq_end_noteq:
            for item2 in start_eq_end_noteq:
                item.text = item.text + "\n" + item2.text
                if item.end_time < item2.end_time:
                    item.end_time = item2.end_time
            new_subtitle.append(item)

            for item2 in start_eq_end_noteq:
                second_subtitle.remove(item2)
        else:
            pass

    # strat_time1 - start_time2 <=mini_time
    for item in first_subtitle:
        assert isinstance(item, Srt)
        start_eq_end_noteq = [
            x
            for x in second_subtitle
            if abs(x.start_time - item.start_time) <= mini_time
        ]
        if start_eq_end_noteq:
            is_one_sentence = True
            for item2 in start_eq_end_noteq:
                if is_one_sentence:
                    item.text = item.text + "\n" + item2.text
                    is_one_sentence = False
                else:
                    item.text = item.text + " " + item2.text

                if item.start_time > item2.start_time:
                    item.start_time = item2.start_time
                if item.end_time < item2.end_time:
                    item.end_time = item2.end_time
            new_subtitle.append(item)

            for item2 in start_eq_end_noteq:
                second_subtitle.remove(item2)
        else:
            pass

    # remove
    for item in new_subtitle:
        first_subtitle.remove(item)

    # unalign
    unalign_subtitle = []
    for item in first_subtitle:
        item.text = mark1 + item.text
        unalign_subtitle.append(item)
        new_subtitle.append(item)

    for item in second_subtitle:
        item.text = mark2 + item.text
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
    """
    重建srt文件索引

    Args:
        subtitles (_type_): _description_
    """
    index_count = 1
    for item in subtitles:
        item.index = index_count
        index_count += 1


def save_srt(fname, subtitles: list):
    """
    srt对象list存储为文件

    Args:
        fname (_type_): _description_
        subtitles (list): _description_
    """
    savelist = [str(x) for x in subtitles]
    savesrt = "\n".join(savelist)
    ff1 = open(file=fname, mode="w", buffering=1000, encoding="utf-8")
    ff1.write(savesrt)
    ff1.close()


def format_ass_time(t_time):
    """
    格式化时间为ass文件格式的时间

    Args:
        t_time (_type_): _description_

    Returns:
        _type_: _description_
    """
    return "{0:1d}:{1:0>2d}:{2:0>2d}.{3:0>2d}".format(
        t_time.hour, t_time.minute, t_time.second, t_time.microsecond // 10000
    )


def split_cnsubtitle(str1: str, maxlen=Srt.CHINESE_SUBTITLE_LENGTH) -> str:
    """
    拆分ass字幕中长度超过maxlen个字的中文字幕，超过后是均分两份，每份字符数 int(总字符数/份数+0.5)。

    默认Srt.CHINESE_SUBTITLE_LENGTH，22个字符

    最多拆为5行。

    如：字符共23个,按默认22字符拆分，则拆分为2行，然后均分2份，int(23/2+0.5)=12，第一行12个字符，第二行23-12=11个字符。

    如：字符共50个,按默认22字符拆分，则拆分为3行，然后均分int(50/3+0.5)=17，第一二行17个字符，第三行50-17-17=16个字符。

    ass以\\N为折行。

    Arguments:
        str1 -- 待拆分的字符串

    Returns:
        拆分结果
    """
    if not str1:
        raise Exception("字符串为空。")
    ret = str1
    strlen = len(str1)
    splite_count = math.ceil(strlen / maxlen)
    splite_len = math.ceil(strlen / splite_count)
    match splite_count:
        case 1:
            ret = str1
        case 2:
            ret = f"{str1[0:splite_len]}\\N{str1[splite_len:]}"
        case 3:
            ret = f"{str1[0:splite_len]}\\N{str1[splite_len:splite_len*2]}\\N{str1[splite_len*2:]}"
        case 4:
            ret = f"{str1[0:splite_len]}\\N{str1[splite_len:splite_len*2]}\\N{str1[splite_len*2:splite_len*3]}\\N{str1[splite_len*3:]}"
        case 5:
            ret = f"{str1[0:splite_len]}\\N{str1[splite_len:splite_len*2]}\\N{str1[splite_len*2:splite_len*3]}\\N{str1[splite_len*3:splite_len*4]}\\N{str1[splite_len*4:]}"
        case _:
            ex = Exception("字幕太长，超过5行。请修改")
            raise ex
    return ret


def merge_to_ass_str(
    first_srt_fname="indata/test_cn.srt",
    second_srt_fname="indata/test_en.srt",
    ass_template="indata/test_ass_template_cn_en.txt",
    ass_head="indata/test_ass_head_cn_en.txt",
    mark1="@@@@@@@-1",
    mark2="!!!!!!!-2",
    mini_time=Srt.MINI_MERGE_TIME,
    max_cnsubtitle=Srt.CHINESE_SUBTITLE_LENGTH,
):
    """
    合并两个srt文件为一个ass文件
    - 中文
    1.合并

        把两个字幕中的‘开始时间’和‘结束时间’一样部分合并,存入新字幕文件。

        把两个字幕中的‘开始时间’一样的部分合并,取两者最晚的‘结束时间’，存入新字幕。

        把两个‘开始时间’绝对值相差‘mini_time’ 的字幕合并，取两者最晚的‘结束时间’，存入新字幕。

    2. 把没有合并的内容存储到一个新文件。
    3. 把第2步中没有合并的内容存储到另一个文件。

    Args:
        first_subtitle_fname (str, optional): 字幕1 Defaults to 'indata/test_cn.srt'.
        second_subtitle_fname (str, optional): 字幕1 Defaults to 'indata/test_en.srt'.
        ass_template (str, optional):ass字幕模板。 Defaults to 'indata/test_ass_template_cn_en.txt'.
        mark1 (str, optional): _description_. 字幕1无法对齐时标记 to '@@@@@@@-1'.
        mark2 (str, optional): _description_. 字幕2无法对齐时标记 to '!!!!!!!-2'.
        mini_time (timedelta, optional):当字幕1和字幕2的开始时间差在mini_time内，两字幕可以合并
        max_cnsubtitle:中文字幕中一行字符最长数，默认22个字符，超出后会折为2行。如果设置为10240就不会折行。
        Defaults to Srt.MINI_MERGE_TIME=500*1000μs(microsecond)=500ms。
    Returns:
        新字幕,无法对齐内容。
        new_subtitle, unalign_subtitle
    """

    ass_info_style, ass_text = load_ass_template(ass_template)

    temp = merge_srt_tostr(
        first_subtitle_fname=first_srt_fname,
        second_subtitle_fname=second_srt_fname,
        mark1=mark1,
        mark2=mark2,
        mini_time=mini_time,
    )
    srts = temp[0]
    unaligne_srts = temp[1]

    texts = []
    ff1 = open(ass_head, "rb")
    str1 = ff1.read()
    ff1.close()

    str1 = detect_code(str1)[0]
    texts.append(str1)

    text = ""
    for item in srts:
        assert isinstance(item, Srt)
        text = ass_text

        text = text.replace("{start_time}", format_ass_time(item.start_time))
        text = text.replace("{end_time}", format_ass_time(item.end_time))
        languages = item.text.split("\n")
        match len(languages):
            case 1:
                text = text.replace(
                    "{language1_subtitle_text}",
                    split_cnsubtitle(languages[0], max_cnsubtitle),
                )
                text = text[: text.find(r"\N{\fn")]
            case 2:
                text = text.replace(
                    "{language1_subtitle_text}",
                    split_cnsubtitle(languages[0], max_cnsubtitle),
                )
                text = text.replace("{language2_subtitle_text}", languages[1])
            case _:
                text = text.replace(
                    "{language1_subtitle_text}",
                    split_cnsubtitle("".join(languages[:-1]), max_cnsubtitle),
                )
                text = text.replace("{language2_subtitle_text}", "".join(languages[-1]))

        texts.append(text)

    savestr = ass_info_style + "\n".join(texts)

    return savestr, unaligne_srts


def load_ass_template(ass_template: str):
    """
    加载ass template，ass:info style events dialogue

    Args:
        ass_template (str): 文件名称

    Returns:
        str,str: 一个是ass_info_style包含ass里[Script Info] [V4+ Styles] 和[Events]的部分。
                 一个是ass_text是ass里的Dialogue
    """
    ff1 = open(ass_template, "rb")
    str1 = ff1.read()
    ff1.close()

    str1 = detect_code(str1)[0]
    assert isinstance(str1, str)

    str1 = str1.replace("\r", "")

    ass_info_style = str1[str1.find("[Script Info]") : str1.find("Dialogue:")]

    ass_text = str1[
        str1.find("Dialogue:") : str1.find("{language2_subtitle_text}") + 25
    ]

    ass_info_style = ass_info_style.replace("{softname}", "srt mergen box")
    ass_info_style = ass_info_style.replace(
        "{softurl}", "xinghuo4096,https://github.com/xinghuo4096/SrtMergeBox"
    )
    ass_info_style = ass_info_style.replace("{title}", "title")
    ass_info_style = ass_info_style.replace("{Original_file}", "srt")
    ass_info_style = ass_info_style.replace("{update_name}", "npc")
    ass_info_style = ass_info_style.replace(
        "{update_detial}", str(datetime.datetime.now())
    )

    return ass_info_style, ass_text


def merge_srt_tofile(
    first_subtitle_fname="indata/test_cn.srt",
    second_subtitle_fname="indata/test_en.srt",
    new_subtitle_fname="outdata/newsrt_cnen.srt",
    unalign_subtitle_fname="outdata/newsrt_cnen.unalign.txt",
    mark1="@@@@@@@-1",
    mark2="!!!!!!!-2",
    mini_time=Srt.MINI_MERGE_TIME,
):
    """
    合并连个srt文件到一个srt文件中,utf-8格式。
    - 中文
    1.合并

        把两个字幕中的‘开始时间’和‘结束时间’一样部分合并,存入新字幕文件。

        把两个字幕中的‘开始时间’一样的部分合并,取两者最晚的‘结束时间’，存入新字幕。

        把两个‘开始时间’绝对值相差‘mini_time’ 的字幕合并，取两者最晚的‘结束时间’，存入新字幕。

    2. 把没有合并的内容存储到一个新文件。
    3. 把第2步中没有合并的内容存储到另一个文件。

    Args:
        first_subtitle_fname (str, optional): 第一个srt字幕的文件名称。
             Defaults to 'indata/test_cn.srt'.
        second_subtitle_fname (str, optional):  第二个srt字幕文件名称。
             Defaults to 'indata/test_en.srt'.
        new_subtitle_fname (str, optional):新ass文件名称。
             Defaults to 'outdata/newsrt_cnen.srt'.
        unalign_subtitle_fname (str, optional): 保存未对齐字幕内容的文件名称。
        Defaults to 'outdata/newsrt_cnen.unalign.txt'.
        mark1 (str, optional): 标记，标记第一个字幕中未对其的字幕内容。
            Defaults to '@@@@@@@-1'.
        mark2 (str, optional): 标记，标记第二个字幕中未对其的字幕内容。
            Defaults to '!!!!!!!-2'.
        mini_time (timedelta, optional):当字幕1和字幕2的开始时间差在mini_time内，两字幕可以合并。
        Defaults to Srt.MINI_MERGE_TIME=500*1000μs(microsecond)=500ms。
    """
    new_subtitle, unalign_subtitle = merge_srt_tostr(
        first_subtitle_fname, second_subtitle_fname, mark1, mark2, mini_time
    )
    save_srt(new_subtitle_fname, new_subtitle)
    save_srt(unalign_subtitle_fname, unalign_subtitle)


def merge_ass_tofile(
    first_subtitle_fname="indata/test_cn.srt",
    second_subtitle_fname="indata/test_en.srt",
    new_subtitle_fname="outdata/new_ass_cnen.ass",
    unalign_subtitle_fname="outdata/new_ass_cnen.unalign.txt",
    ass_template_fname="indata/test_ass_template_cn_en.txt",
    ass_head_fname="indata/test_ass_template_cn_en.txt",
    mark1="@@@@@@@-1",
    mark2="!!!!!!!-2",
    mini_time=Srt.MINI_MERGE_TIME,
    max_cnsubtitle=Srt.CHINESE_SUBTITLE_LENGTH,
):
    """
    合并两个srt格式文件到一个ass格式文件里,utf-8格式。

    Args:
        first_subtitle_fname (str, optional): 第一个srt字幕的文件名称。
            Defaults to 'indata/test_cn.srt'.
        second_subtitle_fname (str, optional): 第二个srt字幕文件名称。
            Defaults to 'indata/test_en.srt'.
        new_subtitle_fname (str, optional): 新ass文件名称。
            Defaults to 'outdata/new_ass.ass'.
        unalign_subtitle_fname (str, optional): 保存未对齐字幕内容的文件名称。
            Defaults to 'outdata/new_ass.unalign.txt'.
        ass_template_fname (str, optional): _description_.
        Defaults to 'indata/test_ass_template_cn_en.txt'.
        ass_head_fname(str,optional):head
        mark1 (str, optional): 标记，标记第一个字幕中未对其的字幕内容。
            Defaults to '@@@@@@@-1'.
        mark2 (str, optional): 标记，标记第二个字幕中未对其的字幕内容。
            Defaults to '!!!!!!!-2'.
        mini_time (timedelta, optional):当字幕1和字幕2的开始时间差在mini_time内，两字幕可以合并。
        Defaults to Srt.MINI_MERGE_TIME=500*1000μs(microsecond)=500ms。
    """

    new_subtitle, unalign_subtitle = merge_to_ass_str(
        first_srt_fname=first_subtitle_fname,
        second_srt_fname=second_subtitle_fname,
        ass_template=ass_template_fname,
        ass_head=ass_head_fname,
        mark1=mark1,
        mark2=mark2,
        mini_time=mini_time,
        max_cnsubtitle=max_cnsubtitle,
    )

    sf1 = open(file=new_subtitle_fname, mode="w", buffering=1000, encoding="utf-8")
    sf1.write(new_subtitle)
    sf1.close()

    save_srt(unalign_subtitle_fname, unalign_subtitle)
