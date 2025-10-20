import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import pillow_heif
import os

# AVIF desteğini etkinleştir
pillow_heif.register_heif_opener()

class ModernButton(tk.Button):
    def __init__(self, master, **kwargs):
        self.default_bg = kwargs.get('bg', '#4CAF50')
        font = kwargs.pop('font', ("Segoe UI", 10, "bold"))
        
        super().__init__(
            master,
            relief="flat",
            cursor="hand2",
            font=font,
            **kwargs
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def on_enter(self, e):
        self['background'] = self.darken_color(self.default_bg)
        
    def on_leave(self, e):
        self['background'] = self.default_bg
    
    def darken_color(self, hex_color):
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = max(0, r-30), max(0, g-30), max(0, b-30)
        return f'#{r:02x}{g:02x}{b:02x}'

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Görsel Format Dönüştürücü Pro")
        self.root.geometry("750x650")
        self.root.resizable(True, True)
        
        # Modern renkler
        self.bg_color = "#1e1e2e"
        self.card_bg = "#2d2d44"
        self.accent_color = "#6366f1"
        self.success_color = "#10b981"
        self.danger_color = "#ef4444"
        self.warning_color = "#f59e0b"
        self.text_color = "#e0e0e0"
        self.text_dim = "#a0a0a0"
        
        self.root.configure(bg=self.bg_color)
        
        self.selected_files = []
        self.thumbnails = []
        self.output_format = tk.StringVar(value="PNG")
        self.save_location = tk.IntVar(value=1)
        self.quality_var = tk.IntVar(value=90)
        
        self.create_widgets()
        self.setup_drag_drop()
    
    def create_widgets(self):
        # Ana container
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Başlık
        header_frame = tk.Frame(main_container, bg=self.bg_color)
        header_frame.pack(fill="x", pady=(0, 15))
        
        title_label = tk.Label(
            header_frame,
            text="🎨 Görsel Format Dönüştürücü Pro",
            font=("Segoe UI", 22, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title_label.pack()
        
        subtitle = tk.Label(
            header_frame,
            text="Modern, Hızlı ve Kullanıcı Dostu",
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg=self.text_dim
        )
        subtitle.pack()
        
        # Sekmeler (Notebook)
        style = ttk.Style()
        style.theme_use('clam')
        
        # Notebook stili
        style.configure('Modern.TNotebook',
                       background=self.bg_color,
                       borderwidth=0)
        style.configure('Modern.TNotebook.Tab',
                       background=self.card_bg,
                       foreground=self.text_color,
                       padding=[20, 10],
                       font=('Segoe UI', 11, 'bold'),
                       borderwidth=0)
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', self.accent_color)],
                 foreground=[('selected', 'white')])
        
        self.notebook = ttk.Notebook(main_container, style='Modern.TNotebook')
        self.notebook.pack(fill="both", expand=True, pady=(0, 15))
        
        # Tab 1: Ana Sayfa (Dosya Seçimi)
        self.main_tab = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(self.main_tab, text="📁 Dosyalar")
        
        # Tab 2: Ayarlar
        self.settings_tab = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(self.settings_tab, text="⚙️ Ayarlar")
        
        # Ana sekme içeriği
        self.create_main_tab()
        
        # Ayarlar sekmesi içeriği
        self.create_settings_tab()
        
        # Progress bar
        self.progress_frame = tk.Frame(main_container, bg=self.bg_color)
        
        style.configure("Modern.Horizontal.TProgressbar",
                       troughcolor='#1a1a2e',
                       background=self.success_color,
                       borderwidth=0,
                       thickness=20)
        
        self.progress = ttk.Progressbar(
            self.progress_frame,
            mode='determinate',
            style="Modern.Horizontal.TProgressbar"
        )
        self.progress.pack(fill="x")
        
        self.progress_label = tk.Label(
            self.progress_frame,
            text="",
            font=("Segoe UI", 9),
            bg=self.bg_color,
            fg=self.text_dim
        )
        self.progress_label.pack(pady=(5, 0))
        
        # Dönüştür butonu
        convert_btn = ModernButton(
            main_container,
            text="✨ Dönüştürmeyi Başlat",
            command=self.convert_images,
            bg=self.success_color,
            fg="white",
            padx=50,
            pady=15,
            font=("Segoe UI", 13, "bold")
        )
        convert_btn.pack(pady=(0, 10))
    
    def create_main_tab(self):
        """Ana sekme - dosya seçimi ve önizleme"""
        # Dosya seçim kartı
        self.drop_zone = tk.Frame(
            self.main_tab,
            bg=self.card_bg,
            relief="flat",
            bd=2,
            highlightbackground=self.accent_color,
            highlightthickness=2
        )
        self.drop_zone.pack(fill="both", expand=True, padx=10, pady=10)
        
        drop_inner = tk.Frame(self.drop_zone, bg=self.card_bg)
        drop_inner.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Boş durum mesajı
        self.empty_state = tk.Frame(drop_inner, bg=self.card_bg)
        self.empty_state.pack(fill="both", expand=True)
        
        drop_icon = tk.Label(
            self.empty_state,
            text="📁",
            font=("Segoe UI", 56),
            bg=self.card_bg,
            fg=self.accent_color
        )
        drop_icon.pack(pady=(30, 10))
        
        drop_text = tk.Label(
            self.empty_state,
            text="Dosyaları buraya sürükle-bırak",
            font=("Segoe UI", 13, "bold"),
            bg=self.card_bg,
            fg=self.text_color
        )
        drop_text.pack(pady=5)
        
        drop_or = tk.Label(
            self.empty_state,
            text="veya",
            font=("Segoe UI", 10),
            bg=self.card_bg,
            fg=self.text_dim
        )
        drop_or.pack(pady=5)
        
        select_btn = ModernButton(
            self.empty_state,
            text="📂 Dosya Seç",
            command=self.select_files,
            bg=self.accent_color,
            fg="white",
            padx=35,
            pady=12,
            font=("Segoe UI", 11, "bold")
        )
        select_btn.pack(pady=(10, 0))
        
        # Thumbnail görünümü
        self.thumbnail_container = tk.Frame(drop_inner, bg=self.card_bg)
        
        control_frame = tk.Frame(self.thumbnail_container, bg=self.card_bg)
        control_frame.pack(fill="x", pady=(0, 10))
        
        self.file_count_label = tk.Label(
            control_frame,
            text="0 dosya seçildi",
            font=("Segoe UI", 11, "bold"),
            bg=self.card_bg,
            fg=self.accent_color
        )
        self.file_count_label.pack(side="left", padx=5)
        
        button_frame = tk.Frame(control_frame, bg=self.card_bg)
        button_frame.pack(side="right")
        
        add_more_btn = ModernButton(
            button_frame,
            text="➕ Daha Fazla Ekle",
            command=self.select_files,
            bg=self.accent_color,
            fg="white",
            padx=15,
            pady=6,
            font=("Segoe UI", 9, "bold")
        )
        add_more_btn.pack(side="left", padx=(0, 5))
        
        clear_btn = ModernButton(
            button_frame,
            text="🗑️ Temizle",
            command=self.clear_files,
            bg=self.danger_color,
            fg="white",
            padx=15,
            pady=6,
            font=("Segoe UI", 9, "bold")
        )
        clear_btn.pack(side="left")
        
        # Scrollable thumbnail frame
        canvas_frame = tk.Frame(self.thumbnail_container, bg=self.card_bg)
        canvas_frame.pack(fill="both", expand=True)
        
        self.canvas = tk.Canvas(
            canvas_frame,
            bg="#1a1a2e",
            highlightthickness=0,
            bd=0
        )
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg="#1a1a2e")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def create_settings_tab(self):
        """Ayarlar sekmesi"""
        settings_container = tk.Frame(self.settings_tab, bg=self.bg_color)
        settings_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Ayarlar kartı
        settings_card = tk.Frame(settings_container, bg=self.card_bg)
        settings_card.pack(fill="both", expand=True)
        
        card_inner = tk.Frame(settings_card, bg=self.card_bg)
        card_inner.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Format seçimi
        format_frame = tk.Frame(card_inner, bg=self.card_bg)
        format_frame.pack(fill="x", pady=(0, 25))
        
        format_label = tk.Label(
            format_frame,
            text="🎯 Hedef Format:",
            font=("Segoe UI", 13, "bold"),
            bg=self.card_bg,
            fg=self.text_color
        )
        format_label.pack(anchor="w", pady=(0, 10))
        
        formats = ["PNG", "JPG", "JPEG", "WebP", "AVIF", "BMP", "GIF", "TIFF"]
        
        format_menu = ttk.Combobox(
            format_frame,
            textvariable=self.output_format,
            values=formats,
            state="readonly",
            font=("Segoe UI", 12),
            width=25
        )
        format_menu.pack(anchor="w")
        
        # Kalite ayarı
        quality_frame = tk.Frame(card_inner, bg=self.card_bg)
        quality_frame.pack(fill="x", pady=(0, 25))
        
        quality_header = tk.Frame(quality_frame, bg=self.card_bg)
        quality_header.pack(fill="x", pady=(0, 10))
        
        quality_label = tk.Label(
            quality_header,
            text="⭐ Kalite (JPG/WebP/AVIF için):",
            font=("Segoe UI", 13, "bold"),
            bg=self.card_bg,
            fg=self.text_color
        )
        quality_label.pack(side="left")
        
        self.quality_value_label = tk.Label(
            quality_header,
            text=str(self.quality_var.get()),
            font=("Segoe UI", 13, "bold"),
            bg=self.card_bg,
            fg=self.accent_color
        )
        self.quality_value_label.pack(side="right")
        
        quality_scale = ttk.Scale(
            quality_frame,
            from_=1,
            to=100,
            orient="horizontal",
            variable=self.quality_var,
            length=500,
            command=self.update_quality_label
        )
        quality_scale.pack(fill="x")
        
        # Kaydetme seçenekleri
        save_frame = tk.Frame(card_inner, bg=self.card_bg)
        save_frame.pack(fill="x")
        
        save_label = tk.Label(
            save_frame,
            text="💾 Kaydetme Konumu:",
            font=("Segoe UI", 13, "bold"),
            bg=self.card_bg,
            fg=self.text_color
        )
        save_label.pack(anchor="w", pady=(0, 15))
        
        radio_style = {
            'bg': self.card_bg,
            'fg': self.text_color,
            'selectcolor': self.card_bg,
            'activebackground': self.card_bg,
            'activeforeground': self.accent_color,
            'font': ("Segoe UI", 11),
            'highlightthickness': 0
        }
        
        tk.Radiobutton(
            save_frame,
            text="📂 Klasör seç ve oraya kaydet",
            variable=self.save_location,
            value=1,
            **radio_style
        ).pack(anchor="w", pady=5)
        
        tk.Radiobutton(
            save_frame,
            text="📍 Dosyaların bulunduğu konuma kaydet",
            variable=self.save_location,
            value=2,
            **radio_style
        ).pack(anchor="w", pady=5)
        
        tk.Radiobutton(
            save_frame,
            text="📁 Aynı konumda 'converted' klasörü oluştur",
            variable=self.save_location,
            value=3,
            **radio_style
        ).pack(anchor="w", pady=5)
    
    def update_quality_label(self, value):
        """Kalite slider değiştiğinde sayıyı güncelle"""
        self.quality_value_label.config(text=str(int(float(value))))
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def setup_drag_drop(self):
        """Sürükle-bırak özelliğini aktifleştir"""
        self.drop_zone.drop_target_register(DND_FILES)
        self.drop_zone.dnd_bind('<<Drop>>', self.drop_files)
        
        self.drop_zone.bind("<Enter>", lambda e: self.drop_zone.config(highlightbackground=self.success_color))
        self.drop_zone.bind("<Leave>", lambda e: self.drop_zone.config(highlightbackground=self.accent_color))
    
    def drop_files(self, event):
        """Sürüklenen dosyaları işle"""
        files = self.root.tk.splitlist(event.data)
        valid_extensions = ('.png', '.jpg', '.jpeg', '.webp', '.avif', '.bmp', '.gif', '.tiff', '.heic')
        
        for file in files:
            if file.lower().endswith(valid_extensions) and file not in self.selected_files:
                self.selected_files.append(file)
        
        self.update_file_list()
    
    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Görsel Dosyalarını Seç",
            filetypes=[
                ("Tüm Görseller", "*.png *.jpg *.jpeg *.webp *.avif *.bmp *.gif *.tiff *.heic"),
                ("PNG", "*.png"),
                ("JPG", "*.jpg *.jpeg"),
                ("WebP", "*.webp"),
                ("AVIF", "*.avif"),
                ("HEIC", "*.heic"),
                ("BMP", "*.bmp"),
                ("GIF", "*.gif"),
                ("TIFF", "*.tiff"),
                ("Tüm Dosyalar", "*.*")
            ]
        )
        
        if files:
            for file in files:
                if file not in self.selected_files:
                    self.selected_files.append(file)
            self.update_file_list()
    
    def create_thumbnail(self, image_path):
        """Görsel için thumbnail oluştur"""
        try:
            img = Image.open(image_path)
            img.thumbnail((100, 100), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except:
            return None
    
    def update_file_list(self):
        """Dosya listesini thumbnail'lerle güncelle"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.thumbnails.clear()
        
        if len(self.selected_files) > 0:
            self.empty_state.pack_forget()
            self.thumbnail_container.pack(fill="both", expand=True)
            
            row = 0
            col = 0
            max_cols = 5
            
            for idx, file_path in enumerate(self.selected_files):
                card = tk.Frame(
                    self.scrollable_frame,
                    bg=self.card_bg,
                    relief="flat",
                    bd=1,
                    highlightbackground=self.accent_color,
                    highlightthickness=1
                )
                card.grid(row=row, column=col, padx=5, pady=5, sticky="n")
                
                thumb = self.create_thumbnail(file_path)
                if thumb:
                    self.thumbnails.append(thumb)
                    img_label = tk.Label(card, image=thumb, bg=self.card_bg)
                else:
                    img_label = tk.Label(
                        card,
                        text="🖼️",
                        font=("Segoe UI", 40),
                        bg=self.card_bg,
                        fg=self.text_dim
                    )
                
                img_label.pack(padx=5, pady=(5, 0))
                
                filename = os.path.basename(file_path)
                if len(filename) > 15:
                    filename = filename[:12] + "..."
                
                name_label = tk.Label(
                    card,
                    text=filename,
                    font=("Segoe UI", 8),
                    bg=self.card_bg,
                    fg=self.text_color,
                    wraplength=100
                )
                name_label.pack(padx=5, pady=(0, 5))
                
                remove_btn = tk.Button(
                    card,
                    text="×",
                    font=("Arial", 12, "bold"),
                    bg=self.danger_color,
                    fg="white",
                    relief="flat",
                    cursor="hand2",
                    width=2,
                    command=lambda i=idx: self.remove_file(i)
                )
                remove_btn.pack(pady=(0, 5))
                
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1
        else:
            self.thumbnail_container.pack_forget()
            self.empty_state.pack(fill="both", expand=True)
        
        count = len(self.selected_files)
        self.file_count_label.config(text=f"{count} dosya seçildi")
    
    def remove_file(self, index):
        """Belirli bir dosyayı listeden çıkar"""
        if 0 <= index < len(self.selected_files):
            self.selected_files.pop(index)
            self.update_file_list()
    
    def clear_files(self):
        self.selected_files = []
        self.update_file_list()
    
    def get_output_folder(self, first_file_path):
        save_option = self.save_location.get()
        
        if save_option == 1:
            folder = filedialog.askdirectory(title="Çıktı Klasörünü Seç")
            return folder if folder else None
            
        elif save_option == 2:
            return os.path.dirname(first_file_path)
            
        else:
            source_dir = os.path.dirname(first_file_path)
            new_folder = os.path.join(source_dir, "converted_images")
            os.makedirs(new_folder, exist_ok=True)
            return new_folder
    
    def convert_images(self):
        if not self.selected_files:
            messagebox.showwarning("Uyarı", "Lütfen önce görsel dosyası seçin!")
            return
        
        output_folder = self.get_output_folder(self.selected_files[0])
        if not output_folder:
            return
        
        output_format = self.output_format.get().lower()
        quality = self.quality_var.get()
        
        self.progress_frame.pack(fill="x", pady=(0, 15))
        self.progress['maximum'] = len(self.selected_files)
        self.progress['value'] = 0
        
        success_count = 0
        error_count = 0
        error_messages = []
        
        for idx, file_path in enumerate(self.selected_files):
            try:
                self.progress['value'] = idx
                filename = os.path.basename(file_path)
                self.progress_label.config(text=f"İşleniyor: {filename}")
                self.root.update_idletasks()
                
                img = Image.open(file_path)
                
                if output_format in ['jpg', 'jpeg']:
                    if img.mode == 'RGBA':
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[3])
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                
                original_name = os.path.splitext(os.path.basename(file_path))[0]
                output_path = os.path.join(output_folder, f"{original_name}.{output_format}")
                
                counter = 1
                while os.path.exists(output_path):
                    output_path = os.path.join(output_folder, f"{original_name}_{counter}.{output_format}")
                    counter += 1
                
                if output_format in ['jpg', 'jpeg', 'webp', 'avif']:
                    img.save(output_path, quality=quality, optimize=True)
                else:
                    img.save(output_path)
                
                success_count += 1
                
            except Exception as e:
                error_count += 1
                error_msg = f"{os.path.basename(file_path)}: {str(e)}"
                error_messages.append(error_msg)
                print(f"Hata ({file_path}): {str(e)}")
        
        self.progress['value'] = len(self.selected_files)
        self.progress_label.config(text="✅ Tamamlandı!")
        
        if error_count == 0:
            messagebox.showinfo(
                "Başarılı! 🎉",
                f"✅ {success_count} dosya başarıyla dönüştürüldü!\n\n📁 Konum: {output_folder}"
            )
        else:
            error_detail = "\n".join(error_messages[:5])
            if len(error_messages) > 5:
                error_detail += f"\n\n... ve {len(error_messages) - 5} hata daha"
            
            messagebox.showwarning(
                "Tamamlandı",
                f"✅ Başarılı: {success_count}\n❌ Hatalı: {error_count}\n\n{error_detail}"
            )
        
        self.root.after(2000, lambda: self.progress_frame.pack_forget())
        self.clear_files()

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ImageConverterApp(root)
    root.mainloop()