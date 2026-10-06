#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit Converter —— 一个用来练习 Git 版本管理的小程序。

第 2 轮（v0.1.2）：换算结果的小数位由 2 位提高到 4 位。

用法:
    python src/unit_converter.py                  # 进入交互模式
    python src/unit_converter.py 100 cm m         # 直接换算
    python src/unit_converter.py --version        # 查看版本
"""

import sys

APP_NAME = "Unit Converter"
VERSION = "0.1.2"

# 所有长度单位统一折算成「米」的系数
LENGTH_UNITS = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
    "inch": 0.0254,
    "foot": 0.3048,
}

# 结果保留的小数位数
DECIMALS = 4


def convert(value, from_unit, to_unit):
    """把 value 从 from_unit 换算成 to_unit。"""
    return value * LENGTH_UNITS[from_unit] / LENGTH_UNITS[to_unit]


def format_result(value, from_unit, to_unit):
    """把一次换算格式化成一行可读的文本。"""
    result = convert(value, from_unit, to_unit)
    return "{} {}  ->  {} {}".format(
        "{:g}".format(value), from_unit, "{:.{d}f}".format(result, d=DECIMALS), to_unit
    )


def show_unit_list():
    print("支持的长度单位: " + ", ".join(LENGTH_UNITS))


def interactive():
    """交互模式：反复读取用户输入并换算。"""
    print("=" * 38)
    print("  {} v{}".format(APP_NAME, VERSION))
    print("  长度单位换算小工具")
    print("=" * 38)
    show_unit_list()
    print("输入格式: 数值 源单位 目标单位    (直接回车退出)")
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            break

        parts = line.split()
        if len(parts) != 3:
            print("格式不对，需要三部分，例如: 100 cm m")
            continue

        raw_value, from_unit, to_unit = parts
        try:
            value = float(raw_value)
        except ValueError:
            print("'{}' 不是有效数字".format(raw_value))
            continue

        if from_unit not in LENGTH_UNITS or to_unit not in LENGTH_UNITS:
            print("不认识这个单位，请看上面的列表")
            continue

        print(format_result(value, from_unit, to_unit))

    print("再见")


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)

    if argv and argv[0] in ("-v", "--version"):
        print("{} v{}".format(APP_NAME, VERSION))
        return 0

    if len(argv) == 3:
        raw_value, from_unit, to_unit = argv
        try:
            value = float(raw_value)
        except ValueError:
            print("错误: '{}' 不是有效数字".format(raw_value))
            return 1
        if from_unit not in LENGTH_UNITS or to_unit not in LENGTH_UNITS:
            print("错误: 不认识这个单位")
            return 1
        print(format_result(value, from_unit, to_unit))
        return 0

    if argv:
        print("用法: unit_converter [数值 源单位 目标单位]")
        print("      unit_converter --version")
        return 2

    interactive()
    return 0


if __name__ == "__main__":
    sys.exit(main())
