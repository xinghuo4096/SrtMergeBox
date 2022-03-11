# SrtMergeBox

## 简介

合并2个srt格式字幕为srt或ass格式字幕。目的是制作双语字幕。

例如：中文字幕和英文字幕合并到同一个srt格式的字幕中，或一个ass格式字幕中。

要求是同一部电影的两种语言的srt格式字幕。

## 使用

1. 做好准备工作。
2. 运行movie_srt_merge.py会把文件夹`indata`下两个字幕`test_cn.srt`和`test_en.srt`，
合并为srt格式字幕`movie_new_srt.srt`和ass格式字幕`moviet_new_ass.ass`，存储到`outdata`文件夹。
    - srt格式字幕源字幕没有对齐的部分存储到`outdata`文件夹，文件名:`movie_new_srt.unalign.txt`
    - ass格式字幕源字幕没有对齐的部分存储到`outdata`文件夹，文件名：`movie_new_ass.unalgin.txt`。
3. 可以调整`mini_time`来减少字幕没有对齐的部分。

### 准备工作

#### 字幕里的时间内容要对齐

同一部电影的两种语言的srt格式字幕，时间要对齐。

#### 需要库chardet

导入命令
命令：pip install chardet

#### 需要建立文件夹 outdata

    默认输出到outdata文件夹

#### ass字幕模板

`test_ass_template_cn_en.txt`是ass的模板文件，可以修改。

- ass格式字幕的模板默认是`indata`文件夹下的`test_ass_template_cn_en.txt`
- ass格式的字幕模板可以修改。
  - 比如修改默认字幕模板  
  `test_ass_template_cn_en.txt`

    1. `Style: Default,方正黑体_GBK,20,&H00FFFFFF,&HF0000000,&H00000000,&H32000000`这行，可以修改字体名称，默认是方正黑体_GBK，大小，默认20，颜色，默认颜色&H00FFFFFF。

        *注意，这里颜色是aabbggrr的格式，倒rgb格式,加上aa，alpha channel。*
  
    2. 修改`{\fn微软雅黑}{\b0}{\fs14}{\3c&H202020&}`，这行就可以修改第二语言字幕的字体名称，默认是微软雅黑，大小默认14，颜色，默认颜色`\3c&H202020&`。

        *注意，这种是`{\3c&H202020&}`形式,颜色是rrggbb格式。因为`\3c&H`修饰的结果*
