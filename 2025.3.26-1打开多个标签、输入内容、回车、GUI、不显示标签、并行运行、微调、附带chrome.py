from DrissionPage import *
import time
import tkinter as tk
from tkinter import ttk
import concurrent.futures

from DrissionPage import Chromium, ChromiumOptions

co = ChromiumOptions(read_file=False).set_paths(local_port='9888',
                                                browser_path=r'.\Chrome\chrome.exe',
                                                user_data_path=r'.\Chrome\userData')
browser = Chromium(addr_or_opts=co, session_options=False)


# ChromiumOptions().set_browser_path(path).save()



# 定义要访问的网址列表
urls = [
    'https://kimi.moonshot.cn/chat',
    'https://metaso.cn/',
    'https://www.wenxiaobai.com/chat/200006',
    'https://chat.deepseek.com/',
    'https://yuanbao.tencent.com/chat',
    'https://zhida.zhihu.com',
    'https://chat.qwen.ai/'
]

# 初始化浏览器
# browser = Chromium()

# 为每个网址分配变量
tabs = {
    'kimi_tab': None,
    'metaso_tab': None,
    'wenxiaobai_tab': None,
    'deepseek_tab': None,
    'yuanbao_tab': None,
    'zhihu_tab': None,
    'qwen_tab': None
}

# 遍历访问每个网址并打开新标签页
for url in urls:
    try:
        new_tab = browser.new_tab()
        new_tab.get(url)
        time.sleep(1)

        if 'kimi.moonshot.cn' in url:
            tabs['kimi_tab'] = new_tab
        elif 'metaso.cn' in url:
            tabs['metaso_tab'] = new_tab
        elif 'wenxiaobai.com' in url:
            tabs['wenxiaobai_tab'] = new_tab
        elif 'deepseek.com' in url:
            tabs['deepseek_tab'] = new_tab
        elif 'yuanbao.tencent.com' in url:
            tabs['yuanbao_tab'] = new_tab
        elif 'zhida.zhihu.com' in url:
            tabs['zhihu_tab'] = new_tab
        elif 'qwen.ai' in url:
            tabs['qwen_tab'] = new_tab

    except Exception as e:
        print(f"访问页面 {url} 时发生错误: {e}")

# 创建GUI窗口
def create_gui():
    def submit_question():
        提问 = question_text.get("1.0", "end-1c")
        # print(f"新的提问内容:\n{提问}")
        operate_tabs_parallel(提问)

    root = tk.Tk()
    root.title("AI 提问工具")

    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # 多行文本输入框
    ttk.Label(main_frame, text="输入提问内容（支持多行）:").pack(anchor=tk.W)
    question_text = tk.Text(main_frame, 
                          height=10,
                          width=50,
                          font=('微软雅黑', 10),
                          wrap=tk.WORD)
    question_text.pack(pady=5)
    question_text.insert("1.0", "讲个笑话")  # 默认提问内容

    # 提交按钮
    submit_btn = ttk.Button(main_frame, 
                          text="同时提交到所有平台", 
                          command=submit_question)
    submit_btn.pack(pady=15)

    root.mainloop()

# 对单个标签页进行操作
def operate_tab(tab, question):
    try:
        if tab:
            time.sleep(0.2)  # 基础等待时间

            if 'kimi.moonshot.cn' in tab.url:
                input_field = tab.ele('@class:chat-input')
                input_field.input(question)
                time.sleep(0.5)
                tab.ele('@class:send-button').click()

            elif 'metaso.cn' in tab.url:
                # input_field = tab.ele('@class:search-consult-textarea')
                input_field = tab.eles('@class:search-consult')[-1]
                # input_field = tab.ele('@class:search-consult')
                input_field.input(question)
                time.sleep(0.5)
                tab.ele('@class:send-arrow-button').click()

            elif 'wenxiaobai.com' in tab.url:
                input_field = tab.ele('@class:TextArea_container')
                input_field.input(question)
                time.sleep(0.5)
                tab.ele('@class:MsgInput_send_btn').click()

            elif 'deepseek.com' in tab.url:
                input_field = tab.ele('@id:chat-input')
                input_field.input(question)
                time.sleep(0.5)
                tab.eles('@class=ds-icon')[-1].click()

            elif 'yuanbao.tencent.com' in tab.url:
                input_field = tab.ele('@class:ql-editor')
                input_field.input(question)
                time.sleep(0.5)
                tab.ele('@class:style__send-btn___ZsLmU').click()

            elif 'zhida.zhihu.com' in tab.url:
                input_field = tab.ele('@class:InputLike')
                input_field.input(question)
                time.sleep(0.5)
                # tab.eles('@class：css-175oi2r')[-1].click()
                tab.eles('@class=css-175oi2r r-1loqt21 r-1otgn73')[-1].click()#知乎直答 127、149
                

            elif 'qwen.ai' in tab.url:
                input_field = tab.ele('@id:chat-input')
                input_field.input(question)
                time.sleep(0.5)
                tab.ele('@class:icon-line-arrow-up').click()

            time.sleep(0.3)  # 操作后统一等待

    except Exception as e:
        print(f"操作标签页时发生错误: {e}")

# 并行操作所有标签页
def operate_tabs_parallel(question):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for tab in tabs.values():
            if tab:
                futures.append(executor.submit(operate_tab, tab, question))
        for future in concurrent.futures.as_completed(futures):
            future.result()

create_gui()

# 最后可以取消注释关闭浏览器
# browser.quit()