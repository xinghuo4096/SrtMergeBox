# SrtMergeBox

## Introduction

Merge 2 subtitles in srt format into srt or ass format subtitles.

Example: Chinese and English subtitles merged into the same srt format subtitle, or one ass format subtitle.

Require srt subtitles in both languages of the same movie.

## Use

1. Do the preparation work.
2. Run movie_srt_merge.py will merge two subtitles `test_cn.srt` and `test_en.srt` under the folder `indata`.
merge them into srt format subtitle `movie_new_srt.srt` and ass format subtitle `moviet_new_ass.ass` and store them in `outdata` folder.
    - srt format subtitles source subtitles that are not aligned are stored to `outdata` folder with the file name: `movie_new_srt.unalign.txt`
    - ass format subtitle source subtitles without alignment stored to `outdata` folder, filename: `movie_new_ass.unalgin.txt`.

### Preparation

#### Time content in subtitles should be aligned

Subtitles in srt format for the same movie in two languages with aligned times.

#### requires library chardet

Import command
Command: pip install chardet

#### need to create folder outdata

    Default output to outdata folder

#### ass subtitle template

`test_ass_template_cn_en.txt` is the template file for ass and can be modified.

- The default template for ass format subtitles is `test_ass_template_cn_en.txt` in the `indata` folder
- The ass format subtitle template can be modified.
  - For example, to modify the default subtitle template  
  `test_ass_template_cn_en.txt`

    1. `Style: Default,方正黑体_GBK,20,&H00FFFFFF,&HF0000000,&H00000000,&H32000000` This line, you can modify the font name, default is 方正黑体_GBK, size, default 20, color, default color &H00FFFFFF.

        *Note that the color here is aabbggrr format, inverted rgb format, plus aa, alpha channel.
  
    2. modify `{\fn微软雅黑}{\b0}{\fs14}{\3c&H202020&}`, this line will modify the font name of the second language subtitle, the default is 微软雅黑, size default 14, color, default color `\3c&H202020&`.

          *Note that this is `{\3c&H202020&}` format, and the color is rrggbb format.Because of the result of '\3c&H' modifier*
