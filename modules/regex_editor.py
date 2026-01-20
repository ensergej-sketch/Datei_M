#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regex Editor - Modul zum Erstellen und Testen von Suchmustern
"""

import tkinter as tk
from tkinter import ttk, messagebox
import re
from datetime import datetime


class RegexEditor:
    """Regex Editor Modul"""
    
    def __init__(self, window):
        self.window = window
        self.window.title("Regex Editor - Suchmuster erstellen")
        self.window.geometry("900x700")
        
        self.setup_ui()
        
    def setup_ui(self):
        """UI-Elemente erstellen"""
        # Header
        header = tk.Label(
            self.window,
            text="🔍 Regex Editor",
            font=("Arial", 18, "bold"),
            bg="#e67e22",
            fg="white",
            pady=15
        )
        header.pack(fill=tk.X)
        
        # Hauptcontainer
        main_frame = tk.Frame(self.window, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Mustervorlagen
        templates_frame = tk.LabelFrame(main_frame, text="Mustervorlagen", padx=10, pady=10)
        templates_frame.pack(fill=tk.X, pady=10)
        
        templates = [
            ("E-Mail", r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            ("Telefon (DE)", r'\b(\+49|0)[1-9]\d{1,4}[\s\-/]?\d{3,}\b'),
            ("Datum (DD.MM.YYYY)", r'\b\d{2}\.\d{2}\.\d{4}\b'),
            ("PLZ (DE)", r'\b\d{5}\b'),
            ("IBAN", r'\b[A-Z]{2}\d{2}[A-Z0-9]{4}\d{7}([A-Z0-9]?){0,16}\b'),
        ]
        
        template_buttons = tk.Frame(templates_frame)
        template_buttons.pack()
        
        for name, pattern in templates:
            tk.Button(
                template_buttons,
                text=name,
                command=lambda p=pattern: self.load_template(p),
                bg="#3498db",
                fg="white",
                padx=10,
                pady=5
            ).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Regex-Pattern
        pattern_frame = tk.LabelFrame(main_frame, text="Regex-Muster", padx=10, pady=10)
        pattern_frame.pack(fill=tk.X, pady=10)
        
        self.pattern_text = tk.Text(pattern_frame, height=3, width=70, font=("Courier", 10))
        self.pattern_text.pack(fill=tk.X)
        
        # Optionen
        options_frame = tk.Frame(pattern_frame)
        options_frame.pack(fill=tk.X, pady=5)
        
        self.case_insensitive = tk.BooleanVar(value=False)
        self.multiline = tk.BooleanVar(value=False)
        self.dotall = tk.BooleanVar(value=False)
        
        tk.Checkbutton(
            options_frame,
            text="Groß-/Kleinschreibung ignorieren (IGNORECASE)",
            variable=self.case_insensitive
        ).pack(anchor=tk.W)
        
        tk.Checkbutton(
            options_frame,
            text="Mehrzeilig (MULTILINE)",
            variable=self.multiline
        ).pack(anchor=tk.W)
        
        tk.Checkbutton(
            options_frame,
            text=". matched auch Zeilenumbrüche (DOTALL)",
            variable=self.dotall
        ).pack(anchor=tk.W)
        
        # Testtext
        testtext_frame = tk.LabelFrame(main_frame, text="Testtext", padx=10, pady=10)
        testtext_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.test_text = tk.Text(testtext_frame, height=10, width=70, font=("Courier", 10))
        test_scrollbar = tk.Scrollbar(testtext_frame, command=self.test_text.yview)
        self.test_text.config(yscrollcommand=test_scrollbar.set)
        
        self.test_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        test_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Beispieltext einfügen
        example_text = """Kontaktdaten:
E-Mail: max.mustermann@example.de
Telefon: +49 123 456789 oder 0171 1234567
Adresse: Musterstraße 42, 12345 Musterstadt
Datum: 15.01.2026
IBAN: DE89370400440532013000
Weitere E-Mail: test@domain.com"""
        
        self.test_text.insert("1.0", example_text)
        
        # Aktions-Button
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame,
            text="Muster testen",
            command=self.test_pattern,
            bg="#27ae60",
            fg="white",
            padx=30,
            pady=10,
            font=("Arial", 11, "bold")
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Muster speichern",
            command=self.save_pattern,
            bg="#3498db",
            fg="white",
            padx=30,
            pady=10,
            font=("Arial", 11, "bold")
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Zurücksetzen",
            command=self.reset_fields,
            bg="#95a5a6",
            fg="white",
            padx=30,
            pady=10,
            font=("Arial", 11, "bold")
        ).pack(side=tk.LEFT, padx=5)
        
        # Ergebnis-Bereich
        result_frame = tk.LabelFrame(main_frame, text="Treffer", padx=10, pady=10)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.result_text = tk.Text(result_frame, height=8, width=70, state=tk.DISABLED, font=("Courier", 10))
        result_scrollbar = tk.Scrollbar(result_frame, command=self.result_text.yview)
        self.result_text.config(yscrollcommand=result_scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tags für Highlighting
        self.test_text.tag_config("match", background="#ffeb3b", foreground="#000000")
        
    def load_template(self, pattern):
        """Vorlage laden"""
        self.pattern_text.delete("1.0", tk.END)
        self.pattern_text.insert("1.0", pattern)
        
    def get_regex_flags(self):
        """Regex-Flags ermitteln"""
        flags = 0
        if self.case_insensitive.get():
            flags |= re.IGNORECASE
        if self.multiline.get():
            flags |= re.MULTILINE
        if self.dotall.get():
            flags |= re.DOTALL
        return flags
        
    def test_pattern(self):
        """Muster gegen Testtext prüfen"""
        pattern = self.pattern_text.get("1.0", tk.END).strip()
        test_text = self.test_text.get("1.0", tk.END)
        
        if not pattern:
            messagebox.showwarning("Warnung", "Bitte geben Sie ein Regex-Muster ein.")
            return
            
        # Alte Highlights entfernen
        self.test_text.tag_remove("match", "1.0", tk.END)
        
        # Ergebnis-Text leeren
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        
        try:
            flags = self.get_regex_flags()
            regex = re.compile(pattern, flags)
            matches = list(regex.finditer(test_text))
            
            if matches:
                self.result_text.insert(tk.END, f"✓ {len(matches)} Treffer gefunden:\n\n")
                
                for i, match in enumerate(matches, 1):
                    # Highlight im Testtext
                    start_idx = f"1.0+{match.start()}c"
                    end_idx = f"1.0+{match.end()}c"
                    self.test_text.tag_add("match", start_idx, end_idx)
                    
                    # Treffer auflisten
                    self.result_text.insert(tk.END, f"Treffer {i}: '{match.group()}'\n")
                    self.result_text.insert(tk.END, f"  Position: {match.start()}-{match.end()}\n")
                    
                    if match.groups():
                        self.result_text.insert(tk.END, f"  Gruppen: {match.groups()}\n")
                    
                    self.result_text.insert(tk.END, "\n")
            else:
                self.result_text.insert(tk.END, "✗ Keine Treffer gefunden.\n")
                
        except re.error as e:
            self.result_text.insert(tk.END, f"✗ Fehler im Regex-Muster:\n{str(e)}\n")
            messagebox.showerror("Regex-Fehler", f"Ungültiges Regex-Muster:\n{str(e)}")
            
        finally:
            self.result_text.config(state=tk.DISABLED)
            
    def save_pattern(self):
        """Muster speichern"""
        pattern = self.pattern_text.get("1.0", tk.END).strip()
        if not pattern:
            messagebox.showwarning("Warnung", "Bitte geben Sie ein Regex-Muster ein.")
            return
            
        # Muster in Datei speichern (simuliert)
        messagebox.showinfo(
            "Gespeichert",
            f"Regex-Muster wurde gespeichert:\n\n{pattern}\n\n"
            f"Optionen:\n"
            f"  IGNORECASE: {self.case_insensitive.get()}\n"
            f"  MULTILINE: {self.multiline.get()}\n"
            f"  DOTALL: {self.dotall.get()}"
        )
        
    def reset_fields(self):
        """Felder zurücksetzen"""
        self.pattern_text.delete("1.0", tk.END)
        self.test_text.tag_remove("match", "1.0", tk.END)
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state=tk.DISABLED)
        self.case_insensitive.set(False)
        self.multiline.set(False)
        self.dotall.set(False)
