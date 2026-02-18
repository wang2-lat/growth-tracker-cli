from typing import Dict, Any
from datetime import datetime
from tabulate import tabulate

def generate_report(roi_data: Dict[str, Dict[str, float]], days: int) -> str:
    """
    生成 ROI 分析报告
    
    Args:
        roi_data: ROI 数据
        days: 分析天数
    
    Returns:
        Markdown 格式的报告
    """
    report_lines = []
    
    # 标题
    report_lines.append(f"# 获客渠道 ROI 分析报告")
    report_lines.append(f"\n**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"**分析周期**: 最近 {days} 天\n")
    
    # 汇总数据
    total_visits = sum(d["visits"] for d in roi_data.values())
    total_conversions = sum(d["conversions"] for d in roi_data.values())
    total_revenue = sum(d["revenue"] for d in roi_data.values())
    total_cost = sum(d["cost"] for d in roi_data.values())
    overall_roi = ((total_revenue - total_cost) / total_cost * 100) if total_cost > 0 else 0
    
    report_lines.append("## 📊 整体概览\n")
    report_lines.append(f"- **总访问量**: {total_visits:,}")
    report_lines.append(f"- **总转化数**: {total_conversions}")
    report_lines.append(f"- **总收入**: ¥{total_revenue:,.2f}")
    report_lines.append(f"- **总成本**: ¥{total_cost:,.2f}")
    report_lines.append(f"- **整体 ROI**: {overall_roi:.2f}%\n")
    
    # 渠道详情表格
    report_lines.append("## 📈 各渠道详情\n")
    
    table_data = []
    for channel, data in sorted(roi_data.items(), key=lambda x: x[1]["roi"], reverse=True):
        table_data.append([
            channel,
            f"{data['visits']:,}",
            data['conversions'],
            f"{data['conversion_rate']:.2f}%",
            f"¥{data['revenue']:,.2f}",
            f"¥{data['cost']:,.2f}",
            f"¥{data['cpa']:.2f}",
            f"{data['roi']:.2f}%"
        ])
    
    headers = ["渠道", "访问量", "转化数", "转化率", "收入", "成本", "CPA", "ROI"]
    table = tabulate(table_data, headers=headers, tablefmt="github")
    report_lines.append(table)
    
    # 优化建议
    report_lines.append("\n## 💡 优化建议\n")
    
    best_roi_channel = max(roi_data.items(), key=lambda x: x[1]["roi"])
    worst_roi_channel = min(roi_data.items(), key=lambda x: x[1]["roi"])
    
    report_lines.append(f"1. **最佳渠道**: {best_roi_channel[0]} (ROI: {best_roi_channel[1]['roi']:.2f}%) - 建议加大投入")
    report_lines.append(f"2. **待优化渠道**: {worst_roi_channel[0]} (ROI: {worst_roi_channel[1]['roi']:.2f}%) - 需要优化或减少投入")
    
    # 识别低转化率渠道
    low_conversion = [ch for ch, d in roi_data.items() if d["conversion_rate"] < 2]
    if low_conversion:
        report_lines.append(f"3. **低转化率渠道**: {', '.join(low_conversion)} - 检查落地页和用户体验")
    
    return "\n".join(report_lines)