import tkinter as tk
from tkinter import ttk, font
import math
import time

class StopwatchApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("⏱️ Stopwatch Pro - Advanced Animation")
        self.window.geometry("800x700")
        
        # Modern color scheme
        self.colors = {
            'bg_main': '#0D1B2A',           # Dark blue background
            'bg_secondary': '#1B263B',      # Secondary dark blue
            'accent_primary': '#415A77',    # Steel blue
            'accent_secondary': '#778DA9',  # Light steel blue
            'text_primary': '#E0E1DD',      # Light gray
            'text_secondary': '#FFFFFF',    # White
            'success': '#06D6A0',           # Turquoise
            'warning': '#FFD60A',           # Yellow
            'danger': '#F72585',            # Pink/Red
            'info': '#4361EE',              # Blue
            'gradient_start': '#0F3460',    # Dark blue
            'gradient_end': '#16537E'       # Medium blue
        }
        
        # Configure window
        self.window.configure(bg=self.colors['bg_main'])
        
        # Custom fonts
        self.setup_fonts()

        # Variabel untuk stopwatch
        self.start_time = 0
        self.elapsed_time = 0
        self.is_running = False
        self.timer_job = None

        # Variabel untuk animasi
        self.animation_job = None
        self.rotation_angle = 0

        self.buat_interface()
        self.start_animation()
        
    def setup_fonts(self):
        """Setup custom fonts untuk aplikasi"""
        try:
            self.fonts = {
                'time_display': font.Font(family="Segoe UI", size=36, weight="bold"),
                'ms_display': font.Font(family="Segoe UI", size=18, weight="normal"),
                'button': font.Font(family="Segoe UI", size=12, weight="bold"),
                'label': font.Font(family="Segoe UI", size=10, weight="bold"),
                'list': font.Font(family="Consolas", size=10)
            }
        except:
            # Fallback fonts jika Segoe UI tidak tersedia
            self.fonts = {
                'time_display': font.Font(family="Arial", size=36, weight="bold"),
                'ms_display': font.Font(family="Arial", size=18, weight="normal"),
                'button': font.Font(family="Arial", size=12, weight="bold"),
                'label': font.Font(family="Arial", size=10, weight="bold"),
                'list': font.Font(family="Courier", size=10)
            }

    def buat_interface(self):
        # Main container dengan gradient effect
        main_container = tk.Frame(self.window, bg=self.colors['bg_main'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header dengan title yang menarik
        header_frame = tk.Frame(main_container, bg=self.colors['bg_main'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(
            header_frame,
            text="⏱️ STOPWATCH PRO",
            font=font.Font(family="Segoe UI", size=24, weight="bold"),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_main']
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Precision Timing with Advanced Animation",
            font=self.fonts['label'],
            fg=self.colors['accent_secondary'],
            bg=self.colors['bg_main']
        )
        subtitle_label.pack(pady=(5, 0))

        # Container untuk display dan animasi
        display_container = tk.Frame(main_container, bg=self.colors['bg_main'])
        display_container.pack(fill='x', pady=20)

        # Frame untuk display waktu dengan styling modern
        time_frame = tk.Frame(display_container, bg=self.colors['bg_secondary'], relief='flat', bd=0)
        time_frame.pack(pady=10)
        
        # Add padding dan styling ke time frame
        time_inner = tk.Frame(time_frame, bg=self.colors['bg_secondary'])
        time_inner.pack(padx=40, pady=25)

        # Label untuk menampilkan waktu dengan styling modern
        self.time_label = tk.Label(
            time_inner,
            text="00:00:00",
            font=self.fonts['time_display'],
            fg=self.colors['success'],
            bg=self.colors['bg_secondary']
        )
        self.time_label.pack()

        # Label untuk milidetik dengan styling yang match
        self.ms_label = tk.Label(
            time_inner,
            text="000",
            font=self.fonts['ms_display'],
            fg=self.colors['warning'],
            bg=self.colors['bg_secondary']
        )
        self.ms_label.pack(pady=(5, 0))

        # Canvas untuk animasi dengan border modern
        canvas_container = tk.Frame(display_container, bg=self.colors['bg_secondary'], relief='flat', bd=0)
        canvas_container.pack(pady=20)
        
        self.canvas = tk.Canvas(
            canvas_container,
            width=320,
            height=320,
            bg=self.colors['bg_secondary'],
            highlightthickness=0
        )
        self.canvas.pack(padx=20, pady=20)

        # Buat desain jam yang lebih modern
        self.buat_desain_jam_modern()

        # Frame untuk tombol kontrol dengan styling modern
        self.buat_tombol_kontrol_modern(main_container)

        # Frame untuk lap times dengan styling modern
        self.buat_lap_section_modern(main_container)

        # Variabel untuk lap times
        self.lap_times = []
        self.lap_count = 0

    def buat_desain_jam_modern(self):
        """Membuat desain jam yang modern dan menarik"""
        center_x, center_y = 160, 160
        radius = 120
        
        # Lingkaran luar dengan gradient effect (simulasi dengan multiple circles)
        for i in range(8):
            self.canvas.create_oval(
                center_x - radius - i, center_y - radius - i,
                center_x + radius + i, center_y + radius + i,
                outline=self.colors['accent_primary'],
                width=1,
                tags="outer_circles"
            )

        # Lingkaran dalam untuk face
        self.canvas.create_oval(
            center_x - radius + 10, center_y - radius + 10,
            center_x + radius - 10, center_y + radius - 10,
            outline=self.colors['text_primary'],
            width=2,
            fill=self.colors['bg_main'],
            tags="watch_face"
        )

        # Buat penanda waktu modern
        self.buat_penanda_waktu_modern()

        # Jarum detik dengan styling modern
        self.jarum_detik = self.canvas.create_line(
            center_x, center_y, center_x, center_y - radius + 30,
            fill=self.colors['danger'],
            width=3,
            capstyle='round',
            tags="second_hand"
        )

        # Titik tengah dengan styling modern
        self.canvas.create_oval(
            center_x - 8, center_y - 8, center_x + 8, center_y + 8,
            fill=self.colors['text_secondary'],
            outline=self.colors['accent_primary'],
            width=2,
            tags="center_point"
        )

        # Add digital indicators around the watch
        self.buat_indikator_digital()

    def buat_penanda_waktu_modern(self):
        """Membuat penanda waktu dengan desain modern"""
        center_x, center_y = 160, 160
        radius = 110
        
        for i in range(60):
            angle = i * 6  # 6 degrees per second mark
            radian = math.radians(angle - 90)  # -90 to start from top
            
            if i % 15 == 0:  # Quarter hour marks
                # Major marks (12, 3, 6, 9)
                inner_radius = radius - 20
                outer_radius = radius - 5
                width = 4
                color = self.colors['text_secondary']
            elif i % 5 == 0:  # Hour marks
                inner_radius = radius - 15
                outer_radius = radius - 5
                width = 2
                color = self.colors['accent_secondary']
            else:  # Minute marks
                inner_radius = radius - 10
                outer_radius = radius - 5
                width = 1
                color = self.colors['accent_primary']
            
            x1 = center_x + inner_radius * math.cos(radian)
            y1 = center_y + inner_radius * math.sin(radian)
            x2 = center_x + outer_radius * math.cos(radian)
            y2 = center_y + outer_radius * math.sin(radian)
            
            self.canvas.create_line(
                x1, y1, x2, y2,
                fill=color,
                width=width,
                capstyle='round',
                tags="time_markers"
            )

    def buat_indikator_digital(self):
        """Menambahkan indikator digital di sekitar jam"""
        center_x, center_y = 160, 160
        positions = [
            (center_x, center_y - 140, "12"),
            (center_x + 120, center_y, "3"),
            (center_x, center_y + 140, "6"),
            (center_x - 120, center_y, "9")
        ]
        
        for x, y, text in positions:
            self.canvas.create_text(
                x, y,
                text=text,
                font=self.fonts['label'],
                fill=self.colors['text_secondary'],
                tags="digital_indicators"
            )

    def buat_tombol_kontrol_modern(self, parent):
        """Membuat tombol kontrol dengan desain modern"""
        control_container = tk.Frame(parent, bg=self.colors['bg_main'])
        control_container.pack(pady=30)
        
        # Frame untuk tombol dengan styling
        button_frame = tk.Frame(control_container, bg=self.colors['bg_secondary'], relief='flat', bd=0)
        button_frame.pack(padx=20, pady=15)
        
        # Style untuk tombol
        button_style = {
            'font': self.fonts['button'],
            'relief': 'flat',
            'bd': 0,
            'padx': 25,
            'pady': 12,
            'cursor': 'hand2'
        }

        # Tombol Start/Stop dengan hover effect
        self.start_stop_btn = tk.Button(
            button_frame,
            text="▶ START",
            bg=self.colors['success'],
            fg=self.colors['text_secondary'],
            command=self.toggle_stopwatch,
            **button_style
        )
        self.start_stop_btn.pack(side=tk.LEFT, padx=10)
        self.add_button_hover_effect(self.start_stop_btn, self.colors['success'])

        # Tombol Reset
        self.reset_btn = tk.Button(
            button_frame,
            text="⟲ RESET",
            bg=self.colors['danger'],
            fg=self.colors['text_secondary'],
            command=self.reset_stopwatch,
            **button_style
        )
        self.reset_btn.pack(side=tk.LEFT, padx=10)
        self.add_button_hover_effect(self.reset_btn, self.colors['danger'])

        # Tombol Lap
        self.lap_btn = tk.Button(
            button_frame,
            text="⏱ LAP",
            bg=self.colors['info'],
            fg=self.colors['text_secondary'],
            command=self.record_lap,
            state=tk.DISABLED,
            **button_style
        )
        self.lap_btn.pack(side=tk.LEFT, padx=10)
        self.add_button_hover_effect(self.lap_btn, self.colors['info'])

    def add_button_hover_effect(self, button, original_color):
        """Menambahkan hover effect pada tombol"""
        def on_enter(e):
            if button['state'] != 'disabled':
                button.configure(bg=self.lighten_color(original_color))
        
        def on_leave(e):
            if button['state'] != 'disabled':
                button.configure(bg=original_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def lighten_color(self, color):
        """Membuat warna lebih terang untuk hover effect"""
        if color == self.colors['success']:
            return '#07EDB7'
        elif color == self.colors['danger']:
            return '#FF4DA6'
        elif color == self.colors['info']:
            return '#5A7BFF'
        return color

    def buat_lap_section_modern(self, parent):
        """Membuat section lap times dengan desain modern"""
        lap_container = tk.Frame(parent, bg=self.colors['bg_main'])
        lap_container.pack(fill='both', expand=True, pady=20)
        
        # Header untuk lap section
        lap_header = tk.Frame(lap_container, bg=self.colors['bg_secondary'], relief='flat', bd=0)
        lap_header.pack(fill='x', pady=(0, 10))
        
        lap_title = tk.Label(
            lap_header,
            text="📊 LAP TIMES",
            font=self.fonts['button'],
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_secondary'],
            pady=10
        )
        lap_title.pack()

        # Frame untuk listbox dengan scrollbar
        list_frame = tk.Frame(lap_container, bg=self.colors['bg_secondary'])
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Scrollbar dengan styling modern
        scrollbar = tk.Scrollbar(list_frame, bg=self.colors['accent_primary'])
        scrollbar.pack(side='right', fill='y', padx=(0, 5), pady=5)

        # Listbox untuk menampilkan lap times dengan styling modern
        self.lap_listbox = tk.Listbox(
            list_frame,
            font=self.fonts['list'],
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary'],
            selectbackground=self.colors['accent_primary'],
            selectforeground=self.colors['text_secondary'],
            yscrollcommand=scrollbar.set,
            relief='flat',
            bd=0,
            highlightthickness=0
        )
        self.lap_listbox.pack(side='left', fill='both', expand=True, padx=(5, 0), pady=5)
        scrollbar.config(command=self.lap_listbox.yview)
    
    def buat_penanda_waktu(self):
        """Membuat penanda waktu di sekeliling lingkaran"""
        center_x, center_y = 150, 150
        radius = 90

        for i in range(60):
            angle = math.radians(i * 6 - 90)  # -90 untuk mulai dari atas

            if i % 5 == 0:  # Penanda jam (setiap 5 detik)
                inner_radius = radius - 15
                width = 3
                color = "white"
            else:  # Penanda detik
                inner_radius = radius - 8
                width = 1
                color = "gray"

            # Titik luar
            x1 = center_x + radius * math.cos(angle)
            y1 = center_y + radius * math.sin(angle)

            # Titik dalam
            x2 = center_x + inner_radius * math.cos(angle)
            y2 = center_y + inner_radius * math.sin(angle)

            self.canvas.create_line(
                x1, y1, x2, y2,
                fill=color,
                width=width
            )
    
    def toggle_stopwatch(self):
        """Toggle start/stop stopwatch"""
        if not self.is_running:
            self.start_stopwatch()
        else:
            self.stop_stopwatch()

    def start_stopwatch(self):
        """Mulai stopwatch"""
        self.is_running = True
        self.start_time = time.time() - self.elapsed_time

        # Update tampilan tombol dengan styling modern
        self.start_stop_btn.config(
            text="⏸ PAUSE", 
            bg=self.colors['warning']
        )
        self.lap_btn.config(
            state=tk.NORMAL,
            bg=self.colors['info']
        )

        # Mulai timer
        self.update_time()

    def stop_stopwatch(self):
        """Stop stopwatch"""
        self.is_running = False

        # Update tampilan tombol dengan styling modern
        self.start_stop_btn.config(
            text="▶ START", 
            bg=self.colors['success']
        )
        self.lap_btn.config(
            state=tk.DISABLED,
            bg=self.colors['accent_primary']
        )

        # Hentikan timer
        if self.timer_job:
            self.window.after_cancel(self.timer_job)

    def reset_stopwatch(self):
        """Reset stopwatch"""
        self.stop_stopwatch()
        self.elapsed_time = 0

        # Reset tampilan dengan styling
        self.time_label.config(text="00:00:00", fg=self.colors['success'])
        self.ms_label.config(text="000", fg=self.colors['warning'])

        # Reset tombol ke state awal
        self.start_stop_btn.config(
            text="▶ START",
            bg=self.colors['success']
        )
        self.lap_btn.config(
            state=tk.DISABLED,
            bg=self.colors['accent_primary']
        )

        # Reset lap times
        self.lap_times.clear()
        self.lap_count = 0
        self.lap_listbox.delete(0, tk.END)

        # Reset jarum detik
        self.update_second_hand(0)

    def record_lap(self):
        """Catat lap time"""
        if self.is_running:
            self.lap_count += 1
            current_time = self.elapsed_time

            # Hitung lap time (selisih dengan lap sebelumnya)
            if self.lap_times:
                lap_time = current_time - self.lap_times[-1][1]
            else:
                lap_time = current_time

            # Simpan lap time
            self.lap_times.append((self.lap_count, current_time, lap_time))

            # Format dan tampilkan
            total_formatted = self.format_time(current_time)
            lap_formatted = self.format_time(lap_time)

            lap_text = f"Lap {self.lap_count:2d}: {lap_formatted} (Total: {total_formatted})"
            self.lap_listbox.insert(tk.END, lap_text)

            # Scroll ke bawah
            self.lap_listbox.see(tk.END)

    def update_time(self):
        """Update tampilan waktu"""
        if self.is_running:
            current_time = time.time()
            self.elapsed_time = current_time - self.start_time

            # Update tampilan waktu
            time_str = self.format_time(self.elapsed_time)
            self.time_label.config(text=time_str)

            # Update milidetik
            ms = int((self.elapsed_time % 1) * 1000)
            self.ms_label.config(text=f"{ms:03d}")

            # Update jarum detik
            seconds = self.elapsed_time % 60
            self.update_second_hand(seconds)

            # Schedule next update
            self.timer_job = self.window.after(10, self.update_time)

    def format_time(self, seconds):
        """Format waktu ke string HH:MM:SS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def update_second_hand(self, seconds):
        """Update posisi jarum detik"""
        # Hitung sudut (0 detik = atas, 15 detik = kanan, dst)
        angle = math.radians(seconds * 6 - 90)  # -90 untuk mulai dari atas

        center_x, center_y = 150, 150
        length = 70

        end_x = center_x + length * math.cos(angle)
        end_y = center_y + length * math.sin(angle)

        # Update koordinat jarum
        self.canvas.coords(
            self.jarum_detik,
            center_x, center_y,
            end_x, end_y
        )

    def start_animation(self):
        """Mulai animasi latar belakang"""
        self.animate_background()

    def animate_background(self):
        """Animasi latar belakang (opsional)"""
        # Rotasi sudut untuk efek visual
        self.rotation_angle = (self.rotation_angle + 1) % 360

        # Update warna border berdasarkan status
        if self.is_running:
            color = f"#{int(127 + 127 * math.sin(math.radians(self.rotation_angle * 4))):02x}0000"
        else:
            color = "white"

        self.canvas.itemconfig("outer_circle", outline=color)

        # Schedule next animation frame
        self.animation_job = self.window.after(50, self.animate_background)

    def jalankan(self):
        """Method untuk menjalankan aplikasi"""
        self.window.mainloop()

# Untuk menjalankan aplikasi
if __name__ == "__main__":
    app = StopwatchApp()
    app.jalankan()