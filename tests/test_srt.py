'''
测试

'''
import datetime
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
    '''
    srt_time = ' 00:03:06,520  '
    t1 = load_time(srt_time)

    assert isinstance(t1, datetime.datetime)
    assert t1.hour == 0
    assert t1.minute == 3
    assert t1.second == 6
    assert t1.microsecond == 520 * 1000
    return t1


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

    td = datetime.timedelta(seconds=10, microseconds=1000)
    now_time += td
    temp = datetime.datetime.strptime('1900-01-01 00:00:10.001000',
                                      '%Y-%m-%d %H:%M:%S.%f')
    assert now_time == temp

    ss = now_time - begin_time
    temp = 10.001
    assert ss.total_seconds() == temp


def main():
    '''   

    main
    '''
    pass


if __name__ == '__main__':
    main()
