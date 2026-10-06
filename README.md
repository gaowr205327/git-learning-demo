# Unit Converter

一个刻意做得很小的命令行单位换算器，用途是**练习 Git 版本管理**：
每轮只改一小处，让 `git diff` 永远只有几行，方便观察版本之间的差异。

---

## 快速开始

直接跑源码（不需要装任何东西）：

```bash
python src/unit_converter.py 100 cm m
```

进入交互模式：

```bash
python src/unit_converter.py
```

```
======================================
  Unit Converter v0.2.0
  长度 / 重量单位换算小工具
======================================
支持的长度单位: mm, cm, m, km, inch, foot
支持的重量单位: mg, g, kg, t, oz, lb
输入格式: 数值 源单位 目标单位    (直接回车退出)
> 100 cm m
100 cm  ->  1.0000 m
> 1 kg lb
1 kg  ->  2.2046 lb
```

## 支持的单位

| 类别 | 单位 |
|---|---|
| 长度 | `mm` `cm` `m` `km` `inch` `foot` |
| 重量 | `mg` `g` `kg` `t` `oz` `lb` |

同一类内的单位可以互相换算；**跨类换算会被拒绝**（例如 `1 kg m` 会报错并以退出码 1 结束）。

## 打包成 exe

```bat
tools\build.bat
```

产物在 `dist\unit_converter.exe`。

打包环境固定为：

- Python **3.14.4**
- PyInstaller **6.22.3**

换版本可能导致产物不一致，请与上表保持一致。

> `dist/` 与 `build/` 已被 `.gitignore` 忽略，**不会进仓库**。
> 可执行文件通过 GitHub Releases 发布。
> 但 `unit_converter.spec` 是**构建配置，属于源码，要提交**。

## 中文显示说明（实测记录）

同一份代码，跑源码和跑 exe 的**输出编码并不相同**：

| 运行方式 | 输出编码 |
|---|---|
| `python src/unit_converter.py` | 跟随环境（通常是 UTF-8） |
| `dist\unit_converter.exe` | GBK（cp936），PyInstaller 不继承 `PYTHONUTF8` |

两者在中文 Windows 控制台里显示都正常。但如果你把输出**重定向到文件**再打开，
可能会看到乱码 —— 这不是程序错了，而是文件的字节编码和你查看时用的编码不一致。

结论：**"源码能跑"不等于"打包后能跑"，打包产物必须单独验证一次。**

## 版本约定

- 版本号写在 `src/unit_converter.py` 的 `VERSION` 常量里，**只此一处**。
- 语义化版本：`MAJOR.MINOR.PATCH`。
  - 改文本 / 调数值 / 修 bug → PATCH +1
  - 增加新功能 → MINOR +1
- 每轮迭代 = **一个提交**，并打一个 tag（`v0.1.1`、`v0.1.2` …）。
- 每轮改动都记在 [CHANGELOG.md](CHANGELOG.md) 里。

## 提交信息格式

采用 Conventional Commits：

| 前缀 | 用途 |
|---|---|
| `feat:` | 新增功能 |
| `fix:` | 修复 bug |
| `docs:` | 只改文档 |
| `chore:` | 构建脚本、忽略规则等杂务 |
| `refactor:` | 重构，行为不变 |

例：`feat: 支持英寸到厘米换算`

## 目录结构

```
git-learning-demo/
├── .gitattributes          # 统一换行符
├── .gitignore              # 排除打包产物与缓存
├── CHANGELOG.md            # 每轮改动记录
├── README.md
├── src/
│   └── unit_converter.py   # 全部程序逻辑（单文件）
└── tools/
    └── build.bat           # 一键打包
```
