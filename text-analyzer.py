import tkinter
from tkinter import filedialog
from konlpy.tag import Okt
import pandas as pd
from tkinter import *
import os

ranking_size = 100
filter_length = 2


def save():
    file = filedialog.asksaveasfile(mode='w', defaultextension='.txt', initialdir="/", title="Select file",
                                 filetypes=(("text files", "*.txt"),
                                            ("all files", "*.*")))
    file.write(result_text.get("1.0", END))
    file.close()


def set_option():
    global ranking_size
    global filter_length
    ranking_size = int(rank.get())
    filter_length = int(filter_len.get())
    rank.delete(0, "end")
    rank.insert(END, str(ranking_size))
    filter_len.delete(0, "end")
    filter_len.insert(END, str(filter_length))
    log.insert(END, "랭킹: {}, 필터: {} 으로 설정 변경 완료.\n".format(ranking_size, filter_length))

def clear_result():
    log.insert(END, "분석 결과가 초기화 되었습니다.\n")
    result_text.delete("1.0", 'end')


def analyze():
    filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                          filetypes=(("text files", "*.txt"),
                                                     ("all files", "*.*")))

    data = open(filename, 'rt', encoding="utf-8")

    try:
        target = data.read()
        if len(target) > 0:
            log.insert(END, "현재 {} 파일을 분석중입니다...잠시만 기다려주세요.\n".format(filename))
            okt = Okt()
            noun = okt.nouns(target)

            noun_list = []

            for i in noun:
                if len(i) >= filter_length:
                    noun_list.append(i)

            words = pd.Series(noun_list)
            result = words.value_counts().head(ranking_size)
            df1 = pd.DataFrame(result, columns=['카운트'])
            df1 = df1.reset_index()
            df1 = df1.rename(columns={"index": "명사"})
            df1.index.name = "순번"
            df1.index += 1
            result_text.insert(END, df1.to_string())
            log.insert(END, "분석완료. 총 추출 명사 개수 : {}개\n".format(len(df1)))
        else:
            log.insert(END, filename + " 파일 내용이 비어있는 것 같습니다. 확인해주세요\n")
    except UnicodeDecodeError:
        path, ext = os.path.splitext(filename)
        log.insert(END, "{} 확장자는 지원하지 않습니다. txt로 변환후 시도해주세요.\n".format(ext))


root = tkinter.Tk()
root.title('텍스트 분석기 beta')

menubar = Menu(root)

filemenu = Menu(menubar, tearoff=0)

menubar.add_cascade(label="파일", menu=filemenu)

filemenu.add_command(label="저장", command=save)

filemenu.add_separator()

filemenu.add_command(label="종료", command=root.quit)

run_menu = Menu(menubar, tearoff=0)

menubar.add_cascade(label="실행", menu=run_menu)

run_menu.add_command(label="파일 찾고 분석", command=analyze)

root.config(menu=menubar)

label1 = Label(root, text="최대 랭킹 사이즈")
label1.grid(row=0, column=0)
rank = Entry(root, width=10)
rank.insert(0, str(ranking_size))
rank.grid(row=0, column=1)

label2 = Label(root, text="필터 사이즈")
label2.grid(row=0, column=2)
filter_len = Entry(root, width=10)
filter_len.insert(0, str(filter_length))
filter_len.grid(row=0, column=3)

button = Button(root, text="변경", command=set_option)
button.grid(row=0, column=4)

button = Button(root, text="분석 결과 초기화", command=clear_result)
button.grid(row=0, column=5)

label3 = Label(root, text="로그")
label3.grid(row=1, column=0)
log = Text(root, height=10)
log.grid(row=2, column=0, columnspan=100)

label4 = Label(root, text="분석 결과")
label4.grid(row=3, column=0)
result_text = Text(root, height=30)
result_text.grid(row=4, column=0, columnspan=100)

root.mainloop()
