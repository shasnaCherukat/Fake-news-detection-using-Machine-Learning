import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
from fake import manual_testing,url_enter
import validators

def switch_to_input_frame():
    main_frame.pack_forget()
    input_frame.pack(fill="both", expand=True)

def switch_to_url_frame():
    input_frame.pack_forget()
    url_frame.pack(fill="both", expand=True)

def switch_to_news_frame():
    input_frame.pack_forget()
    news_frame.pack(fill="both", expand=True)

def switch_to_input_from_url_frame():
    url_frame.pack_forget()
    input_frame.pack(fill="both", expand=True)

def switch_to_input_from_news_frame():
    news_frame.pack_forget()
    input_frame.pack(fill="both", expand=True)

def submit_url():
    url = url_entry.get()
    if url.strip():
        if validators.url(url):
            result = url_enter(url)
            messagebox.showinfo("Result", f"The news is: {result}")
        else:
            messagebox.showerror("Error", "Invalid URL entered. Please enter a valid URL.")
    else:
        messagebox.showwarning("Warning", "Please enter the URL.")




def submit_news():
    news_input = news_entry.get("1.0", "end-1c")
    if news_input.strip():
        result = manual_testing(news_input)
        messagebox.showinfo("Result", f"The news is: {result}")
    else:
        messagebox.showwarning("Warning", "Please enter a news article.")

root = tk.Tk()
root.title("Fake News API")

# Load the background image
background_image = Image.open(r"C:\Users\rohan\Downloads\_4fbc0c76-24dd-45b8-ba51-5da32a87f93c.jpg")
background_image = background_image.resize((1920, 1080), Image.LANCZOS)
background_image = ImageTk.PhotoImage(background_image)

backy = Image.open(r"C:\Users\rohan\Downloads\mini\gray2.jpg")
backy = backy.resize((1920, 1080), Image.LANCZOS)
backy = ImageTk.PhotoImage(backy)

window_width = 1920
window_height = 1080

main_frame = tk.Frame(root, width=window_width, height=window_height)
main_frame.pack_propagate(False)
main_frame.pack(fill="both", expand=True)
background_label = tk.Label(main_frame, image=background_image)
background_label.place(relwidth=1, relheight=1)

next_button = tk.Button(main_frame, text="START", command=switch_to_input_frame, font=("Helvetica", 16), bg="gray", relief="flat")
next_button.pack()
next_button.place(x=700, y=700, width=150, height=50)

input_frame = ttk.Frame(root, width=window_width, height=window_height, style='TFrame')
input_frame.pack_propagate(False)

input_background_label = tk.Label(input_frame, image=backy)
input_background_label.place(relwidth=1, relheight=1)

url_button = tk.Button(input_frame, text="Enter URL", command=switch_to_url_frame, font=("Helvetica", 25), fg="white", relief="raised", bg="gray")
url_button.pack()
url_button.place(x=600, y=500, width=300, height=65)

news_button = tk.Button(input_frame, text="Enter news article", command=switch_to_news_frame, font=("Helvetica", 25), fg="white", relief="raised", bg="gray")
news_button.pack()
news_button.place(x=600, y=600, width=300, height=65)

url_frame = ttk.Frame(root, width=window_width, height=window_height, style='TFrame')
url_frame.pack_propagate(False)
url_frame_bg_label = tk.Label(url_frame, image=backy)
url_frame_bg_label.place(relwidth=1, relheight=1)

url_heading_text = "Enter the URL"
url_heading_label = tk.Label(url_frame, text=url_heading_text, font=("Times", 17), bg="gray12", fg="white")
url_heading_label.pack(side="left")
url_heading_label.place(x=230, y=360)

url_entry = tk.Entry(url_frame, font=("Helvetica", 15))
url_entry.pack()
url_entry.place(x=380, y=360, width=800,height=30)

submit_url_button = tk.Button(url_frame, text="Submit", command=submit_url, fg="white", relief="raised", bg="gray")
submit_url_button.pack()
submit_url_button.place(x=888, y=700, width=80, height=35)

back_url_button = tk.Button(url_frame, text="Go back", command=switch_to_input_from_url_frame, fg="white", relief="raised", bg="gray")
back_url_button.pack()
back_url_button.place(x=600, y=700, width=80, height=35)

news_frame = ttk.Frame(root, width=window_width, height=window_height, style='TFrame')
news_frame.pack_propagate(False)
news_frame_bg_label = tk.Label(news_frame, image=backy)
news_frame_bg_label.place(relwidth=1, relheight=1)

news_heading_text = "Enter the news article"
news_heading_label = tk.Label(news_frame, text=news_heading_text, font=("Times", 20), bg="gray12", fg="white")
news_heading_label.place(x=630, y=65)

news_entry = tk.Text(news_frame, height=30, width=125, font=("Helvetica", 15), bg='gray25',fg='white')
news_entry.pack()
news_entry.place(x=180, y=100,width=1200,height=550)

submit_news_button = tk.Button(news_frame, text="Submit", command=submit_news, fg="white", relief="raised", bg="gray")
submit_news_button.pack()
submit_news_button.place(x=888, y=700, width=80, height=35)

back_news_button = tk.Button(news_frame, text="Go back", command=switch_to_input_from_news_frame,  fg="white", relief="raised", bg="gray")
back_news_button.pack()
back_news_button.place(x=600, y=700, width=80, height=35)

root.mainloop()