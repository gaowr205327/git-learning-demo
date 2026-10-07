#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit Converter —— 一个用来练习 Git 版本管理的小程序。

第 6 轮（v0.3.0）：新增温度单位换算。由于温度带偏移量（华氏度转摄氏度不是简单乘系数），
换算模型由「纯比例」扩展为「比例 + 偏移」。

用法:
    python src/unit_converter.py                  # 进入交互模式
    python src/unit_converter.py 100 cm m         # 直接换算
    python src/unit_converter.py --version        # 查看版本
"""

import sys

APP_NAME = "Unit Converter"
VERSION = "0.3.0"

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

# 温度单位统一折算成「摄氏度」，写法为 (scale, offset)，含义是：
#     摄氏度 = scale * 输入值 + offset
# 长度和重量只有比例、没有偏移，所以直接写一个数字即可（详见 scale_offset()）。
TEMPERATURE_UNITS = {
    "c": (1.0, 0.0),                 # 摄氏度 = 摄氏度
    "f": (5.0 / 9.0, -160.0 / 9.0),  # 摄氏度 = (华氏度 - 32) * 5 / 9
    "k": (1.0, -273.15),             # 摄氏度 = 开尔文 - 273.15
}

# 按类别归组：展示时按类列出，换算也只在同一类里进行
UNIT_TABLES = {
    "长度": LENGTH_UNITS,
    "重量": WEIGHT_UNITS,
    "温度": TEMPERATURE_UNITS,
}

# 结果保留的小数位数
DECIMALS = 4


def resolve_table(from_unit, to_unit):
    """两个单位必须属于同一类，返回该类的单位表；否则返回 None。"""
    for table in UNIT_TABLES.values():
        if from_unit in table and to_unit in table:
            return table
    return None


def scale_offset(spec):
    """把单位定义归一化成 (scale, offset) 二元组。

    纯比例单位可以直接写一个数字（等价于 offset 为 0）；带偏移的单位写成二元组。
    两种写法在这里统一，后续换算只需要一套公式。
    """
    if isinstance(spec, tuple):
        return spec
    return spec, 0.0


def convert(value, from_unit, to_unit, table):
    """在同一类单位表 table 内，把 value 从 from_unit 换算成 to_unit。

    分两步走：先把输入换算成该类的基准单位，再从基准换算到目标单位。
        基准值 = from_scale * value + from_offset
        结果   = (基准值 - to_offset) / to_scale
    对纯比例单位（offset 为 0）而言，这与直接乘除系数完全等价。
    """
    from_scale, from_offset = scale_offset(table[from_unit])
    to_scale, to_offset = scale_offset(table[to_unit])
    base = from_scale * value + from_offset
    return (base - to_offset) / to_scale


def format_result(value, from_unit, to_unit, table):
    """把一次换算格式化成一行可读的文本。"""
    result = convert(value, from_unit, to_unit, table)
    return "{} {}  ->  {} {}".format(
        "{:g}".format(value), from_unit, "{:.{d}f}".format(result, d=DECIMALS), to_unit
    )


def show_unit_list():
    for name, table in UNIT_TABLES.items():
        print("支持的{}单位: {}".format(name, ", ".join(table)))


def interactive():
    """交互模式：反复读取用户输入并换算。"""
    print("=" * 38)
    print("  {} v{}".format(APP_NAME, VERSION))
    print("  长度 / 重量 / 温度单位换算小工具")
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
