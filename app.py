import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# GitHub 上 Excel 文件的原始 URL
url = "https://github.com/Jiemuluyin/-/blob/main/Replacements.xlsx"

# 获取文件内容
response = requests.get(url)

# 使用 openpyxl 引擎读取 Excel 文件
df = pd.read_excel(BytesIO(response.content), engine='openpyxl')

# 设置网页标题
st.set_page_config(page_title="文本转换器", layout="wide")
st.title("文本转换器")

# 创建两列布局
col1, col2 = st.columns(2)

# 原始输入区域
with col1:
    st.subheader("原始文本")
    input_text = st.text_area("在此输入原始文本", height=400, label_visibility="collapsed")

# 中间区域用于按钮
with st.container():
    # 自定义按钮和文本框的悬停样式
    button_and_textbox_style = """
    <style>
        .stButton>button {
            font-size: 24px; /* 调整字体大小 */
            font-weight: bold; /* 字体加粗 */
            padding: 10px 20px;
            border-radius: 30px;
            background-color: #4CAF50;
            color: white; /* 文字颜色改为白色 */
            border: none;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #4CAF50; /* 不变的背景色 */
            color: white; /* 保持白色文字 */
        }

        .stTextArea textarea:focus {
            border: 2px solid #FFA500; /* 橘黄色边框 */
            box-shadow: 0 0 5px 2px rgba(255, 165, 0, 0.5); /* 橘黄色阴影 */
        }
    </style>
    """
    st.markdown(button_and_textbox_style, unsafe_allow_html=True)

    # 圆形按钮改为显示"开始转换"
    if st.button("开始转换", use_container_width=True):
        # 执行替换逻辑
        converted_text = input_text
        if input_text:
            for _, row in df.iterrows():
                if pd.notna(row["原词"]) and pd.notna(row["替换词"]):
                    converted_text = converted_text.replace(str(row["原词"]), str(row["替换词"]))

# 转换后输出区域
with col2:
    st.subheader("转换后文本")
    converted_text = converted_text if 'converted_text' in locals() else ""
    st.text_area("转换结果", converted_text, height=400, label_visibility="collapsed", key="converted")
