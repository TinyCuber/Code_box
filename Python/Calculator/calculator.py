import tkinter as tk
from tkinter import messagebox
import math
from tkinter import ttk


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Exquisite Calculator (Landscape)")
        # Increase the window size
        self.root.geometry("900x500")
        self.root.configure(bg="#f0f0f0")

        # Text box for displaying results, increase the font size
        self.entry = tk.Entry(root, font=("Arial", 30), bd=5, justify="right")
        self.entry.grid(row=0, column=0, columnspan=10, padx=10, pady=10, sticky="nsew")

        # History list
        self.history = []
        # Memory number, initialized to 0
        self.memory = 0
        # Flag indicating whether the memory has a value
        self.memory_has_value = False

        # History and memory area, increase the font size and button size
        tk.Button(root, text="History", font=("Arial", 20), width=20, height=2,
                  command=self.show_history,
                  bg="#e0e0e0", activebackground="#d0d0d0").grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        tk.Button(root, text="M+", font=("Arial", 20), width=10, height=2,
                  command=lambda: self.memory_plus(),
                  bg="#e0e0e0", activebackground="#d0d0d0").grid(row=1, column=2, padx=5, pady=5)
        tk.Button(root, text="M-", font=("Arial", 20), width=10, height=2,
                  command=lambda: self.memory_minus(),
                  bg="#e0e0e0", activebackground="#d0d0d0").grid(row=1, column=3, padx=5, pady=5)
        tk.Button(root, text="MRC", font=("Arial", 20), width=10, height=2,
                  command=lambda: self.on_button_click('MRC'),
                  bg="#e0e0e0", activebackground="#d0d0d0").grid(row=1, column=4, padx=5, pady=5)

        # Bracket area, increase the font size and button size
        bracket_buttons = [
            '(', ')', '[', ']',
            '{', '}'
        ]
        col_val = 5
        for button in bracket_buttons:
            tk.Button(root, text=button, font=("Arial", 20), width=10, height=2,
                      command=lambda b=button: self.on_button_click(b),
                      bg="#e0e0e0", activebackground="#d0d0d0").grid(row=1, column=col_val, padx=5, pady=5)
            col_val += 1

        # Number area, increase the font size and button size
        number_buttons = [
            '7', '8', '9',
            '4', '5', '6',
            '1', '2', '3',
            '0', '.'
        ]
        row_val = 2
        col_val = 0
        for button in number_buttons:
            tk.Button(root, text=button, font=("Arial", 20), width=10, height=2,
                      command=lambda b=button: self.on_button_click(b),
                      bg="#e0e0e0", activebackground="#d0d0d0").grid(row=row_val, column=col_val, padx=5, pady=5)
            col_val += 1
            if col_val > 2:
                col_val = 0
                row_val += 1

        # Symbol area, increase the font size and button size
        symbol_buttons = [
            '+', '-', '*', '/',
            '^', '!', 'x√y', '√',
            '%', '1/x', '±', '='
        ]
        row_val = 2
        col_val = 3
        for button in symbol_buttons:
            tk.Button(root, text=button, font=("Arial", 20), width=10, height=2,
                      command=lambda b=button: self.on_button_click(b),
                      bg="#e0e0e0", activebackground="#d0d0d0").grid(row=row_val, column=col_val, padx=5, pady=5)
            col_val += 1
            if col_val > 5:
                col_val = 3
                row_val += 1

        # Clear button, increase the font size and button size
        tk.Button(root, text="C", font=("Arial", 20), width=10, height=2,
                  command=lambda: self.on_button_click('C'),
                  bg="#e0e0e0", activebackground="#d0d0d0").grid(row=5, column=2, padx=5, pady=5)

        # π button, increase the font size and button size
        tk.Button(root, text="π", font=("Arial", 20), width=10, height=2,
                  command=lambda: self.on_button_click('π'),
                  bg="#e0e0e0", activebackground="#d0d0d0").grid(row=1, column=11, padx=5, pady=5)

        # Adjust the grid layout weight
        for i in range(6):
            root.grid_rowconfigure(i, weight=1)
        for i in range(12):
            root.grid_columnconfigure(i, weight=1)

    def on_button_click(self, button):
        current = self.entry.get()
        if button == '=':
            try:
                # Check if the brackets match
                if not self.is_bracket_matching(current):
                    messagebox.showerror("Error", "Brackets do not match, please check!")
                    return
                # Replace ^ with ** to support exponentiation
                expression = current.replace('^', '**')
                # Handle factorial
                expression = self.handle_factorial(expression)
                # Handle nth root
                expression = self.handle_nth_root(expression)
                # Replace π with math.pi
                expression = expression.replace('π', 'math.pi')
                # Replace square brackets and curly braces with parentheses
                expression = expression.replace('[', '(').replace(']', ')').replace('{', '(').replace('}', ')')
                result = eval(expression)
                # Record history
                self.history.append(f"{current} = {result}")
                self.entry.delete(0, tk.END)
                self.entry.insert(0, str(result))
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input, please check! Error message: {str(e)}")
        elif button == 'C':
            self.entry.delete(0, tk.END)
        elif button == '±':
            if current:
                if current[0] == '-':
                    self.entry.delete(0)
                else:
                    self.entry.insert(0, '-')
        elif button == '%':
            if current:
                try:
                    num = float(current)
                    result = num / 100
                    self.entry.delete(0, tk.END)
                    self.entry.insert(0, str(result))
                except ValueError:
                    messagebox.showerror("Error", "Invalid input, please enter a number!")
        elif button == '√':
            if current:
                try:
                    num = float(current)
                    if num >= 0:
                        result = math.sqrt(num)
                        self.entry.delete(0, tk.END)
                        self.entry.insert(0, str(result))
                    else:
                        messagebox.showerror("Error", "Cannot take the square root of a negative number!")
                except ValueError:
                    messagebox.showerror("Error", "Invalid input, please enter a number!")
        elif button == '1/x':
            if current:
                try:
                    num = float(current)
                    if num != 0:
                        result = 1 / num
                        self.entry.delete(0, tk.END)
                        self.entry.insert(0, str(result))
                    else:
                        messagebox.showerror("Error", "Cannot divide by zero!")
                except ValueError:
                    messagebox.showerror("Error", "Invalid input, please enter a number!")
        elif button == 'MRC':
            if self.memory_has_value:
                self.entry.delete(0, tk.END)
                self.entry.insert(0, str(self.memory))
            else:
                self.memory = 0
                self.memory_has_value = True
        elif button == 'π':
            self.entry.insert(tk.END, 'π')
        else:
            self.entry.insert(tk.END, button)

    def is_bracket_matching(self, expression):
        stack = []
        bracket_map = {')': '(', ']': '[', '}': '{'}
        for char in expression:
            if char in '([{':
                stack.append(char)
            elif char in ')]}':
                if not stack or stack.pop() != bracket_map[char]:
                    return False
        return len(stack) == 0

    def handle_factorial(self, expression):
        import re
        factorial_pattern = re.compile(r'(\d+)!')
        while factorial_pattern.search(expression):
            match = factorial_pattern.search(expression)
            num = int(match.group(1))
            factorial_result = math.factorial(num)
            expression = expression.replace(match.group(0), str(factorial_result))
        return expression

    def handle_nth_root(self, expression):
        import re
        nth_root_pattern = re.compile(r'(\d+)x√y(\d+)')
        while nth_root_pattern.search(expression):
            match = nth_root_pattern.search(expression)
            root = int(match.group(1))
            number = int(match.group(2))
            nth_root_result = number ** (1 / root)
            expression = expression.replace(match.group(0), str(nth_root_result))
        return expression

    def memory_plus(self):
        current = self.entry.get()
        try:
            num = float(current)
            self.memory += num
            self.memory_has_value = True
        except ValueError:
            messagebox.showerror("Error", "Invalid input, please enter a number!")

    def memory_minus(self):
        current = self.entry.get()
        try:
            num = float(current)
            self.memory -= num
            self.memory_has_value = True
        except ValueError:
            messagebox.showerror("Error", "Invalid input, please enter a number!")

    def show_history(self):
        if not self.history:
            messagebox.showinfo("History", "No history records available.")
        else:
            history_window = tk.Toplevel(self.root)
            history_window.title("History")

            # Use Treeview to display two columns
            tree = ttk.Treeview(history_window, columns=('Serial Number', 'Record'), show='headings')
            tree.heading('Serial Number', text='Serial Number')
            tree.heading('Record', text='Record')
            tree.column('Serial Number', width=50, anchor='center')
            tree.column('Record', width=200)
            tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

            for i, item in enumerate(self.history, start=1):
                tree.insert('', 'end', values=(i, item))

            # Delete selected record button
            delete_selected_button = tk.Button(history_window, text="Delete Selected Record",
                                               command=lambda: self.delete_selected_history(tree))
            delete_selected_button.pack(pady=5)

            # Delete all records button
            delete_all_button = tk.Button(history_window, text="Delete All Records",
                                          command=lambda: self.delete_all_history(tree))
            delete_all_button.pack(pady=5)

    def delete_selected_history(self, tree):
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showinfo("Prompt", "Please select the record to delete.")
            return
        if messagebox.askyesno("Confirmation", "Are you sure you want to delete the selected history record?"):
            indices_to_delete = []
            for item in selected_items:
                index = int(tree.item(item)['values'][0]) - 1
                indices_to_delete.append(index)
            indices_to_delete.sort(reverse=True)

            for index in indices_to_delete:
                del self.history[index]
                tree.delete(tree.get_children()[index])

            # Reorder the serial numbers
            for i, item in enumerate(tree.get_children(), start=1):
                tree.item(item, values=(i, tree.item(item)['values'][1]))

    def delete_all_history(self, tree):
        if messagebox.askyesno("Confirmation", "Are you sure you want to delete all history records?"):
            self.history = []
            for item in tree.get_children():
                tree.delete(item)


if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()