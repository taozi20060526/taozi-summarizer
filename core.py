from dashscope import Generation
import re
import os
import time

class AdvancedSummarizer:
    def __init__(self):
        # 通义千问API密钥 - 请替换为您的实际密钥
        self.api_key = os.getenv('TONGYI_API_KEY', 'sk-b11af86b510848768f3d961001806b86')
    
    def safe_text_preprocessing(self, text, max_chars=3000):
        """安全文本预处理"""
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > max_chars:
            text = text[:max_chars] + " [文本已截断]"
        return text
    
    def generate_summary(self, text, summary_percent=30, style="academic"):
        """生成高质量摘要"""
        try:
            # 根据百分比计算摘要长度
            max_length = max(50, min(len(text) * summary_percent // 100, 500))
            
            # 根据风格定制提示词
            if style == "academic":
                prompt = f"请用严谨的学术语言，用不超过{max_length}字概括以下文本的核心内容，包含研究背景、方法、结果和结论：\n{text}"
            elif style == "news":
                prompt = f"请用简洁的新闻语言，用不超过{max_length}字概括以下内容，使用倒金字塔结构：\n{text}"
            else:  # concise
                prompt = f"请用最简洁的语言，用不超过{max_length}字概括以下内容：\n{text}"
            
            # 调用通义千问API
            response = Generation.call(
                model='qwen-max',
                prompt=prompt,
                api_key=self.api_key,
                max_length=max_length * 2,  # 最大token数
                temperature=0.3,
                top_p=0.8
            )
            
            # 解析结果
            if response.status_code == 200:
                summary = response.output.text
                
                # 后处理
                summary = re.sub(r'^(摘要[：:]|总结[：:]|概括[：:])', '', summary)
                if not summary.endswith(("。", "！", "？", ".")):
                    summary += "。"
                return summary.strip(), max_length
            else:
                return f"生成失败: {response.message}", 0
        except Exception as e:
            return f"API错误: {str(e)}", 0
    
    def evaluate_summary(self, summary):
        """摘要质量评估"""
        if "失败" in summary or "错误" in summary:
            return "错误：摘要生成失败", "❌"  # 使用叉号emoji
        
        # 质量评估逻辑
        sentence_count = len(re.split(r'[。！？]', summary))
        word_count = len(summary)
        
        if word_count < 20:
            return "质量差：摘要过短", "⚠️"  # 使用警告emoji
        elif sentence_count == 1:
            return "质量一般：单句摘要", "⭐"  # 使用星星emoji
        elif sentence_count >= 3:
            return "质量优秀：多句概括", "⭐⭐⭐⭐⭐"  # 使用五颗星星
        else:
            return "质量良好：基本概括", "⭐⭐⭐"  # 使用三颗星星