#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Datei_M - Desktop-Tool zum Sortieren, Analysieren und Organisieren von Dateien
Haupteinstiegspunkt der Anwendung
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Module importieren
from modules.dateien_manager import DateienManager
from modules.dokumente_manager import DokumenteManager
from modules.regex_editor import RegexEditor
from modules.kategorie_manager import KategorieManager


class DateiMApp:
    """Hauptanwendung Datei_M"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Datei_M - Dateien und Dokumenten Manager")
        self.root.geometry("1000x700")
        
        # Stil konfigurieren
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.setup_ui()
        
    def setup_ui(self):
        """UI-Elemente erstellen"""
        # Header
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="Datei_M",
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Desktop-Tool zum Sortieren, Analysieren und Organisieren von Dateien und Dokumenten",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        subtitle_label.pack()
        
        # Hauptcontainer
        main_container = tk.Frame(self.root, bg="#ecf0f1")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Info-Text
        info_frame = tk.Frame(main_container, bg="#ecf0f1")
        info_frame.pack(pady=10)
        
        info_label = tk.Label(
            info_frame,
            text="Wählen Sie ein Modul aus:",
            font=("Arial", 12, "bold"),
            bg="#ecf0f1"
        )
        info_label.pack()
        
        # Button-Container
        button_frame = tk.Frame(main_container, bg="#ecf0f1")
        button_frame.pack(pady=20)
        
        # Modul-Buttons erstellen
        self.create_module_button(
            button_frame,
            "📁 Dateien Manager",
            "Ordner automatisch aufräumen und organisieren",
            self.open_dateien_manager,
            row=0, col=0
        )
        
        self.create_module_button(
            button_frame,
            "📄 Dokumente Manager",
            "Dokumente mit Regeln und OCR verwalten",
            self.open_dokumente_manager,
            row=0, col=1
        )
        
        self.create_module_button(
            button_frame,
            "🔍 Regex Editor",
            "Suchmuster erstellen und testen",
            self.open_regex_editor,
            row=1, col=0
        )
        
        self.create_module_button(
            button_frame,
            "🏷️ Kategorie Manager",
            "Begriffe trainieren und klassifizieren",
            self.open_kategorie_manager,
            row=1, col=1
        )
        
        # Footer
        footer_frame = tk.Frame(self.root, bg="#34495e", height=40)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        
        footer_label = tk.Label(
            footer_frame,
            text="Datei_M v1.0 | © 2026 ensergej-sketch",
            font=("Arial", 9),
            bg="#34495e",
            fg="white"
        )
        footer_label.pack(pady=10)
        
    def create_module_button(self, parent, title, description, command, row, col):
        """Erstellt einen Modul-Button"""
        button_container = tk.Frame(parent, bg="white", relief=tk.RAISED, borderwidth=2)
        button_container.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        
        # Button
        btn = tk.Button(
            button_container,
            text=title,
            font=("Arial", 14, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            command=command,
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=15
        )
        btn.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Beschreibung
        desc_label = tk.Label(
            button_container,
            text=description,
            font=("Arial", 9),
            bg="white",
            fg="#7f8c8d",
            wraplength=200
        )
        desc_label.pack(pady=(0, 10))
        
        # Grid-Konfiguration
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
    def open_dateien_manager(self):
        """Öffnet das Dateien Manager Modul"""
        window = tk.Toplevel(self.root)
        DateienManager(window)
        
    def open_dokumente_manager(self):
        """Öffnet das Dokumente Manager Modul"""
        window = tk.Toplevel(self.root)
        DokumenteManager(window)
        
    def open_regex_editor(self):
        """Öffnet den Regex Editor"""
        window = tk.Toplevel(self.root)
        RegexEditor(window)
        
    def open_kategorie_manager(self):
        """Öffnet den Kategorie Manager"""
        window = tk.Toplevel(self.root)
        KategorieManager(window)


def main():
    """Hauptfunktion"""
    root = tk.Tk()
    app = DateiMApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
