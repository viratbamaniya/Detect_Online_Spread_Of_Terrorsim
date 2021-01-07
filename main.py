import json                                         # to print list/dict in textbox
import tkinter as tk                                # root GUI module
import tkinter.scrolledtext as scrolledtext         # module for scrollable text widget
import tkinter.ttk as ttk                           # themed GUI module
from tkinter.filedialog import askopenfile          # module to read file

import requests                                     # module to get all contents of a website
from bs4 import BeautifulSoup                       # module to get only text from a website
from PIL import Image, ImageTk                      # module to open and load a image
from ttkthemes import ThemedStyle                   # module to use in-built GUI themes


# class to get all frames together
class MyApp(tk.Tk):

    def __init__(self, *args, **kwargs, ):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        menu = tk.Menu(container)

        ex = tk.Menu(menu, tearoff=0)
        menu.add_cascade(menu=ex, label="Menu")
        ex.add_command(label="Exit",
                    command=self.destroy)

        # code to make theme choosable
        style = ThemedStyle(self)

        def theme(thm,inde):
            style.set_theme(thm.entrycget(inde,"label"))

        th = tk.Menu(menu,tearoff=0)
        menu.add_cascade(menu=th, label="Theme")

        th.add_command(label="aquativo",command=lambda:theme(th,0))
        th.add_command(label="black",command=lambda:theme(th,1))
        th.add_command(label="blue",command=lambda:theme(th,2))
        th.add_command(label="clearlooks",command=lambda:theme(th,3))
        th.add_command(label="radiance",command=lambda:theme(th,4))
        th.add_command(label="winxpblue",command=lambda:theme(th,5))
        th.add_command(label="keramik",command=lambda:theme(th,6))
        th.add_command(label="kroc",command=lambda:theme(th,7))
        th.add_command(label="plastik",command=lambda:theme(th,8))
        
        tk.Tk.config(self, menu=menu)

        for F in (Startpage, PageOne, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Startpage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Home page
class Startpage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Home",font=("Simplifica",22))         # page heading
        label.pack(pady=5, padx=5)

        ttk.Label(self,text="").pack()

        button1 = ttk.Button(self, text="Detect",                           
                        command=lambda: controller.show_frame(PageOne))     # got to detect page
        button1.pack()

        ttk.Label(self,text="").pack()

        button2 = ttk.Button(self, text="About",
                        command=lambda: controller.show_frame(PageTwo))     # got to about page
        button2.pack()

        ttk.Label(self,text="").pack()

        img=ImageTk.PhotoImage(Image.open("wall.jpg").resize((1200,700)))   # set the home page image
        img.image = img
        ttk.Label(self,image=img).pack()



#   *****   PAGES   *****
# Detect page
class PageOne(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Detect",font=("Simplifica",22))       # page heading
        label.pack(pady=5, padx=5)

        ttk.Label(self,text="\n").pack()

        ttk.Label(self,text="Enter a webpage",font=(18)).pack()     
        text = tk.Entry(self,font=(26),width=70,bg="lightgray")             # textbox to enter a website
        text.pack()

        ttk.Label(self,text="").pack()


        # load the file containing fixed keywords
        j=[]
        f = open("keywords.txt", "r")
        for line in f:
            j.append(line.strip())
        f.close()
        d = dict.fromkeys(j,0)

        # code to scan the website given in textbox
        def scan():
            count=0
            url = text.get()
            text.delete(0,"end")
            result = requests.get(url.strip())
            soup = BeautifulSoup(result.content, 'lxml')
            for i in soup.get_text().split():
                if(i.lower()in j):
                    count+=1
                    if i.lower() in d:
                        d[i.lower()] +=1
            l3.config(state=tk.NORMAL)
            l3.delete('1.0',"end")
            di = dict(sorted(d.items(),reverse=True, key=lambda item: item[1]))
            lis = [(k,v) for k,v in di.items() if v >= 1]
            l3.insert(tk.END,url.strip()+" = "+str(count)+"\n\nKeywords matched:  \n"+json.dumps(lis))
            l3.config(state=tk.DISABLED)

        b2=ttk.Button(self,text="Scan",command= scan)
        b2.pack()

        ttk.Label(self,text="").pack()


        # code to open and scan the list of websites given in a text file
        def open_n_scan():
            files = askopenfile(mode ='r', filetypes =[("Text File", "*.txt")])
            l3.config(state=tk.NORMAL)
            l3.delete('1.0',"end")
            for url in files:
                count=0
                result = requests.get(url.strip())
                soup = BeautifulSoup(result.content, 'lxml')
                for i in soup.get_text().split():
                    if(i.lower()in j):
                        count+=1
                l3.insert(tk.END,url.strip()+" = "+str(count)+"\n")
            l3.config(state=tk.DISABLED)

        ttk.Label(self,text="Select your text file containing urls",font=(18)).pack()

        b1=ttk.Button(self,text="Open and Scan",command= open_n_scan)
        b1.pack()

        ttk.Label(self,text="").pack()

        l3=scrolledtext.ScrolledText(self,font=(18),height=10,width=70,bg="lightgray",state=tk.DISABLED)       # multiline textbox
        l3.pack()

        ttk.Label(self,text="").pack()

        button1 = ttk.Button(self, text="Back to Home",
                        command=lambda: controller.show_frame(Startpage))                           # go to home page
        button1.pack()

        ttk.Label(self,text="").pack()

        button2 = ttk.Button(self, text="About",
                        command=lambda: controller.show_frame(PageTwo))                             # got to about page
        button2.pack()


# About page
class PageTwo(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="About",font=("Simplifica",22))                    # page heading
        label.pack(pady=5, padx=5)

        ttk.Label(self,text="").pack()

        button1 = ttk.Button(self, text="Back to Home",
                        command=lambda: controller.show_frame(Startpage))               # got to home page
        button1.pack()

        ttk.Label(self,text="").pack()

        button2 = ttk.Button(self, text="Detect",
                        command=lambda: controller.show_frame(PageOne))                 # got to detect page
        button2.pack()

        ttk.Label(self,text="").pack()

        tk.Message(self,relief="sunken",bd=4,font=(20),width=1100,text="Terrorism is, in the broadest sense, the use of intentional violence for political or religious purposes. It is used in this regard primarily to refer to violence during peacetime or in the context of war against non-combatants (mostly civilians and neutral military personnel). The terms terrorist and terrorism originated during the French Revolution of the late 18th century but gained mainstream popularity in the 1970s during the conflicts of Northern Ireland, the Basque Country and Palestine. The increased use of suicide attacks from the 1980s onwards was typified by the September 11 attacks in New York City and Washington, D.C. in 2001.").pack()
                                                                                        # Info on terrorism
        ttk.Label(self,text="").pack()

        tk.Message(self,relief="sunken",bd=4,font=(20),width=1100,text="Cyberterrorism is the use of the Internet to conduct violent acts that result in, or threaten, loss of life or significant bodily harm, in order to achieve political or ideological gains through threat or intimidation. It is also sometimes considered an act of Internet terrorism where terrorist activities, including acts of deliberate, large-scale disruption of computer networks, especially of personal computers attached to the Internet by means of tools such as computer viruses, computer worms, phishing, and other malicious software and hardware methods and programming scripts. Cyberterrorism is a controversial term.").pack()
                                                                                        # Info on cyberterrorism
        ttk.Label(self,text="").pack()

        tk.Message(self,relief="sunken",bd=4,font=(20),width=1100,text="We use web mining algorithms to mine textual information on web pages and detect their relevancy to terrorism. This system will check web pages whether a webpage is promoting terrorism. Data mining is a technique used to mine out patterns of useful data from large data sets and make the most use of obtained results. Web mining also consists of text mining methodologies that allow us to scan and extract useful content from unstructured data.").pack()
                                                                                        # About
        ttk.Label(self,text="").pack()

        ttk.Label(self,text="© Virat Bamaniya and Milan Solanki",font=(20)).pack()                        # copyright


app = MyApp()

# set default app theme
style = ThemedStyle(app)
style.set_theme("black")

# set app icon
icon = ImageTk.PhotoImage(Image.open("icon.jpg"))
app.iconphoto(False,icon)

app.resizable(0,0)
app.title("Detect Terrorism")                                                           # app title
app.state('zoomed')                                                                     # maximized app by default
app.mainloop()
