# -*- coding: utf-8 -*-
from urllib import request
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
import summarizer
from bs4 import BeautifulSoup as bs
import nltk

#Global variables
result=""
summary_sent = 0
summary_words = 0
summary_read_time = 0
original_sent = 0
original_words = 0
original_read_time = 0



#METHODS

# SUMMARY GENERATION
def get_summary():
    global result

    fetched_content=text_entry.get('1.0',tk.END)
    fetched_content = fetched_content.strip()
    if len(fetched_content)==0 :
        messagebox.showinfo("ERROR", "ENTER TEXT FOR SUMMARIZATION")
    else:
        result=summarizer.summary(fetched_content)
        if len(text_entry1.get('1.0',END)) != 0:
            text_entry1.delete('1.0',END)
        #print(result)
        text_entry1.insert(INSERT,result)           # summary insertion
        
    
# WEB SCRAPPING FROM URL
def get_text():
    global result
    result=""
    full_content=""
    url_text=url.get()                            # get() is used to retrieve the url text from the object- url
    if len(url_text)==0 :
        messagebox.showinfo("Warning","URL NOT ENTERED")
        
    else:
        html_doc = request.urlopen(url_text)
        info=bs(html_doc,'html.parser')               # defining  html parser
        contents=info.findAll('p')                    # findAll - finds and retrieves the contents of paragraph tag
        for content in contents:                      # identifying only the text
                       full_content+=content.text
        
        if len(result)!=0:
            result=""

        result=summarizer.summary(full_content)
        if len(text_entry2.get('1.0',END))!=0:
            text_entry2.delete('1.0',END)
        text_entry2.insert(INSERT,result)
        


#FILE OPENING AND SUMMARIZATION
    
def get_info():
    file1=tk.filedialog.askopenfilename(filetypes = (('Text Files','.txt'),('All files','*')))
    read_text=open(file1).read()                                                                #reading the contents file
    text_entry3.insert(INSERT,read_text)                                                        #inserting the contents of file
    

def conclusion():
    global result
    if len(result)==0:
        result=""
                                                            
    full_content=text_entry3.get('1.0',END)
    full_content=full_content.strip()
    if len(full_content)==0 :
        messagebox.showinfo("Warning","FILE IS EMPTY")
    else:
        result=summarizer.summary(full_content)             #generating the summary
        if len(result_text.get('1.0',END)) !=0:
            result_text.delete('1.0',END)
        result_text.insert(INSERT,result)                   #displaying the summary
        
        
                                              
    
    
    
#RESET FUNCTIONALITY
    
def reset(tag):
    if tag==1:
        text_entry.delete('1.0',END)
        text_entry1.delete('1.0',END)
    elif tag==2:
        url_input.delete(0,END)
        text_entry2.delete('1.0',END)
    elif tag==3 :
        text_entry3.delete('1.0',END)
        result_text.delete('1.0',END)
        

#SAVING INTO FILE
def save_file(tab):
    if tab==1:
        final_summary =  text_entry1.get('1.0',tk.END)
    elif tab==2:
        final_summary =  text_entry2.get('1.0',tk.END)
    elif tab==3:
        final_summary = result_text.get('1.0',tk.END)
        
    file_summary = tk.filedialog.asksaveasfilename(filetypes = (('Text Files','.txt'),('all files','*')))
    with open(file_summary,'w') as w:
        w.write(final_summary)

    messagebox.showinfo('ack','File saved successfully')
    
#Compare Method

def get_comparision():
    global summary_sent,summary_words,summary_read_time,original_sent,original_words,original_read_time
    
    if len(original_text.get('1.0',END))!=0:
        original_text.delete('1.0',END)
    if len(summarized_text.get('1.0',END))!= 0:
        summarized_text.delete('1.0',END)
    
    summarized_text.insert(INSERT,result)
    original_text.insert(INSERT, summarizer.final_text)
    summary_sent = summarizer.count
    print(summary_sent)
    summary_words = nltk.word_tokenize(result)
    summary_read_time = len(summary_words)/200
    
    original_sent,original_words,original_read_time = summarizer.compare()
    tree.insert('','end' ,values=("Original Text",len(original_words),len(original_sent),original_read_time ))

    
    item = tree.get_children()
    for child in item:
            tree.delete(child)
    
    tree.insert('','end' ,values=("Original Text",len(original_words),len(original_sent),original_read_time ))
    tree.insert('','end' ,values=("Summarized Text",len(summary_words),summary_sent,summary_read_time ))
        
    
  # Window creation 
    

window= Tk()
window.title("Text- Summarizer")
window.geometry("")

tab_control=ttk.Notebook(window)

t1= ttk.Frame(tab_control)
t2= ttk.Frame(tab_control)


tab_control.add(t1,text = 'summarizer')
tab_control.add(t2,text = 'compare')



tab_control.pack(expan = 1, fill="both")

tab_control1=ttk.Notebook(t1)

ttab=ttk.Frame(tab_control1)
utab=ttk.Frame(tab_control1)
dtab=ttk.Frame(tab_control1)

tab_control1.add(ttab,text="Text")
tab_control1.add(utab,text="URL")
tab_control1.add(dtab,text="DOC")



tab_control1.pack(expan=1 , fill="both")

#IN TEXT TAB

#title
title=Label(ttab,text="Enter the Text for summarization",padx=5,pady=5, relief= GROOVE)
title.pack()

Frame(ttab,height=10,bg="#ececec").pack()

#Text area for entering text
text_entry=scrolledtext.ScrolledText(ttab,height=15, width=160)
text_entry.pack()

Frame(ttab,height=10,bg="#ececec").pack()

#button for summarization
Summarize = Button(ttab, text="Summarize", bg="white" , padx=5,pady=5,command=get_summary,width=10)
Summarize.pack()

Frame(ttab,height=10,bg="#ececec").pack()

#summarized output
text_entry1=scrolledtext.ScrolledText(ttab,height=15, width=160)
text_entry1.pack()

bframe = ttk.Frame(ttab)
bframe.pack(side=BOTTOM,expand=YES)



#Button for clearing the text
clear=Button(bframe,text="Reset",padx=5,pady=5,bg="white",command= lambda:reset(1),width=10)
clear.grid(row=0,column=0)

Frame(bframe,height=10,width=20,bg="#ececec").grid(row=0,column=1)
#BUTTON FOR SAVING THE FILE
save = Button(bframe, text = "Save" , padx=5, pady =5,command= lambda: save_file(1),width=10)
save.grid(row=0,column=2)


#IN URL TAB

url=tk.StringVar(utab)   #url is the instance of StringVar class

#Text area for URL entry
title1=Label(utab,text="Enter the URL For summarization",padx=5,pady=5)
title1.pack()
Frame(utab,height=15,bg="#ececec").pack()

url_input= Entry(utab,exportselection=0,xscrollcommand=True,width=120,textvariable=url ) #textvariable is used to retrieve the content in Entry widget
url_input.pack()
Frame(utab,height=15,bg="#ececec").pack()


#button for summarization
summarize1=Button(utab,text="Summarize",bg="white", padx=5,pady=5,command=get_text,width=10)
summarize1.pack()
Frame(utab,height=15,bg="#ececec").pack()


# Text area for Summarized output
text_entry2=scrolledtext.ScrolledText(utab,height=28, width=160)
text_entry2.pack()


uframe = ttk.Frame(utab)
uframe.pack(side=BOTTOM,expand=YES)


#Button for clearing the text
clear1=Button(uframe,text="Reset",padx=5,pady=5,command = lambda:reset(2),width=10)
clear1.grid(row=0,column=0)

Frame(uframe,height=10, width=20,bg="#ececec").grid(row=0,column=1)


#Button for saving the file
save1= Button(uframe,text="Save",padx=5,pady=5,command=lambda: save_file(2),width=10)
save1.grid(row=0,column=2)



# IN FILE OPEN TAB

title3=Label(dtab,text="Open a file for Summarization ", padx=5,pady=5,bd=3,relief=GROOVE)
title3.grid(row=0,column=0,columnspan=8)

Frame(dtab,height=10,bg="#ececec").grid(row=1,column=0,columnspan=8)


#Text area for the file 
text_entry3=scrolledtext.ScrolledText(dtab,height=15,width=160)
text_entry3.grid(row=2,column=0,columnspan=8)

Frame(dtab,height=10,bg="#ececec").grid(row=3,column=0,columnspan=8)



open_file = Button(dtab, text = "Open", padx=5,pady=5, command=get_info,width=10)
open_file.grid(row=4,column=3)


#BUTTON FOR SUMMARIZATION
summarize2= Button(dtab,text="Summarize",padx=5,pady=5,command=conclusion,width=10)
summarize2.grid(row=4,column=4)

Frame(dtab,height=10,bg="#ececec").grid(row=5,column=0,columnspan=8)


 

# TEXT AREA FOR SUMMARIZED OUTPUT
result_text=scrolledtext.ScrolledText(dtab,height=15,width=160)
result_text.grid(row=6,column=0,columnspan=8)

Frame(dtab,height=10,bg="#ececec").grid(row=7,column=0,columnspan=8)


# Button for reset
clear2=Button(dtab,text="Reset",padx=5,pady=5,command = lambda:reset(3),width=10)
clear2.grid(row=8,column=3)

#butoon for saving the file
save2 = Button(dtab, text='Save' ,padx=5, pady=5,command= lambda: save_file(3),width=10)
save2.grid(row=8,column=4)

# Compare Frame

#Titles
title4 = Label(t2, text = 'Original Text',padx=5,pady=5, relief = GROOVE)
title4.grid(row=0,column=0,columnspan=2)

title5 = Label(t2, text='Summarized Text' , padx=5, pady=5 , relief =GROOVE)
title5.grid(row = 0, column= 3,columnspan=2)

#Text areas

original_text = scrolledtext.ScrolledText(t2,width = 80)
original_text.grid(row=1,column=0,columnspan=2)

Frame(t2,width=20,bg='#ececec').grid(row=1,column=2)
    
summarized_text = scrolledtext.ScrolledText(t2 , width=80)
summarized_text.grid(row=1,column=3,columnspan=2)
Frame(t2,height =15,bg='#ececec').grid(row=2,column=0,columnspan= 2)
      
cols=('TYPE','Word-count','Sentence-count','Average-Reading-Time(Minutes)')
tree = ttk.Treeview(t2,columns=cols,show ='headings')

for col in cols:
    tree.heading(col, text=col) 

tree.grid(row=3 ,column =0,columnspan=5)

compareButton = Button(t2,text='compare',padx=5,pady=5,command= get_comparision)
compareButton.grid(row=5,column=0,columnspan=5)
    
    
window.resizable(0,0)

window.mainloop()

    


