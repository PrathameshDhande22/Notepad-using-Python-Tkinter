from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os
from tkinter import font

'''
Made by:- Prathamesh Dhande
Version : 1.0
Since :- 17/03/2022
if you get any error contact email me on prathameshdhande534@gmail.com
'''


class notepad(Tk):
    def __init__(self):
        super().__init__()
        self.title("Untitled - Notepad")
        self.geometry("700x500")
        self.wm_iconbitmap('notepad.ico')
        self.protocol("WM_DELETE_WINDOW",self.closing)

    # creating gui
    def gui(self):
        # creating menubar
        self.menubar=Menu(relief='flat')

        # creating filemenu
        self.filemenu=Menu(self.menubar,tearoff=0)  
        self.filemenu.add_command(label="New",command=self.new) 
        self.filemenu.add_command(label="Open",command=self.open)
        self.filemenu.add_command(label='Save',command=self.save)
        self.filemenu.add_command(label="Save As",command=self.saveas)
        self.filemenu.add_command(label="New window",command=self.new_window)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit",command=self.exit)
        self.menubar.add_cascade(label="File",menu=self.filemenu)

        # creating edit menu
        self.editmenu=Menu(self.menubar,tearoff=0)
        
        self.editmenu.add_command(label="Cut",accelerator='Ctrl+X',command=self.cut)
        self.editmenu.add_command(label='Copy',accelerator='Ctrl+C',command=self.copy)
        self.editmenu.add_command(label='Paste',accelerator='Ctrl+Y',command=self.paste)
        self.editmenu.add_command(label='Select All',accelerator='Ctrl+A',command=self.select)
        self.editmenu.add_command(label='Delete',accelerator='Del',command=self.delete)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Change Font",command=self.font)
        self.menubar.add_cascade(label='Edit',menu=self.editmenu)

        # creating help menu
        self.helpmenu=Menu(self.menubar,tearoff=0)
        self.helpmenu.add_command(label='Help',command=self.help)
        self.menubar.add_cascade(label='Help',menu=self.helpmenu)
        

        # creating scrollbar
        self.scrollbar=Scrollbar(self)
        self.scrollbar.pack(side='right',fill='y')
        
        # creating textfield
        self.textfont=font.Font(family="calibri", size='14')
        self.textarea=Text(self,font=self.textfont)
        self.textarea.pack(expand=True,fill='both')
        self.textarea.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.textarea.yview)
        self.filename=''
        

        # creating the status bar
        self.statusbar=Label(self.textarea,text="\t\t\t\t\t\t\t\t\t\t\tLine 1, Column 0")
        self.updateline()
        self.textarea.bind("<KeyPress>",self.updateline)

        # creating the theme
        self.theme=Menu(self.menubar,tearoff=0)
        self.theme.add_radiobutton(label="Dark",command=self.dark,value=0)
        self.theme.add_radiobutton(label="Light",command=self.light,value=1)
        self.menubar.add_cascade(label="Theme",menu=self.theme)
        self.configure(menu=self.menubar)
        
    def new(self):
        self.filename=""
        self.title("Untitled - Notepad")
        self.textarea.delete(1.0,END)
        self.updateline()
        

    def open(self):
        self.filename=filedialog.askopenfilename(defaultextension='.txt',filetypes=[('Text Files Only','*.txt'),('All Files','*.*')])
        print(self.filename)
        
        if self.filename=="":
            self.filename=""
        else:
            try:
                self.title(os.path.basename(self.filename)+' - Notepad')
                self.textarea.delete(1.0,END)
                with open(self.filename,'r') as f:
                    self.textarea.insert(1.0,f.read())
                self.updateline()
                # self.star()
            except:
                messagebox.showerror(title='Error',message="Can't Open This file")
                self.title("Untitled - Notepad")
    def saveas(self):
        try:
            self.filename=filedialog.asksaveasfilename(initialfile='Untitled.txt',defaultextension='.txt',filetypes=[('All Files','*.*'),('Text Files Only','*.txt')])
            with open(self.filename,'w') as f:
                f.write(self.textarea.get(1.0,END))
            self.title(os.path.basename(self.filename)+' - Notepad')
            self.updateline()
        except:
            pass

    def new_window(self):
        wt=notepad()
        wt.gui()
        wt.mainloop()
        
    def exit(self):
        self.closing()

    def cut(self,event=None):
        self.textarea.event_generate('<<Cut>>')
        self.updateline()

    def copy(self):
        self.textarea.event_generate("<<Copy>>")
        self.updateline()

    def paste(self):
        self.textarea.event_generate('<<Paste>>')
        self.updateline()

    def delete(self):
        self.textarea.event_generate('<<Clear>>')
        self.updateline()

    def help(self):
        nt=About()


    def save(self):
        if self.filename=="":
            self.saveas()
        else:
            with open(self.filename,'w') as f:
                f.write(self.textarea.get(1.0,END))
            self.updateline()

    def select(self):
        # self.textarea.event_generate('<<Selectall>>')
        self.textarea.tag_add('sel','1.0','end')

    # when cross button is pressed this function is called
    def closing(self):
        if len(self.textarea.get(1.0,END))==1:
            self.destroy()
        elif self.filename=="" and len(self.textarea.get(1.0,END))>0:
            if messagebox.askyesno(title="Confirmation",message="Do You Want To Save The File?"):
                self.saveas()
            else:
                self.destroy()
        else:
            self.destroy()

    def updateline(self,event=None):
        line,columline=self.textarea.index("insert").split(".")
        # print(line,"    ",columline)
        self.statusbar.config(text=f"\t\t\t\t\t\t\t\t\t\t\tLine {line}, Column {columline}")
        self.statusbar.pack(expand=True,fill="x",side='bottom',anchor='s')
    
    # creating font dialog box
    def font(self):
        self.r=Tk()
        self.r.wm_iconbitmap('notepad.ico')
        self.r.geometry("350x400")
        self.r.title("Change Font")
        self.r.config(bg="white")
        
        Label(self.r,text="Choose Font Style: ",font="calibri 14 ",bg='white').place(x=3,y=10)
        self.l=Listbox(self.r,width=25,relief=FLAT,bd=3)
        self.l.place(x=3,y=40)
        self.sc=Scrollbar(self.r,command=self.l.yview)
        self.sc.place(x=158,y=40)
        self.l.config(yscrollcommand=self.sc.set)
        

        Label(self.r,text="Choose Font Size :",font='calibri 14',bg='white').place(x=200,y=10)
        self.sw=Spinbox(self.r,from_=1,to=80,width=10,font="7")
        self.sw.place(x=200,y=45)
        

        for i in font.families():
            self.l.insert(END,i)

        Label(self.r,text="Choose Font :",font='calibri 14',bg='white').place(x=200,y=100)
        self.l1=Listbox(self.r,width=10,relief=FLAT,bd=3,height=5)
        self.l1.place(x=200,y=125)
        self.l1.insert(END,"bold")
        self.l1.insert(END,"italic")

        Button(self.r,text="Apply",command=self.setfont).place(x=300,y=370)
        Button(self.r,text="Cancel",command=self.r.destroy).place(x=250,y=370)
        self.r.mainloop()

        

    def setfont(self):
        fontsize=self.sw.get()
        fontfamily=self.l.get(ACTIVE)
        fontstyle=self.l1.get(ACTIVE)
        self.textfont.config(family=fontfamily,size=fontsize,weight=fontstyle)
        print(fontstyle)
        self.r.destroy()
        
        
    def dark(self):
        self.config(bg="black")
        self.textarea.config(bg="black",fg="white")
        self.filemenu.config(bg="black",fg="white",bd=1)
        self.editmenu.config(bg="black",fg="white",bd=1)
        self.helpmenu.config(bg="black",fg="white",bd=1)
        self.theme.config(bg="black",fg="white",bd=1)
        self.statusbar.config(bg="black",fg="white")
        

    def light(self):
        self.config(bg="white")
        self.textarea.config(fg="black",bg="white")
        self.filemenu.config(fg="black",bg="white",bd=1)
        self.editmenu.config(fg="black",bg="white",bd=1)
        self.helpmenu.config(fg="black",bg="white",bd=1)
        self.theme.config(fg="black",bg="white",bd=1)
        self.statusbar.config(fg="black",bg="white")

# creates the about dialog box
class About(Tk):
    def __init__(self):
        super().__init__()
        self.title("About")
        self.geometry('300x200')
        self.resizable(False,False)
        self.config(bg='white')
        self.wm_iconbitmap('notepad.ico')
        Label(self,text='ABOUT',bg='white',font='Arial 13 bold').place(x=120,y=3)
        Label(self,text="This Notepad is Created by Prathamesh Dhande using \nPython Tkinter used Python 3.9.10 and VS Code\n The Source Code of this Notepad is \nAvailable on My Blogspot\n\nI Also Thank TO You for Using MY notepad",bg='white',font='calibri 9',justify=LEFT).place(x=1,y=30)
        Button(self,text="OK",font='14',padx=15,pady=2,command=self.destroy,relief='flat',bg='grey',fg='white').place(x=230,y=150)
    

    

if __name__=="__main__":
    nt=notepad()
    nt.gui()
    # nt.font()
    nt.mainloop()
    # ab=About()


