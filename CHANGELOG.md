# 更新记录

本项目的所有改动都会记录在这里，方便对照 `git log` 观察版本演进。

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [0.1.0] - 2026-10-06

### 新增

- 基线版本。命令行单位换算器，支持长度单位：mm、cm、m、km、inch、foot。
- 交互模式：反复输入「数值 源单位 目标单位」进行换算。
- 命令行参数模式：`unit_converter 100 cm m`。
- `--version` 查看版本号。
- `tools/build.bat` 一键打包为单个 exe。
