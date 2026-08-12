# 申报书 7 表结构（python-docx `d.tables` 索引）

> 官方专利奖申报书为固定 7 表格式。以下为通用映射，具体行/列以所用模板为准；改动前务必用 `verify_doc.py` 打印每格索引核对。

```
[0] 基本信息
    row0 专利号
    row1 专利名称
    row2 专利权人
    row3 IPC 主分类号
    row4 申报单位
    row5 通讯地址 / 邮编
    row6-9 联系人1/2（姓名、手机、办公电话、邮箱）
    row10 推荐单位

[1] 专利质量
    row0 新颖性和创造性   ★ 三步法论证核心格
    row1 实用性
    row2 文本质量
    row3 同族专利          ★ 只列本公司真实持有的相关专利

[2] 技术先进性
    row0 核心发明点        （可覆盖权1-权11，先概括后详述）
    row1 技术原创性及重要性
    row2 技术优势          ★ 含嵌套对比表（改写时保留表、仅补文字）
    row3 技术通用性

[3] 运用及保护成效
    row0 制度建设
    row1 专利运用成效      ★ 许可/出资/融资如实写"无"
    row2 专利保护成效      ★ 专利池口径须与 [1].row3 一致

[4] 经济效益
    row0-4 自行实施情况（项目/时间、销售额、利税额、出口额、市场份额；2023/2024/2025/合计）
    row5-8 专利许可情况
    row9-12 其他收益情况（出资、融资等途径）
    row13 效益综述          ★ 注明"量化金额需财务核算并加盖财务专用章"

[5] 社会效益 / 政策
    row0 社会效益
    row1 行业影响力
    row2 政策适应性

[6] 获奖
    （无则诚实写"暂无单独获奖记录"）
```

## 改写时定位单元格的通用方法

```python
from docx import Document
d = Document('申报书.docx')
cell = d.tables[TI].rows[RI].cells[CI]   # TI/RI/CI 从 0 开始
```

或直接用脚本：
```bash
python scripts/edit_cell.py --docx 申报书.docx --table TI --row RI --col CI --text paras.txt
```
