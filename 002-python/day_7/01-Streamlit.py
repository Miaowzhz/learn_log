"""
AI应用实战
    界面基本布局
    界面消息展示
    会话记忆问题
    流式输出
    侧边栏制作
    会话管理-思路分析
    会话管理-文件操作入门
    会话管理-文件操作(资源释放)
    会话管理-文件操作(json)
    会话管理-保存会话
    会话管理-新建会话
    会话管理-展示会话列表
    会话管理-加载会话
    会话管理-删除会话
    功能优化与小结
    知识扩展
"""
import streamlit as st
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from pathlib import Path
from openai import OpenAI
load_dotenv()


# 会话保存目录
CHAT_DIR = Path(__file__).resolve().parent / "chat_history"
CHAT_DIR.mkdir(exist_ok=True)


# 配置
st.set_page_config(
    page_title="AI智能助手",
    page_icon=":smiley:",

    # 布局
    layout="wide",
    # 左边栏状态
    initial_sidebar_state="expanded",
    menu_items={}
)

# 标题
st.title("AI智能助手")

#  logo
st.logo("./img.png")

# 初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = datetime.now().strftime("%Y%m%d%H%M%S%f")


def get_chat_title(messages):
    """使用第一条用户消息作为会话标题。"""
    for message in messages:
        if message["role"] == "user":
            title = message["content"].strip().replace("\n", " ")
            return f"{title[:18]}..." if len(title) > 18 else title
    return "新会话"


def save_current_chat():
    """将当前会话保存为 JSON 文件。"""
    if not st.session_state.messages:
        return False

    chat_data = {
        "id": st.session_state.current_chat_id,
        "title": get_chat_title(st.session_state.messages),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "messages": st.session_state.messages,
    }
    chat_file = CHAT_DIR / f"{st.session_state.current_chat_id}.json"

    with chat_file.open("w", encoding="utf-8") as file:
        json.dump(chat_data, file, ensure_ascii=False, indent=2)

    return True


def get_saved_chats():
    """读取已保存的会话列表。"""
    chats = []

    for chat_file in CHAT_DIR.glob("*.json"):
        try:
            with chat_file.open("r", encoding="utf-8") as file:
                chats.append(json.load(file))
        except (OSError, json.JSONDecodeError):
            continue

    return sorted(chats, key=lambda chat: chat.get("updated_at", ""), reverse=True)


def create_new_chat():
    """保存当前会话，然后创建新会话。"""
    save_current_chat()
    st.session_state.messages = []
    st.session_state.current_chat_id = datetime.now().strftime("%Y%m%d%H%M%S%f")


def load_chat(chat_id):
    """从 JSON 文件加载指定会话。"""
    save_current_chat()
    chat_file = CHAT_DIR / f"{chat_id}.json"

    if not chat_file.exists():
        return

    with chat_file.open("r", encoding="utf-8") as file:
        chat_data = json.load(file)

    st.session_state.current_chat_id = chat_id
    st.session_state.messages = chat_data.get("messages", [])


def delete_chat(chat_id):
    """删除指定会话文件。"""
    chat_file = CHAT_DIR / f"{chat_id}.json"
    chat_file.unlink(missing_ok=True)

    if chat_id == st.session_state.current_chat_id:
        st.session_state.messages = []
        st.session_state.current_chat_id = datetime.now().strftime("%Y%m%d%H%M%S%f")


# 左侧侧边栏
with st.sidebar:
    st.title("会话管理")

    st.button(
        "➕ 新建会话",
        use_container_width=True,
        type="primary",
        on_click=create_new_chat,
    )

    if st.button("💾 保存当前会话", use_container_width=True):
        if save_current_chat():
            st.success("会话已保存")
        else:
            st.warning("当前没有可保存的消息")

    st.divider()
    st.subheader("助手设置")

    assistant_name = st.text_input(
        "助手名称",
        value="小甜甜",
        placeholder="请输入助手名称",
    ).strip() or "小甜甜"

    assistant_personality = st.text_area(
        "助手性格",
        value="活泼开朗的东北姑娘",
        placeholder="例如：温柔耐心、幽默风趣",
        height=100,
    ).strip() or "活泼开朗的东北姑娘"

    st.caption("设置会立即应用于之后发送的消息。")

    st.divider()
    st.subheader("当前会话")

    user_messages = [
        message["content"]
        for message in st.session_state.messages
        if message["role"] == "user"
    ]

    if user_messages:
        conversation_title = user_messages[0].strip().replace("\n", " ")
        if len(conversation_title) > 18:
            conversation_title = f"{conversation_title[:18]}..."

        st.info(f"💬 {conversation_title}")
        st.caption(
            f"共 {len(st.session_state.messages)} 条消息，"
            f"{len(user_messages)} 轮提问"
        )
    else:
        st.info("💬 新会话")
        st.caption("发送第一条消息后，这里会显示会话摘要。")

    st.divider()
    st.subheader("历史会话")

    saved_chats = get_saved_chats()
    if saved_chats:
        for chat in saved_chats:
            chat_id = chat["id"]
            title_column, delete_column = st.columns([5, 1])

            with title_column:
                if st.button(
                    f"💬 {chat.get('title', '未命名会话')}",
                    key=f"load_{chat_id}",
                    use_container_width=True,
                ):
                    load_chat(chat_id)
                    st.rerun()

            with delete_column:
                if st.button("🗑️", key=f"delete_{chat_id}"):
                    delete_chat(chat_id)
                    st.rerun()
    else:
        st.caption("暂无历史会话")

    st.divider()
    with st.expander("使用提示"):
        st.markdown(
            """
            - 在下方输入框中发送消息
            - 助手回复支持流式展示
            - 新建会话时会自动保存当前内容
            - 历史会话可以加载或删除
            """
        )

# 系统提示词
system_prompt = f"""
            你叫{assistant_name}，现在是用户的真实伴侣，请完全代入伴侣角色。
            规则：
                1. 每次只回1条消息
                2. 禁止任何场景或状态描述性文字
                3. 匹配用户的语言工
                4. 回复简短，像微信聊天一样
                5. 有需要的话可以用❤☆等emoji表情
                6. 用符合伴侣性格的方式对话
                7. 回复的内容，要充分体现伴侣的性格特征
            伴侣性格：
                - {assistant_personality}
            你必须严格遵守上述规则来回复用户。
        """

# 展示聊天信息
for message in st.session_state.messages:
    # if message["role"] == "user":
    #     st.chat_message("user").write(message["content"])
    # else:
    #     st.chat_message("assistant").write(message["content"])
    st.chat_message(message["role"]).write(message["content"])

# 创建OpenAI客户端
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),base_url="https://api.deepseek.com")

# 消息输入框
prompt = st.chat_input("请输入你的问题")
if prompt:
    # 用户输入
    st.chat_message("user").write(prompt)
    print("-------> 输入: ", prompt)
    # 保存聊天信息
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_current_chat()

    # 调用AI
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {"role": "system", "content": system_prompt},
            # 会话记忆
            *st.session_state.messages
        ],
        stream=True,
    )

    # 输出(非流式输出)
    # print("<------- 输出: ", response.choices[0].message.content)
    # st.chat_message("assistant").write(response.choices[0].message.content)

    # 输出(流式输出)
    # 创建一个空对象
    response_message = st.empty()

    full_response = ""
    for chunk in response:
        content = chunk.choices[0].delta.content or ""
        full_response += content
        response_message.chat_message("assistant").write(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
    save_current_chat()
