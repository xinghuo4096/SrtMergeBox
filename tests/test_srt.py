'''
测试

'''
import datetime
import re
from urllib.request import urlopen
from Srt import Srt, detect_code, load_srt_fromfile, load_time, format_time


def test_load_srt():
    '''
    test

    '''
    subs = load_srt_fromfile('indata/test_srt1.srt')

    assert len(subs) == 10
    item = subs[-1]
    assert isinstance(item, Srt)
    assert item.text == 'I will.'
    assert item.index == 10


RE_SDH = re.compile('[-\\s]*\\s*[\\[(]+[\\s\\S]+?[\\])]+[\\s+:]*')
RE_TEXT = re.compile(r'\w+')


def clear_sdh(str1: str) -> str:
    '''
     去掉-()[]*包围的sdh内容。

    Args:
        str1 (str): _description_

    Returns:
        _type_: bool
    '''
    cleartext = str1.strip()
    if cleartext:
        cleartext = RE_SDH.sub('', cleartext)
        cleartext = cleartext.strip()
    return cleartext


def test_clear_sdh():
    '''
    test can add srt

    Args:
        srt1 (str): _description_
    '''
    str0 = 'this is test.'
    assert str0 == clear_sdh(str0)

    str1 = '[mysterious clanging music]'
    str2 = '- [wind howling]'
    str3 = '''- [wind howling]
    - [woman choking]
    '''
    str4 = '(mysterious clanging music)'
    str5 = '- (wind howling)'
    str6 = '''
    - (wind howling)
    - (woman choking)
    '''
    str7 = '''[wind howling]
    [woman choking]
    '''
    str8 = '''[wind howling]
    [woman choking]
    '''
    assert not clear_sdh(str1)
    assert not clear_sdh(str2)
    assert not clear_sdh(str3)
    assert not clear_sdh(str4)
    assert not clear_sdh(str5)
    assert not clear_sdh(str6)
    assert not clear_sdh(str7)
    assert not clear_sdh(str8)

    str9 = "* *"
    str10 = "*this is test. *"
    str11 = "[wind howling]*this is test. *"
    str12 = "(wind howling) this is test."
    str13 = "- [wind howling] this is test.[wind]:this is test2."
    str14 = "- (wind howling) this is test.(wind):this is test2."
    str15 = "- [wind howling] : this is test.(wind)this is test2."

    assert str9 == clear_sdh(str9)
    assert str10 == clear_sdh(str10)
    assert '*this is test. *' == clear_sdh(str11)
    assert 'this is test.' == clear_sdh(str12)
    assert 'this is test.this is test2.' == clear_sdh(str13)
    assert 'this is test.this is test2.' == clear_sdh(str14)
    assert 'this is test.this is test2.' == clear_sdh(str15)


def test_detect():
    '''
    _test
    '''
    rawdata = urlopen('http://m.baidu.com/').read()
    ret = detect_code(rawdata)
    str1 = ret[0]
    code = ret[1]
    assert len(str1) > 1
    assert 'baidu' in str1
    assert '百度一下' in str1
    assert code.lower() == 'utf-8-sig'


def test_load_time():
    '''
    test
    srt1 = '00:00:33,46'
    srt2 = '00:00:33,046'
    应该是一样的时间。
    '''
    srt_time = ' 00:03:06,520  '
    time1 = load_time(srt_time)

    assert isinstance(time1, datetime.datetime)
    assert time1.hour == 0
    assert time1.minute == 3
    assert time1.second == 6
    assert time1.microsecond == 520 * 1000

    srt1 = '02:03:33,46'
    srt2 = '02:03:33,046'

    tm1 = load_time(srt1)
    tm2 = load_time(srt2)

    assert isinstance(time1, datetime.datetime)
    assert tm1.hour == 2
    assert tm1.minute == 3
    assert tm1.second == 33
    assert tm1.microsecond == 46 * 1000

    assert tm1 == tm2



def test_time():
    '''
    test
    '''
    begin_time = datetime.datetime.strptime('0', '%S')
    now_time = datetime.datetime.strptime('0', '%S')

    assert begin_time == datetime.datetime.strptime('1900-01-01 00:00:00',
                                                    '%Y-%m-%d %H:%M:%S')

    assert now_time == datetime.datetime.strptime('1900-01-01 00:00:00',
                                                  '%Y-%m-%d %H:%M:%S')

    timestr = format_time(begin_time)
    assert timestr == '0:0:0,0'

    td1 = datetime.timedelta(seconds=10, microseconds=1000)
    now_time += td1
    temp = datetime.datetime.strptime('1900-01-01 00:00:10.001000',
                                      '%Y-%m-%d %H:%M:%S.%f')
    assert now_time == temp

    ss1 = now_time - begin_time
    temp = 10.001
    assert ss1.total_seconds() == temp


def main():
    '''

    main
    '''
    test_time()


if __name__ == '__main__':
    main()
