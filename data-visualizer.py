import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import pandas as pd
from tkinter import filedialog
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import threading
import time

class DataVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Visualizer - Aplikasi Visualisasi Data")
        self.root.geometry("1000x700")
        self.root.configure(bg="white")

        self.setup_ui()
        self.setup_controls()
        self.setup_plot()
        self.setup_data_controls()

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
    
    def setup_data_controls(self):
        # Separator
        separator = tk.Frame(self.control_frame, height=2, bg="darkblue")
        separator.pack(fill=tk.X, pady=20)

        # Label untuk data section
        data_label = tk.Label(
            self.control_frame, 
            text="VISUALISASI DATA", 
            font=("Arial", 14, "bold"),
            bg="lightblue"
        )
        data_label.pack(pady=10)

        # Button untuk load data
        load_btn = tk.Button(
            self.control_frame,
            text="Load Data CSV",
            font=("Arial", 11, "bold"),
            command=self.load_data,
            bg="orange",
            fg="white",
            width=20
        )
        load_btn.pack(pady=5)

        # Button untuk generate sample data
        sample_btn = tk.Button(
            self.control_frame,
            text="Generate Sample Data",
            font=("Arial", 11),
            command=self.generate_sample_data,
            bg="green",
            fg="white",
            width=20
        )
        sample_btn.pack(pady=5)

        # Info label untuk status data
        self.data_info_label = tk.Label(
            self.control_frame,
            text="Belum ada data dimuat",
            font=("Arial", 9),
            bg="lightblue",
            wraplength=200
        )
        self.data_info_label.pack(pady=10)

        # Variabel untuk menyimpan data
        self.current_data = None

         # Pemilihan jenis plot untuk data
        plot_type_label = tk.Label(
            self.control_frame, 
            text="Jenis Plot:", 
            font=("Arial", 12, "bold"),
            bg="lightblue"
        )
        plot_type_label.pack(pady=(15, 5))

        self.plot_type = tk.StringVar(value="line")
        plot_type_combo = ttk.Combobox(
            self.control_frame,
            textvariable=self.plot_type,
            values=["line", "scatter", "bar", "histogram", "box"],
            state="readonly",
            width=18
        )
        plot_type_combo.pack(pady=5)
        plot_type_combo.bind("<<ComboboxSelected>>", self.on_plot_type_change)

        # Checkbox untuk multiple subplot
        self.use_subplot = tk.BooleanVar(value=False)
        subplot_check = tk.Checkbutton(
            self.control_frame,
            text="Gunakan Multiple Subplot",
            variable=self.use_subplot,
            command=self.toggle_subplot,
            font=("Arial", 10),
            bg="lightblue"
        )
        subplot_check.pack(pady=10)

        # Real-time data simulation
        realtime_label = tk.Label(
            self.control_frame, 
            text="Real-time Simulation:", 
            font=("Arial", 12, "bold"),
            bg="lightblue"
        )
        realtime_label.pack(pady=(20, 5))

        self.realtime_active = tk.BooleanVar(value=False)
        self.realtime_btn = tk.Button(
            self.control_frame,
            text="Start Real-time",
            font=("Arial", 11),
            command=self.toggle_realtime,
            bg="red",
            fg="white",
            width=20
        )
        self.realtime_btn.pack(pady=5)

        # Kecepatan update
        speed_label = tk.Label(
            self.control_frame, 
            text="Update Speed (ms):", 
            font=("Arial", 10),
            bg="lightblue"
        )
        speed_label.pack(pady=(10, 2))

        self.update_speed = tk.IntVar(value=500)
        speed_scale = tk.Scale(
            self.control_frame,
            from_=100,
            to=2000,
            resolution=100,
            orient=tk.HORIZONTAL,
            variable=self.update_speed,
            length=180,
            bg="lightblue"
        )
        speed_scale.pack(pady=5)

        # Initialize real-time data
        self.realtime_data = []
        self.max_points = 50

    def toggle_realtime(self):
        if not self.realtime_active.get():
            # Start real-time
            self.realtime_active.set(True)
            self.realtime_btn.config(text="Stop Real-time", bg="green")
            self.start_realtime_thread()
        else:
            # Stop real-time
            self.realtime_active.set(False)
            self.realtime_btn.config(text="Start Real-time", bg="red")

    def start_realtime_thread(self):
        def update_loop():
            while self.realtime_active.get():
                # Generate new data point
                timestamp = len(self.realtime_data)
                value1 = 50 + 20 * np.sin(timestamp * 0.1) + np.random.normal(0, 5)
                value2 = 30 + 15 * np.cos(timestamp * 0.15) + np.random.normal(0, 3)
                value3 = 40 + 10 * np.sin(timestamp * 0.08) + np.random.normal(0, 4)

                self.realtime_data.append({
                    'timestamp': timestamp,
                    'sensor1': value1,
                    'sensor2': value2,
                    'sensor3': value3
                })

                # Keep only last max_points
                if len(self.realtime_data) > self.max_points:
                    self.realtime_data.pop(0)

                # Update plot in main thread
                self.root.after(0, self.update_realtime_plot)

                # Sleep based on update speed
                time.sleep(self.update_speed.get() / 1000.0)

        # Start thread
        thread = threading.Thread(target=update_loop, daemon=True)
        thread.start()

    def update_realtime_plot(self):
        if not self.realtime_data:
            return

        # Convert to arrays for plotting
        timestamps = [d['timestamp'] for d in self.realtime_data]
        sensor1 = [d['sensor1'] for d in self.realtime_data]
        sensor2 = [d['sensor2'] for d in self.realtime_data]
        sensor3 = [d['sensor3'] for d in self.realtime_data]

        # Clear and plot
        if hasattr(self, 'ax'):
            self.ax.clear()
            self.ax.plot(timestamps, sensor1, 'b-', label='Sensor 1', linewidth=2)
            self.ax.plot(timestamps, sensor2, 'r-', label='Sensor 2', linewidth=2)
            self.ax.plot(timestamps, sensor3, 'g-', label='Sensor 3', linewidth=2)

            self.ax.set_title('Real-time Sensor Data')
            self.ax.set_xlabel('Time')
            self.ax.set_ylabel('Value')
            self.ax.legend()
            self.ax.grid(True, alpha=0.3)

            # Set axis limits for smooth scrolling effect
            if len(timestamps) > 10:
                self.ax.set_xlim(timestamps[-self.max_points], timestamps[-1])

            self.canvas.draw()

    def toggle_subplot(self):
        if self.current_data is not None:
            self.setup_subplot() if self.use_subplot.get() else self.setup_single_plot()
        else:
            messagebox.showwarning("Peringatan", "Muat data terlebih dahulu!")
            self.use_subplot.set(False)

    def setup_single_plot(self):
        # Reset ke single plot
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.plot_data_advanced()

    def setup_subplot(self):
        if self.current_data is None:
            return

        # Clear figure
        self.fig.clear()

        numeric_columns = self.current_data.select_dtypes(include=[np.number]).columns
        n_cols = len(numeric_columns)

        if n_cols < 2:
            messagebox.showinfo("Info", "Minimal 2 kolom numerik diperlukan untuk subplot")
            self.use_subplot.set(False)
            self.setup_single_plot()
            return

        # Tentukan layout subplot
        if n_cols == 2:
            rows, cols = 1, 2
        elif n_cols == 3:
            rows, cols = 2, 2
        elif n_cols == 4:
            rows, cols = 2, 2
        else:
            rows, cols = 2, 3

        # Limit maksimal 6 subplot
        n_plots = min(n_cols, 6)

        # Buat subplot
        for i in range(n_plots):
            ax = self.fig.add_subplot(rows, cols, i+1)
            col = numeric_columns[i]

            # Plot berbagai jenis untuk setiap subplot
            if i % 4 == 0:  # Line plot
                ax.plot(self.current_data[col], color='blue', linewidth=1.5)
                ax.set_title(f'Line: {col}')
            elif i % 4 == 1:  # Histogram
                ax.hist(self.current_data[col].dropna(), bins=20, alpha=0.7, color='green')
                ax.set_title(f'Histogram: {col}')
            elif i % 4 == 2:  # Box plot
                ax.boxplot(self.current_data[col].dropna())
                ax.set_title(f'Box: {col}')
            else:  # Scatter dengan kolom pertama
                if len(numeric_columns) > 1:
                    ax.scatter(self.current_data[numeric_columns[0]], 
                            self.current_data[col], alpha=0.6)
                    ax.set_title(f'Scatter: {col}')

            ax.grid(True, alpha=0.3)

        self.fig.tight_layout()
        self.canvas.draw()
        

    def on_plot_type_change(self, event=None):
        if self.current_data is not None:
            self.plot_data_advanced()
        else:
            messagebox.showwarning("Peringatan", "Muat data terlebih dahulu!")

    def plot_data_advanced(self):
        if self.current_data is None:
            return

        # Clear plot
        self.ax.clear()

        numeric_columns = self.current_data.select_dtypes(include=[np.number]).columns
        date_columns = self.current_data.select_dtypes(include=['datetime64']).columns

        plot_type = self.plot_type.get()

        if plot_type == "line":
            # Line plot
            if len(date_columns) > 0 and len(numeric_columns) > 0:
                date_col = date_columns[0]
                colors = ['blue', 'red', 'green', 'orange', 'purple']
                for i, col in enumerate(numeric_columns[:3]):
                    self.ax.plot(
                        self.current_data[date_col], 
                        self.current_data[col], 
                        color=colors[i % len(colors)],
                        label=col,
                        linewidth=2
                    )
                self.ax.set_xlabel('Tanggal')
                self.ax.legend()
            elif len(numeric_columns) >= 1:
                col = numeric_columns[0]
                self.ax.plot(self.current_data[col], linewidth=2)
                self.ax.set_xlabel('Index')
                self.ax.set_ylabel(col)

        elif plot_type == "scatter":
            if len(numeric_columns) >= 2:
                x_col, y_col = numeric_columns[0], numeric_columns[1]
                self.ax.scatter(
                    self.current_data[x_col], 
                    self.current_data[y_col],
                    alpha=0.6,
                    s=50,
                    c='blue'
                )
                self.ax.set_xlabel(x_col)
                self.ax.set_ylabel(y_col)

        elif plot_type == "bar":
            if len(numeric_columns) >= 1:
                col = numeric_columns[0]
                data_sample = self.current_data[col].head(20)
                self.ax.bar(range(len(data_sample)), data_sample, color='skyblue')
                self.ax.set_xlabel('Index')
                self.ax.set_ylabel(col)

        elif plot_type == "histogram":
            if len(numeric_columns) >= 1:
                col = numeric_columns[0]
                self.ax.hist(
                    self.current_data[col].dropna(), 
                    bins=30, 
                    alpha=0.7, 
                    color='lightgreen',
                    edgecolor='black'
                )
                self.ax.set_xlabel(col)
                self.ax.set_ylabel('Frekuensi')

        elif plot_type == "box":
            if len(numeric_columns) >= 1:
                data_to_plot = [self.current_data[col].dropna() for col in numeric_columns[:5]]
                labels = numeric_columns[:5].tolist()
                self.ax.boxplot(data_to_plot, labels=labels)
                self.ax.set_ylabel('Nilai')
                plt.setp(self.ax.xaxis.get_majorticklabels(), rotation=45)

        self.ax.set_title(f'{plot_type.title()} Plot')
        self.ax.grid(True, alpha=0.3)
        self.fig.tight_layout()
        self.canvas.draw()

    def load_data(self):
        file_path = filedialog.askopenfilename(
            title="Pilih file CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if file_path:
            try:
                # Baca CSV
                self.current_data = pd.read_csv(file_path)

                # Update info label
                rows, cols = self.current_data.shape
                self.data_info_label.config(
                    text=f"Data dimuat:\n{rows} baris, {cols} kolom\nFile: {file_path.split('/')[-1]}"
                )

                # Plot data
                self.plot_data()

            except Exception as e:
                messagebox.showerror("Error", f"Gagal membaca file:\n{str(e)}")

    def generate_sample_data(self):
        # Generate data sample yang menarik
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')

        # Simulasi data penjualan dengan tren dan noise
        trend = np.linspace(100, 200, len(dates))
        seasonal = 30 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
        noise = np.random.normal(0, 15, len(dates))
        sales = trend + seasonal + noise

        # Simulasi data temperature
        temp_base = 25 + 10 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
        temp_noise = np.random.normal(0, 5, len(dates))
        temperature = temp_base + temp_noise

        # Buat DataFrame
        self.current_data = pd.DataFrame({
            'Date': dates,
            'Sales': sales,
            'Temperature': temperature,
            'Category_A': sales * 0.6 + np.random.normal(0, 10, len(dates)),
            'Category_B': sales * 0.4 + np.random.normal(0, 8, len(dates))
        })

        # Update info label
        rows, cols = self.current_data.shape
        self.data_info_label.config(
            text=f"Sample data dibuat:\n{rows} baris, {cols} kolom\nData penjualan tahunan"
        )

        # Plot data
        self.plot_data()

    def plot_data(self):
        if self.current_data is None:
            return

        # Clear plot
        self.ax.clear()

        # Deteksi jenis data dan plot accordingly
        numeric_columns = self.current_data.select_dtypes(include=[np.number]).columns
        date_columns = self.current_data.select_dtypes(include=['datetime64']).columns

        if len(date_columns) > 0 and len(numeric_columns) > 0:
            # Time series plot
            date_col = date_columns[0]

            # Plot multiple numeric columns
            colors = ['blue', 'red', 'green', 'orange', 'purple']
            for i, col in enumerate(numeric_columns[:5]):  # Limit to 5 columns
                self.ax.plot(
                    self.current_data[date_col], 
                    self.current_data[col], 
                    color=colors[i % len(colors)],
                    label=col,
                    linewidth=2,
                    marker='o' if len(self.current_data) < 50 else None,
                    markersize=3
                )

            self.ax.set_xlabel('Tanggal')
            self.ax.set_ylabel('Nilai')
            self.ax.set_title('Time Series Data')
            self.ax.legend()

            # Format tanggal pada x-axis
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            self.ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
            plt.setp(self.ax.xaxis.get_majorticklabels(), rotation=45)

        elif len(numeric_columns) >= 2:
            # Scatter plot untuk 2 kolom numerik pertama
            x_col, y_col = numeric_columns[0], numeric_columns[1]
            self.ax.scatter(
                self.current_data[x_col], 
                self.current_data[y_col],
                alpha=0.6,
                s=50
            )
            self.ax.set_xlabel(x_col)
            self.ax.set_ylabel(y_col)
            self.ax.set_title(f'Scatter Plot: {x_col} vs {y_col}')

        else:
            # Bar plot untuk data kategorikal
            if len(numeric_columns) > 0:
                col = numeric_columns[0]
                data_sample = self.current_data[col].head(20)  # Limit to first 20 rows
                self.ax.bar(range(len(data_sample)), data_sample)
                self.ax.set_xlabel('Index')
                self.ax.set_ylabel(col)
                self.ax.set_title(f'Bar Plot: {col}')

        self.ax.grid(True, alpha=0.3)
        self.fig.tight_layout()
        self.canvas.draw()
        self.plot_data_advanced()


# Membuat dan menjalankan aplikasi
if __name__ == "__main__":
    root = tk.Tk()
    app = DataVisualizer(root)
    root.mainloop()