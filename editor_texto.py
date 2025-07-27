import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter.font import Font

class BaseEditor:
    def __init__(self, root):
        self._root = root
        self._root.geometry("800x600")
        self._file_path = None

    def _create_menu(self):
        raise NotImplementedError("Subclasses devem implementar o método '_create_menu'.")

    def _create_widgets(self):
        raise NotImplementedError("Subclasses devem implementar o método '_create_widgets'.")


class TextEditor(BaseEditor):
    def __init__(self, root):
        super().__init__(root)
        self._root.title("Editor de Texto")
        self._font = Font(family="Arial", size=12)
        self._create_widgets()
        self._create_menu()

    def _create_widgets(self):
        # Área de texto
        self._text_area = tk.Text(self._root, wrap="word", undo=True, font=self._font)
        self._text_area.pack(expand=1, fill="both")

        # Barra de rolagem
        scroll_bar = tk.Scrollbar(self._root, command=self._text_area.yview)
        scroll_bar.pack(side="right", fill="y")
        self._text_area.config(yscrollcommand=scroll_bar.set)

        # Barra de status
        self._status_bar = tk.Label(self._root, text="Linhas: 1 | Colunas: 1", anchor="e")
        self._status_bar.pack(fill="x", side="bottom")
        self._update_status_bar()

        self._text_area.bind("<KeyRelease>", lambda e: self._update_status_bar())

    def _create_menu(self):
        menu_bar = tk.Menu(self._root)

        # Menu Arquivo
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Novo", command=self._new_file)
        file_menu.add_command(label="Abrir", command=self._open_file)
        file_menu.add_command(label="Salvar", command=self._save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self._exit_editor)
        menu_bar.add_cascade(label="Arquivo", menu=file_menu)

        # Menu Editar
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Copiar", command=self._copy_text)
        edit_menu.add_command(label="Recortar", command=self._cut_text)
        edit_menu.add_command(label="Colar", command=self._paste_text)
        menu_bar.add_cascade(label="Editar", menu=edit_menu)

        # Menu Formatar
        format_menu = tk.Menu(menu_bar, tearoff=0)
        format_menu.add_command(label="Alterar Fonte", command=self._change_font)
        format_menu.add_command(label="Negrito", command=self._toggle_bold)
        format_menu.add_command(label="Itálico", command=self._toggle_italic)
        format_menu.add_command(label="Sublinhado", command=self._toggle_underline)
        menu_bar.add_cascade(label="Formatar", menu=format_menu)

        # Menu Listas
        list_menu = tk.Menu(menu_bar, tearoff=0)
        list_menu.add_command(label="Adicionar Lista Numerada", command=self._add_numbered_list)
        list_menu.add_command(label="Adicionar Lista com Marcadores", command=self._add_bulleted_list)
        menu_bar.add_cascade(label="Listas", menu=list_menu)

        self._root.config(menu=menu_bar)

    def _new_file(self):
        self._text_area.delete(1.0, tk.END)
        self._root.title("Novo Arquivo - Editor de Texto")
        self._file_path = None

    def _open_file(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    self._text_area.delete(1.0, tk.END)
                    self._text_area.insert(1.0, file.read())
                self._root.title(f"{file_path} - Editor de Texto")
                self._file_path = file_path
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível abrir o arquivo: {e}")

    def _save_file(self):
        if not self._file_path:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")]
            )
            if file_path:
                self._file_path = file_path
        try:
            with open(self._file_path, "w", encoding="utf-8") as file:
                file.write(self._text_area.get(1.0, tk.END))
            self._root.title(f"{self._file_path} - Editor de Texto")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar o arquivo: {e}")

    def _exit_editor(self):
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            self._root.destroy()

    def _copy_text(self):
        self._root.clipboard_clear()
        self._root.clipboard_append(self._text_area.selection_get())

    def _cut_text(self):
        self._copy_text()
        self._text_area.delete("sel.first", "sel.last")

    def _paste_text(self):
        self._text_area.insert(tk.INSERT, self._root.clipboard_get())

    def _change_font(self):
        family = simpledialog.askstring("Fonte", "Digite a família da fonte (ex: Arial):")
        size = simpledialog.askinteger("Tamanho", "Digite o tamanho da fonte:")
        if family and size:
            self._font.config(family=family, size=size)

    def _toggle_bold(self):
        weight = "bold" if self._font.cget("weight") != "bold" else "normal"
        self._font.config(weight=weight)

    def _toggle_italic(self):
        slant = "italic" if self._font.cget("slant") != "italic" else "roman"
        self._font.config(slant=slant)

    def _toggle_underline(self):
        underline = 1 if self._font.cget("underline") == 0 else 0
        self._font.config(underline=underline)

    def _add_numbered_list(self):
        lines = self._text_area.get("sel.first", "sel.last").split("\n")
        numbered_lines = [f"{i+1}. {line}" for i, line in enumerate(lines)]
        self._text_area.delete("sel.first", "sel.last")
        self._text_area.insert(tk.INSERT, "\n".join(numbered_lines))

    def _add_bulleted_list(self):
        lines = self._text_area.get("sel.first", "sel.last").split("\n")
        bulleted_lines = [f"• {line}" for line in lines]
        self._text_area.delete("sel.first", "sel.last")
        self._text_area.insert(tk.INSERT, "\n".join(bulleted_lines))

    def _update_status_bar(self):
        line, column = self._text_area.index(tk.INSERT).split(".")
        self._status_bar.config(text=f"Linhas: {line} | Colunas: {column}")


if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()
