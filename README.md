# patent-award-doc-skill

快速制作**中国专利奖 / 广东专利奖**等政府专利奖项申报书（官方 `.docx` 7 表格式）的 WorkBuddy 技能。

> 本技能源自 2026 年广东省专利奖申报实战（专利 CN119689312B「一种并联化成分容设备串联模式校准方法」），把可复用的工作流沉淀为技能，供更多企业快速、合规地制作专利奖申报材料。

## 核心理念

**真实、可追溯、前后一致、红线干净**——一切结论只引用"事实锚点"，不编造、不张冠李戴。

- 不确定信息留空或写否定句，**绝不编造**数据
- 他人专利与自家专利严格区分（对比文件只在"新创性"出现，专利池只在"同族/保护成效"出现）
- 量化财务数字必须来自本专利、由财务盖章，不套用姊妹专利数据

## 目录结构

```
patent-award-doc-skill/
├── SKILL.md                      # 技能主文档（何时用/输入/7表结构/红线/工作流/三步法）
├── scripts/
│   ├── edit_cell.py              # lxml 安全改写单格（绕过 python-docx 合并单元格段错误）
│   ├── redline_scan.py           # 全文档红线扫描（防编造/张冠李戴）
│   └── verify_doc.py             # 结构校验（顶层表/图/媒体/嵌套表 + 每格字数）
├── references/
│   ├── structure.md              # 申报书 7 表结构映射
│   ├── redlines.md               # 红线清单 + 必需输入 + 事实锚点模板
│   └── sanbuhfa_template.md      # 三步法论证模板（占位符可填）
├── README.md
└── LICENSE
```

## 安装

### 方式一：WorkBuddy 本地安装（立即可用）
将本目录复制到用户技能目录：
```
cp -r patent-award-doc-skill ~/.workbuddy/skills/patent-award-doc
```
重启/刷新 WorkBuddy 后，对话中提到"专利奖申报书"即会触发本技能。

### 方式二：从 GitHub 安装
```
git clone https://github.com/IPRshang/patent-award-doc-skill.git
cp -r patent-award-doc-skill ~/.workbuddy/skills/patent-award-doc
```

## 快速使用

```bash
# 1) 红线扫描（每轮改完必跑，要求 0 命中）
python scripts/redline_scan.py 申报书.docx

# 2) 结构校验
python scripts/verify_doc.py 申报书.docx

# 3) 安全改写单元格（支持 --sync 多副本同步）
python scripts/edit_cell.py --docx 申报书.docx --table 1 --row 0 --col 1 \
    --text paras.txt --sync 副本1.docx 副本2.docx
```

在 WorkBuddy 中直接说：
> "帮我填广东专利奖申报书，专利号 CN119689312B，对比文件用这 3 篇 PDF"

技能会自动建事实锚点、按 7 表结构填写、跑红线扫描与结构校验。

## 贡献

欢迎 PR 优化：
- 补充更多省份/国家级专利奖的表结构差异
- 增加更多「获奖范式」参考写法
- 改进三步法论证模板
- 增加自动化截图/OCR 抽取通知书清单的能力

请遵循本技能的**红线原则**：所有产出必须基于真实事实，不确定处留空，严禁编造。

## 许可证

MIT —— 自由用于任何专利奖申报场景，修改与再分发请保留本声明。
