import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from modules import send_post, like_post, comment_post, profile_system

# App Setup
app = tk.Tk()
app.title("NITHYA'S PROFILE 🌌")
app.geometry("850x620")
app.configure(bg="#000000")  # Full page black

# Main frame (Blue content area)
main_frame = tk.Frame(app, bg="#001F3F")
main_frame.place(relwidth=1, relheight=1)

# Fonts
TITLE_FONT = ("Helvetica", 20, "bold")
LABEL_FONT = ("Arial", 12)
BUTTON_FONT = ("Arial", 11, "bold")

# Top Bar
frame_top = tk.Frame(main_frame, bg="#0074D9", height=60)
frame_top.pack(fill=tk.X)

title = tk.Label(frame_top, text="NITHYA'S PROFILE 🌟", fg="white", bg="#0074D9", font=TITLE_FONT)
title.pack(pady=10)

# Post Creator
post_frame = tk.LabelFrame(main_frame, text="📝 Create Post", bg="#003366", font=LABEL_FONT, padx=12, pady=10, bd=2, relief=tk.RIDGE)
post_frame.pack(pady=10)

post_text = tk.Text(post_frame, height=4, width=65, font=LABEL_FONT, bg="#002244", fg="white", insertbackground="white")
post_text.pack()

image_path = None
def upload_image():
    global image_path
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if image_path:
        messagebox.showinfo("Image Selected", f"Selected: {image_path}")

def post():
    content = post_text.get("1.0", tk.END).strip()
    if content:
        send_post.create_post(content, image_path)
        messagebox.showinfo("Posted", "Your post has been published.")
        render_feed()
        post_text.delete("1.0", tk.END)
    else:
        messagebox.showwarning("Empty", "Please write something before posting.")

def style_button(btn):
    btn.configure(bg="#00BFFF", fg="white", font=BUTTON_FONT, activebackground="#009ACD", relief=tk.FLAT)
    btn.bind("<Enter>", lambda e: btn.configure(bg="#009ACD"))
    btn.bind("<Leave>", lambda e: btn.configure(bg="#00BFFF"))

btn_upload = tk.Button(post_frame, text="📸 Upload Image", command=upload_image)
btn_post = tk.Button(post_frame, text="💌 Post", command=post)
style_button(btn_upload)
style_button(btn_post)
btn_upload.pack(side=tk.LEFT, padx=5)
btn_post.pack(side=tk.RIGHT, padx=5)

# Feed Section
feed_frame = tk.Frame(main_frame, bg="#001F3F")
feed_frame.pack(fill=tk.BOTH, expand=True)

post_widgets = []

def render_feed():
    for widget in post_widgets:
        widget.destroy()
    post_widgets.clear()

    for post in send_post.posts[::-1]:
        frame = tk.Frame(feed_frame, bg="#003366", padx=12, pady=12, bd=2, relief=tk.RIDGE)
        frame.pack(pady=8, fill=tk.X)

        tk.Label(frame, text=f"👤 {post['user']}", font=("Arial", 11, "bold"), bg="#003366", fg="white").pack(anchor='w')
        tk.Label(frame, text=post['content'], wraplength=700, bg="#003366", justify="left", font=LABEL_FONT, fg="white").pack(anchor='w')

        if post['image']:
            try:
                img = Image.open(post['image'])
                img = img.resize((220, 220))
                photo = ImageTk.PhotoImage(img)
                img_label = tk.Label(frame, image=photo, bg="#003366")
                img_label.image = photo
                img_label.pack(anchor='w', pady=5)
            except Exception as e:
                tk.Label(frame, text=f"[Error loading image: {e}]", fg="red", bg="#003366").pack(anchor='w')

        btn_like = tk.Button(frame, text=f"❤️ {post['likes']}", command=lambda p=post: [like_post.like(p), render_feed()])
        btn_comment = tk.Button(frame, text="💬 Comment", command=lambda p=post: comment_post.comment_window(app, p))
        style_button(btn_like)
        style_button(btn_comment)
        btn_like.pack(side=tk.LEFT)
        btn_comment.pack(side=tk.LEFT, padx=5)

        if post["comments"]:
            tk.Label(frame, text="🌠 Comments:", font=("Arial", 10, "italic"), bg="#003366", fg="white").pack(anchor='w')
            for c in post["comments"]:
                tk.Label(frame, text=f"- {c['user']}: {c['text']}", bg="#003366", wraplength=700, justify="left", fg="white").pack(anchor='w')

        post_widgets.append(frame)

# Profile View
def view_profile():
    window = tk.Toplevel(app)
    window.title("Profile: Nithya")
    window.geometry("500x600")
    window.configure(bg="#000000")

    def edit_profile():
        edit_window = tk.Toplevel(window)
        edit_window.title("Edit Profile")
        edit_window.geometry("300x200")
        edit_window.configure(bg="#002244")

        tk.Label(edit_window, text="Name:", font=LABEL_FONT, bg="#002244", fg="white").pack(pady=5)
        name_entry = tk.Entry(edit_window, bg="#001F3F", fg="white", insertbackground="white")
        name_entry.insert(0, "Nithya")
        name_entry.pack()

        tk.Label(edit_window, text="Bio:", font=LABEL_FONT, bg="#002244", fg="white").pack(pady=5)
        bio_entry = tk.Entry(edit_window, bg="#001F3F", fg="white", insertbackground="white")
        bio_entry.insert(0, "Passionate developer.")
        bio_entry.pack()

        def save_profile():
            new_name = name_entry.get()
            new_bio = bio_entry.get()
            messagebox.showinfo("Profile Updated", f"Name: {new_name}\nBio: {new_bio}")
            edit_window.destroy()

        btn_save = tk.Button(edit_window, text="💾 Save", command=save_profile)
        style_button(btn_save)
        btn_save.pack(pady=10)

    tk.Label(window, text="🧭 Nithya's Profile", font=("Arial", 16, "bold"), bg="#000000", fg="#00BFFF").pack(pady=10)
    btn_edit = tk.Button(window, text="🖍️ Edit Profile", command=edit_profile)
    style_button(btn_edit)
    btn_edit.pack(pady=5)

    posts = [p for p in send_post.posts if p["user"] == "Nithya"]
    for post in posts[::-1]:
        frame = tk.Frame(window, bg="#003366", padx=10, pady=10, bd=1, relief=tk.SOLID)
        frame.pack(pady=5, fill=tk.X)

        tk.Label(frame, text=post['content'], wraplength=450, justify="left", bg="#003366", font=LABEL_FONT, fg="white").pack(anchor="w")

        if post["image"]:
            try:
                img = Image.open(post["image"])
                img = img.resize((200, 200))
                photo = ImageTk.PhotoImage(img)
                img_label = tk.Label(frame, image=photo, bg="#003366")
                img_label.image = photo
                img_label.pack(anchor='w', pady=5)
            except Exception as e:
                tk.Label(frame, text=f"[Error loading image: {e}]", fg="red", bg="#003366").pack(anchor='w')

        tk.Label(frame, text=f"❤️ {post['likes']} Likes | 💬 {len(post['comments'])} Comments", fg="lightgray", bg="#003366").pack(anchor="w")

        if post["comments"]:
            tk.Label(frame, text="📝 All Comments:", font=("Arial", 10, "italic"), bg="#003366", fg="white").pack(anchor='w')
            for c in post["comments"]:
                tk.Label(frame, text=f"- {c['user']}: {c['text']}", bg="#003366", wraplength=450, justify="left", fg="white").pack(anchor='w')

# Menu
menu = tk.Menu(app)
app.config(menu=menu)
menu.add_command(label="View Profile", command=view_profile)

render_feed()
app.mainloop()