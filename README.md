
gurddy-mcp
=========

这个仓库包含一个功能完整的 MCP（Model Context Protocol）服务器，提供约束满足问题(CSP)和线性规划(LP)的求解能力。基于 `gurddy` 包实现，支持多种经典问题的求解。

## 主要功能

### CSP 问题求解
- **N-Queens问题**: 在N×N棋盘上放置N个皇后使其互不攻击
- **图着色问题**: 为图的顶点分配颜色，使相邻顶点颜色不同
- **地图着色问题**: 为地图区域分配颜色，使相邻区域颜色不同
- **数独求解**: 求解9×9数独谜题
- **通用CSP求解器**: 支持自定义约束满足问题

### LP/优化问题
- **线性规划**: 求解线性目标函数和约束的优化问题
- **生产规划**: 资源约束下的生产优化问题
- **整数规划**: 支持整数变量的优化问题

### HTTP API 服务
- RESTful API接口，支持JSON格式的请求和响应
- 完整的错误处理和性能监控
- 支持多种CSP和LP问题的在线求解

## 快速开始

### 环境准备
```bash
# 安装依赖
pip install -r requirements.txt

# 或手动安装主要依赖
pip install fastapi uvicorn gurddy pulp requests
```

## 使用方式

### 1. HTTP API 服务

启动HTTP服务器：
```bash
uvicorn mcp_server.http_api:app --host 127.0.0.1 --port 8000
```

访问API文档：http://127.0.0.1:8000/docs

### 2. 直接调用演示

运行完整的CSP功能演示：
```bash
python demo_csp_examples.py
```

测试API函数（无需启动服务器）：
```bash
python test_api_direct.py
```

### 3. 命令行工具

检查/安装 gurddy：
```bash
python -c "from mcp_server.tools.gurddy_install import run; print(run({'package':'gurddy'}))"
```

运行示例：
```bash
python -c "from mcp_server.tools.gurddy_demo import run; print(run({'example':'csp'}))"
```

## API 端点

### CSP 问题求解

#### N-Queens 问题
```bash
POST /solve-n-queens
{
  "n": 8
}
```

#### 图着色问题
```bash
POST /solve-graph-coloring
{
  "edges": [[0,1], [1,2], [2,0]],
  "num_vertices": 3,
  "max_colors": 3
}
```

#### 地图着色问题
```bash
POST /solve-map-coloring
{
  "regions": ["A", "B", "C"],
  "adjacencies": [["A", "B"], ["B", "C"]],
  "max_colors": 2
}
```

#### 数独求解
```bash
POST /solve-sudoku
{
  "puzzle": [[5,3,0,...], [6,0,0,...], ...]
}
```

#### 通用CSP求解器
```bash
POST /solve-csp
{
  "problem_type": "n_queens",
  "parameters": {"n": 4}
}
```

### LP/优化问题

#### 线性规划
```bash
POST /solve-lp
{
  "problem": {
    "profits": {"ProductA": 10, "ProductB": 15},
    "consumption": {
      "ProductA": {"Resource1": 2, "Resource2": 1},
      "ProductB": {"Resource1": 1, "Resource2": 3}
    },
    "capacities": {"Resource1": 100, "Resource2": 80}
  }
}
```

#### 生产规划
```bash
POST /solve-production-planning
{
  "profits": {"ProductA": 10, "ProductB": 15},
  "consumption": {...},
  "capacities": {...},
  "integer": true,
  "sensitivity_analysis": false
}
```

## 项目结构

```
mcp_server/
├── handlers/
│   └── gurddy.py          # 核心求解器实现
├── tools/                 # MCP工具包装器
├── examples/              # 丰富的CSP问题示例
│   ├── n_queens.py        # N皇后问题
│   ├── graph_coloring.py  # 图着色问题
│   ├── map_coloring.py    # 地图着色问题
│   ├── logic_puzzles.py   # 逻辑谜题
│   └── scheduling.py      # 调度问题
├── http_api.py           # HTTP API服务器
└── server.py             # MCP服务器

# 测试和演示文件
demo_csp_examples.py      # 完整功能演示
test_api_direct.py        # API直接测试
test_csp_api.py          # HTTP API测试
CSP_API_GUIDE.md         # API使用指南
```

## 使用示例

### 经典问题求解

#### 澳大利亚地图着色
```python
import requests

response = requests.post("http://127.0.0.1:8000/solve-map-coloring", json={
    "regions": ['WA', 'NT', 'SA', 'QLD', 'NSW', 'VIC', 'TAS'],
    "adjacencies": [
        ['WA', 'NT'], ['WA', 'SA'], ['NT', 'SA'], ['NT', 'QLD'], 
        ['SA', 'QLD'], ['SA', 'NSW'], ['SA', 'VIC'],
        ['QLD', 'NSW'], ['NSW', 'VIC']
    ],
    "max_colors": 4
})
```

#### 8皇后问题
```python
response = requests.post("http://127.0.0.1:8000/solve-n-queens", 
                        json={"n": 8})
```

#### Petersen图着色
```python
response = requests.post("http://127.0.0.1:8000/solve-graph-coloring", json={
    "edges": [
        [0,1], [1,2], [2,3], [3,4], [4,0],  # 外环
        [5,6], [6,7], [7,8], [8,9], [9,5],  # 内环  
        [0,5], [1,6], [2,7], [3,8], [4,9]   # 连接
    ],
    "num_vertices": 10,
    "max_colors": 3
})
```

## 支持的问题类型

### CSP问题
- **N-Queens**: 经典的N皇后问题，支持任意大小的棋盘
- **图着色**: 支持任意图结构的顶点着色
- **地图着色**: 地理区域的着色问题，验证四色定理
- **数独**: 标准9×9数独谜题求解
- **逻辑谜题**: 包括斑马谜题等经典逻辑推理问题
- **调度问题**: 课程调度、会议安排、资源分配等

### 优化问题  
- **线性规划**: 连续变量的线性优化
- **整数规划**: 离散变量的优化问题
- **生产规划**: 资源约束下的生产优化
- **混合整数规划**: 连续和离散变量混合的优化

## 性能特点

- **快速求解**: 对于中小规模问题（N≤12的N-Queens，<50个顶点的图着色）通常在毫秒级完成
- **内存高效**: 使用回溯搜索和约束传播，内存占用小
- **可扩展**: 支持自定义约束和目标函数
- **并发安全**: HTTP API支持并发请求处理

## 故障排查

### 常见错误
- `"gurddy package not available"`: 需要安装gurddy包
- `"No solution found"`: 在给定约束下无解，尝试放宽约束
- `"Invalid input types"`: 检查输入参数的数据类型
- `"Unknown problem type"`: 使用支持的问题类型

### 安装问题
```bash
# 如果gurddy安装失败，尝试升级pip
pip install --upgrade pip
pip install gurddy

# 如果PuLP安装失败
pip install pulp

# 检查Python环境
python -c "import sys; print(sys.executable)"
```

## 扩展开发

### 添加新的CSP问题
1. 在 `mcp_server/examples/` 中创建问题实现
2. 在 `mcp_server/handlers/gurddy.py` 中添加求解函数
3. 在 `mcp_server/http_api.py` 中添加API端点

### 自定义约束
```python
# 在gurddy中定义自定义约束
def custom_constraint(var1, var2):
    return var1 + var2 <= 10

model.addConstraint(gurddy.FunctionConstraint(custom_constraint, (var1, var2)))
```

## 许可证

本项目遵循开源许可证，具体请查看LICENSE文件。
