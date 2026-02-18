import json
import yaml
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any

def load_config() -> Dict[str, Any]:
    """加载配置文件"""
    config_path = Path("config.yaml")
    if not config_path.exists():
        raise FileNotFoundError("配置文件不存在，请先运行 'growth-tracker init'")
    
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def fetch_channel_data(days: int) -> List[Dict[str, Any]]:
    """
    获取渠道数据
    
    Args:
        days: 获取最近 N 天的数据
    
    Returns:
        渠道数据列表
    """
    config = load_config()
    data_source = config.get("data_source", {})
    source_type = data_source.get("type", "local")
    
    if source_type == "local":
        return _fetch_local_data(data_source.get("local_file", "data/channel_data.json"), days)
    elif source_type == "google_analytics":
        # 预留 GA 集成接口
        raise NotImplementedError("Google Analytics 集成待实现")
    elif source_type == "database":
        # 预留数据库集成接口
        raise NotImplementedError("数据库集成待实现")
    else:
        raise ValueError(f"不支持的数据源类型: {source_type}")

def _fetch_local_data(file_path: str, days: int) -> List[Dict[str, Any]]:
    """从本地 JSON 文件读取数据"""
    data_file = Path(file_path)
    if not data_file.exists():
        return []
    
    with open(data_file, "r", encoding="utf-8") as f:
        all_data = json.load(f)
    
    # 过滤最近 N 天的数据
    cutoff_date = (datetime.now() - timedelta(days=days)).date()
    filtered_data = [
        item for item in all_data
        if datetime.strptime(item["date"], "%Y-%m-%d").date() >= cutoff_date
    ]
    
    return filtered_data

def calculate_roi(channel_data: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
    """
    计算各渠道的 ROI
    
    Args:
        channel_data: 渠道数据列表
    
    Returns:
        各渠道的汇总数据和 ROI
    """
    config = load_config()
    channel_costs = config.get("channel_costs", {})
    
    # 按渠道聚合数据
    aggregated = {}
    for item in channel_data:
        channel = item["channel"]
        if channel not in aggregated:
            aggregated[channel] = {
                "visits": 0,
                "conversions": 0,
                "revenue": 0,
                "days": set()
            }
        
        aggregated[channel]["visits"] += item.get("visits", 0)
        aggregated[channel]["conversions"] += item.get("conversions", 0)
        aggregated[channel]["revenue"] += item.get("revenue", 0)
        aggregated[channel]["days"].add(item["date"])
    
    # 计算 ROI
    roi_data = {}
    for channel, data in aggregated.items():
        days_count = len(data["days"])
        daily_cost = channel_costs.get(channel, 0)
        total_cost = daily_cost * days_count
        
        revenue = data["revenue"]
        roi = ((revenue - total_cost) / total_cost * 100) if total_cost > 0 else 0
        cpa = total_cost / data["conversions"] if data["conversions"] > 0 else 0
        conversion_rate = (data["conversions"] / data["visits"] * 100) if data["visits"] > 0 else 0
        
        roi_data[channel] = {
            "visits": data["visits"],
            "conversions": data["conversions"],
            "revenue": revenue,
            "cost": total_cost,
            "roi": roi,
            "cpa": cpa,
            "conversion_rate": conversion_rate,
        }
    
    return roi_data