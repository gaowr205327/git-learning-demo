#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit Converter —— 一个用来练习 Git 版本管理的小程序。

第 5 轮（v0.2.2）：整数结果不再补小数零。

用法:
    python src/unit_converter.py                  # 进入交互模式
    python src/unit_converter.py 100 cm m         # 直接换算
    python src/unit_converter.py --version        # 查看版本
"""

import sys

APP_NAME = "Unit Converter"
VERSION = "0.2.2"

# 所有长度单位统一折算成「米」的系数
LENGTH_UNITS = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
    "inch": 0.0254,
    "foot": 0.3048,
}

# 所有重量单位统一折算成「克」的系数
WEIGHT_UNITS = {
    "mg": 0.001,
    "g": 1.0,
    "kg": 1000.0,
    "t": 1000000.0,
    "oz": 28.349523125,
    "lb": 453.59237,
}

# 按类别归组：展示时按类列出，换算也只在同一类里进行
UNIT_TABLES = {
    "长度": LENGTH_UNITS,
    "重量": WEIGHT_UNITS,
}

# 非整数结果保留的小数位数
DECIMALS = 4


def resolve_table(from_unit, to_unit):
    """两个单位必须属于同一类，返回该类的单位表；否则返回 None。"""
    for table in UNIT_TABLES.values():
        if from_unit in table and to_unit in table:
            return table
    return None


def convert(value, from_unit, to_unit, table):
    """在同一类单位表 table 内，把 value 从 from_unit 换算成 to_unit。"""
    return value * table[from_unit] / table[to_unit]


def format_number(value):
    """整数不补小数零，其它情况保留 DECIMALS 位。"""
    if value.is_integer():
        return "{:.0f}".format(value)
    return "{:.{d}f}".format(value, d=DECIMALS)


def format_result(value, from_unit, to_unit, table):
    """把一次换算格式化成一行可读的文本。"""
    result = convert(value, from_unit, to_unit, table)
    return "{} {}  ->  {} {}".format(
        "{:g}".format(value), from_unit, format_number(result), to_unit
    )


def show_unit_list():
    for name, table in UNIT_TABLES.items():
        print("支持的{}单位: {}".format(name, ", ".join(table)))


def interactive():
    """交互模式：反复读取用户输入并换算。"""
    print("=" * 38)
    print("  {} v{}".format(APP_NAME, VERSION))
    print("  长度 / 重量单位换算小工具")
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

        table = resolve_table(from_unit, to_unit)
        if table is None:
            print("不认识这两个单位，或它们不属于同一类")
            continue

        print(format_result(value, from_unit, to_unit, table))

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
        table = resolve_table(from_unit, to_unit)
        if table is None:
            print("错误: 单位无效，或两个单位不属于同一类")
            return 1
        print(format_result(value, from_unit, to_unit, table))
        return 0

    if argv:
        print("用法: unit_converter [数值 源单位 目标单位]")
        print("      unit_converter --version")
        return 2

    interactive()
    return 0


if __name__ == "__main__":
    sys.exit(main())
