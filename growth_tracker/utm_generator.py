from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
from typing import Optional

def generate_utm_link(
    base_url: str,
    source: str,
    medium: str,
    campaign: str,
    term: Optional[str] = None,
    content: Optional[str] = None,
) -> str:
    """
    生成带 UTM 参数的追踪链接
    
    Args:
        base_url: 基础 URL
        source: 流量来源 (utm_source)
        medium: 媒介类型 (utm_medium)
        campaign: 活动名称 (utm_campaign)
        term: 关键词 (utm_term)
        content: 广告内容 (utm_content)
    
    Returns:
        完整的 UTM 追踪链接
    """
    # 解析原始 URL
    parsed = urlparse(base_url)
    query_params = parse_qs(parsed.query)
    
    # 添加 UTM 参数
    utm_params = {
        "utm_source": source,
        "utm_medium": medium,
        "utm_campaign": campaign,
    }
    
    if term:
        utm_params["utm_term"] = term
    if content:
        utm_params["utm_content"] = content
    
    # 合并参数
    for key, value in utm_params.items():
        query_params[key] = [value]
    
    # 重建 URL
    new_query = urlencode(query_params, doseq=True)
    new_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))
    
    return new_url