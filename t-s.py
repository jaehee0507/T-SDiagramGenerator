# -*- coding: utf-8 -*-
"""
Orion T-S Diagram Generator 1.0
Created : 2021-06-29
Copyright 2021. Jo Jae Hee all rights reserved.
"""

import os
import numpy as np
import gsw

import tkinter.filedialog
import tkinter.font
import tkinter.messagebox

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


class TSDGenerator:
    minTemp = -5
    maxTemp = 25
    minSaln = 20
    maxSaln = 35
    densLevel = 0.5

    def __init__(self):
        window = tkinter.Tk()
        window.title("Orion T-S Diagram Generator 1.0 (by JJH)")
        window.geometry("650x480")
        window.resizable(False, False)

        title = tkinter.Label(window, font=("맑은 고딕", 17),
                              text="Orion T-S Diagram Generator 1.0 (by JJH)")
        title.place(x=0, y=0, relwidth=1.0)

        usage = tkinter.Label(window, font=("맑은 고딕", 11),
                              text="만들 그래프의 수온 범위, 염분 범위, 표시될 등밀도선  입력하여 생성 버튼을 누르세요.\n그래프 파일은 SVG 파일로 저장되며, 저장될 경로를 설정해주세요.")
        usage.place(x=0, y=50, relwidth=1.0)

        tempLabel = tkinter.Label(window, font=("맑은 고딕", 11),
                                  text="==========================<수온 범위>==========================")
        tempLabel.place(x=0, y=100, relwidth=1.0)

        minTempLabel = tkinter.Label(window, font=("맑은 고딕", 11), text="최소 수온(℃) = ")
        minTempLabel.place(x=0, y=125, width=150)

        self.minTempEntry = tkinter.Entry(window)
        self.minTempEntry.place(x=140, y=130, width=150)
        self.minTempEntry.insert(0, str(self.minTemp))

        maxTempLabel = tkinter.Label(window, font=("맑은 고딕", 11), text="최대 수온(℃) = ")
        maxTempLabel.place(x=0, y=155, width=150)

        self.maxTempEntry = tkinter.Entry(window)
        self.maxTempEntry.place(x=140, y=160, width=150)
        self.maxTempEntry.insert(0, str(self.maxTemp))

        tempLabel = tkinter.Label(window, font=("맑은 고딕", 11),
                                  text="==========================<염분 범위>==========================")
        tempLabel.place(x=0, y=180, relwidth=1.0)

        minSalLabel = tkinter.Label(window, font=("맑은 고딕", 11), text="최소 염분(psu) = ")
        minSalLabel.place(x=0, y=205, width=150)

        self.minSalnEntry = tkinter.Entry(window)
        self.minSalnEntry.place(x=140, y=210, width=150)
        self.minSalnEntry.insert(0, str(self.minSaln))

        maxSalLabel = tkinter.Label(window, font=("맑은 고딕", 11), text="최대 염분(psu) = ")
        maxSalLabel.place(x=0, y=235, width=150)

        self.maxSalnEntry = tkinter.Entry(window)
        self.maxSalnEntry.place(x=140, y=240, width=150)
        self.maxSalnEntry.insert(0, str(self.maxSaln))

        tempLabel = tkinter.Label(window, font=("맑은 고딕", 11),
                                  text="==========================<등밀도선 간격>==========================")
        tempLabel.place(x=0, y=260, relwidth=1.0)

        denseLevelLabel = tkinter.Label(window, font=("맑은 고딕", 11), text="등밀도선 간격 = ")
        denseLevelLabel.place(x=0, y=285, width=150)

        self.densLevelEntry = tkinter.Entry(window)
        self.densLevelEntry.place(x=140, y=290, width=150)
        self.densLevelEntry.insert(0, str(self.densLevel))

        fileLabel = tkinter.Label(window, font=("맑은 고딕", 11),
                                  text="==========================<파일 저장>==========================")
        fileLabel.place(x=0, y=310, relwidth=1.0)

        saveLabel = tkinter.Label(window, font=("맑은 고딕", 11), text="파일 저장 경로 = ")
        saveLabel.place(x=0, y=335, width=150)

        self.currentSaveDir = tkinter.StringVar()
        self.currentSaveDir.set(f"{os.path.expanduser('~')}/Desktop/t-s_diagram.svg".replace("\\", "/"))

        self.saveEntry = tkinter.Entry(window, state="readonly", textvariable=self.currentSaveDir)
        self.saveEntry.place(x=140, y=340, width=250)

        saveButton = tkinter.Button(window, text="찾아보기", command=self.set_save_dir)
        saveButton.place(x=400, y=335, width=80)

        generateButton = tkinter.Button(window, text="Generate", command=self.generate, bg="grey", fg="white")
        generateButton.place(x=175, y=385, width=300, height=50)

        copyRight = tkinter.Label(window, text="Orion T-S Diagram Generator. © 2021. Jo Jae Hee all rights reserved.")
        copyRight.pack(side="bottom")

        window.mainloop()

    def set_save_dir(self):
        filename = tkinter.filedialog.asksaveasfilename(initialdir=self.currentSaveDir.get(), title="저장 경로 및 파일명 지정",
                                                        filetypes=(("SVG files", "*.svg"), ("all files", "*.*")), initialfile=os.path.basename(self.currentSaveDir.get()))

        if not len(filename) == 0:
            if not filename.endswith(".svg"):
                filename = filename + ".svg"
            self.currentSaveDir.set(filename)

    def cut_not_digit(self):
        self.minTemp = int(self.minTempEntry.get())
        self.maxTemp = int(self.maxTempEntry.get())
        self.minSaln = int(self.minSalnEntry.get())
        self.maxSaln = int(self.maxSalnEntry.get())
        self.densLevel = float(self.densLevelEntry.get())

    def generate(self):
        try:
            self.cut_not_digit()

            temp_l = np.linspace(self.minTemp, self.maxTemp, 156)
            sal_l = np.linspace(self.minSaln, self.maxSaln, 156)

            tg, sg = np.meshgrid(temp_l, sal_l)
            sigma_theta = gsw.sigma0(sg, tg)

            fig, ax = plt.subplots(figsize=(10, 10))
            cs = ax.contour(sg, tg, sigma_theta, np.arange(0, 100, self.densLevel), colors='grey', zorder=1)
            plt.clabel(cs, fontsize=10, inline=False, fmt='10%.2f')

            ax.set_xlabel("Salinity (psu)")
            ax.set_ylabel("Temperature (℃)")
            ax.set_title("T-S Diagram (Generated by Orion T-S Diagram Generator)", fontsize=14, fontweight="bold")
            ax.xaxis.set_major_locator(MaxNLocator(nbins=(self.maxSaln - self.minSaln + 1)))
            ax.yaxis.set_major_locator(MaxNLocator(nbins=(self.maxTemp - self.minTemp + 1)))
            plt.tight_layout()
            plt.savefig(self.currentSaveDir.get(), format="svg")

            with open(self.currentSaveDir.get(), 'r', encoding="UTF8") as file:
                filedata = file.read()

            filedata = filedata.replace("clip-path", "jjh")

            with open(self.currentSaveDir.get(), 'w', encoding="UTF8") as file:
                file.write(filedata)

            tkinter.messagebox.showinfo("생성 완료", "SVG 파일이 생성되었습니다.")

        except:
            tkinter.messagebox.showerror("생성 오류", "오류가 발생하였습니다.")


TSDGenerator()
