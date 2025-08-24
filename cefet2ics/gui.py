import csv
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class CourseForm(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(padx=10, pady=10)
        self.fields = {}
        labels = [
            ('Alias', 'alias'),
            ('Nome completo', 'full_name'),
            ('Professor', 'professor'),
            ('Sala', 'room'),
            ('Códigos CEFET', 'schedule_codes')
        ]
        for i, (label, key) in enumerate(labels):
            ttk.Label(self, text=label).grid(row=i, column=0, sticky='w')
            entry = ttk.Entry(self, width=30)
            entry.grid(row=i, column=1)
            self.fields[key] = entry
        self.add_btn = ttk.Button(self, text='Adicionar disciplina', command=self.add_course)
        self.add_btn.grid(row=len(labels), column=0, columnspan=2, pady=5)
        self.courses = []
        self.listbox = tk.Listbox(self, width=60)
        self.listbox.grid(row=len(labels)+1, column=0, columnspan=2, pady=5)
        self.save_csv_btn = ttk.Button(self, text='Salvar CSV', command=self.save_csv)
        self.save_csv_btn.grid(row=len(labels)+2, column=0, pady=5)
        self.save_json_btn = ttk.Button(self, text='Salvar JSON', command=self.save_json)
        self.save_json_btn.grid(row=len(labels)+2, column=1, pady=5)

    def add_course(self):
        course = {k: v.get() for k, v in self.fields.items()}
        if not course['alias'] or not course['schedule_codes']:
            messagebox.showerror('Erro', 'Alias e Códigos CEFET são obrigatórios.')
            return
        self.courses.append(course)
        self.listbox.insert(tk.END, f"{course['alias']} | {course['full_name']} | {course['professor']} | {course['room']} | {course['schedule_codes']}")
        for v in self.fields.values():
            v.delete(0, tk.END)

    def save_csv(self):
        if not self.courses:
            messagebox.showerror('Erro', 'Nenhuma disciplina adicionada.')
            return
        path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files','*.csv')])
        if not path:
            return
        with open(path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['alias','full_name','professor','room','schedule_codes'])
            writer.writeheader()
            writer.writerows(self.courses)
        messagebox.showinfo('Sucesso', f'Arquivo CSV salvo: {path}')

    def save_json(self):
        if not self.courses:
            messagebox.showerror('Erro', 'Nenhuma disciplina adicionada.')
            return
        path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON files','*.json')])
        if not path:
            return
        def save_semester():
            win = tk.Toplevel(self)
            win.title('Dados do semestre')
            entries = {}
            for i, (label, key) in enumerate([
                ('Data início (YYYY-MM-DD)', 'start_date'),
                ('Data fim (YYYY-MM-DD)', 'end_date'),
                ('Nome do calendário', 'calendar_name')
            ]):
                ttk.Label(win, text=label).grid(row=i, column=0)
                entry = ttk.Entry(win, width=25)
                entry.grid(row=i, column=1)
                entries[key] = entry
            def confirm():
                semester = {k: entry.get() for k, entry in entries.items()}
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump({'semester': semester, 'courses': self.courses}, f, ensure_ascii=False, indent=2)
                messagebox.showinfo('Sucesso', f'Arquivo JSON salvo: {path}')
                win.destroy()
            ttk.Button(win, text='Salvar', command=confirm).grid(row=3, column=0, columnspan=2, pady=5)
        save_semester()

def main():
    root = tk.Tk()
    root.title('CEFET2ICS - Adicionar Disciplinas')
    CourseForm(root)
    root.mainloop()

if __name__ == '__main__':
    main()
