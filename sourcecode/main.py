import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import threading
from pathlib import Path
from tkinter import filedialog
import os
import sys
import tempfile
import shutil
import datetime

import checkport
import httpserver
import ipconfig
import server, client


current_time = datetime.datetime.now().time().strftime("%H:%M")

server_started = False
web_sharing_started = False
path = None


def StopServer():
    global server_started
    if server_started:
        server_started = False
        server.server.close()
def StopConnection():
    client.socket_server.close()
def StopWebSer():
    if web_sharing_started:
        httpserver.stopwebsharing()

def finish():
    StopServer()
    StopWebSer()
    win.destroy()

def changeserverstatus(trfl):
    global server_started
    server_started = trfl

def checkserverstatus():
    global server_started
    return server_started

def changewebstatus(trfl):
    global web_sharing_started
    web_sharing_started = trfl

def getfilename(file_path):
    if file_path:
        file_name = os.path.basename(file_path)  # Получаем только имя файла
        return file_name

def file_size(path):
    return os.path.getsize(path)

def getname(data):
    namelabel.configure(text=data)

def connectionlost():
    global username, port
    username = "user"
    port = 8080
    message_frame = ctk.CTkFrame(second_frame, fg_color="transparent", corner_radius=0)
    message_frame.pack(fill='x', anchor='w' , expand=True, padx=10, pady=5)
    connection_lost_label = ctk.CTkLabel(message_frame, text="connection failed", fg_color="#5a2f2e", bg_color="#2b2b2b", corner_radius=10)
    connection_lost_label.pack(anchor='center')
    scroll_to_bottom()

def serverfailed():
    global server_started
    global username_entry
    global host_port_entry
    global ip_label
    server_started = False

    message_frame = ctk.CTkFrame(second_frame, fg_color="transparent", corner_radius=0)
    message_frame.pack(fill='x', anchor='w' , expand=True, padx=10, pady=5)
    connection_lost_label = ctk.CTkLabel(message_frame, text=f"Starting the server is failed.", fg_color="#5a2f2e", bg_color="#2b2b2b", corner_radius=10)
    connection_lost_label.pack(anchor='center')
    scroll_to_bottom()

    username_entry.configure(state='normal')
    host_port_entry.delete(0, "end")
    ip_label.configure(text="")

def serverinfo(port):
    myip = ipconfig.get_local_ip()
    ip_label.configure(text=f'Your Ip: {myip}:{port}')

def web_start_info(ip, portt):
    message_frame = ctk.CTkFrame(second_frame, fg_color="transparent", corner_radius=0)
    message_frame.pack(fill='x', anchor='w' , expand=True, padx=10, pady=5)
    if portt:
        connection_lost_label = ctk.CTkLabel(message_frame, text=f"Web server started! Your IP address: {ip}:{portt}", fg_color="#385d37", bg_color="#2b2b2b", corner_radius=10)
    else:
        connection_lost_label = ctk.CTkLabel(message_frame, text=f"Web server started! Your IP address: {ip}:8080", fg_color="#385d37", bg_color="#2b2b2b", corner_radius=10)

    connection_lost_label.pack(anchor='center')
    scroll_to_bottom()



def portinuse(port):
    message_frame = ctk.CTkFrame(second_frame, fg_color="transparent", corner_radius=0)
    message_frame.pack(fill='x', anchor='w' , expand=True, padx=10, pady=5)
    connection_lost_label = ctk.CTkLabel(message_frame, text=f"Starting the server is failed. The port '{port}' is already in use", fg_color="#5a2f2e", bg_color="#2b2b2b", corner_radius=10)
    connection_lost_label.pack(anchor='center')
    scroll_to_bottom()

def gettime():
    global current_time
    current_time = datetime.datetime.now().time().strftime("%H:%M")

def showmessage(data):
    message_frame = ctk.CTkFrame(
        second_frame,
        fg_color=second_frame.cget("fg_color"),  # НЕ прозрачный
    )


    m_block_frame = ctk.CTkFrame(
        message_frame,
        fg_color="purple",
        bg_color=message_frame.cget("fg_color"),
        corner_radius=10
    )
    m_block_frame.pack(side="left", padx=5, pady=5)

    ctk.CTkLabel(
        m_block_frame,
        text=data,
        fg_color="transparent",
        bg_color="transparent",
        wraplength=400,
        font=('Arial', 20),
        anchor="w"
    ).pack(side='top', pady=(5, 0), padx=5)

    gettime()

    ctk.CTkLabel(
        m_block_frame,
        text=current_time,
        fg_color="transparent",
        bg_color="transparent",
        anchor="e",
        height=7,
        font=('Roboto', 9)
    ).pack(side="bottom", fill="x", padx=5, pady=(0, 5))

    message_frame.pack(fill='x', anchor='w', expand=True, padx=10, pady=5)

    scroll_to_bottom()


"""def showrecievingfile(data):
    message_frame = ctk.CTkFrame(second_frame, fg_color="transparent")
    message_frame.pack(fill='x', anchor='w', expand=True, padx=10, pady=5)
    label = ctk.CTkLabel(message_frame, text=data, fg_color="purple", wraplength=400, corner_radius=10,
                 font=('Arial', 20))
    label.pack(side='left')
    scroll_to_bottom()
"""
def showsendingfile(data):
    message_frame = ctk.CTkFrame(
        second_frame,
        fg_color=second_frame.cget("fg_color"),  # НЕ прозрачный
    )

    message_frame.pack(fill='x', anchor='w', expand=True, padx=10, pady=5)

    m_block_frame = ctk.CTkFrame(
        message_frame,
        fg_color="blue",
        bg_color=message_frame.cget("fg_color"),
        corner_radius=10
    )
    m_block_frame.pack(side="right", padx=5, pady=5)

    ctk.CTkLabel(
        m_block_frame,
        text=data,
        fg_color="transparent",
        bg_color="transparent",
        wraplength=400,
        font=('Arial', 20),
        anchor="e"
    ).pack(side='top', pady=(5, 0), padx=5)

    gettime()

    ctk.CTkLabel(
        m_block_frame,
        text=current_time,
        fg_color="transparent",
        bg_color="transparent",
        anchor="e",
        height=7,
        font=('Roboto', 9)
    ).pack(side="bottom", fill="x", padx=5, pady=(0, 5))

    scroll_to_bottom()

def sendfile():

    path2 = filedialog.askopenfilename()
    global path
    path = Path(path2)
    filename = getfilename(str(path))
    size = file_size(str(path))
    global server_started
    if server_started:
        server.sendmessage("<file>"+str(size)+">"+filename)
    else:
        client.sendmessage("<file>"+str(size)+">"+filename)
    showsendingfile(filename)

def sendfiledata():
    global server_started
    global path
    if server_started:
        server.sendfile(path)
    else:
        client.sendfile(path)

def serverstart():
    global server_started
    if not server_started:
        port_text = host_port_entry.get().strip()
        port = int(port_text) if port_text else 8080
        if checkport.is_port_free(int(port)):
            name = username_entry.get().strip()
            username = name if name else "user"

            def freezeentry():
                if server.ison:
                    host_port_entry.delete(0, "end")
                    host_port_entry.insert(0, port)
                    host_port_entry.configure(state="readonly")
                    username_entry.delete(0, "end")
                    username_entry.insert(0, username)
                    username_entry.configure(state="readonly")
                    serverinfo(port)
                    changeserverstatus(True)
            thread = threading.Thread(
                target=server.serverstart,
                args=(getname, showmessage, username, port, serverfailed, freezeentry, sendfiledata)
            )
            thread.start()
        else:
            portinuse(port)

def connectserver():
    port_text = join_port_entry.get().strip()
    port = int(port_text) if port_text else 8080
    name = username_entry.get().strip()
    username = name if name else "user"
    ip = ip_entry.get().strip() if ip_entry.get().strip() else "127.0.0.1"
    def freezeentry():
        join_port_entry.delete(0, "end")
        join_port_entry.insert(0, port)
        join_port_entry.configure(state="readonly")
        username_entry.delete(0, "end")
        username_entry.insert(0, username)
        username_entry.configure(state="readonly")
        ip_entry.delete(0, "end")
        ip_entry.insert(0, ip)
        ip_entry.configure(state="readonly")
    thread = threading.Thread(target=client.connect, args=(getname, showmessage, username, connectionlost, ip, port, freezeentry, sendfiledata))
    thread.start()




def ch_directory():
    global path
    path = filedialog.askdirectory()
    path = Path(path)
    start_web_btn.configure(state="normal")

def startwebser():
    global web_sharing_started
    if not web_sharing_started:
        global web_port_entry
        global path
        global ip_label
        port = web_port_entry.get()
        if port:
            local_ip = ipconfig.get_local_ip()
            httpserver.startwebsharing(Path(path), int(port))
            web_start_info(local_ip, port)
        else :
            local_ip = ipconfig.get_local_ip()
            httpserver.startwebsharing(Path(path), 8080)
            web_start_info(local_ip, port)
        changewebstatus(True)

def resource_path(relative_path):
    """Возвращает путь к файлу, работает и в .py, и в exe"""
    try:
        base_path = sys._MEIPASS  # путь, где PyInstaller кладет файлы
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Работа с окном
win = ctk.CTk()
win.minsize(750, 720)
win.geometry("750x720+62+36")

icon_path = resource_path("icon.ico")
tmp_icon = os.path.join(tempfile.gettempdir(), "app_icon.ico")
shutil.copy(icon_path, tmp_icon)

win.after(201, lambda :win.iconbitmap(icon_path))

win.title("PeerShare")


def validate(new_value):
    return new_value == "" or (new_value.isdigit() and int(new_value) <= 65535)

vcmd = (win.register(validate), '%P')


def validateIp(new_value):
    return (new_value.isdigit()) or (new_value == '.') or (new_value == '')

vcmdIp = (win.register(validateIp), '%S')


# ---------- Верхняя панель ----------
upper_frame = tk.Frame(win, height=100, bg="red")
upper_frame.pack(fill="x", side="top")
upper_frame.pack_propagate(False)

username_frame = tk.Frame(upper_frame, width=300, bg="purple")
username_frame.pack(fill="y", side="left", anchor="center")
username_frame.pack_propagate(False)

namelabel = ctk.CTkLabel(username_frame, text=" ")
namelabel.pack()

username_entry = ctk.CTkEntry(username_frame, placeholder_text="Username")
username_entry.pack()


ip_label = ctk.CTkLabel(username_frame , text="")
ip_label.pack(anchor='center')

connections_frame = tk.Frame(upper_frame, bg="pink")
connections_frame.pack(side="right", fill="both", expand=True)



style = ttk.Style()
style.theme_use('default')

# Стиль для всего Notebook
style.configure("Custom.TNotebook", background="#3f003f", borderwidth=0)

# Стиль для вкладок
style.configure("Custom.TNotebook.Tab",
                background="#4d004d",      # цвет фона вкладки
                foreground="white",          # цвет текста
                padding=[10, 5],
                borderwidth=0)

# Цвет выбранной вкладки
style.map("Custom.TNotebook.Tab",
          background=[("selected", "#660066")],
          foreground=[("selected", "white")])


tab_control = ttk.Notebook(connections_frame, style="Custom.TNotebook")
host_tab = tk.Frame(connections_frame, bg="#660066")
join_tab = tk.Frame(connections_frame, bg="#660066")
web_sharing_tab = tk.Frame(connections_frame, bg="#660066")

tab_control.add(host_tab, text="   Host   ")
tab_control.add(join_tab, text="   Join   ")
tab_control.add(web_sharing_tab, text="   Web Sharing   ")
tab_control.pack(fill="both", expand=1)


port_label = tk.Label(host_tab, text="Port: ", bg="#660066", fg="white")
port_label.pack(side="left", anchor="center", padx=(20,0))
host_port_entry = ctk.CTkEntry(host_tab, placeholder_text="8080", width=60, validate='key', validatecommand=vcmd )
host_port_entry.pack(side="left", anchor="center")

host_button = ctk.CTkButton(host_tab, text="Start Server", fg_color="#b100b1", hover_color="#7d007d", border_width=2, border_color="#4d004d",command=serverstart )
host_button.pack(side="right", padx=20)

ip_entry = ctk.CTkEntry(join_tab, placeholder_text="IP address", validate='key', validatecommand=vcmdIp )
ip_entry.pack(side="left", anchor="center", padx=(20,0))

join_port_entry = ctk.CTkEntry(join_tab, placeholder_text="8080", width=60, validate='key', validatecommand=vcmd )
join_port_entry.pack(side="left", anchor="center")

connect_button = ctk.CTkButton(join_tab, text="connect", fg_color="#b100b1", hover_color="#7d007d", border_width=2, border_color="#4d004d", command=connectserver )
connect_button.pack(side="right", padx=20)

web_port_label = tk.Label(web_sharing_tab, text="Port: ", bg="#660066", fg="white")
web_port_label.pack(side="left", anchor="center", padx=(20,0))
web_port_entry = ctk.CTkEntry(web_sharing_tab, placeholder_text="8080", width=60, validate='key', validatecommand=vcmd )
web_port_entry.pack(side="left", anchor="center")


start_web_btn = ctk.CTkButton(web_sharing_tab, text="Start web sharing", command=startwebser, fg_color="#b100b1", hover_color="#7d007d", border_width=2, border_color="#4d004d" )
start_web_btn.pack(side="right", padx=(0,20))
start_web_btn.configure(state="disabled")
directory_btn = ctk.CTkButton(web_sharing_tab, text="Choose directory", command=ch_directory, fg_color="#b100b1", hover_color="#7d007d", border_width=2, border_color="#4d004d" )
directory_btn.pack(side="right", padx=(20,0))

# ---------- Основная область ----------
main_frame = tk.Frame(win, bg="green")
main_frame.pack(side="bottom", expand=True, fill="both")

# Отправка (внизу)
entry_frame = tk.Frame(main_frame, bg="#0a273c", height=50,)
entry_frame.pack(side="bottom", fill="x")
entry_frame.pack_propagate(False)

# Если файл с иконкой есть — покажет; если нет — просто убери/замени путь
icon_path2 = resource_path("choosefile.png")
try:
    img = tk.PhotoImage(file=icon_path2)
    file_explore = ctk.CTkButton(entry_frame, image=img, text="", width=28, command=sendfile )
except Exception:
    file_explore = ctk.CTkButton(entry_frame, text="...", width=28, command=sendfile)
file_explore.pack(side="left", padx=10)

entry = ctk.CTkEntry(entry_frame, font=("Arial", 18), placeholder_text="Enter your message here...")
entry.pack(fill="x", side="left", expand=True)


def sendmessage():
    global server_started
    msg = entry.get().strip()
    if not msg:
        return
    if checkserverstatus():
        server.sendmessage("<text>"+msg)
    else:
        client.sendmessage("<text>"+msg)


    # отображение сообщения в GUI
    my_message_frame = ctk.CTkFrame(
        second_frame,
        fg_color=second_frame.cget("fg_color"),  # НЕ прозрачный
    )
    my_message_frame.pack(fill='x', anchor='e', expand=True, padx=15, pady=5)

    m_block_frame = ctk.CTkFrame(
        my_message_frame,
        fg_color="blue",
        bg_color=my_message_frame.cget("fg_color"),
        corner_radius=10
    )
    m_block_frame.pack(side="right", padx=5, pady=5)



    ctk.CTkLabel(
        m_block_frame,
        text=msg,
        fg_color="transparent",
        bg_color="transparent",
        wraplength=400,
        font=('Arial', 20),
        anchor="e"
    ).pack(side='top', pady=(5, 0), padx=5)

    gettime()

    ctk.CTkLabel(
        m_block_frame,
        text=current_time,
        fg_color="transparent",
        bg_color="transparent",
        anchor="e",
        height=7,
        font=('Roboto', 9)
    ).pack(side="bottom", fill="x", padx=5, pady=(0, 5))

    entry.delete(0, "end")
    scroll_to_bottom()


send_btn = ctk.CTkButton(entry_frame, text="Send", width=20, command=sendmessage )
send_btn.pack(side="right", padx=10)

# ---------- Чат (скролл) ----------
chat_frame = ctk.CTkFrame(main_frame, corner_radius=0)
chat_frame.pack(fill="both", expand=True)

my_canvas = tk.Canvas(chat_frame, highlightthickness=0, bg="#2b2b2b")
my_canvas.pack(fill="both", side="left", expand=True)

my_scrollbar = ctk.CTkScrollbar(chat_frame, orientation="vertical", command=my_canvas.yview)
my_scrollbar.pack(side="right", fill="y")

my_canvas.configure(yscrollcommand=my_scrollbar.set)

# Frame внутри canvas
second_frame = ctk.CTkFrame(my_canvas, bg_color="#2b2b2b", fg_color="#2b2b2b", corner_radius=0)
window_id = my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

# --- Синхронизация ширины окна внутри canvas с шириной canvas ---
def _on_canvas_configure(event):
    # устанавливем ширину окна равной ширине canvas, чтобы внутренний фрейм "подстраивался"
    my_canvas.itemconfig(window_id, width=event.width)
my_canvas.bind("<Configure>", _on_canvas_configure)

# --- Обновление scrollregion по изменению внутреннего фрейма ---
def _on_frame_configure(event):
    my_canvas.configure(scrollregion=my_canvas.bbox("all"))
second_frame.bind("<Configure>", _on_frame_configure)

# ====== ФУНКЦИЯ ДЛЯ СКРОЛЛА МЫШЬЮ (работает на Windows/Linux/macOS) ======
def _on_mouse_wheel(event):
    if hasattr(event, "delta") and event.delta:
        my_canvas.yview_scroll(-int(event.delta / 120), "units")
    else:
        if event.num == 4:
            my_canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            my_canvas.yview_scroll(1, "units")

# привязываем прокрутку к canvas и к second_frame (чтобы работало при наведении)
my_canvas.bind_all("<MouseWheel>", _on_mouse_wheel)   # Windows/macOS
my_canvas.bind_all("<Button-4>", _on_mouse_wheel)     # Linux up
my_canvas.bind_all("<Button-5>", _on_mouse_wheel)     # Linux down


# автоскролл ВНИЗ после того, как всё будет отрисовано
def scroll_to_bottom():
    my_canvas.update_idletasks()
    my_canvas.yview_moveto(1.0)

# after_idle гарантирует вызов ПОСЛЕ всех внутренних перерасчётов Tk
win.after_idle(scroll_to_bottom)

win.protocol("WM_DELETE_WINDOW", finish)
win.mainloop()
