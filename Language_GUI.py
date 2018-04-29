from tkinter import *
from tkinter import messagebox
import Language as lang

# region initialize root(empty) window
root = Tk()
root.title("Behaviour Analyzer")
root.geometry("400x150")
# root.resizable(False, False)
# root.configure(background='grey')
# endregion

# region initialize frames (DISABLED)
# top_frame = Frame(root)
# top_frame.pack(fill=X)
# bottom_frame = Frame(root)
# bottom_frame.pack(side=BOTTOM, fill=X)
# endregion

# region Top Area
empty = "        "
empty_label_1 = Label(root, text=empty)
empty_label_1.grid(row=0, column=0)
# create a label (textbox)
# input_type_label = Label(root, text="Input type :")
# # put the label in the first possible place
# input_type_label.grid(row=0, column=1, sticky=E)
#
#
# input type parameters
input_type = StringVar(root)
input_type.set("Select required type")
#
#
# def update_input_type_label(in_type):
#     """ this function handles the update of the label"""
#     input_type_label.configure(text=in_type + " :")
#     input_type_label.update()
#
input_type_list = OptionMenu(root, input_type, "NaiveBayes","MaxEntropy")
input_type_list.grid(row=0, column=2, sticky=E)

# endregion

# region Bottom Area
empty_label_2 = Label(root, text=empty)
empty_label_2.grid(row=1, column=0)

input_type_label = Label(root, text="Input :")
# put the label in the first possible place
input_type_label.grid(row=1, column=1, sticky=E)


# user input field
user_input = Text(root, height=3, width=30)
user_input.grid(row=1, column=2)

def submit_data():
    data = user_input.get("1.0", 'end-1c')
    print(data)

    # tweet : @mileskimball a second Trump Administration will be in position to attack rural and many urban druggers in Mexico,… https://t.co/dnFF1Pcg4q"
    #if input_type.get() == "Tweet":
    result = lang.Main(data,input_type.get())
    string = ''
    for obj in result:
        string += obj[0]+' => '+obj[1]+'\n\n'
    messagebox.showinfo("Result : " ,string)
    #print(result)
    return


empty_label_3 = Label(root, text=empty)
empty_label_3.grid(row=2, column=1)
empty_label_4 = Label(root, text=empty)
empty_label_4.grid(row=3, column=0)
# submit button
submit_button = Button(root, text="Submit", command=submit_data)
submit_button.grid(row=3, column=2)

# endregion

# create GUI loop
root.mainloop()