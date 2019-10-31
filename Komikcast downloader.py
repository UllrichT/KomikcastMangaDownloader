import os
import shutil
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import scrolledtext
from bs4 import BeautifulSoup as soup
from urllib.request import urlretrieve
from urllib.request import urlopen as uReq

def disbleList(event):
    list.configure(state = 'disabled')

def enableList(event):
    list.configure(state = 'normal')

def downloader(image_url, file_name):
    urlretrieve(image_url, file_name)

def mover(path, img_name):
    shutil.move(img_name, path)

def checker(temp):
    while temp[len(temp)-1] == ' ':
        temp = temp[0:len(temp)-1]
    return temp

def updateScroll(baris, index, replaceWith):
    temp = str(baris) + '.' + str(index)
    processBox.delete(temp, END)
    processBox.insert(INSERT, replaceWith)
    processBox.see('end')
    MainWindow.update()

def getList(event):
    index = list.curselection()
    selectedBox.delete(0.0,END)
    for a in index:
        text = list.get(a)
        selectedBox.insert(INSERT, str(text) + '\n')

def makeFolder(path, name, line):
    try:
        line = printScroll("Creating folder '{}'\n".format(name), line)
        os.mkdir(path)
    except Exception as e:
        print(e)
    return line

def cari(cari, path):
    file_list = os.listdir(path)
    try:
        coba = file_list.index(cari)
        return 'Already exist'
    except:
        return 'Start download'

def change(a,b,c):
    en1.configure(state = 'enabled')
    en1.insert(0, a)
    en1.configure(state = 'disabled')
    en2.configure(state = 'enabled')
    en2.insert(0, b)
    en2.configure(state = 'disabled')
    en3.configure(state = 'enabled')
    en3.insert(0, c)
    en3.configure(state = 'disabled')

def printScroll(teks, baris):
    # processBox.insert(INSERT, str(baris) + teks)
    processBox.insert(INSERT, teks)
    if '\n' in teks:
        baris += 1
    processBox.see('end')
    MainWindow.update()
    return baris

def ChapterOpener(ChapterLink, ChapterName, path, line):
    num = 1
    temp_list = []
    conn = uReq(ChapterLink)
    getPage = conn.read()
    conn.close()
    getHtml = soup(getPage,"html.parser")
    getDiv = getHtml.find('div', {'id' : 'readerarea'})
    getImage = getDiv.findAll('img')
    for a in getImage:
        link = a['src']
        if(str(link)!=''):
            ImageName = ChapterName + ' - ' + str(num) + '.jpg'
            dir = path + '/' + ImageName
            temp_list.append(dir)
            temp_str = ImageName + ' : '
            line = printScroll(temp_str, line)
            num += 1
            stats = cari(ImageName, path)
            if stats == 'Start download':
                try:
                    line = printScroll(stats, line)
                    downloader(link, ImageName)
                    updateScroll(line, len(temp_str), 'Download complete')
                    updateScroll(line, len(temp_str), 'Moving')
                    mover(dir, ImageName)
                    updateScroll(line, len(temp_str), 'Complete')
                except Exception as e:
                    print(e)
                    updateScroll(line, len(temp_str), 'Failed')
            else:
                line = printScroll(stats, line)
            line = printScroll('\n', line)
    return temp_list, line

def Scrapping():
    try:
        url = input.get()
        conn = uReq(url)
        getPage = conn.read()
        conn.close()
        getHtml = soup(getPage,"html.parser")
        strJudul = getHtml.find('h1').text
        strJudul = strJudul.replace(' Bahasa Indonesia','')
        div = getHtml.find('div', {'class':'spe'})
        span = div.findAll('span')
        for a in span:
            str = a.text
            if 'Author' in str:
                pengarang = str.replace('Author: ','')
            elif 'Type' in str:
                tipe = str.replace('Type: ','')
        change(strJudul, pengarang, tipe)
        ChapLink['title'] = strJudul
        getChap = getHtml.findAll('span',{'class':'leftoff'})
        for a in getChap:
            chap = a.find('a').text
            chap = checker(chap)
            link = a.find('a')['href']
            ChapLink[chap] = link
            ChapList.append(chap)
            list.insert(0,chap)
            # print(chap + ChapLink[chap])
        mode = varDown.get()
        if mode:
            list.configure(state = 'normal')
            list.focus()
        else:
            list.configure(state = 'disabled')
    except Exception as e:
        # print(e)
        messagebox.showerror('Something not right',e)

def HTML_maker(title, target, img_list, line):
    index = ChapList.index(target)
    NextName = ChapList[index - 1]
    PrevName = ChapList[index + 1]

    html1 = """<!DOCTYPE html>
    <html lang="en" dir="ltr">
      <head>
        <meta charset="utf-8">
        <title>NUT's Library</title>
        <style media="screen">
        .head{
          background-color: #16151d;
          color: white;
          display: block;
          font-weight: bold;
          height: 50px;
          padding: 0.1em 0.1em;
          padding-bottom: 30px;
        }
        .nav{
          background-color: #3367d6;
          color: white;
          display: block;
        }
        .foot{
          background-color: #3367d6;
          color: white;
          display: block;
          align-items: center;
        }
        .back{
          background-color: #16151d;
          color: white;
          display: block;
        }
        .konten{
          background-color: #323232;
          color: white;
          width: 750px;
          display: block;
          padding-top: 25px;
          padding-bottom: 25px;
        }
        img{
          width: 700px;
          display: block;
        }
        button{
          background-color: #323232;
          color: white;
          border: none;
          cursor: pointer;
          border-radius: 10px;
          padding: 10px 32px;
        }
        .right{
          padding-left: 15px;
        }
        .left{
          padding-right: 15px;
        }
        </style>
      </head>
      <body>
        <!-- header -->
        <div class="head" align='center'>
          <h1>NUT's Offline Library</h1>
        </div>
        <!-- header -->

        <!-- navbar -->
        <div class="nav" align='center'>
          <table>
            <tr>
              <td class="left"> <button id='left' type="button" name="button" onclick="window.location.href = 'p_chap';"> previous chapter </button> </td>
              <td> <p>t_chap</p> </td> <!-- disini diganti chapter-->
              <td class="right"> <button id='right' type="button" name="button" onclick="window.location.href = 'n_chap';"> next chapter </button> </td>
            </tr>
          </table>
        </div>
        <!-- navbar -->

        <!-- konten -->
        <div class="back" align='center'>
          <div class="konten" align='center'>t_img
          </div>
        </div>
        <!-- konten -->

        <!-- footer -->
        <div class="foot" align='center'>
          <table>
            <tr>
              <td class="left"> <button id='left2' type="button" name="button" onclick="window.location.href = 'p_chap';"> previous chapter </button> </td>
              <td> <p>t_chap</p> </td> <!-- disini diganti chapter-->
              <td class="right"> <button id='right2' type="button" name="button" onclick="window.location.href = 'n_chap';"> next chapter </button> </td>
            </tr>
          </table>
        </div>
        <!-- footer -->

        <script type="text/javascript">
        t_script
        </script>
      </body>
    </html>
    """

    hide_p = """      document.getElementById('left').style.display = 'none';
          document.getElementById('left2').style.display = 'none';
    """
    hide_n = """      document.getElementById('right').style.display = 'none';
          document.getElementById('right2').style.display = 'none';
    """
    html2 = html1.replace('t_chap', target)
    if((index-1) < 0):
        html3 = html2.replace('p_chap', title + ' - ' + PrevName + '.html')
        html4 = html3.replace('n_chap', '#')
        html5 = html4.replace('t_script', hide_n)
    elif ((index+1) > (len(ChapList)-1)):
        html3 = html2.replace('p_chap', '#')
        html4 = html3.replace('n_chap', title + ' - ' + NextName + '.html')
        html5 = html4.replace('t_script', hide_p)
    else:
        html3 = html2.replace('p_chap', title + ' - ' + PrevName + '.html')
        html4 = html3.replace('n_chap', title + ' - ' + NextName + '.html')
        html5 = html4.replace('t_script', '')

    template = """\n        <img src="ganti" alt="">"""
    temp = """"""
    tempHtml = """"""
    for x in range(0, len(img_list)):
        temp = template.replace('ganti', img_list[x])
        tempHtml += temp
    html6 = html5.replace('t_img', tempHtml)
    htmlName = title + ' - ' + target + '.html'
    file = open(htmlName, 'w')
    file.write(html6)
    file.close()
    line = printScroll('Writing HTML complete\n', line)
    return line

def startDown():
    DownQue = {'Chap':'Link'}
    line = 1
    mode = varDown.get()
    processBox.delete(0.0, END)
    folder = 'Img'
    if mode:
        line = printScroll('Start download selected chapter\n', line)
        line = printScroll('======================================\n', line)
        index = list.curselection()
        for a in index:
            text = list.get(a)
            link = ChapLink[text]
            DownQue[text] = link
    else:
        line = printScroll('Start download all chapter\n', line)
        line = printScroll('======================================\n', line)
        DownQue = ChapLink.copy()
    line = makeFolder(folder, folder, line)
    folder = folder + '/' + ChapLink['title']
    line = makeFolder(folder, ChapLink['title'],line)
    line = printScroll('======================================\n', line)
    for a in DownQue:
        if a != 'Chap' and a != 'title':
            line = printScroll(a + '\n', line)
            line = printScroll('link : ' + DownQue[a] + '\n', line)
            temp_path = folder + '/' + a
            line = makeFolder(temp_path, a, line)
            image_list, line = ChapterOpener(DownQue[a], a, temp_path, line)
            line = HTML_maker(ChapLink['title'], a, image_list, line)
            line = printScroll('======================================\n', line)


ChapLink = {'Chap':'Link'}
ChapList = []

MainWindow = Tk()
MainWindow.title('Komikcast downloader')
MainWindow.geometry('640x405')

frame1 = Frame(MainWindow)
frame1.place(x=10, y=25)
frame2 = Frame(MainWindow)
frame2.place(x=10, y=150)
frame3 = Frame(MainWindow)
frame3.place(x=10, y=60)
frame4 = Frame(MainWindow)
frame4.place(x=160, y=130)

text1 = Label(MainWindow, text='Input your Komikcast link here : ')
text1.place(x=10, y=5)

# masuk frame1
input = Entry(frame1, width=70)
input.focus()
input.grid(column = 0, row = 0)
btn1 = Button(frame1, text='Start Scrapping', command = Scrapping)
btn1.grid(column = 1, row = 0)

# masuk frame3
judul = Label(frame3, text='Title')
judul.grid(sticky='w',column=0, row=0)
en1 = Entry(frame3, width=50, state = 'disabled')
en1.grid(column=1, row=0)
pengarang = Label(frame3, text='Author')
pengarang.grid(sticky='w',column=0, row=1)
en2 = Entry(frame3, state = 'disabled', width=50)
en2.grid(column=1, row=1)
tipe = Label(frame3, text='Type')
tipe.grid(sticky='w',column=0, row=2)
en3 = Entry(frame3, state = 'disabled', width=50)
en3.grid(column=1, row=2)

text2 = Label(MainWindow, text = 'Chapter List :')
text2.place(x=10, y=130)

# masuk frame2
scroll = Scrollbar(frame2)
scroll.pack(side = RIGHT, fill = Y)
list = Listbox(frame2, height = 15, selectmode = 'multiple',yscrollcommand = scroll.set)
list.bind('<ButtonRelease-1>',getList)
list.pack(side = LEFT, fill = BOTH)
scroll.config( command = list.yview )

# masuk frame4
text3 = Label(frame4, text = 'Download mode : ')
text3.grid(sticky ='w', column=0, row=0)
varDown = BooleanVar()
Down1 = Radiobutton(frame4, text = 'All chapters', value = False, var = varDown)
Down1.grid(sticky ='w', column=0, row=1)
Down1.bind('<ButtonRelease-1>', disbleList)
Down2 = Radiobutton(frame4, text = 'Selected chapters', value = True, var = varDown)
Down2.grid(sticky ='w', column=0, row=2)
Down2.bind('<ButtonRelease-1>', enableList)

selectedBox = scrolledtext.ScrolledText(MainWindow, width = 15, height = 12)
selectedBox.place(x=160, y=197)

startDown = Button(MainWindow, text = 'Start Download', command = startDown)
startDown.place(x=306, y=135)
processBox = scrolledtext.ScrolledText(MainWindow, width = 38, height = 14)
processBox.place(x=307, y=165)

MainWindow.mainloop()
