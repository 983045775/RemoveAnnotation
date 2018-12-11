#!D:\Python32
# -*- coding: utf-8-*-
# 过滤JAVA程序中的注释
# 如果字符串中有注释符号的话会有问题。

import os
import re

# 改这个目录！！！
top_dir = "D:\\iFlytekSource\\Source2.0\\app\\ScreenRecorder_new\\app\\src";

# 状态
S_INIT = 0
S_SLASH = 1
S_BLOCK_COMMENT = 2
S_BLOCK_COMMENT_DOT = 3
S_LINE_COMMENT = 4
S_STR = 5
S_STR_ESCAPE = 6


def trim_dir(path):
    print("dir：" + path)
    for root, dirs, files in os.walk(path):
        for name in files:
            trim_file(os.path.join(root, name))

        # for name in dirs:
        # trim_dir(os.path.join(root, name))


def trim_file(path):
    print("file:" + path)
    if re.match(r".*?\.(java|c|cpp|h)$", path):
        print("process")
    else:
        print("ignore")
        return

    bak_file = path + ".bak"
    try:
        os.rename(path, bak_file)
    except:
        print
        "bak except", bak_file;

    fp_src = open(bak_file, encoding='UTF-8');
    fp_dst = open(path, 'w', encoding='UTF-8');
    state = S_INIT;
    for line in fp_src.readlines():
        for c in line:
            if state == S_INIT:
                if c == '/':
                    state = S_SLASH;
                elif c == '"':
                    state = S_STR;
                    fp_dst.write(c);
                else:
                    fp_dst.write(c);
            elif state == S_SLASH:
                if c == '*':
                    state = S_BLOCK_COMMENT;
                elif c == '/':
                    state = S_LINE_COMMENT;
                else:
                    fp_dst.write('/');
                    fp_dst.write(c);
                    state = S_INIT;
            elif state == S_BLOCK_COMMENT:
                if c == '*':
                    state = S_BLOCK_COMMENT_DOT;
            elif state == S_BLOCK_COMMENT_DOT:
                if c == '/':
                    state = S_INIT;
                elif c == '*':
                    state = S_BLOCK_COMMENT_DOT;  # 再次碰到*号还是要继续状态，否则会出错
                else:
                    state = S_BLOCK_COMMENT;
            elif state == S_LINE_COMMENT:
                if c == '\n':
                    state = S_INIT;
                    fp_dst.write(c);
            elif state == S_STR:
                if c == '\\':
                    state = S_STR_ESCAPE;
                elif c == '"':
                    state = S_INIT;
                fp_dst.write(c);
            elif state == S_STR_ESCAPE:
                # 这里未完全实现全部序列，如\oNNN \xHH \u1234 \U12345678，但没影响
                state = S_STR;
                fp_dst.write(c);

    fp_src.close();
    fp_dst.close();
    # os.remove(bak_file);


def del_files(path):
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith(".bak"):
                os.remove(os.path.join(root, name))
                print("Delete File: " + os.path.join(root, name))


if __name__ == "__main__":
    trim_dir(top_dir);
    del_files(top_dir)
