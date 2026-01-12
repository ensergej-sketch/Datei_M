#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dokumente Manager - Modul zur intelligenten Dokumentenverwaltung mit Regeln und OCR
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from datetime import datetime
from pathlib import Path


class DokumenteManager:
    """Dokumente Manager Modul"""
    
    def __init__(self, window):
        self.window = window
        self.window.title("Dokumente Manager - Regeln und OCR")
        self.window.geometry("900x600")
        
        self.document_dir = tk.StringVar()
        self.rules = []
        
        self.setup_ui()
        
    def setup_ui(self):
        """UI-Elemente erstellen"""
        # Header
        header = tk.Label(
            self.window,
            text="📄 Dokumente Manager",
            font=("Arial", 18, "bold"),
            bg="#9b59b6",
            fg="white",
            pady=15
        )
        header.pack(fill=tk.X)
        
        # Hauptcontainer
        main_frame = tk.Frame(self.window, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Dokumentenordner
        dir_frame = tk.LabelFrame(main_frame, text="Dokumentenordner", padx=10, pady=10)
        dir_frame.pack(fill=tk.X, pady=10)
        
        tk.Entry(dir_frame, textvariable=self.document_dir, width=60).pack(side=tk.LEFT, padx=5)
        tk.Button(
            dir_frame,
            text="Durchsuchen...",
            command=self.browse_directory,
            bg="#95a5a6",
            fg="white"
        ).pack(side=tk.LEFT)
        
        # Regeln-Bereich
        rules_frame = tk.LabelFrame(main_frame, text="Verarbeitungsregeln", padx=10, pady=10)
        rules_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Listbox für Regeln
        list_frame = tk.Frame(rules_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.rules_listbox = tk.Listbox(list_frame, height=8)
        scrollbar = tk.Scrollbar(list_frame, command=self.rules_listbox.yview)
        self.rules_listbox.config(yscrollcommand=scrollbar.set)
        
        self.rules_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Regel-Buttons
        rule_buttons = tk.Frame(rules_frame)
        rule_buttons.pack(pady=10)
        
        tk.Button(
            rule_buttons,
            text="Regel hinzufügen",
            command=self.add_rule,
            bg="#3498db",
            fg="white",
            padx=10
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            rule_buttons,
            text="Regel entfernen",
            command=self.remove_rule,
            bg="#e74c3c",
            fg="white",
            padx=10
        ).pack(side=tk.LEFT, padx=5)
        
        # Vordefinierte Regeln
        predefined_frame = tk.LabelFrame(main_frame, text="Vordefinierte Regeln", padx=10, pady=10)
        predefined_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(
            predefined_frame,
            text="Rechnungen erkennen",
            command=lambda: self.add_predefined_rule("Rechnung"),
            bg="#27ae60",
            fg="white",
            padx=10
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            predefined_frame,
            text="Briefe erkennen",
            command=lambda: self.add_predefined_rule("Brief"),
            bg="#27ae60",
            fg="white",
            padx=10
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            predefined_frame,
            text="Verträge erkennen",
            command=lambda: self.add_predefined_rule("Vertrag"),
            bg="#27ae60",
            fg="white",
            padx=10
        ).pack(side=tk.LEFT, padx=5)
        
        # OCR-Optionen
        ocr_frame = tk.LabelFrame(main_frame, text="OCR-Optionen", padx=10, pady=10)
        ocr_frame.pack(fill=tk.X, pady=10)
        
        self.ocr_enabled = tk.BooleanVar(value=True)
        self.ocr_language = tk.StringVar(value="deu")
        
        tk.Checkbutton(
            ocr_frame,
            text="OCR aktivieren (Texterkennung in Bildern und PDFs)",
            variable=self.ocr_enabled
        ).pack(anchor=tk.W)
        
        lang_frame = tk.Frame(ocr_frame)
        lang_frame.pack(anchor=tk.W, pady=5)
        tk.Label(lang_frame, text="Sprache:").pack(side=tk.LEFT, padx=5)
        ttk.Combobox(
            lang_frame,
            textvariable=self.ocr_language,
            values=["deu", "eng", "fra", "spa"],
            width=10,
            state="readonly"
        ).pack(side=tk.LEFT)
        
        # Aktions-Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        tk.Button(
            button_frame,
            text="Dokumente analysieren",
            command=self.analyze_documents,
            bg="#f39c12",
            fg="white",
            padx=20,
            pady=10,
            font=("Arial", 11, "bold")
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Verarbeitung starten",
            command=self.process_documents,
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=10,
            font=("Arial", 11, "bold")
        ).pack(side=tk.LEFT, padx=5)
        
    def browse_directory(self):
        """Dokumentenordner auswählen"""
        directory = filedialog.askdirectory(title="Dokumentenordner auswählen")
        if directory:
            self.document_dir.set(directory)
            
    def add_rule(self):
        """Neue Regel hinzufügen"""
        rule_window = tk.Toplevel(self.window)
        rule_window.title("Neue Regel hinzufügen")
        rule_window.geometry("400x300")
        
        tk.Label(rule_window, text="Regelname:", font=("Arial", 10, "bold")).pack(pady=10)
        rule_name = tk.Entry(rule_window, width=40)
        rule_name.pack(pady=5)
        
        tk.Label(rule_window, text="Suchbegriff/Muster:", font=("Arial", 10, "bold")).pack(pady=10)
        search_term = tk.Entry(rule_window, width=40)
        search_term.pack(pady=5)
        
        tk.Label(rule_window, text="Zielordner:", font=("Arial", 10, "bold")).pack(pady=10)
        target_folder = tk.Entry(rule_window, width=40)
        target_folder.pack(pady=5)
        
        def save_rule():
            name = rule_name.get()
            term = search_term.get()
            folder = target_folder.get()
            
            if name and term and folder:
                rule = f"{name}: '{term}' -> {folder}"
                self.rules.append(rule)
                self.rules_listbox.insert(tk.END, rule)
                rule_window.destroy()
            else:
                messagebox.showwarning("Warnung", "Bitte füllen Sie alle Felder aus.")
                
        tk.Button(
            rule_window,
            text="Speichern",
            command=save_rule,
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=10
        ).pack(pady=20)
        
    def remove_rule(self):
        """Ausgewählte Regel entfernen"""
        selection = self.rules_listbox.curselection()
        if selection:
            index = selection[0]
            self.rules_listbox.delete(index)
            del self.rules[index]
            
    def add_predefined_rule(self, doc_type):
        """Vordefinierte Regel hinzufügen"""
        patterns = {
            "Rechnung": ("Rechnung", "rechnung|invoice|betrag|mwst"),
            "Brief": ("Brief", "sehr geehrte|mit freundlichen|anschreiben"),
            "Vertrag": ("Vertrag", "vertrag|vereinbarung|vertragspartner")
        }
        
        if doc_type in patterns:
            name, pattern = patterns[doc_type]
            rule = f"{name}: '{pattern}' -> {name}_Ordner"
            self.rules.append(rule)
            self.rules_listbox.insert(tk.END, rule)
            messagebox.showinfo("Erfolg", f"Regel '{name}' wurde hinzugefügt.")
            
    def analyze_documents(self):
        """Dokumente analysieren"""
        directory = self.document_dir.get()
        if not directory or not os.path.exists(directory):
            messagebox.showerror("Fehler", "Bitte wählen Sie einen gültigen Ordner aus.")
            return
            
        # Dokumente zählen
        doc_count = 0
        doc_types = {}
        
        for file in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file)):
                doc_count += 1
                ext = Path(file).suffix.lower()
                doc_types[ext] = doc_types.get(ext, 0) + 1
                
        result = f"Analyseergebnis:\n\n"
        result += f"Gefundene Dokumente: {doc_count}\n\n"
        result += "Dateitypen:\n"
        for ext, count in doc_types.items():
            result += f"  {ext}: {count}\n"
            
        if self.ocr_enabled.get():
            result += f"\nOCR aktiviert (Sprache: {self.ocr_language.get()})"
            result += "\nHinweis: OCR-Integration in Entwicklung"
            
        messagebox.showinfo("Analyseergebnis", result)
        
    def process_documents(self):
        """Dokumente verarbeiten"""
        directory = self.document_dir.get()
        if not directory or not os.path.exists(directory):
            messagebox.showerror("Fehler", "Bitte wählen Sie einen gültigen Ordner aus.")
            return
            
        if not self.rules:
            messagebox.showwarning("Warnung", "Bitte definieren Sie mindestens eine Regel.")
            return
            
        messagebox.showinfo(
            "Verarbeitung",
            f"Dokumente werden mit {len(self.rules)} Regel(n) verarbeitet.\n\n"
            f"OCR: {'Aktiviert' if self.ocr_enabled.get() else 'Deaktiviert'}\n"
            f"Hinweis: Dies ist eine Demofunktion. OCR-Integration in Entwicklung."
        )
