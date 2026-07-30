import base64
from io import BytesIO
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from PIL import Image
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen3.5:0.8b",
    temperature=0,
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

chain = prompt_func | llm | StrOutputParser()

file_path = "胆大党.jpg"
pil_image = Image.open(file_path)

image_b64 = convert_to_base64(pil_image)
query_chain = chain.invoke(
    {"text": "图片里有什么内容？", "image": image_b64}
)

print(query_chain)
