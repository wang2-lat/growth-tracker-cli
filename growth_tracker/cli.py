import typer
from pathlib import Path
from typing import Optional
from .utm_generator import generate_utm_link
from .analytics import fetch_channel_data, calculate_roi
from .reporter import generate_report

app = typer.Typer(help="轻量级用户获客渠道追踪与 ROI 分析工具")

@app.command()
def generate(
    url: str = typer.Argument(..., help="基础推广链接"),
    source: str = typer.Option(..., "--source", "-s", help="流量来源 (如: google, facebook)"),
    medium: str = typer.Option(..., "--medium", "-m", help="媒介类型 (如: cpc, email, social)"),
    campaign: str = typer.Option(..., "--campaign", "-c", help="活动名称"),
    term: Optional[str] = typer.Option(None, "--term", "-t", help="关键词"),
    content: Optional[str] = typer.Option(None, "--content", help="广告内容标识"),
):
    """生成带 UTM 参数的追踪链接"""
    utm_link = generate_utm_link(url, source, medium, campaign, term, content)
    typer.echo(f"\n✅ UTM 链接已生成:\n{utm_link}\n")

@app.command()
def analyze(
    days: int = typer.Option(7, "--days", "-d", help="分析最近 N 天的数据"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="输出 Markdown 报告路径"),
):
    """分析渠道数据并生成 ROI 报告"""
    try:
        typer.echo(f"📊 正在分析最近 {days} 天的渠道数据...\n")
        
        # 获取渠道数据
        channel_data = fetch_channel_data(days)
        
        if not channel_data:
            typer.echo("⚠️  未找到渠道数据，请先配置数据源或添加测试数据")
            return
        
        # 计算 ROI
        roi_data = calculate_roi(channel_data)
        
        # 生成报告
        report = generate_report(roi_data, days)
        
        # 输出到终端
        typer.echo(report)
        
        # 保存到文件
        if output:
            output.write_text(report, encoding="utf-8")
            typer.echo(f"\n✅ 报告已保存至: {output}")
            
    except Exception as e:
        typer.echo(f"❌ 错误: {str(e)}", err=True)
        raise typer.Exit(1)

@app.command()
def init():
    """初始化配置文件"""
    config_path = Path("config.yaml")
    if config_path.exists():
        typer.echo("⚠️  config.yaml 已存在")
        return
    
    config_content = """# Growth Tracker 配置文件

# 数据源配置 (选择一种)
data_source:
  type: "local"  # local | google_analytics | database
  
  # 本地 JSON 数据文件路径
  local_file: "data/channel_data.json"
  
  # Google Analytics 配置 (如使用 GA)
  # ga_property_id: "GA4-XXXXXX"
  # ga_credentials: "path/to/credentials.json"
  
  # 数据库配置 (如使用数据库)
  # db_type: "postgresql"
  # db_host: "localhost"
  # db_port: 5432
  # db_name: "growth_tracker"
  # db_user: "user"
  # db_password: "password"

# 渠道成本配置 (每日成本，单位: 元)
channel_costs:
  google: 500
  facebook: 300
  xiaohongshu: 200
  wechat: 100
  email: 50
"""
    config_path.write_text(config_content, encoding="utf-8")
    
    # 创建示例数据文件
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    sample_data = """[
  {
    "date": "2026-02-17",
    "channel": "google",
    "visits": 150,
    "conversions": 8,
    "revenue": 2400
  },
  {
    "date": "2026-02-17",
    "channel": "facebook",
    "visits": 200,
    "conversions": 5,
    "revenue": 1500
  },
  {
    "date": "2026-02-16",
    "channel": "google",
    "visits": 120,
    "conversions": 6,
    "revenue": 1800
  }
]"""
    (data_dir / "channel_data.json").write_text(sample_data, encoding="utf-8")
    
    typer.echo("✅ 配置文件已创建: config.yaml")
    typer.echo("✅ 示例数据已创建: data/channel_data.json")
    typer.echo("\n请编辑 config.yaml 配置您的数据源和渠道成本")

if __name__ == "__main__":
    app()