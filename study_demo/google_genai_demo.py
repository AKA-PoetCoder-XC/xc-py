from google import genai
from google.genai.types import Content
import json

def chat_demo():
    # 初始化API客户端
    client = genai.Client(api_key="AIzaSyB2ntGmr5ZFNv8fkVfRdRo7lxPObzsuSog")
    
    print("欢迎使用Gemini聊天程序！输入'退出'结束对话。")
    
    # 创建聊天会话 - 使用 client.chats.create 而不是 client.chat
    chat_session = client.chats.create(model="gemini-2.5-pro-exp-03-25")
    
    while True:
        # 获取用户输入
        user_input = input("\n你: ")
        
        # 检查是否退出
        if user_input.lower() in ["退出", "exit", "quit"]:
            print("谢谢使用，再见！")
            break
        
        try:
            # 发送消息并获取回复 返回流式响应
            # response = chat_session.send_message_stream(user_input)
            # 获取AI回复
            # for chunk in response:
            #     print(chunk.text, end="", flush=True)  # 实时输出每一个chunk的text

            # 发送消息并获取回复 返回文本响应
            response = chat_session.send_message(user_input)
            # 获取AI回复
            print(f"\nGemini: {response.text}")
            
        except Exception as e:
            print(f"\n发生错误: {str(e)}")

if __name__ == "__main__":
    chat_demo()
