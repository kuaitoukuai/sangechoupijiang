
from DrissionPage import *
import time
import tkinter as tk
from tkinter import ttk
import concurrent.futures
import requests
import re
from datetime import datetime
import socket

# 尝试使用默认的 Chromium 初始化
try:
    browser = Chromium()
except Exception as e:
    co = ChromiumOptions(read_file=False).set_paths(
        local_port='9888',
        browser_path=r'.\Chrome\chrome.exe',
        user_data_path=r'.\Chrome\userData'
    )
    browser = Chromium(addr_or_opts=co, session_options=False)

# 定义API列表
services = [
    {'url': 'https://myip.ipip.net  ', 'type': 'regex'},
    {'url': 'http://httpbin.org/ip  ', 'type': 'json', 'field': 'origin'},
    {'url': 'https://ident.me  ', 'type': 'text'},
    {'url': 'https://jsonip.com  ', 'type': 'json', 'field': 'ip'},
    {'url': 'https://checkip.amazonaws.com  ', 'type': 'text'},
    {'url': 'https://ipinfo.io/ip  ', 'type': 'text'}
]

# 定义要访问的网址列表
urls = [
    'https://kimi.moonshot.cn/chat  ',
    'https://metaso.cn/  ',
    'https://www.wenxiaobai.com/chat/200006  ',
    'https://chat.deepseek.com/  ',
    'https://yuanbao.tencent.com/chat  ',
    'https://zhida.zhihu.com  ',
    'https://chat.qwen.ai/  ',
    'https://claude.ai/new  ',
    'https://www.n.cn/  ',
    'https://www.google.com/  ',
    'https://gemini.google.com/app  ',
    'https://x.com/i/grok  ',
    'https://chatgpt.com/  ',
    'https://chatglm.cn/main  ',
    'https://tongyi.aliyun.com/qianwen/  ',
    'https://www.doubao.com/chat/  ',
    'https://yiyan.baidu.com/X1  ',
    'https://chat.baidu.com/search  '
]

# 为每个网址分配变量
# 初始化标签页字典
tabs = {
    'kimi.moonshot.cn': None,
    'metaso.cn': None,
    'wenxiaobai.com': None,
    'deepseek.com': None,
    'yuanbao.tencent.com': None,
    'zhida.zhihu.com': None,
    'qwen.ai': None,
    'www.google.com': None,
    'gemini.google.com': None,
    'x.com': None,
    'claude.ai': None,
    'www.n.cn': None,
    'chatgpt.com': None,
    'chatglm.cn': None,
    'tongyi.aliyun.com': None,
    'www.doubao.com': None,
    'yiyan.baidu.com': None,
    'chat.baidu.com': None
}

# 在全局变量中添加一个标志变量
first_submit = True

# 新增一个函数，用于只对当前激活的标签提问
def operate_active_tab(question):
    try:
        active_tab = browser.latest_tab
        if active_tab:
            operate_tab(active_tab, question)
    except Exception as e:
        pass

# 修改GUI创建函数，添加一个新按钮
def create_gui():
    def submit_question_to_all():
        提问 = question_text.get("1.0", "end-1c")
        operate_tabs_parallel(提问)

    def submit_question_to_active():
        提问 = question_text.get("1.0", "end-1c")
        operate_active_tab(提问)

    def check_tabs():
        count = 0  # 计数器
        tabs.clear()  # 清空旧数据
        
        # 清空旧状态显示
        status_var.set("正在检测...")
        
        for tab in browser.get_tabs():
            url = tab.url
            found = False
            if 'kimi.moonshot.cn' in url:
                tabs['kimi.moonshot.cn'] = tab
                found = True
            elif 'metaso.cn' in url:
                tabs['metaso.cn'] = tab
                found = True
            elif 'wenxiaobai.com' in url:
                tabs['wenxiaobai.com'] = tab
                found = True
            elif 'deepseek.com' in url:
                tabs['deepseek.com'] = tab
                found = True
            elif 'yuanbao.tencent.com' in url:
                tabs['yuanbao.tencent.com'] = tab
                found = True
            elif 'zhida.zhihu.com' in url:
                tabs['zhida.zhihu.com'] = tab
                found = True
            elif 'qwen.ai' in url:
                tabs['qwen.ai'] = tab
                found = True
            elif 'www.google.com' in url:
                tabs['www.google.com'] = tab
                found = True
            elif 'gemini.google.com' in url:
                tabs['gemini.google.com'] = tab
                found = True
            elif 'x.com' in url or 'twitter.com' in url:
                tabs['x.com'] = tab
                found = True
            elif 'claude.ai' in url:
                tabs['claude.ai'] = tab
                found = True
            elif 'www.n.cn' in url:
                tabs['www.n.cn'] = tab
                found = True
            elif 'chatgpt.com' in url:
                tabs['chatgpt.com'] = tab
                found = True
            elif 'chatglm.cn' in url:
                tabs['chatglm.cn'] = tab
                found = True
            elif 'tongyi.aliyun.com' in url:
                tabs['tongyi.aliyun.com'] = tab
                found = True
            elif 'www.doubao.com' in url:
                tabs['www.doubao.com'] = tab
                found = True
            elif 'yiyan.baidu.com' in url:
                tabs['yiyan.baidu.com'] = tab
                found = True
            elif 'chat.baidu.com' in url:
                tabs['chat.baidu.com'] = tab
                found = True
            
            if found:
                count += 1
        
        # 更新状态显示
        status_var.set(f"检测到 {count} 个标签页")
        if count > 0:
            status_label.config(foreground="green")
        else:
            status_label.config(foreground="red")

    root = tk.Tk()
    root.title("《三个臭皮匠》AI 提问工具-2025年3月28日版")

    # 创建主框架
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # 创建顶部控制栏框架
    control_frame = ttk.Frame(main_frame)
    control_frame.pack(fill=tk.X, pady=10)

    # 检查按钮放在左侧
    check_btn = ttk.Button(control_frame, 
                         text="检查已打开标签", 
                         command=check_tabs)
    check_btn.pack(side=tk.LEFT)

    # 状态标签放在右侧
    global status_var, status_label
    status_var = tk.StringVar(value="就绪")
    status_label = ttk.Label(control_frame, 
                           textvariable=status_var,
                           font=('微软雅黑', 10),
                           foreground="gray",
                           anchor="e")  # 文字右对齐
    status_label.pack(side=tk.RIGHT, padx=10)

    # 多行文本输入框（保持不变）
    ttk.Label(main_frame, text="输入提问内容（支持多行）:").pack(anchor=tk.W)
    question_text = tk.Text(main_frame, 
                          height=10,
                          width=50,
                          font=('微软雅黑', 10),
                          wrap=tk.WORD)
    question_text.pack(pady=5, fill=tk.BOTH, expand=True)
    question_text.insert("1.0", "一句话告诉我，今天股票新闻")

    # 提交按钮框架
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=15)

    # 提交到所有AI按钮
    submit_all_btn = ttk.Button(button_frame, 
                              text="提交到所有AI", 
                              command=submit_question_to_all)
    submit_all_btn.pack(side=tk.LEFT, padx=5)

    # 提交到当前AI按钮
    submit_active_btn = ttk.Button(button_frame, 
                                 text="提交到当前AI", 
                                 command=submit_question_to_active)
    submit_active_btn.pack(side=tk.LEFT, padx=5)

    root.mainloop()

# 获取本地IP地址
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        return "127.0.0.1"  # 默认返回本地回环地址

# 对单个标签页进行操作
def operate_tab(tab, question):
    try:
        if tab:
            full_question = f"{question}\n\n"  # 在问题末尾添加换行符

            if 'kimi.moonshot.cn' in tab.url:
                input_field = tab.ele('@class:chat-input')
                input_field.input(clear=True, vals=full_question)

            elif 'metaso.cn' in tab.url:
                input_field = tab.eles('@class:search-consult')[-1]
                input_field.input(clear=True, vals=full_question)

            elif 'wenxiaobai.com' in tab.url:
                input_field = tab.ele('@class:TextArea_container')
                try :
                    input_field.input(clear=True, vals=question)
                    time.sleep(0.1)
                    tab.ele('@class:MsgInput_send_btn').click()
                    time.sleep(0.1)
                    input_field.input(clear=False, vals="\n")
                except:
                    input_field.input(clear=True, vals=full_question)

            elif 'deepseek.com' in tab.url:
                input_field = tab.ele('@id:chat-input')
                input_field.input(clear=True, vals=full_question)

            elif 'yuanbao.tencent.com' in tab.url:
                input_field = tab.ele('@class:ql-editor')
                input_field.input(clear=True, vals=full_question)

            elif 'zhida.zhihu.com' in tab.url:
                input_field = tab.ele('@class:InputLike')
                input_field.input(clear=True, vals=full_question[0:9900]+'\n')

            elif 'qwen.ai' in tab.url:
                try:
                    input_field = tab.ele('@id:chat-input')
                    input_field.input(clear=True, vals=full_question)
                except:
                    input_field = tab.ele('@id:chat-input')
                    input_field.input(clear=True, vals=full_question)
                    time.sleep(0.1)
                    tab.ele('@class:icon-line-arrow-up').click()

            elif 'www.google.com' in tab.url:
                input_field = tab.eles('@class:gLFyf')[-1]
                input_field.input(clear=True, vals=full_question)
                
            elif 'gemini.google.com' in tab.url:
                input_field = tab.eles('@class:text-input-field_textarea-wrapper')[-1]
                input_field.input(clear=True, vals=full_question)
                
            elif 'x.com' in tab.url:
                input_field = tab.ele('@class:r-30o5oe r-1dz5y72 r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-1ny4l3l r-xyw6el r-13awgt0 r-ubezar r-k8qxaj r-1knelpx r-13qz1uu r-fdjqy7')
                input_field.input(clear=True, vals=full_question)
            
            elif 'claude.ai' in tab.url:
                input_field = tab.ele('@class:is-empty is-editor-empty before:!text-text-500 before:whitespace-nowrap')
                input_field.input(clear=True, vals=full_question)
                
            elif 'www.n.cn' in tab.url:
                try:
                    input_field = tab.eles('@id=composition-input')[-1]
                    input_field.input(clear=True, vals=question)
                    time.sleep(0.1)
                    tab.ele('@class:text-white undefined').click()
                except:
                    input_field = tab.eles('@id=composition-input')[-1]
                    input_field.input(clear=True, vals=full_question)
                
            elif 'chatgpt.com' in tab.url:
                input_field = tab.ele('@class:prosemirror-parent')
                input_field.input(clear=True, vals=full_question)
                
            elif 'chatglm.cn' in tab.url:
                input_field = tab.ele('@class=scroll-display-none')
                input_field.input(clear=True, vals=full_question)
                
            elif 'tongyi.aliyun.com' in tab.url:
                input_field = tab.ele('@class:chatInput')
                input_field.input(clear=True, vals=full_question)
                
            elif 'www.doubao.com' in tab.url:
                input_field = tab.ele('@class:semi-input-textarea semi-input-textarea-autosize')
                input_field.input(clear=True, vals=full_question)
                
            elif 'yiyan.baidu.com' in tab.url:
                try:
                    input_field = tab.ele('@class:yc-editor-paragraph')
                    input_field.input(clear=True, vals=question)
                    time.sleep(0.1)
                    tab.ele('@id=sendBtn').click()
                except:
                    input_field = tab.ele('@class:yc-editor-paragraph')
                    input_field.input(clear=True, vals=full_question)
                
            elif 'chat.baidu.com' in tab.url:
                input_field = tab.ele('@class:input-container')
                input_field.input(clear=True, vals=full_question)
                time.sleep(0.1)
                tab.ele('@class=cos-icon cos-icon-arrow-up-circle-fill send-icon active-send-icon').click()

    except Exception as e:
        pass

# 并行操作所有标签页
def operate_tabs_parallel(question):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for tab in tabs.values():
            if tab:
                futures.append(executor.submit(operate_tab, tab, question))
        for future in concurrent.futures.as_completed(futures):
            future.result()

# 创建GUI
create_gui()