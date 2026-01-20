#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dateien Manager - Modul zum automatischen Aufräumen und Organisieren von Ordnern
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
from datetime import datetime
from pathlib import Path


class DateienManager:
    """Dateien Manager Modul"""
    
    def __init__(self, window):
        self.window = window
        self.window.title("Dateien Manager - Ordner automatisch aufräumen")
        self.window.geometry("900x600")
        
        self.source_dir = tk.StringVar()
        self.target_dir = tk.StringVar()
        
        self.setup_ui()
        
    def setup_ui(self):
        """UI-Elemente erstellen"""
        # Header
        header = tk.Label(
            self.window,
            text="📁 Dateien Manager",
            font=("Arial", 18, "bold"),
            bg="#3498db",
            fg="white",
            pady=15
        )
        header.pack(fill=tk.X)
        
        # Hauptcontainer
        main_frame = tk.Frame(self.window, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Quellordner
        source_frame = tk.LabelFrame(main_frame, text="Quellordner auswählen", padx=10, pady=10)
        source_frame.pack(fill=tk.X, pady=10)
        
        tk.Entry(source_frame, textvariable=self.source_dir, width=60).pack(side=tk.LEFT, padx=5)
        tk.Button(
            source_frame,
            text="Durchsuchen...",
            command=self.browse_source,
            bg="#95a5a6",
            fg="white"
        ).pack(side=tk.LEFT)
        
        # Zielordner
        target_frame = tk.LabelFrame(main_frame, text="Zielordner (optional)", padx=10, pady=10)
        target_frame.pack(fill=tk.X, pady=10)
        
        tk.Entry(target_frame, textvariable=self.target_dir, width=60).pack(side=tk.LEFT, padx=5)
        tk.Button(
            target_frame,
            text="Durchsuchen...",
            command=self.browse_target,
            bg="#95a5a6",
            fg="white"
        ).pack(side=tk.LEFT)
        
        # Optionen
        options_frame = tk.LabelFrame(main_frame, text="Sortieroptionen", padx=10, pady=10)
        options_frame.pack(fill=tk.X, pady=10)
        
        self.sort_by_type = tk.BooleanVar(value=True)
        self.sort_by_date = tk.BooleanVar(value=False)
        self.remove_duplicates = tk.BooleanVar(value=False)
        
        tk.Checkbutton(
            options_frame,
            text="Nach Dateityp sortieren",
            variable=self.sort_by_type
        ).pack(anchor=tk.W)
        
        tk.Checkbutton(
            options_frame,
            text="Nach Datum sortieren",
            variable=self.sort_by_date
        ).pack(anchor=tk.W)
        
        tk.Checkbutton(
            options_frame,
            text="Duplikate entfernen",
            variable=self.remove_duplicates
        ).pack(anchor=tk.W)
        
        # Aktions-Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        tk.Button(
            button_frame,
            text="Vorschau anzeigen",
            command=self.show_preview,
            bg="#f39c12",
            fg="white",
            padx=20,
            pady=10,
            font=("Arial", 11, "bold")
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Aufräumen starten",
            command=self.start_organizing,
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=10,
            font=("Arial", 11, "bold")
        ).pack(side=tk.LEFT, padx=5)
        
        # Statusbereich
        status_frame = tk.LabelFrame(main_frame, text="Status", padx=10, pady=10)
        status_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.status_text = tk.Text(status_frame, height=10, width=70, state=tk.DISABLED)
        scrollbar = tk.Scrollbar(status_frame, command=self.status_text.yview)
        self.status_text.config(yscrollcommand=scrollbar.set)
        
        self.status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def browse_source(self):
        """Quellordner auswählen"""
        directory = filedialog.askdirectory(title="Quellordner auswählen")
        if directory:
            self.source_dir.set(directory)
            
    def browse_target(self):
        """Zielordner auswählen"""
        directory = filedialog.askdirectory(title="Zielordner auswählen")
        if directory:
            self.target_dir.set(directory)
            
    def log_status(self, message):
        """Statusnachricht ausgeben"""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        self.window.update()
        
    def show_preview(self):
        """Vorschau der Änderungen anzeigen"""
        source = self.source_dir.get()
        if not source or not os.path.exists(source):
            messagebox.showerror("Fehler", "Bitte wählen Sie einen gültigen Quellordner aus.")
            return
            
        self.log_status("Analysiere Ordner...")
        
        file_count = 0
        type_dict = {}
        
        for root, dirs, files in os.walk(source):
            for file in files:
                file_count += 1
                ext = Path(file).suffix.lower() or '.ohne_erweiterung'
                type_dict[ext] = type_dict.get(ext, 0) + 1
                
        self.log_status(f"Gefunden: {file_count} Dateien")
        self.log_status("Verteilung nach Dateityp:")
        for ext, count in sorted(type_dict.items(), key=lambda x: x[1], reverse=True):
            self.log_status(f"  {ext}: {count} Dateien")
            
    def start_organizing(self):
        """Aufräumen starten"""
        source = self.source_dir.get()
        target = self.target_dir.get() or source
        
        if not source or not os.path.exists(source):
            messagebox.showerror("Fehler", "Bitte wählen Sie einen gültigen Quellordner aus.")
            return
            
        if not messagebox.askyesno(
            "Bestätigung",
            f"Möchten Sie die Dateien in '{source}' organisieren?\nZielordner: {target}"
        ):
            return
            
        self.log_status("Starte Organisierung...")
        organized_count = 0
        
        try:
            if self.sort_by_type.get():
                self.log_status("Sortiere nach Dateityp...")
                
                for root, dirs, files in os.walk(source):
                    # Nur Dateien im Hauptverzeichnis verarbeiten
                    if root == source:
                        for file in files:
                            file_path = os.path.join(root, file)
                            ext = Path(file).suffix.lower()
                            
                            if not ext:
                                ext = "ohne_erweiterung"
                            else:
                                ext = ext[1:]  # Punkt entfernen
                                
                            # Zielordner erstellen
                            dest_dir = os.path.join(target, ext.upper())
                            os.makedirs(dest_dir, exist_ok=True)
                            
                            # Datei verschieben (nur wenn noch nicht am Zielort)
                            dest_path = os.path.join(dest_dir, file)
                            if source != target or os.path.basename(file_path) != file or not os.path.exists(dest_path):
                                shutil.move(file_path, dest_path)
                                organized_count += 1
                                
            self.log_status(f"Erfolgreich! {organized_count} Dateien organisiert.")
            messagebox.showinfo("Erfolg", f"{organized_count} Dateien wurden erfolgreich organisiert!")
            
        except Exception as e:
            self.log_status(f"Fehler: {str(e)}")
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {str(e)}")
