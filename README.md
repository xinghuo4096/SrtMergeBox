# SrtMergeBox

## 简介

用于把对应同一部电影的两种语言的srt格式字幕合并为一个srt格式文件，或一个ass格式的字幕文件。
例如：中英文字幕合并到同一个srt格式的字幕中，或一个ass格式字幕中。

## 使用

1. 做好准备工作。
2. 运行movie_srt_merge.py会把文件夹`indata`下两个字幕`test_cn.srt`和`test_en.srt`，
合并为srt格式字幕`movie_new_srt.srt`和ass格式字幕`moviet_new_ass.ass`，存储到`outdata`文件夹。
    - srt格式字幕源字幕没有对齐的部分存储到`outdata`文件夹，文件名:`movie_new_srt.unalign.txt`
    - ass格式字幕源字幕没有对齐的部分存储到`outdata`文件夹，文件名：`movie_new_ass.unalgin.txt`。

### 准备工作

#### 字幕的时间要对齐

同一部电影的两种语言的srt格式

#### 需要库chardet

导入命令
命令：pip install chardet

#### 需要建立目录 outdata

test_ass_template_cn_en.txt是ass的模板文件，可以修改。

#### ass字幕模板

    - ass格式字幕的模板默认是`indata`文件夹下的`test_ass_template_cn_en.txt`
    - ass格式的字幕模板可以修改。比如默认字幕模板`test_ass_template_cn_en.txt`，修改两种字幕的字体``，大小``等。
