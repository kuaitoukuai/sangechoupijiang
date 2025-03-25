from DrissionPage import *
import time
import tkinter as tk
from tkinter import ttk
import concurrent.futures

# 定义要访问的网址列表
urls = [
    'https://kimi.moonshot.cn/chat',  # Kimi
    'https://metaso.cn/',                                # 秘塔AI搜索
    'https://www.wenxiaobai.com/chat/200006',  # 问小白
    'https://chat.deepseek.com/',                        # DeepSeek
    'https://yuanbao.tencent.com/chat',       # 腾讯元宝
    'https://zhida.zhihu.com',# 知乎直答
    'https://chat.qwen.ai/'                             # Qwen
]

# 初始化浏览器
browser = Chromium()

# 为每个网址分配一个独立的变量
kimi_tab = None
metaso_tab = None
wenxiaobai_tab = None
deepseek_tab = None
yuanbao_tab = None
zhihu_tab = None
qwen_tab = None

# 遍历访问每个网址并打开新标签页
for url in urls:
    try:
        new_tab = browser.new_tab()
        new_tab.get(url)
        # print(f"打开新标签页: {url}")
        time.sleep(1)

        if 'kimi.moonshot.cn' in url:
            kimi_tab = new_tab
            # print("Kimi 标签页已分配")
        elif 'metaso.cn' in url:
            metaso_tab = new_tab
            # print("秘塔AI搜索 标签页已分配")
        elif 'wenxiaobai.com' in url:
            wenxiaobai_tab = new_tab
            # print("问小白 标签页已分配")
        elif 'deepseek.com' in url:
            deepseek_tab = new_tab
            # print("DeepSeek 标签页已分配")
        elif 'yuanbao.tencent.com' in url:
            yuanbao_tab = new_tab
            # print("腾讯元宝 标签页已分配")
        elif 'zhida.zhihu.com' in url:
            zhihu_tab = new_tab
            # print("知乎直答 标签页已分配")
        elif 'qwen.ai' in url:
            qwen_tab = new_tab
            # print("Qwen 标签页已分配")

    except Exception as e:
        print(f"访问页面 {url} 时发生错误: {e}")

# 定义提问内容和间隔时间
提问 = "讲个笑话"
interval = 0.5  # 默认间隔时间

# 创建GUI窗口
def create_gui():
    global 提问, interval

    def submit_question():
        global 提问, interval
        提问 = question_entry.get()
        try:
            interval = float(interval_entry.get())
        except:
            interval = 1  # 默认间隔时间
        print(f"新的提问内容: {提问}, 间隔时间: {interval}秒")
        operate_tabs_parallel()  # 提交后立即执行操作

    root = tk.Tk()
    root.title("提问设置")

    frame = ttk.Frame(root, padding="20")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # 提问输入框
    question_label = ttk.Label(frame, text="请输入提问内容:")
    question_label.grid(row=0, column=0, sticky=tk.W, pady=5)

    question_entry = ttk.Entry(frame, width=50)
    question_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
    question_entry.insert(0, 提问)

    # 间隔时间输入框
    interval_label = ttk.Label(frame, text="请输入操作间隔时间(秒):")
    interval_label.grid(row=2, column=0, sticky=tk.W, pady=5)

    interval_entry = ttk.Entry(frame, width=50)
    interval_entry.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
    interval_entry.insert(0, str(interval))

    submit_button = ttk.Button(frame, text="提交", command=submit_question)
    submit_button.grid(row=4, column=0, pady=10)

    root.mainloop()

# 对单个标签页进行操作
def operate_tab(tab, question, interval):
    try:
        if tab:
            # print(f"操作 {tab.title} 标签页")
            # browser.activate_tab(tab)
            # print(f"当前激活的标签页: {tab.title}")
            time.sleep(0.2)  # 短暂等待页面响应

            if 'kimi.moonshot.cn' in tab.url:
                # input_field = tab.ele('@class:chat-input-editor')
                input_field = tab.ele('@class:chat-input')
                input_field.input(question)
                time.sleep(interval)
                send_button = tab.ele('@class:send-button')
                send_button.click()
                time.sleep(interval)

            elif 'metaso.cn' in tab.url:
                input_field = tab.ele('@class:search-consult-textarea search-consult-textarea_search-consult-textarea__kjgyz')
                input_field.input(question)
                time.sleep(interval)
                send_button = tab.ele('@class:MuiButtonBase-root MuiIconButton-root MuiIconButton-sizeMedium send-arrow-button css-1rab04c')
                send_button.click()
                time.sleep(interval)

            elif 'wenxiaobai.com' in tab.url:
                input_field = tab.ele('@class:TextArea_container')
                time.sleep(interval)
                input_field.input(question)
                time.sleep(interval)
                send_button = tab.ele('@class:icon-font-svg MsgInput_send_btn')
                send_button.click()
                time.sleep(interval)

            elif 'deepseek.com' in tab.url:
                input_field = tab.ele('@id:chat-input')
                input_field.input(question)
                time.sleep(interval)
                send_button = tab.eles('@class=ds-icon')[-1]
                send_button.click()
                time.sleep(interval)

            elif 'yuanbao.tencent.com' in tab.url:
                # input_field = tab.ele('@class=ql-editor ql-blank') #输入后这个class变化了
                input_field = tab.ele('@class:ql-editor')
                input_field.input(question)
                time.sleep(interval)
                send_button = tab.ele('@class:style__send-btn___ZsLmU')
                send_button.click()
                time.sleep(interval)

            elif 'zhida.zhihu.com' in tab.url:
                # input_field = tab.ele('@class=css-11aywtz')
                input_field = tab.ele('@class:InputLike') #知乎直答完成
                input_field.input(question)
                time.sleep(interval)
                send_button = tab.eles('@class=css-175oi2r r-1loqt21 r-1otgn73')[-1]
                send_button.click()
                time.sleep(interval)

            elif 'qwen.ai' in tab.url:
                input_field = tab.ele('@id:chat-input')
                input_field.input(question)
                time.sleep(interval)
                send_button = tab.ele('@class:iconfont leading-none icon-line-arrow-up !text-20')
                send_button.click()
                time.sleep(interval)

    except Exception as e:
        print(f"操作标签页 {tab.title} 时发生错误: {e}")

# 并行操作所有标签页
def operate_tabs_parallel():
    tabs = [kimi_tab, metaso_tab, wenxiaobai_tab, deepseek_tab, yuanbao_tab, zhihu_tab, qwen_tab]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for tab in tabs:
            if tab:
                futures.append(executor.submit(operate_tab, tab, 提问, interval))
        for future in concurrent.futures.as_completed(futures):
            future.result()

create_gui()

# 关闭浏览器
# browser.quit()
