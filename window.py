import sys
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import os
from PIL import Image, ImageTk


class Window:
    def __init__(self):
        #self.wsize,self.hsize=wsize,hsize
        self.root=tk.Tk()
        self.root.title("Bbox Annotaton")

        self.root.geometry("1400x800")

        #self.root.bind('<ButtonRelease-1>', self.release)
        #self.after_click=False
        self.start_x=None
        self.start_y=None
        self.rect=None
        self.rect_list=[]
        self.layout()
        self.root.bind('<ButtonPress-1>', self.left_click)
        self.root.bind('<B1-Motion>', self.dragging)
        self.root.bind('<ButtonRelease-1>',self.release)
        self.review()
        self.root.mainloop()




    def  layout(self):
        self.image_canvas=tk.Canvas(self.root,width=1600,height=1200)
        self.IDirButton = tk.Button(self.root, text="画像フォルダ指定", command=self.dirdialog_clicked,bg="LemonChiffon2").place(x=0,y=0)
        self.NextButton = tk.Button(self.root, text="次の画像", command=self.next_clicked,bg="LemonChiffon2").place(x=200,y=0)
        self.DeleteButton = tk.Button(self.root, text="最新のbboxを削除", command=self.delete,bg="LemonChiffon2").place(x=800,y=0)
        self.rest_txt = tk.Entry(width=20)
        self.rest_txt = tk.Entry(width=20)
        self.rest_txt.place(x=600,y=5)
        self.current_txt=tk.Entry(width=20)
        self.current_txt.place(x=350,y=5)
        self.image_canvas.place(x=0, y=50)
        self.bbox_id=0



    
    def dirdialog_clicked(self):
        self.idx=0
        iDir = os.path.abspath(os.path.dirname(__file__))
        self.iDirPath = filedialog.askdirectory(initialdir = "iDir"+"/../")
        self.file_list=os.listdir(self.iDirPath)
        self.len=len(self.file_list)
        image_path=os.path.join(self.iDirPath,self.file_list[self.idx])
        image=Image.open(image_path)
        self.image=ImageTk.PhotoImage(image)
        self.image_canvas.create_image(0,0,image=self.image,anchor=tk.NW)
        self.rest_txt.insert(tk.END,"残り画像は{}枚です".format(self.len-self.idx))
        self.current_txt.insert(tk.END,"現在の画像は{}枚目です".format(self.idx+1))

    def next_clicked(self):
        self.idx+=1
        image_path=os.path.join(self.iDirPath,self.file_list[self.idx])
        image=Image.open(image_path)
        self.image=ImageTk.PhotoImage(image)
        self.image_canvas.create_image(0,0,image=self.image,anchor=tk.NW)
        self.rest_txt.delete(0, tk.END)
        self.current_txt.delete(0, tk.END)
        self.rest_txt.insert(tk.END,"残り画像は{}枚です".format(self.len-self.idx))
        self.current_txt.insert(tk.END,"現在の画像は{}枚目です".format(self.idx+1))

    def left_click(self,e):
        self.start_x=e.x
        self.start_y=e.y
        #self.max_x=None
        #self.max_y=None
        #self.rect = self.image_canvas.create_rectangle(self.min_x,
                    #self.min_y, self.max_x, self.max_y, outline='red')
        #self.after_click=True
        #self.drug_i=0
    def dragging(self,e):
        self.end_x=e.x
        self.end_y=e.y
        #self.rect = self.image_canvas.create_rectangle(self.min_x,
        #            self.min_y, self.max_x, self.max_y, outline='red')
        if self.rect:
            self.image_canvas.coords("new",
                min(self.start_x,self.end_x),min(self.start_y,self.end_y),
                max(self.start_x,self.end_x),max(self.start_y,self.end_y))
        else:
            print("aaaa")
            self.rect = self.image_canvas.create_rectangle(self.start_x,
                    self.start_y, self.end_x, self.end_y, outline='red',tags="new")

    def release(self,e):
        if self.rect:
            bbox=[self.start_x,self.start_y, self.end_x, self.end_y]
            self.rect_list.append(bbox)
            self.image_canvas.delete("new")
            self.rect=None
            for  bbox in self.rect_list:
                self.image_canvas.create_rectangle(bbox[0],
                    bbox[1], bbox[2], bbox[3], outline='blue',tags="previous")
            #area=(self.start_x-self.end_x)*(self.start_y-self.end_y)
    def review(self):
        self.image_canvas.delete("previous")
        for  bbox in self.rect_list:
                self.image_canvas.create_rectangle(bbox[0],
                    bbox[1], bbox[2], bbox[3], outline='blue',tags="previous")
            #if  area<10:
             #   self.image_canvas.delete(str(self.bbox_id))

            #else:
            #self.rect_list.append(self.bbox_id)
            #self.bbox_id+=1
            #print(self.rect_list)
            #self.rect=None

    def delete(self):
        self.rect_list.pop(-1)
        self.image_canvas.delete("previous")
        for  bbox in self.rect_list:
                self.image_canvas.create_rectangle(bbox[0],
                    bbox[1], bbox[2], bbox[3], outline='blue',tags="previous")



Window()


