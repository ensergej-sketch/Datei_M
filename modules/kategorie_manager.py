#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kategorie Manager - Modul zum Trainieren und Verwalten von Kategorien
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime


class KategorieManager:
    """Kategorie Manager Modul"""
    
    def __init__(self, window):
        self.window = window
        self.window.title("Kategorie Manager - Begriffe trainieren")
        self.window.geometry("900x700")
        
        self.categories = {}
        self.current_category = None
        
        self.setup_ui()
        self.load_default_categories()
        
    def setup_ui(self):
        """UI-Elemente erstellen"""
        # Header
        header = tk.Label(
            self.window,
            text="🏷️ Kategorie Manager",
            font=("Arial", 18, "bold"),
            bg="#16a085",
            fg="white",
            pady=15
        )
        header.pack(fill=tk.X)
        
        # Hauptcontainer
        main_frame = tk.Frame(self.window, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Oberer Bereich: Kategorien und Begriffe
        top_frame = tk.Frame(main_frame)
        top_frame.pack(fill=tk.BOTH, expand=True)
        
        # Linke Seite: Kategorien
        categories_frame = tk.LabelFrame(top_frame, text="Kategorien", padx=10, pady=10)
        categories_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Kategorien-Listbox
        cat_list_frame = tk.Frame(categories_frame)
        cat_list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.categories_listbox = tk.Listbox(cat_list_frame, height=15)
        cat_scrollbar = tk.Scrollbar(cat_list_frame, command=self.categories_listbox.yview)
        self.categories_listbox.config(yscrollcommand=cat_scrollbar.set)
        self.categories_listbox.bind('<<ListboxSelect>>', self.on_category_select)
        
        self.categories_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Kategorien-Buttons
        cat_buttons = tk.Frame(categories_frame)
        cat_buttons.pack(pady=10)
        
        tk.Button(
            cat_buttons,
            text="Neue Kategorie",
            command=self.add_category,
            bg="#27ae60",
            fg="white",
            padx=10
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            cat_buttons,
            text="Löschen",
            command=self.delete_category,
            bg="#e74c3c",
            fg="white",
            padx=10
        ).pack(side=tk.LEFT, padx=2)
        
        # Rechte Seite: Begriffe
        terms_frame = tk.LabelFrame(top_frame, text="Begriffe", padx=10, pady=10)
        terms_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Begriff hinzufügen
        add_term_frame = tk.Frame(terms_frame)
        add_term_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(add_term_frame, text="Neuer Begriff:").pack(side=tk.LEFT, padx=5)
        self.term_entry = tk.Entry(add_term_frame, width=30)
        self.term_entry.pack(side=tk.LEFT, padx=5)
        self.term_entry.bind('<Return>', lambda e: self.add_term())
        
        tk.Button(
            add_term_frame,
            text="Hinzufügen",
            command=self.add_term,
            bg="#3498db",
            fg="white"
        ).pack(side=tk.LEFT, padx=5)
        
        # Begriffe-Listbox
        terms_list_frame = tk.Frame(terms_frame)
        terms_list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.terms_listbox = tk.Listbox(terms_list_frame, height=12)
        terms_scrollbar = tk.Scrollbar(terms_list_frame, command=self.terms_listbox.yview)
        self.terms_listbox.config(yscrollcommand=terms_scrollbar.set)
        
        self.terms_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        terms_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Begriff entfernen Button
        tk.Button(
            terms_frame,
            text="Begriff entfernen",
            command=self.remove_term,
            bg="#e74c3c",
            fg="white",
            padx=10
        ).pack(pady=5)
        
        # Trainingsbereich
        training_frame = tk.LabelFrame(main_frame, text="Textklassifikation testen", padx=10, pady=10)
        training_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Label(training_frame, text="Text zum Klassifizieren:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        self.classify_text = tk.Text(training_frame, height=5, width=70, font=("Courier", 10))
        self.classify_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        classify_button = tk.Button(
            training_frame,
            text="Text klassifizieren",
            command=self.classify_text_action,
            bg="#9b59b6",
            fg="white",
            padx=20,
            pady=8,
            font=("Arial", 10, "bold")
        )
        classify_button.pack(pady=5)
        
        self.result_label = tk.Label(
            training_frame,
            text="",
            font=("Arial", 11, "bold"),
            fg="#2c3e50"
        )
        self.result_label.pack(pady=5)
        
        # Aktions-Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame,
            text="Kategorien exportieren",
            command=self.export_categories,
            bg="#3498db",
            fg="white",
            padx=15,
            pady=8
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Kategorien importieren",
            command=self.import_categories,
            bg="#3498db",
            fg="white",
            padx=15,
            pady=8
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Statistik anzeigen",
            command=self.show_statistics,
            bg="#f39c12",
            fg="white",
            padx=15,
            pady=8
        ).pack(side=tk.LEFT, padx=5)
        
    def load_default_categories(self):
        """Standardkategorien laden"""
        default_categories = {
            "Rechnung": ["rechnung", "invoice", "betrag", "mwst", "netto", "brutto", "zahlung"],
            "Brief": ["sehr geehrte", "mit freundlichen grüßen", "anschreiben", "betreff"],
            "Vertrag": ["vertrag", "vereinbarung", "vertragspartner", "laufzeit", "kündigung"],
            "Technisch": ["server", "datenbank", "api", "code", "software", "entwicklung"],
            "Finanzen": ["steuer", "umsatz", "gewinn", "bilanz", "konto", "überweisung"]
        }
        
        self.categories = default_categories
        self.refresh_categories_list()
        
    def refresh_categories_list(self):
        """Kategorien-Liste aktualisieren"""
        self.categories_listbox.delete(0, tk.END)
        for category in sorted(self.categories.keys()):
            term_count = len(self.categories[category])
            self.categories_listbox.insert(tk.END, f"{category} ({term_count} Begriffe)")
            
    def refresh_terms_list(self):
        """Begriffe-Liste aktualisieren"""
        self.terms_listbox.delete(0, tk.END)
        if self.current_category and self.current_category in self.categories:
            for term in sorted(self.categories[self.current_category]):
                self.terms_listbox.insert(tk.END, term)
                
    def on_category_select(self, event):
        """Kategorie ausgewählt"""
        selection = self.categories_listbox.curselection()
        if selection:
            category_text = self.categories_listbox.get(selection[0])
            # Extract category name (remove count)
            self.current_category = category_text.split(" (")[0]
            self.refresh_terms_list()
            
    def add_category(self):
        """Neue Kategorie hinzufügen"""
        category_window = tk.Toplevel(self.window)
        category_window.title("Neue Kategorie")
        category_window.geometry("300x150")
        
        tk.Label(category_window, text="Kategoriename:", font=("Arial", 10, "bold")).pack(pady=10)
        category_entry = tk.Entry(category_window, width=30)
        category_entry.pack(pady=5)
        category_entry.focus()
        
        def save_category():
            name = category_entry.get().strip()
            if name:
                if name not in self.categories:
                    self.categories[name] = []
                    self.refresh_categories_list()
                    category_window.destroy()
                    messagebox.showinfo("Erfolg", f"Kategorie '{name}' wurde erstellt.")
                else:
                    messagebox.showwarning("Warnung", "Diese Kategorie existiert bereits.")
            else:
                messagebox.showwarning("Warnung", "Bitte geben Sie einen Namen ein.")
                
        tk.Button(
            category_window,
            text="Erstellen",
            command=save_category,
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=8
        ).pack(pady=20)
        
    def delete_category(self):
        """Kategorie löschen"""
        if not self.current_category:
            messagebox.showwarning("Warnung", "Bitte wählen Sie eine Kategorie aus.")
            return
            
        if messagebox.askyesno("Bestätigung", f"Möchten Sie die Kategorie '{self.current_category}' wirklich löschen?"):
            del self.categories[self.current_category]
            self.current_category = None
            self.refresh_categories_list()
            self.refresh_terms_list()
            
    def add_term(self):
        """Begriff hinzufügen"""
        if not self.current_category:
            messagebox.showwarning("Warnung", "Bitte wählen Sie zuerst eine Kategorie aus.")
            return
            
        term = self.term_entry.get().strip().lower()
        if term:
            if term not in self.categories[self.current_category]:
                self.categories[self.current_category].append(term)
                self.refresh_terms_list()
                self.refresh_categories_list()
                self.term_entry.delete(0, tk.END)
            else:
                messagebox.showinfo("Info", "Dieser Begriff existiert bereits in dieser Kategorie.")
        else:
            messagebox.showwarning("Warnung", "Bitte geben Sie einen Begriff ein.")
            
    def remove_term(self):
        """Begriff entfernen"""
        if not self.current_category:
            messagebox.showwarning("Warnung", "Bitte wählen Sie zuerst eine Kategorie aus.")
            return
            
        selection = self.terms_listbox.curselection()
        if selection:
            term = self.terms_listbox.get(selection[0])
            self.categories[self.current_category].remove(term)
            self.refresh_terms_list()
            self.refresh_categories_list()
            
    def classify_text_action(self):
        """Text klassifizieren"""
        text = self.classify_text.get("1.0", tk.END).strip().lower()
        if not text:
            messagebox.showwarning("Warnung", "Bitte geben Sie einen Text ein.")
            return
            
        # Einfache Klassifikation basierend auf Begriff-Matching
        # Für bessere Performance bei großen Texten könnte Tokenisierung verwendet werden
        scores = {}
        for category, terms in self.categories.items():
            score = sum(1 for term in terms if term in text)
            if score > 0:
                scores[category] = score
                
        if scores:
            # Beste Kategorie finden
            best_category = max(scores, key=scores.get)
            best_score = scores[best_category]
            
            result_text = f"✓ Klassifiziert als: {best_category} (Score: {best_score})\n\n"
            result_text += "Alle Treffer:\n"
            for cat, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
                result_text += f"  {cat}: {score}\n"
                
            self.result_label.config(text=f"Ergebnis: {best_category}", fg="#27ae60")
            messagebox.showinfo("Klassifikationsergebnis", result_text)
        else:
            self.result_label.config(text="Keine Kategorie gefunden", fg="#e74c3c")
            messagebox.showinfo("Klassifikationsergebnis", "✗ Keine passende Kategorie gefunden.")
            
    def export_categories(self):
        """Kategorien exportieren"""
        filename = filedialog.asksaveasfilename(
            title="Kategorien exportieren",
            defaultextension=".json",
            filetypes=[("JSON-Dateien", "*.json"), ("Alle Dateien", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.categories, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("Erfolg", f"Kategorien wurden erfolgreich exportiert nach:\n{filename}")
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Exportieren:\n{str(e)}")
                
    def import_categories(self):
        """Kategorien importieren"""
        filename = filedialog.askopenfilename(
            title="Kategorien importieren",
            filetypes=[("JSON-Dateien", "*.json"), ("Alle Dateien", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    imported = json.load(f)
                    
                if isinstance(imported, dict):
                    self.categories.update(imported)
                    self.refresh_categories_list()
                    self.refresh_terms_list()
                    messagebox.showinfo("Erfolg", f"{len(imported)} Kategorien wurden importiert.")
                else:
                    messagebox.showerror("Fehler", "Ungültiges Dateiformat.")
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Importieren:\n{str(e)}")
                
    def show_statistics(self):
        """Statistik anzeigen"""
        total_categories = len(self.categories)
        total_terms = sum(len(terms) for terms in self.categories.values())
        avg_terms = total_terms / total_categories if total_categories > 0 else 0
        
        stats_text = f"Statistik:\n\n"
        stats_text += f"Anzahl Kategorien: {total_categories}\n"
        stats_text += f"Gesamtzahl Begriffe: {total_terms}\n"
        stats_text += f"Durchschnitt Begriffe/Kategorie: {avg_terms:.1f}\n\n"
        stats_text += "Kategorien nach Begriffanzahl:\n"
        
        sorted_cats = sorted(self.categories.items(), key=lambda x: len(x[1]), reverse=True)
        for cat, terms in sorted_cats:
            stats_text += f"  {cat}: {len(terms)} Begriffe\n"
            
        messagebox.showinfo("Statistik", stats_text)
