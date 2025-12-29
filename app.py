import streamlit as st
from core import AdvancedSummarizer
import time
import streamlit.components.v1 as components
import tempfile
import os

# 应用初始化
def setup_page():
    st.set_page_config(
        page_title="智汇摘要 - AI文本摘要生成器",
        page_icon="📝",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 注入高科技风格CSS
    
    st.markdown("""
    <style>
        /* 高科技主题配色 */
        :root {
            --primary: #1E40AF;    /* 藏青色 */
            --secondary: #1E3A8A;  /* 深藏青 */
            --accent: #60A5FA;     /* 浅天蓝 */
            --light: #F0F4FF;      /* 极浅蓝页面背景 */
            --card-bg: #FFFFFF;    /* 白色卡片背景 */
            --border: #D1D5DB;     /* 灰色边框 */
            --dark: #1F2937;       /* 深色文字 */
            --guide-bg: #F8FAFC;   /* 使用说明背景 */
        }
        
        /* 整体布局 */
        .stApp {
            background-color: var(--light);
            color: var(--dark);
            font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
        }
        
        /* 标题样式 */
        .header {
            background: linear-gradient(to right, var(--primary), var(--secondary));
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            text-align: center;
            font-size: 1.4rem;
            font-weight: 700;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
        }
        
        /* 副标题 */
        .subtitle {
            font-size: 1rem;
            color: rgba(255, 255, 255, 0.85);
            margin-top: 5px;
        }
        
        /* 主要卡片样式 */
        .main-card {
            background: var(--card-bg);
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
            border: 2px solid var(--border);
            margin-bottom: 15px;
        }
        
        /* 使用说明主卡片 */
        .guide-main-card {
            background: var(--guide-bg);
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
            border: 2px solid var(--accent);
            margin-bottom: 15px;
        }
        
        /* 卡片标题 */
        .card-title {
            color: var(--primary);
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid var(--accent);
        }
        
        /* 使用说明子模块卡片 */
        .sub-card {
            background: var(--card-bg);
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 12px;
            border: 1px solid var(--border);
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
        }
        
        /* 子卡片标题 */
        .sub-card-title {
            color: var(--secondary);
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        /* 输入框样式 */
        .stTextArea>textarea {
            background: white;
            color: var(--dark);
            border-radius: 8px;
            border: 1px solid #D1D5DB;
            padding: 15px;
            font-size: 16px;
            min-height: 200px;
            box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.03);
            font-family: 'Segoe UI', sans-serif;
            line-height: 1.8;
        }
        
        /* 文件上传样式 */
        .stFileUploader > div > div {
            border: 2px dashed var(--border);
            border-radius: 8px;
            background: white;
            padding: 20px;
        }
        
        /* 文件信息样式 */
        .file-info {
            background: #f8fafc;
            border-radius: 6px;
            padding: 10px;
            margin-top: 10px;
            border: 1px solid #e2e8f0;
        }
        
        /* 摘要框样式 */
        .summary-box {
            background: var(--card-bg);
            border-radius: 8px;
            padding: 20px;
            border: 1.5px solid var(--border);
            font-size: 16px;
            line-height: 1.8;
            min-height: 300px;
            white-space: pre-wrap;
        }
        
        /* 等待状态 */
        .placeholder-box {
            background: var(--guide-bg);
            border-radius: 8px;
            border: 2px dashed var(--border);
            color: #6B7280;
            font-size: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 300px;
            padding: 30px;
            text-align: center;
        }
        
        /* 按钮样式 */
        .stButton>button {
            background: linear-gradient(to right, var(--accent), #059669);
            color: white;
            border: none;
            border-radius: 6px;
            padding: 10px 25px;
            font-weight: 600;
            font-size: 15px;
            width: 100%;
            max-width: 280px;
            margin: 10px auto;
            display: block;
        }
        
        /* 字数统计 */
        .word-count {
            background: rgba(37, 99, 235, 0.1);
            color: var(--primary);
            border-radius: 4px;
            padding: 4px 10px;
            font-size: 0.85rem;
            font-weight: 500;
            border: 1px solid rgba(37, 99, 235, 0.2);
            display: inline-block;
            margin-bottom: 10px;
        }
        
        /* 关于我们样式 */
        .about-section {
            text-align: center;
            padding: 15px;
            margin-top: 20px;
            font-size: 0.9rem;
            color: var(--dark);
            background: var(--card-bg);
            border-radius: 10px;
            border: 2px solid var(--border);
        }
        
        /* 简洁列表样式 */
        .simple-list {
            margin: 0;
            padding: 0;
        }
        
        .simple-list div {
            margin-bottom: 8px;
            font-size: 0.9rem;
            line-height: 1.5;
        }
        
        /* 标签样式 */
        .simple-tag {
            display: inline-block;
            background: rgba(96, 165, 250, 0.1);
            color: var(--primary);
            border-radius: 4px;
            padding: 2px 8px;
            margin-right: 6px;
            font-size: 0.85rem;
            font-weight: 500;
            border: 1px solid rgba(96, 165, 250, 0.3);
        }
        
        /* 上传成功提示 */
        .upload-success {
            background: #d1fae5;
            color: #065f46;
            padding: 8px 12px;
            border-radius: 6px;
            margin-top: 10px;
            font-size: 0.9rem;
        }
    </style>
    """, unsafe_allow_html=True)

# 文档文本提取函数
def extract_text_from_file(uploaded_file):
    """从上传的PDF或Word文档中提取文本"""
    try:
        file_type = uploaded_file.name.lower()
        text = ""
            # 创建临时文件
        suffix = os.path.splitext(uploaded_file.name)  # 获取文件扩展名
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        try:
            if file_type.endswith('.pdf'):
                # 尝试导入pypdf
                try:
                    from pypdf import PdfReader
                except ImportError:
                    st.error("未安装pypdf库，无法处理PDF文件")
                    return None, "缺少依赖库"
                
                reader = PdfReader(tmp_path)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                        
            elif file_type.endswith(('.doc', '.docx')):
                # 尝试导入docx
                try:
                    from docx import Document
                except ImportError:
                    st.error("未安装python-docx库，无法处理Word文档")
                    return None, "缺少依赖库"
                
                doc = Document(tmp_path)
                for paragraph in doc.paragraphs:
                    if paragraph.text.strip():
                        text += paragraph.text + "\n"
            else:
                return None, "不支持的文件格式"
                
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
        
        if not text.strip():
            return None, "文档中没有提取到有效文本"
            
        return text.strip(), "成功"
        
    except Exception as e:
        return None, f"文档处理错误: {str(e)}"

# 复制到剪贴板函数
def copy_to_clipboard(text):
    js_code = f"""
    <script>
    function copyToClipboard() {{
        const text = `{text}`;
        navigator.clipboard.writeText(text)
            .then(() => alert('摘要已复制到剪贴板！'))
            .catch(err => alert('复制失败: ' + err));
    }}
    copyToClipboard();
    </script>
    """
    components.html(js_code, height=0)

# 主应用
def main():
    setup_page()
    summarizer = AdvancedSummarizer()
    
    # 初始化session state
    if 'text_input' not in st.session_state:
        st.session_state.text_input = ""
    if 'summary' not in st.session_state:
        st.session_state.summary = None
    if 'evaluation' not in st.session_state:
        st.session_state.evaluation = ("", "", "")
    if 'generate_clicked' not in st.session_state:
        st.session_state.generate_clicked = False
    
    # 动态标题
    st.markdown("""
    <div class="header">
        <div>📝 智汇摘要 - AI文本摘要生成器</div>
        <div class="subtitle">智能解析 · 专业提炼 · 一键生成高质量摘要</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 创建三列布局 
    col1, col2, col3 = st.columns([4, 4, 2], gap="medium")
    
    # 左侧列：输入原文
    with col1:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📝 输入原文</div>', unsafe_allow_html=True)
        
        # 文件上传区域
        uploaded_file = st.file_uploader(
            "上传PDF或Word文档",
            type=['pdf', 'doc', 'docx'],
            help="支持上传PDF、DOC、DOCX格式的文档",
            label_visibility="collapsed"
        )
        
        text_input = ""
        extracted_text = ""
        
        if uploaded_file is not None:
            # 显示文件信息
            file_size = uploaded_file.size / 1024  # KB
            st.markdown(f"""
            <div class="file-info">
                <strong>📄 已上传文件:</strong> {uploaded_file.name} ({file_size:.1f} KB)
            </div>
            """, unsafe_allow_html=True)
            
            # 提取文本
            with st.spinner('正在从文档中提取文本...'):
                extracted_text, status = extract_text_from_file(uploaded_file)
                
                if status == "成功" and extracted_text:
                    # 显示提取的文本
                    text_input = extracted_text
                    st.text_area(
                        "文档内容",
                        value=extracted_text,
                        height=200,
                        key="extracted_text",
                        label_visibility="collapsed"
                    )
                    
                    st.markdown(f'<div class="upload-success">✅ 文本提取成功！</div>', unsafe_allow_html=True)
                else:
                    st.error(f"❌ 提取失败: {status}")
        
        # 如果没上传文件或有文本输入，显示文本输入框
        if not extracted_text:
            text_input = st.text_area(
                "", 
                height=200,
                placeholder="在此粘贴或输入需要摘要的文本，或上传文档...",
                label_visibility="collapsed",
                key="input_text",
                value=st.session_state.text_input
            )
            st.session_state.text_input = text_input
        
        # 字数统计
        word_count = len(text_input) if text_input else 0
        st.markdown(f'<div class="word-count">字数: {word_count}/3000</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 摘要设置
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">⚙️ 摘要设置</div>', unsafe_allow_html=True)
        
        col_set1, col_set2 = st.columns(2)
        with col_set1:
            style = st.selectbox("摘要风格", ["学术论文", "新闻报道", "简洁概括"], index=0)
        with col_set2:
            summary_percent = st.slider("长度(%)", 10, 50, 30)
        
        # 生成按钮
        if st.button("✨ 生成智能摘要", type="primary", use_container_width=True, key="generate_btn"):
            st.session_state.generate_clicked = True
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 中间列：摘要结果
    with col2:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📄 摘要结果</div>', unsafe_allow_html=True)
        
        if st.session_state.summary:
            st.markdown(f'<div class="summary-box">{st.session_state.summary}</div>', unsafe_allow_html=True)
            
            if st.session_state.evaluation:
                eval_text, eval_icon, eval_info = st.session_state.evaluation
                st.info(f"{eval_icon} {eval_text} {eval_info}")
            
            # 功能按钮
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("📋 复制摘要", key="copy_btn", use_container_width=True):
                    copy_to_clipboard(st.session_state.summary)
            with col_btn2:
                st.download_button(
                    label="📥 导出文档",
                    data=st.session_state.summary,
                    file_name="智能摘要.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        else:
            st.markdown('<div class="placeholder-box">等待生成摘要...</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 右侧列：使用说明
    with col3:
        st.markdown('<div class="guide-main-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📖 使用说明</div>', unsafe_allow_html=True)
           # 输入文本要求
        st.markdown('<div class="sub-card">', unsafe_allow_html=True)
        st.markdown('<div class="sub-card-title">📝 文本要求</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="simple-list">
            <div>• 支持中文文本</div>
            <div>• 建议300-3000字</div>
            <div>• 结构完整，主题明确</div>
            <div>• 支持上传PDF/Word文档</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 摘要风格选择
        st.markdown('<div class="sub-card">', unsafe_allow_html=True)
        st.markdown('<div class="sub-card-title">🎨 风格选择</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="simple-list">
            <div><span class="simple-tag">学术论文</span> 学术文献</div>
            <div><span class="simple-tag">新闻报道</span> 新闻稿件</div>
            <div><span class="simple-tag">简洁概括</span> 核心要点</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 摘要长度设置
        st.markdown('<div class="sub-card">', unsafe_allow_html=True)
        st.markdown('<div class="sub-card-title">📏 长度设置</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="simple-list">
            <div>• 滑块控制长度</div>
            <div>• 范围：10%-50%</div>
            <div>• 默认：30%</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 文件支持说明
        st.markdown('<div class="sub-card">', unsafe_allow_html=True)
        st.markdown('<div class="sub-card-title">📎 文件支持</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="simple-list">
            <div>• <span class="simple-tag">PDF</span> 格式文档</div>
            <div>• <span class="simple-tag">DOC</span> Word文档</div>
            <div>• <span class="simple-tag">DOCX</span> Word文档</div>
            <div>• 最大文件：2MB</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 质量评估标准
        st.markdown('<div class="sub-card">', unsafe_allow_html=True)
        st.markdown('<div class="sub-card-title">⭐ 质量评估</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="simple-list">
            <div><span style="color: #059669;">⭐⭐⭐⭐⭐</span> 优秀</div>
            <div><span style="color: #059669;">⭐⭐⭐</span> 良好</div>
            <div><span style="color: #F59E0B;">⭐</span> 一般</div>
            <div><span style="color: #DC2626;">⚠️</span> 错误</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)  # 关闭guide-main-card
    
    # 处理生成摘要逻辑
    if st.session_state.get('generate_clicked', False):
        if not text_input.strip():
            st.warning("请输入文本内容或上传文档！", icon="⚠️")
            st.session_state.generate_clicked = False
        else:
            with st.spinner('AI分析中...'):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i in range(101):
                    progress_bar.progress(i)
                    status_text.text(f"进度: {i}%")
                    time.sleep(0.01)
                
                status_text.empty()
                
                start_time = time.time()
                summary, max_length = summarizer.generate_summary(text_input, summary_percent, style.lower())
                elapsed = time.time() - start_time
                
                st.session_state.summary = summary
                eval_text, eval_icon = summarizer.evaluate_summary(summary)
                eval_info = f"| 耗时: {elapsed:.1f}秒 | 字数: {len(summary)}/{max_length}"
                st.session_state.evaluation = (eval_text, eval_icon, eval_info)
                st.session_state.generate_clicked = False
                
                st.rerun()
    
    # 关于我们
    st.markdown("""
    <div class="about-section">
        <div style="font-size: 1rem; font-weight: 600; margin-bottom: 5px;">北京师范大学 人工智能导论 课程设计</div>
        <div style="font-size: 0.9rem;">作者：赵钰涛，张启轩</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 页脚
    st.markdown("""
    <div style="text-align: center; padding: 10px; margin-top: 10px; color: #6B7280; font-size: 0.8rem;">
        <p>© 2025 智汇摘要 - AI文本摘要生成系统 | 版本 2.0（支持文档上传）</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

