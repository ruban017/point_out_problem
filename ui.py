from tkinter import *
from tkinter import filedialog
from g_drive import auth, up, down
from g_mail import auth_gmail, send_mail
import requests
from time import sleep
from yolov5.detect import main, parse_opt
import shutil
from coor import get_coor
from pinpoint import locatee
import os


auth()
auth_gmail()

ui = Tk()
ui.geometry("400x250")

opt = parse_opt()

def open():
        global path
        ui.filename = filedialog.askopenfilename(initialdir = "E:", title = 'Select the image', filetype = (("all file types", "*.*"), ("png files", "*.png")))
        path = ui.filename
        
        up(fr'{path}')

l = Label(ui, text="Enter your Email")
l.pack()

u_email = Entry(ui, width=30)
u_email.pack()


#E:\pop(panimalar)\token.json

def up_page():
    
    up_ui = Toplevel(ui)
    up_ui.geometry("250x400")


    
    def req():
        open_ui = Toplevel(up_ui)
        open_ui.geometry('250x400')

        l_sus = Label(open_ui, text = 'ENTER YOUR PROBLEM')
        l_sus.pack()
        e_sus = Entry(open_ui, width=30)
        e_sus.pack()

        l_area = Label(open_ui, text = "ENTER THE APPROX AREA")
        l_area.pack()
        e_area = Entry(open_ui, width = 30)
        e_area.pack()

        def submit():
            global contents

            email = u_email.get()
            sus = e_sus.get()
            area = e_area.get()


            res = requests.get(f"http://localhost:5000/api/{email}/{sus}/{area}")
            contents = res.text
            print(contents)
            try:
                c = get_coor(fr"drive_images\{f_name}")
                print('No error till now')
                locatee(c[0], c[1])
            except:
                pass

            print('Still no')
            send_mail(contents, fr"yolov5\runs\detect\exp\{f_name}")
            sleep(1)
            

            shutil.move(fr"yolov5\runs\detect\exp\{f_name}", r'after_det')

            shutil.rmtree(r'yolov5\runs\detect')
            os.remove(r'location.html')

            

        sub_b = Button(open_ui, text = 'SUBMIT', command = submit)
        sub_b.pack()


        down(path)
        sleep(4)
        main(opt)
        path_lst = path.split('/')
        f_name = path_lst[-1]

        shutil.move(fr'yolov5\data\images\{f_name}', r'drive_images')


        




    
    up_button = Button(up_ui, text = "UPLOAD", command=lambda: [open(), req()])
    up_button.pack()
    
    



enter_butt = Button(ui, text="ENTER", command=up_page)
enter_butt.pack()




ui.mainloop()