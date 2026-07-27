"""
Streamlit初体验

需求：创建第一个Streamlit应用
思路：1) 安装Streamlit 2) 创建简单页面 3) 运行应用
"""
import streamlit as st

st.title("我的第一个Streamlit应用")
st.header("一级标题")
st.subheader("二级标题")

# 段落文字
st.write("这是一个段落文字")
# 图片
st.image("./img.png")
# 音频
st.audio("https://upload-images.jianshu.io/upload_images/1439070-c0c0c0c0c0c0c0c0.png?imageMogr2/auto-orient/strip|imageView2/2/w/1240")
# 视频
st.video("https://upload-images.jianshu.io/upload_images/1439070-c0c0c0c0c0c0c0c0.png?imageMogr2/auto-orient/strip|imageView2/2/w/1240")
# 表格
st.table([
    ["姓名", "性别", "年龄"],
    ["张三", "男", "18"],
    ["李四", "女", "19"]
])
# 输入框
name = st.text_input("请输入你的名字")