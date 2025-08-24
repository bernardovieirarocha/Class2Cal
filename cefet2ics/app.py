import csv
import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from cefet2ics.ics_writer import write_ics
from cefet2ics.parser import validate_dates


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('CEFET2ICS - Gerador de Horários (.ics)')
        self.geometry('700x600')
        self.courses = []
        self.semester = {'start_date': '', 'end_date': '', 'calendar_name': ''}
        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self)
        frm.pack(padx=10, pady=10, fill='x')
        # Campos do semestre
        ttk.Label(frm, text='Data início (YYYY-MM-DD)').grid(row=0, column=0)
        self.start_entry = ttk.Entry(frm, width=15)
        self.start_entry.grid(row=0, column=1)
        ttk.Label(frm, text='Data fim (YYYY-MM-DD)').grid(row=0, column=2)
        self.end_entry = ttk.Entry(frm, width=15)
        self.end_entry.grid(row=0, column=3)
        ttk.Label(frm, text='Nome do calendário').grid(row=0, column=4)
        self.calname_entry = ttk.Entry(frm, width=20)
        self.calname_entry.grid(row=0, column=5)
        # Campos da disciplina
        labels = [
            ('Alias', 'alias'),
            ('Nome completo', 'full_name'),
            ('Professor', 'professor'),
            ('Sala', 'room'),
            ('Códigos CEFET', 'schedule_codes')
        ]
        self.fields = {}
        for i, (label, key) in enumerate(labels):
            ttk.Label(frm, text=label).grid(row=i+1, column=0, sticky='w')
            entry = ttk.Entry(frm, width=30)
            entry.grid(row=i+1, column=1, columnspan=2, sticky='w')
            self.fields[key] = entry
        self.add_btn = ttk.Button(frm, text='Adicionar disciplina', command=self.add_course)
        self.add_btn.grid(row=6, column=0, columnspan=2, pady=5)
        self.listbox = tk.Listbox(frm, width=90, height=10)
        self.listbox.grid(row=7, column=0, columnspan=6, pady=5)
        # Botões de salvar/abrir
        self.save_csv_btn = ttk.Button(frm, text='Salvar CSV', command=self.save_csv)
        self.save_csv_btn.grid(row=8, column=0, pady=5)
        self.save_json_btn = ttk.Button(frm, text='Salvar JSON', command=self.save_json)
        self.save_json_btn.grid(row=8, column=1, pady=5)
        self.load_btn = ttk.Button(frm, text='Abrir CSV/JSON', command=self.load_file)
        self.load_btn.grid(row=8, column=2, pady=5)
        self.gen_ics_btn = ttk.Button(frm, text='Gerar .ics', command=self.generate_ics)
        self.gen_ics_btn.grid(row=8, column=3, pady=5)
        self.clear_btn = ttk.Button(frm, text='Limpar tudo', command=self.clear_all)
        self.clear_btn.grid(row=8, column=4, pady=5)

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
        self.semester['start_date'] = self.start_entry.get()
        self.semester['end_date'] = self.end_entry.get()
        self.semester['calendar_name'] = self.calname_entry.get()
        path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON files','*.json')])
        if not path:
            return
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({'semester': self.semester, 'courses': self.courses}, f, ensure_ascii=False, indent=2)
        messagebox.showinfo('Sucesso', f'Arquivo JSON salvo: {path}')

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[('CSV/JSON files','*.csv *.json')])
        if not path:
            return
        self.courses.clear()
        self.listbox.delete(0, tk.END)
        if path.endswith('.csv'):
            with open(path, encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.courses.append(row)
                    self.listbox.insert(tk.END, f"{row['alias']} | {row['full_name']} | {row['professor']} | {row['room']} | {row['schedule_codes']}")
        elif path.endswith('.json'):
            with open(path, encoding='utf-8') as f:
                data = json.load(f)
                self.semester = data.get('semester', self.semester)
                self.start_entry.delete(0, tk.END)
                self.start_entry.insert(0, self.semester.get('start_date',''))
                self.end_entry.delete(0, tk.END)
                self.end_entry.insert(0, self.semester.get('end_date',''))
                self.calname_entry.delete(0, tk.END)
                self.calname_entry.insert(0, self.semester.get('calendar_name',''))
                for course in data.get('courses', []):
                    self.courses.append(course)
                    self.listbox.insert(tk.END, f"{course['alias']} | {course['full_name']} | {course['professor']} | {course['room']} | {course['schedule_codes']}")
        messagebox.showinfo('Sucesso', f'Arquivo carregado: {os.path.basename(path)}')

    def generate_ics(self):
        if not self.courses:
            messagebox.showerror('Erro', 'Nenhuma disciplina adicionada.')
            return
        self.semester['start_date'] = self.start_entry.get()
        self.semester['end_date'] = self.end_entry.get()
        self.semester['calendar_name'] = self.calname_entry.get()
        start, end = validate_dates(type('Args', (), {'start': self.semester['start_date'], 'end': self.semester['end_date']}), self.semester)
        if not start or not end:
            messagebox.showerror('Erro', 'Datas do semestre inválidas.')
            return
        out_path = filedialog.asksaveasfilename(defaultextension='.ics', filetypes=[('ICS files','*.ics')])
        if not out_path:
            return
        n_events = write_ics(self.courses, start, end, self.semester['calendar_name'], out_path)
        messagebox.showinfo('Sucesso', f'.ics gerado: {out_path}\nEventos: {n_events}')

    def clear_all(self):
        self.courses.clear()
        self.listbox.delete(0, tk.END)
        for v in self.fields.values():
            v.delete(0, tk.END)
        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)
        self.calname_entry.delete(0, tk.END)
        self.semester = {'start_date': '', 'end_date': '', 'calendar_name': ''}

if __name__ == '__main__':
    app = MainApp()
    app.mainloop()
