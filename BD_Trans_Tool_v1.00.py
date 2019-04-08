import tkinter
from tkinter import filedialog
from tkinter import messagebox

import http.client
import hashlib
import urllib.parse
import random
import json
import re

# LANGUAGE LIST
language_dict = {
    "zh":"中文",
    "en":"英语",
    "yue":"粤语",
    "wyw":"文言文",
    "jp":"日语",
    "kor":"韩语",
    "fra":"法语",
    "th":"泰语",
    "spa":"西班牙语",
    "ara":"阿拉伯语",
    "ru":"俄语",
    "pt":"葡萄牙语",
    "de":"德语",
    "it":"意大利语",
    "el":"希腊语",
    "nl":"荷兰语",
    "pl":"波兰语",
    "bul":"保加利亚语",
    "est":"爱沙尼亚语",
    "dan":"丹麦语",
    "fin":"芬兰语",
    "cs":"捷克语",
    "rom":"罗马尼亚语",
    "slo":"斯洛文尼亚语",
    "swe":"瑞典语",
    "hu":"匈牙利语",
    "cht":"繁体中文",
    "vie":"越南语"
}


# LANGUAGE LIST

def baiduTranslate(q="translate", fromLang="auto", toLang="zh"):
    appid = '20190405000284840'
    secretKey = 'eYK0BQrpLj0tPtPppE32' 

    httpClient = None
    myurl = '/api/trans/vip/translate'
    salt = random.randint(32768, 65536)
    sign = appid+q+str(salt)+secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode())
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+urllib.parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    result = ""
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        response = httpClient.getresponse()
        result = response.read()
    except Exception as e:
        print (e)
    finally:
        if httpClient:
            httpClient.close()

    return result


def clean_up_reg(wow):
    raw = str(wow)
    print (raw)
    ss = re.search(r"dst': '",raw)
    ee = re.search(r"'}]}",raw)
    print(ss)
    print(ee)
    sd = ss.end()
    ed = ee.start()
    c_string = raw[sd:ed]
    return c_string

def clean_up_lan(wow):
    raw = str(wow)
    ss = re.search(r"'from': '",raw)
    ee = re.search(r"', 'to': '",raw)
    sd = ss.end()
    ed = ee.start()
    c_string = raw[sd:ed]
    return c_string


# GUI VIA TKINTER
tool_title = "多语言到简体中文翻译 | Version 1.00 | Copyright © 2019 Zach X.G. Zheng | Zach@Zachitect.com | Zachitect.com"

# --- LONG TEXT CONTENT
R_Introduction = '''
左侧文本框输入或粘贴需要翻译的文本，并点击左侧Translate按钮翻译。
此工具需要联网，基于百度在线翻译，自动检测输入语种。目前支持的语言有：
中、英、日、韩、西、法、泰、阿、俄、葡、德、意、荷、芬、丹等28种语言。
'''

# --- TKINTER GRAPHIC CONTROL
root_colour = "#2A363B"
cursor_type = "plus"

button_act_bg = "#2A363B"
button_act_fg = "#ffffff"
button_fg = "#ffffff"

button_borderwidth = 0
button_font = ("Helvetica", 11)
button_relief = "flat"

text_bg = "#3f4a4e"
text_fg = "#ffffff"
text_borderwidth = 0
text_cursor = "plus"
text_font = ("Helvetica", 10)
text_pad_LR = 2
text_pad_TD = 2
text_relif = "flat"

entry_fg = "#ffffff"
entry_hlc = "#86A3C3"
entry_hlb = "#86A3C3"
entry_hl_thickness = 5
entry_relief = "flat"

entry_borderwidth = 0
entry_font = ("Helvetica", 10)

# --- TKINTER GUI MAIN WINDOW
root = tkinter.Tk()
root.title(tool_title)
root.configure(bg = "#86A3C3",cursor = cursor_type, bd = 5)
root.resizable(True, True)
root.overrideredirect(False)

for row in range(0,6):
    root.rowconfigure(row, weight=1)
for column in range(0,9):
    root.columnconfigure(column, weight=1)



# --- TKINTER CLASSES
class frame:
    def __init__(self, parent_frame, back_ground, frame_hl_thickness, frame_hl_bg,row_coordinate, column_coordinate, row_span, column_span):
        self.object = tkinter.Frame(parent_frame, bg = back_ground, bd = 0, cursor = cursor_type, relief = "flat", highlightbackground = frame_hl_bg, highlightthickness = frame_hl_thickness, highlightcolor = frame_hl_bg)
        self.object.grid(row = row_coordinate, column = column_coordinate, rowspan = row_span, columnspan = column_span, sticky = "news")
        for row in range(0, row_span):
            self.object.rowconfigure(row, weight = 1)
        for column in range(0, column_span):
            self.object.columnconfigure(column, weight = 1)
        self.object.grid_propagate(False)

class button:
    def __init__(self, parent_frame, button_bg, button_text, button_command, button_state, row_coordinate, column_coordinate, row_span, column_span):
        self.object = tkinter.Button(parent_frame, activebackground = button_act_bg, activeforeground = button_act_fg, text = button_text, bd = button_borderwidth, bg = button_bg, fg = button_fg, font = button_font, relief = button_relief, state = button_state, command = button_command)
        self.object.grid(row = row_coordinate, column = column_coordinate, rowspan = row_span, columnspan = column_span, sticky = "news")
        self.object.grid_propagate(False)

class display:
    def __init__(self, parent_frame, row_coordinate, column_coordinate, row_span, column_span):
        self.object = tkinter.Text(parent_frame, height = 10, width = 10, bg = text_bg, fg = text_fg, bd = text_borderwidth, cursor = text_cursor, font = text_font, padx = text_pad_LR, pady = text_pad_TD, relief = text_relif, state = "disabled")
        self.object.grid(row = row_coordinate, column = column_coordinate, rowspan = row_span, columnspan = column_span, sticky = "news")
        self.object.grid_propagate(False)

class entry:
    def __init__(self, parent_frame, entry_bg, entry_textvariable,row_coordinate, column_coordinate, row_span, column_span):
        self.object = tkinter.Entry(parent_frame, bg = entry_bg, fg = entry_fg, highlightcolor = entry_hlc, highlightbackground = entry_hlb, highlightthickness = entry_hl_thickness, relief = entry_relief, bd = entry_borderwidth, font = entry_font, textvariable = entry_textvariable, justify = "center")
        self.object.grid(row = row_coordinate, column = column_coordinate, rowspan = row_span, columnspan = column_span, sticky = "ew")
        self.object.grid_propagate(False)


# FUNCTIONS
help_condiiton = False
def help_hit():
    global help_condiiton
    if help_condiiton == False:
        help_condiiton = True
        frame_intro.object.grid(row = 6, column = 0, rowspan = 1, columnspan = 9)
        root.geometry("900x511")
    else:
        help_condiiton = False
        frame_intro.object.grid_forget()
        root.geometry("900x335")

def tkupdate_text(tk_textbox, content):
    tk_textbox.config(state = "normal")
    tk_textbox.delete("1.0", "end")
    tk_textbox.insert("1.0", str(content))
    tk_textbox.config(state = "disabled")


def read_text():
    text_pasted = t_existing_names.object.get(1.0, "end-1c")
    split_pasted = text_pasted.splitlines()
    combine_text = []
    combine_lan = []
    for s in split_pasted:
        if len(s)>0:
            translate = json.loads(baiduTranslate(q=s))
            translated = clean_up_reg(translate)
            lan = clean_up_lan(translate)
            sc_lan = language_dict[lan]
            combine_text.append(translated)
            combine_lan.append(sc_lan)
    translated_result = ('\n'+"\n").join(combine_text)
    tkupdate_text(t_new_names.object,translated_result)
    tkupdate_text(t_directory.object,"自动检测语言为：" + combine_lan[0])
    

# --- TKINTER FRAMES
frame_button = frame(root,"#2A363B",0, "#2A363B", 0,0,5,1)
frame_display_dir = frame(root,"#3f4a4e",0, root_colour, 0,1,1,8)
frame_display_name_frame = frame(root,"#2A363B",0, root_colour, 1,1,4,8)
frame_display_names = frame(frame_display_name_frame.object,"#2A363B",5, root_colour, 0,0,4,8)
frame_old = frame(frame_display_names.object,"#2A363B",0, "#2A363B", 0,0,4,4)
frame_new = frame(frame_display_names.object,"#2A363B",0, "#2A363B", 0,4,4,4)
frame_entry = frame(root,"#86A3C3",0, "#ffffff", 5,1,1,8)
frame_empty = frame(root, "#86A3C3",0, "#ffffff", 5,0,1,1)
frame_intro = frame(root,"#86A3C3",0,"#86A3C3", 6,0,1,9)
frame_intro_sub = tkinter.Frame(frame_intro.object)
frame_intro_sub.pack(side = "bottom")


# --- TKINTER SEPARATORS (USING FRAME WIDTH = 1)
frame_separator = tkinter.Frame(frame_display_names.object,bg = root_colour,bd = 1,height = 10, width = 0, relief = "flat")
frame_separator.pack(expand =1, fill = "y")

 # --- TKINTER TEXT BOXES
t_directory = display(frame_display_dir.object, 0,0,1,8)
t_existing_names = display(frame_old.object, 0,0,4,4)
t_new_names = display(frame_new.object, 0,0,4,4)

# --- TKINTER BUTTONS
b_select_directory = button(frame_button.object,"#F8B195" ,"•",print(),"normal", 0,0,1,1)
b_select_files = button(frame_button.object,"#F67280" ,"Translate",read_text,"normal", 1,0,1,1)
b_preview = button(frame_button.object,"#C06C84" ,"•",print(),"normal", 2,0,1,1)
b_rename = button(frame_button.object,"#6C5B7B" ,"•",print(),"normal", 3,0,1,1)
b_cancel = button(frame_button.object,"#355C7D","•",print(),"normal", 4,0,1,1)
b_help = button(frame_empty.object,"#86A3C3","⮟",help_hit,"normal", 0,0,1,1)


# --- TKINTER LABELS
plus_label = tkinter.Label(frame_entry.object, text = "", fg = "#ffffff",bg = "#86A3C3",font=("Helvetica", 10))
ext_label = tkinter.Label(frame_entry.object, text = "", fg = "#ffffff",bg = "#86A3C3",font=("Helvetica", 10))
intro_label = tkinter.Label(frame_intro_sub, justify = "left", text = R_Introduction, height = 10, fg = "#ffffff",bg = "#86A3C3",font = ("Helvetica", 11))

plus_label.grid(row = 0, column = 2, rowspan = 1, columnspan = 1, sticky = "ew")
ext_label.grid(row = 0, column = 5,rowspan = 1, columnspan = 1, sticky = "ew")
intro_label.pack()

tkupdate_text(t_existing_names.object,"输入需要翻译的内容，支持28种语言")
tkupdate_text(t_new_names.object,"显示翻译后的简体中文")
tkupdate_text(t_directory.object,"自动检测输入文本语言")
t_existing_names.object.config(state = "normal")
    

# --- TKINTER MAINLOOP
frame_intro.object.grid_forget()
root.geometry("900x335")
root.mainloop()