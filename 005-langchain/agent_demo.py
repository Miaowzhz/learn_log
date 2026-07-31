import base64
from io import BytesIO
from PIL import Image
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from langchain_deepseek import ChatDeepSeek

ollama = ChatOllama(
    model="qwen3.5:0.8b",
    temperature=0,
)

deepseek = ChatDeepSeek(
    model="deepseek-v4-flash",
    temperature=0.7
)

# 判断是否有图片
def contains_image(messages):
    for message in messages:
        if isinstance(getattr(message, "content", None), list):
            for part in message.content:
                if isinstance(part, dict) and part.get("type") == "image_url":
                    return True
    return False

@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
    """Choose model based on conversation complexity."""
    message_count = len(request.state["messages"])

    # print(request.state["messages"])

    if contains_image(request.state['messages']):
        model = ollama
    else:
        model = deepseek

    return handler(request.override(model=model))

agent = create_agent(
    model=ollama,
    middleware=[dynamic_model_selection]
)

def convert_to_base64(pil_image, max_size=(512, 512)):
    """
    Convert PIL images to Base64 encoded strings

    :param pil_image: PIL image
    :param max_size: 最大尺寸，超过会等比缩放
    :return: Re-sized Base64 string
    """

    # 缩放图片以控制 token 数
    pil_image.thumbnail(max_size, Image.LANCZOS)

    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG", quality=75)  # You can change the format if needed
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def prompt_func(data):
    text = data["text"]
    image = data["image"]

    image_part = {
        "type": "image_url",
        "image_url": f"data:image/jpeg;base64,{image}",
    }

    content_parts = []

    text_part = {"type": "text", "text": text}

    content_parts.append(image_part)
    content_parts.append(text_part)

    return [HumanMessage(content=content_parts)]

file_path = "胆大党.jpg"
pil_image = Image.open(file_path)
image_b64 = convert_to_base64(pil_image)

message1 = prompt_func({"text": "图片里有什么内容？", "image": image_b64})
message2 = [
    HumanMessage("你是什么模型?")
]


response = agent.invoke({"messages": message1})

print( response['messages'][1].content)