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
