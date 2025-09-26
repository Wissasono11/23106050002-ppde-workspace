import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

class DataVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Visualizer - Aplikasi Visualisasi Data")
        self.root.geometry("1000x700")
        self.root.configure(bg="white")

        self.setup_ui()
        self.setup_controls()
        self.setup_plot()

    def setup_ui(self):
        # Frame utama
        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame untuk kontrol (kiri)
        self.control_frame = tk.Frame(main_frame, bg="lightblue", width=250)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        self.control_frame.pack_propagate(False)  # Maintain fixed width

        # Frame untuk plot (kanan)
        self.plot_frame = tk.Frame(main_frame, bg="white")
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Judul di control frame
        title_label = tk.Label(
            self.control_frame, 
            text="KONTROL VISUALISASI", 
            font=("Arial", 14, "bold"),
            bg="lightblue"
        )
        title_label.pack(pady=20)

    def setup_plot(self):
        # Membuat Figure matplotlib
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)

        # Embed plot ke dalam Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Toolbar navigasi
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame)
        self.toolbar.update()

        # Plot awal
        self.update_plot()
    
    def setup_controls(self):
        # Variabel kontrol
        self.frequency = tk.DoubleVar(value=1.0)
        self.amplitude = tk.DoubleVar(value=1.0)
        self.phase = tk.DoubleVar(value=0.0)

        # Kontrol frekuensi
        freq_label = tk.Label(
            self.control_frame, 
            text="Frekuensi:", 
            font=("Arial", 12, "bold"),
            bg="lightblue"
        )
        freq_label.pack(pady=(20, 5))

        freq_scale = tk.Scale(
            self.control_frame,
            from_=0.1,
            to=5.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.frequency,
            command=self.on_parameter_change,
            length=200,
            bg="lightblue"
        )
        freq_scale.pack(pady=5)

        # Label untuk menampilkan nilai
        self.freq_value_label = tk.Label(
            self.control_frame,
            text=f"Nilai: {self.frequency.get()}",
            font=("Arial", 10),
            bg="lightblue"
        )
        self.freq_value_label.pack()

        # Kontrol amplitudo
        amp_label = tk.Label(
            self.control_frame, 
            text="Amplitudo:", 
            font=("Arial", 12, "bold"),
            bg="lightblue"
        )
        amp_label.pack(pady=(20, 5))

        amp_scale = tk.Scale(
            self.control_frame,
            from_=0.1,
            to=3.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.amplitude,
            command=self.on_parameter_change,
            length=200,
            bg="lightblue"
        )
        amp_scale.pack(pady=5)

        self.amp_value_label = tk.Label(
            self.control_frame,
            text=f"Nilai: {self.amplitude.get()}",
            font=("Arial", 10),
            bg="lightblue"
        )
        self.amp_value_label.pack()

        # Kontrol phase
        phase_label = tk.Label(
            self.control_frame, 
            text="Phase:", 
            font=("Arial", 12, "bold"),
            bg="lightblue"
        )
        phase_label.pack(pady=(20, 5))

        phase_scale = tk.Scale(
            self.control_frame,
            from_=0.0,
            to=6.28,  # 2π
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.phase,
            command=self.on_parameter_change,
            length=200,
            bg="lightblue"
        )
        phase_scale.pack(pady=5)

        self.phase_value_label = tk.Label(
            self.control_frame,
            text=f"Nilai: {self.phase.get()}",
            font=("Arial", 10),
            bg="lightblue"
        )
        self.phase_value_label.pack()

        # Pemilihan jenis fungsi
        func_label = tk.Label(
            self.control_frame, 
            text="Jenis Fungsi:", 
            font=("Arial", 12, "bold"),
            bg="lightblue"
        )
        func_label.pack(pady=(30, 5))

        self.function_type = tk.StringVar(value="sin")
        function_combo = ttk.Combobox(
            self.control_frame,
            textvariable=self.function_type,
            values=["sin", "cos", "tan", "exp", "log"],
            state="readonly",
            width=18
        )
        function_combo.pack(pady=5)
        function_combo.bind("<<ComboboxSelected>>", self.on_function_change)

        # Pemilihan warna
        color_label = tk.Label(
            self.control_frame, 
            text="Warna Garis:", 
            font=("Arial", 12, "bold"),
            bg="lightblue"
        )
        color_label.pack(pady=(20, 5))

        self.line_color = tk.StringVar(value="blue")
        color_combo = ttk.Combobox(
            self.control_frame,
            textvariable=self.line_color,
            values=["blue", "red", "green", "orange", "purple", "brown", "pink"],
            state="readonly",
            width=18
        )
        color_combo.pack(pady=5)
        color_combo.bind("<<ComboboxSelected>>", self.on_style_change)

        # Pemilihan line style
        style_label = tk.Label(
            self.control_frame, 
            text="Style Garis:", 
            font=("Arial", 12, "bold"),
            bg="lightblue"
        )
        style_label.pack(pady=(15, 5))

        self.line_style = tk.StringVar(value="-")
        style_combo = ttk.Combobox(
            self.control_frame,
            textvariable=self.line_style,
            values=["-", "--", "-.", ":", "solid", "dashed", "dashdot", "dotted"],
            state="readonly",
            width=18
        )
        style_combo.pack(pady=5)
        style_combo.bind("<<ComboboxSelected>>", self.on_style_change)

        # Line width
        width_label = tk.Label(
            self.control_frame, 
            text="Ketebalan Garis:", 
            font=("Arial", 12, "bold"),
            bg="lightblue"
        )
        width_label.pack(pady=(15, 5))

        self.line_width = tk.DoubleVar(value=2.0)
        width_scale = tk.Scale(
            self.control_frame,
            from_=0.5,
            to=5.0,
            resolution=0.5,
            orient=tk.HORIZONTAL,
            variable=self.line_width,
            command=self.on_style_change,
            length=200,
            bg="lightblue"
        )
        width_scale.pack(pady=5)

    def on_style_change(self, value=None):
        self.update_plot()


    def on_function_change(self, event=None):
        self.update_plot()

    def on_parameter_change(self, value=None):
        # Update semua label nilai
        self.freq_value_label.config(text=f"Nilai: {self.frequency.get()}")
        self.amp_value_label.config(text=f"Nilai: {self.amplitude.get()}")
        self.phase_value_label.config(text=f"Nilai: {round(self.phase.get(), 2)}")
        # Update plot
        self.update_plot()
    
    def update_plot(self):
        # Clear plot sebelumnya
        self.ax.clear()

        # Parameter
        x = np.linspace(0, 10, 100)
        freq = self.frequency.get()
        amp = self.amplitude.get()
        phase = self.phase.get()
        func_type = self.function_type.get()
        color = self.line_color.get()
        style = self.line_style.get()
        width = self.line_width.get()

        # Hitung y berdasarkan jenis fungsi (sama seperti sebelumnya)
        try:
            if func_type == "sin":
                y = amp * np.sin(freq * x + phase)
                title = f"y = {amp} × sin({freq}x + {round(phase, 2)})"
            elif func_type == "cos":
                y = amp * np.cos(freq * x + phase)
                title = f"y = {amp} × cos({freq}x + {round(phase, 2)})"
            elif func_type == "tan":
                y = amp * np.tan(freq * x + phase)
                y = np.clip(y, -10, 10)
                title = f"y = {amp} × tan({freq}x + {round(phase, 2)})"
            elif func_type == "exp":
                y = amp * np.exp(freq * (x - 5) + phase)
                y = np.clip(y, 0, 100)
                title = f"y = {amp} × exp({freq}(x-5) + {round(phase, 2)})"
            elif func_type == "log":
                y = amp * np.log(freq * x + 1) + phase
                title = f"y = {amp} × log({freq}x + 1) + {round(phase, 2)}"
        except:
            y = amp * np.sin(freq * x + phase)
            title = f"y = {amp} × sin({freq}x + {round(phase, 2)})"

        # Plot dengan style yang dipilih
        self.ax.plot(x, y, linestyle=style, color=color, linewidth=width)
        self.ax.set_title(title, fontsize=14)
        self.ax.set_xlabel("X", fontsize=12)
        self.ax.set_ylabel("Y", fontsize=12)
        self.ax.grid(True, alpha=0.3)

        # Refresh canvas
        self.canvas.draw()

# Membuat dan menjalankan aplikasi
if __name__ == "__main__":
    root = tk.Tk()
    app = DataVisualizer(root)
    root.mainloop()