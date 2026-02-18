# Growth Tracker CLI

轻量级用户获客渠道追踪与 ROI 分析工具

## 功能特性

- ✅ **UTM 链接生成器**: 自动生成带追踪参数的推广链接
- 📊 **渠道数据聚合**: 从本地文件/Google Analytics/数据库读取转化数据
- 💰 **ROI 分析报告**: 计算每个渠道的获客成本、转化率和投资回报率
- 📝 **Markdown 报告**: 生成可分享的分析报告

## 安装


## 快速开始

### 1. 初始化配置


这会创建:
- `config.yaml`: 配置文件
- `data/channel_data.json`: 示例数据文件

### 2. 编辑配置文件

编辑 `config.yaml`，设置各渠道的每日成本:


### 3. 生成 UTM 追踪链接


输出示例:

### 4. 分析渠道数据


## 数据格式

### 本地 JSON 数据格式

在 `data/channel_data.json` 中添加您的渠道数据:


字段说明:
- `date`: 日期 (YYYY-MM-DD)
- `channel`: 渠道名称 (需与 config.yaml 中的渠道成本配置一致)
- `visits`: 访问量
- `conversions`: 转化数 (注册/购买等)
- `revenue`: 收入 (单位: 元)

## 报告示例


## 命令参考

### `generate` - 生成 UTM 链接


### `analyze` - 分析渠道数据


### `init` - 初始化配置


## 数据源扩展

目前支持本地 JSON 文件，未来可扩展:

1. **Google Analytics 4**: 直接从 GA4 拉取数据
2. **数据库**: 从 PostgreSQL/MySQL 读取数据
3. **API 集成**: 对接第三方分析平台

## 解决用户痛点

针对"产品上线 4 个月只有不到 200 用户"的问题，本工具帮助您:

1. **追踪渠道效果**: 通过 UTM 参数精确追踪每个推广渠道的表现
2. **量化投资回报**: 计算每个渠道的 ROI，识别高效和低效渠道
3. **优化预算分配**: 基于数据决策，将预算投入到 ROI 最高的渠道
4. **降低获客成本**: 通过 CPA 分析，优化转化漏斗

## 最佳实践

1. **统一 UTM 命名**: 为所有推广链接添加 UTM 参数
2. **每日记录数据**: 定期更新 `channel_data.json` 或对接自动化数据源
3. **周期性分析**: 每周运行 `analyze` 命令，调整推广策略
4. **A/B 测试**: 使用 `utm_content` 参数测试不同广告素材

## 许可证

MIT License
cd growth-tracker-cli
pip install -e .
growth-tracker init
growth-tracker generate https://yoursite.com -s google -m cpc -c spring_sale
growth-tracker analyze --days 7 --output report.md