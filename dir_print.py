""" dir_print.py
    Directories and/or files are specified.
    Specified contents of in_dropdown are written to out_dropdown/entry_file.txt
    Textbox shows lines output to file.
"""

import customtkinter as ctk
from pathlib import Path
import psutil  # Used to find disk partitions to initiate comboboxes
import re  # Used in remove_excess_spaces(path)

app = ctk.CTk()
app.geometry("400x270")
app.resizable(False, False)
app.title("Directory Printer.py")
app.eval("tk::PlaceWindow . center")
ctk.set_appearance_mode("System")
files_chk = ctk.CTkCheckBox(app)
files_var = ctk.IntVar(value=False)
dirs_chk = ctk.CTkCheckBox(app)
dirs_var = ctk.IntVar(value=False)
subs_chk = ctk.CTkCheckBox(app)
subs_var = ctk.IntVar(value=False)
cb_in = ctk.CTkComboBox(app)
cb_in_var = ctk.StringVar(value="")
cb_out = ctk.CTkComboBox(app)
cb_out_var = ctk.StringVar(value="")
e_file = ctk.CTkEntry(app)
textbox = ctk.CTkTextbox(app)
drives = [str(p.mountpoint) for p in psutil.disk_partitions(all=True) if p.fstype]
max_combobox_items = 20  # Menu items displayed


def main():
    draw_widgets()
    app.mainloop()


def widget(self, widget, t, *args) -> None:
    """Generate and place widet"""
    # Common args: app, widget, text, args
    blue_color = "#5da3d1"
    var_font = ("Tahoma", 14)
    fixed_font = ("Courier New", 16)
    *arg, x, y = args  # {widget defined}, relx, rely
    match widget:  # widget defined params required
        case "label":
            # global: none
            ref = ctk.CTkLabel(self, text=t, font=var_font)
        case "radio":
            # global: var=ctk.StringVar(value="x") (x=default)
            var, v = arg  # var, val
            ref = ctk.CTkRadioButton(self, text=t, variable=var, value=v)
        case "checkbox":
            # global: ref=ctk.IntVar(value=x), var=ctk.CTkCheckBox(self) (x=True/False)
            ref, var = arg  # name, var
            ref.configure(self, text=t, font=var_font, variable=var)
        case "button":
            # global: none
            c, w, r = arg  # action, width, radius
            ref = ctk.CTkButton(self, text=t, command=c, width=w, corner_radius=r)
        case "combo":
            # global: ref=ctk.CTkComboBox(self), var=ctk.StringVar(value="")
            ref, v, c, var, w, x1 = arg  # name, val, action, var, width, label_start
            lab = ctk.CTkLabel(self, text=t, font=var_font)
            lab.place(relx=x1, rely=y, anchor="nw")
            ref.configure(values=v, font=var_font, command=c, variable=var, width=w)
        case "entry":
            # global: ref=ctk.CTkEntry(self)
            ref, w, x1 = arg  # name, width, label_start
            lab = ctk.CTkLabel(self, text=t, font=var_font)
            lab.place(relx=x1, rely=y, anchor="nw")
            ref.configure(width=w, font=var_font, text_color=blue_color)
        case "textbox":
            # global: ref=ctk.CTkTextbox(self)
            ref, wr, w, h = arg  # name, wrap, width, height
            ref.configure(
                self,
                fg_color="transparent",
                font=var_font,
                text_color=blue_color,
                wrap=wr,
                width=w,
                height=h,
                corner_radius=5,
            )
    ref.place(relx=x, rely=y, anchor="nw")


def draw_widgets():
    """generates customtkinter window"""
    rx1, rx2, rx3, rx4 = 0.05, 0.13, 0.28, 0.75
    ry1 = 0.02  # files cb
    ry2 = 0.13  # dirs cb
    ry3 = 0.24  # in combo
    ry4 = 0.37  # out combo
    ry5 = 0.50  # entry
    ry6 = 0.63  # buttons
    ry7 = 0.75  # textbox

    cb_init = [drive for drive in drives]
    widget(app, "label", "Output Type:", rx1, ry1)
    widget(app, "checkbox", "Files", files_chk, files_var, rx3, ry1)
    widget(app, "checkbox", "Directories", dirs_chk, dirs_var, rx3, ry2)
    widget(app, "checkbox", "SubDirectories", subs_chk, subs_var, 0.55, ry2)
    widget(app, "combo", "In:", cb_in, cb_init, cbox_in, cb_in_var, 330, rx1, rx2, ry3)
    widget(
        app, "combo", "Out:", cb_out, cb_init, cbox_out, cb_out_var, 330, rx1, rx2, ry4
    )
    widget(app, "entry", "Output File:", e_file, 185, rx1, rx3, ry5)
    widget(app, "label", ".txt", rx4, ry5)
    widget(app, "button", "Run", run_button, 80, 5, rx3, ry6)
    widget(app, "button", "Exit", exit, 80, 5, rx4, ry6)
    widget(app, "textbox", "", textbox, "none", 360, 65, rx1, ry7)


def dropdown_values(val):
    """populate dropdown menus"""
    path = Path(val)
    if str(path) in drives:  # Populate with partitions
        directory = [drive for drive in drives]
    else:  # Populate with parent path
        directory = [str(path.parent)]
    directory += [str(subdir) for subdir in path.iterdir() if subdir.is_dir()]
    if len(directory) > max_combobox_items:
        directory = directory[:max_combobox_items]
    return directory


def cbox_in(val) -> None:
    """populate input dir dropdown menu"""
    cb_in.configure(values=dropdown_values(val))


def cbox_out(val) -> None:
    """populate output dir dropdown menu"""
    cb_out.configure(values=dropdown_values(val))


def write_line(text: str) -> str:
    """output str to textbox"""
    data = textbox.get(1.0, "end")
    line_to_write = sum(1 for char in data if char == "\n") + 1
    textbox.configure(state="normal")
    textbox.insert(f"{line_to_write}.0", f"{text}\n")
    textbox.configure(state="disabled")


def run_button() -> None:
    """writes input dropdown selection to output dropdown selection"""
    if not (cb_in.get() and cb_out.get() and e_file.get()):
        write_line(f"ERROR: directories and txt file must be supplied.")
        return
    out_file = f"{cb_out.get()}\\{e_file.get()}.txt"
    lines_out = write_textfile(cb_in.get(), out_file)
    write_line(f"{lines_out} lines written to {out_file}")


def remove_excess_spaces(path) -> str:
    name = path.parts[-1]
    new_name = re.sub(r"\s+", " ", name)
    if name != new_name:
        path = path.rename(path.with_name(new_name))
    return path


def file_tree(p: Path, subdir: bool = False) -> dict:
    files = {}
    if subdir or (not subdir and files_var.get()):
        files = {f"{p}": []}  # files[path.parent]
    for path in p.iterdir():
        path = remove_excess_spaces(path)
        if path.is_dir():
            if dirs_var.get() or subdir:
                files[f"{path}"] = []
            if subs_var.get():
                files.update(file_tree(path, True))
        elif files_var.get() and path.is_file():
            files[f"{path.parent}"].append(f"{path.parts[-1]}")
    return files


def write_textfile(input_dir: str, output_file: str) -> int:
    """write sub-directory names to file"""
    input_dir: Path = Path(input_dir)
    # Create title line
    txt = ""
    if dirs_var.get():
        txt = f"Directories"
    txt += (
        f" and SubDirectories"
        if txt and subs_var.get()
        else "SubDirectories" if subs_var.get() else ""
    )
    txt += (
        f" and Files" if txt and files_var.get() else "Files" if files_var.get() else ""
    )
    if txt:
        txt += f" of {input_dir}"
    else:
        return 0  # nothing selected

    files = file_tree(input_dir)
    n = 0
    with open(output_file, "w") as f:
        f.write(f"{txt}\n\n")
        for k, v in files.items():
            first = True
            f.write(k)
            if not v:
                f.write("\n")
                n += 1
                continue
            for file in v:
                if first:
                    f.write(f"\\{file}\n")
                    first = False
                else:
                    f.write(f"{" "*(len(k)+1)}{file}\n")
                n += 1
    return n


if __name__ == "__main__":
    main()
