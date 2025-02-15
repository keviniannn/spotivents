import tkinter as tk
from tkinter import ttk
import sv_ttk
import webbrowser
from event_finder import EventFinder

client_id = 'd58389caed48416294ea8c57d349f254'
client_secret = 'a5eceb1189714c5fa642675338e0bb01'
redirect_uri = 'https://localhoast:8888/callback'

class ClickableText(tk.Text):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.tag_configure("link", foreground="lime green", underline=True)
        self.bind("<Button-1>", self._on_click)
        self.bind("<Motion>", self._on_motion)
        self.config(state="disabled", cursor="arrow")
        self.is_hovering_link = False

    def _on_click(self, event):
        index = self.index("@%s,%s" % (event.x, event.y))
        tags = self.tag_names(index)
        if "link" in tags:
            url = self.get(index + " linestart", index + " lineend")
            webbrowser.open_new(url)

    def _on_motion(self, event):
        index = self.index("@%s,%s" % (event.x, event.y))
        tags = self.tag_names(index)
        if "link" in tags:
            self.config(cursor="heart")
            self.is_hovering_link = True
        elif self.is_hovering_link:
            self.config(cursor="arrow")
            self.is_hovering_link = False


class ChangeTerm():
    term_options = ['short_term', 'medium_term', 'long_term']
    output_terms = ['Short term', 'Medium term', 'Long term']
    current_index = 1

    @classmethod
    def get_current_term(cls):
        return cls.term_options[cls.current_index]
    
    @classmethod
    def get_output_terms(cls):
        return cls.output_terms[cls.current_index]

    @classmethod
    def next_term(cls):
        cls.current_index = (cls.current_index + 1) % len(cls.term_options)
        return cls.get_current_term()
    
    
class ChangeLimit():
    limit_options = [5, 10, 25]
    output_limits = ['Top 5', 'Top 10', 'Top 25']
    current_index = 1

    @classmethod
    def get_current_limit(cls):
        return cls.limit_options[cls.current_index]
    
    @classmethod
    def get_output_limits(cls):
        return cls.output_limits[cls.current_index]

    @classmethod
    def next_limit(cls):
        cls.current_index = (cls.current_index + 1) % len(cls.limit_options)
        return cls.get_current_limit()


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_coordinate = (screen_width - 800) // 2
        y_coordinate = (screen_height - 600) // 2
        self.geometry(f"800x600+{x_coordinate}+{y_coordinate}")

        def start_program():
            clear_text()
            text_output.config(state="normal")
            event_finder = EventFinder(
                client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
            term = ChangeTerm.get_current_term()
            limit = ChangeLimit.get_current_limit()
            events_info = event_finder.find_events_for_top_artists(limit=limit,term=term)
            for event_info in events_info:
                text_output.insert(tk.END, event_info)
                start_index = "1.0"
                while True:
                    start_index = text_output.search(
                        "https", start_index, stopindex=tk.END)
                    if not start_index:
                        break
                    end_index = text_output.search(
                        "\n", start_index, stopindex=tk.END)
                    text_output.tag_add("link", start_index, end_index)
                    start_index = end_index
            text_output.config(state="disabled")

        def clear_text():
            text_output.config(state="normal")
            text_output.delete(1.0, tk.END)
            text_output.config(state="disabled")

        def cycle_term():
            clear_text()
            text_output.config(state="normal")
            ChangeTerm.next_term()
            text_output.insert(tk.END, 
                               f"Time range: {ChangeTerm.get_output_terms()}")
            text_output.config(state="disabled")

        def cycle_limit():
            clear_text()
            text_output.config(state="normal")
            ChangeLimit.next_limit()
            text_output.insert(tk.END, 
                               f"Artist limit: {ChangeLimit.get_output_limits()}")
            text_output.config(state="disabled")

        def read_me():
            clear_text()
            with open('README.txt', 'r') as file:
                readme_content = file.read()
            text_output.config(state="normal")
            text_output.insert(tk.END, readme_content)
            text_output.config(state="disabled")

        self.title("Spotivents")
        self.geometry("800x600")
        self.resizable(False, False)

        left_frame = ttk.Frame(self, width=300, height=600)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        right_frame = ttk.Frame(self, width=400, height=600)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

        title = ttk.Label(left_frame, text="SPOTIVENTS", font=(
            'System', 24, 'bold'), foreground='lime green')
        title.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

        start_button = ttk.Button(
            left_frame, text="Start", command=start_program, width=15)
        start_button.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

        term_button = ttk.Button(
            left_frame, text='Change Term', command=cycle_term, width=15)
        term_button.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        limit_button = ttk.Button(
            left_frame, text='Change Limit', command=cycle_limit, width=15)
        limit_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        read_me_button = ttk.Button(
            left_frame, text="Read Me", command=read_me, width=15)
        read_me_button.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

        text_output = ClickableText(right_frame, wrap=tk.WORD,
                                    borderwidth=4, highlightthickness=2, relief=tk.SOLID, highlightbackground='lime green', highlightcolor='lime green', background='grey17')
        text_output.pack(fill=tk.BOTH, expand=True)

        read_me()

        sv_ttk.set_theme("dark")


def main():
    root = MainWindow()
    root.mainloop()


if __name__ == "__main__":
    main()
