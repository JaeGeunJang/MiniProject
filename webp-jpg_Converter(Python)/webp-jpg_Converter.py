from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image
import os
from tkinter.filedialog import askdirectory
import shutil

class Window(Frame) :
    def __init__(self, master) :
        Frame.__init__(self, master)

        self.master = master
        self.master.title("webp-jpg Converter")
        self.pack(fill=BOTH, expand=True)

        frame1 = Frame(self)
        frame1.pack()
        self.btnOpen = Button(frame1, text = "Folder", command = self.openDir, width = 280)
        self.btnOpen.pack(side = LEFT, padx = 10, pady = 10)
        
        frame2 = Frame(self)
        frame2.pack()
        self.lblName = Label(frame2, text = "No Directory Open", wraplength = 280)
        self.lblName.pack(side = LEFT, padx = 10, pady = 10)

        frame3 = Frame(self)
        frame3.pack()
        self.btnChange = Button(frame3, text = "Change", width = 280, state = DISABLED, command = self.main)
        self.btnChange.pack(side = LEFT, padx = 10, pady = 10)

        self.checkVar = IntVar()
        
        frame4 = Frame(self)
        frame4.pack()
        self.c1 = Checkbutton(frame4, text = "Delete Original Webp Files", variable = self.checkVar)
        self.c1.pack()

        frame5 = Frame(self)
        frame5.pack()
        self.foldName = Label(frame5, text = "", wraplength = 280)
        self.foldName.pack(side = LEFT, padx = 10, pady = 10)

    #Press Open Button
    def openDir(self) :
        self.fileDir = askdirectory()
        if self.fileDir == "" :
            self.fileDir = "No Directory Open"
        self.lblName.configure(text = self.fileDir)
        self.foldName.configure(text = "")
        

        if self.fileDir != "No Directory Open" :
            self.btnChange["state"] = NORMAL

    #If Find Right Folder, Change webp to jpg
    def change_jpg(self, folder, yes) :
        file_list = os.listdir(folder)
        
        flag = 0
        for i in file_list :
            if ".webp" in i :
                flag = 1

        if flag == 1 :
            fname = folder.split("/")
            if yes == 0 :
                os.mkdir(folder+"/webp")
                movedir = folder + "/webp"
            
                for i in file_list:
                    im = Image.open("{0}{1}".format(folder + "/", i)).convert("RGB")
                    im.save("{0}{1}.jpg".format(folder + "/", i[:-5]), "jpeg")
                    shutil.move("{0}{1}".format(folder + "/", i), movedir)

            else :
                for i in file_list:
                    im = Image.open("{0}{1}".format(folder + "/", i)).convert("RGB")
                    im.save("{0}{1}.jpg".format(folder + "/", i[:-5]), "jpeg")
                    os.remove("{0}{1}".format(folder + "/", i))

    #Search Right Folder
    def search_folder(self, dest, yes) :
        files = os.listdir(dest)
        folders = []
        
        for fs in files :
            if os.path.isdir(dest + "/" + fs) :
                folders.append(fs)

        if len(folders) == 0 :
            self.change_jpg(dest, yes)
            return True
        
        if len(folders) == 1 and folders[0] == "webp" :
            return True
        
        else :
            for folder in folders :
                dest_fold = dest + "/" + folder
                self.search_folder(dest_fold, yes)

    #Main Function to Change Button
    def main(self) :
        files = self.fileDir
        yes = self.checkVar.get()
        
        self.search_folder(files, yes)

        self.foldName.configure(text = "DONE!")


        
def main() :
    root = Tk()
    root.geometry("300x200")
    app = Window(root)
    root.mainloop()

if __name__ == "__main__" :
    main()
