import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os

class IPSApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("IPS - Procesador de Facturas")
        self.root.geometry("800x600")
        
        # Configurar estilos
        self.style = ttk.Style()
        self.style.configure('Main.TButton', 
                           font=('Arial', 10, 'bold'),
                           padding=10,
                           width=25)
        self.style.configure('Regime.TButton',
                           font=('Arial', 10),
                           padding=8,
                           width=30)
        self.style.configure('Config.TButton',
                           font=('Arial', 10),
                           padding=8,
                           width=20)
        self.style.configure('Back.TButton',
                           font=('Arial', 10),
                           padding=8,
                           width=25)
        
        # Variables de configuración
        self.nit = ""
        self.contract_number = ""
        self.prefix = ""
        
        # Crear estructura de directorios
        self.create_directory_structure()
        
        # Cargar configuración existente
        self.load_config()
        
        # Mostrar ventana de configuración inicial
        self.show_config_window()
    
    def create_directory_structure(self):
        """Crear la estructura de directorios necesaria"""
        try:
            # Directorios base
            regimes = ['SUBSIDIADO', 'CONTRIBUTIVO']
            subdirs = ['FACTURAS', 'SOPORTES', 'EMPAQUETADO']
            
            # Obtener el directorio actual
            base_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Crear estructura para cada régimen
            for regime in regimes:
                regime_path = os.path.join(base_dir, regime)
                if not os.path.exists(regime_path):
                    os.makedirs(regime_path)
                
                # Crear subdirectorios
                for subdir in subdirs:
                    subdir_path = os.path.join(regime_path, subdir)
                    if not os.path.exists(subdir_path):
                        os.makedirs(subdir_path)
            
            # Guardar rutas en la configuración
            self.directories = {
                'SUBSIDIADO': {
                    'FACTURAS': os.path.join(base_dir, 'SUBSIDIADO', 'FACTURAS'),
                    'SOPORTES': os.path.join(base_dir, 'SUBSIDIADO', 'SOPORTES'),
                    'EMPAQUETADO': os.path.join(base_dir, 'SUBSIDIADO', 'EMPAQUETADO')
                },
                'CONTRIBUTIVO': {
                    'FACTURAS': os.path.join(base_dir, 'CONTRIBUTIVO', 'FACTURAS'),
                    'SOPORTES': os.path.join(base_dir, 'CONTRIBUTIVO', 'SOPORTES'),
                    'EMPAQUETADO': os.path.join(base_dir, 'CONTRIBUTIVO', 'EMPAQUETADO')
                }
            }
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear la estructura de directorios: {str(e)}")
    
    def load_config(self):
        """Cargar configuración desde archivo JSON"""
        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r') as f:
                    config = json.load(f)
                    self.nit = config.get('nit', '')
                    self.contract_number = config.get('contract_number', '')
                    self.prefix = config.get('prefix', '')
        except Exception as e:
            print(f"Error al cargar configuración: {str(e)}")
    
    def save_config(self, nit, contract, prefix):
        """Guardar configuración en archivo JSON"""
        try:
            config = {
                'nit': nit,
                'contract_number': contract,
                'prefix': prefix
            }
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error al guardar configuración: {str(e)}")
            return False
    
    def show_config_window(self):
        """Mostrar ventana de configuración inicial"""
        config_window = tk.Toplevel(self.root)
        config_window.title("Configuración")
        
        # Establecer tamaño mínimo y máximo
        config_window.minsize(600, 400)
        config_window.maxsize(800, 600)
        
        # Configurar el grid de la ventana principal
        config_window.grid_columnconfigure(0, weight=1)
        config_window.grid_rowconfigure(0, weight=1)
        
        # Frame principal con padding
        frame = ttk.Frame(config_window, padding="40")
        frame.grid(row=0, column=0, sticky="nsew")
        
        # Configurar el grid del frame
        frame.grid_columnconfigure(1, weight=1)
        
        # Variables
        nit_var = tk.StringVar(value=self.nit)
        contract_var = tk.StringVar(value=self.contract_number)
        prefix_var = tk.StringVar(value=self.prefix)
        
        # Título
        title_label = ttk.Label(frame, text="Configuración del Sistema", 
                              font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 30), sticky="ew")
        
        # Campos con más espacio y etiquetas más grandes
        ttk.Label(frame, text="NIT:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=15)
        nit_entry = ttk.Entry(frame, textvariable=nit_var, width=40, font=("Arial", 10))
        nit_entry.grid(row=1, column=1, pady=15, padx=10, sticky="ew")
        
        ttk.Label(frame, text="Número de Contrato:", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=15)
        contract_entry = ttk.Entry(frame, textvariable=contract_var, width=40, font=("Arial", 10))
        contract_entry.grid(row=2, column=1, pady=15, padx=10, sticky="ew")
        
        ttk.Label(frame, text="Prefijo de Facturación:", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=15)
        prefix_entry = ttk.Entry(frame, textvariable=prefix_var, width=40, font=("Arial", 10))
        prefix_entry.grid(row=3, column=1, pady=15, padx=10, sticky="ew")
        
        # Frame para botones
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=30)
        
        def on_save():
            if self.save_config(nit_var.get(), contract_var.get(), prefix_var.get()):
                self.nit = nit_var.get()
                self.contract_number = contract_var.get()
                self.prefix = prefix_var.get()
                config_window.destroy()
                self.show_main_menu()
            else:
                messagebox.showerror("Error", "No se pudo guardar la configuración")
        
        # Botón más grande y con mejor estilo
        save_button = ttk.Button(button_frame, text="Guardar", command=on_save, width=20)
        save_button.pack(padx=10)
        
        # Centrar la ventana después de que todos los widgets estén creados
        config_window.update_idletasks()
        width = config_window.winfo_width()
        height = config_window.winfo_height()
        x = (config_window.winfo_screenwidth() // 2) - (width // 2)
        y = (config_window.winfo_screenheight() // 2) - (height // 2)
        config_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Hacer la ventana modal
        config_window.transient(self.root)
        config_window.grab_set()
        
        # Enfocar el primer campo
        nit_entry.focus_set()
    
    def show_main_menu(self):
        """Mostrar menú principal"""
        # Limpiar ventana principal
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(3, weight=0)
        
        # Título
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, pady=(0, 10))
        ttk.Label(title_frame, text="Menú Principal", 
                 font=("Arial", 16, "bold")).pack()
        
        # Frame de configuración
        config_frame = ttk.LabelFrame(main_frame, text="Configuración Actual", padding="10")
        config_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        
        # Información de configuración
        config_info = ttk.Frame(config_frame)
        config_info.pack(fill="x", expand=True)
        
        # Crear etiquetas de configuración
        ttk.Label(config_info, text=f"NIT: {self.nit}", 
                 font=("Arial", 9)).pack(anchor="w", pady=2)
        ttk.Label(config_info, text=f"Contrato: {self.contract_number}", 
                 font=("Arial", 9)).pack(anchor="w", pady=2)
        ttk.Label(config_info, text=f"Prefijo: {self.prefix}", 
                 font=("Arial", 9)).pack(anchor="w", pady=2)
        
        # Frame para botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, sticky="nsew", pady=10)
        
        # Botones con nuevo estilo
        ttk.Button(button_frame, text="Régimen Subsidiado", 
                  command=lambda: self.show_regime_menu("SUBSIDIADO"),
                  style='Main.TButton').pack(pady=10, fill="x")
        
        ttk.Button(button_frame, text="Régimen Contributivo", 
                  command=lambda: self.show_regime_menu("CONTRIBUTIVO"),
                  style='Main.TButton').pack(pady=10, fill="x")
        
        ttk.Button(button_frame, text="Ver Estructura de Carpetas", 
                  command=self.show_directory_structure,
                  style='Config.TButton').pack(pady=10, fill="x")
        
        ttk.Button(button_frame, text="Cambiar Configuración", 
                  command=self.show_config_window,
                  style='Config.TButton').pack(pady=10, fill="x")
        
        ttk.Button(button_frame, text="Salir", 
                  command=self.root.quit,
                  style='Main.TButton').pack(pady=10, fill="x")
        
        # Frame para la consola
        console_frame = ttk.LabelFrame(main_frame, text="Consola", padding="5")
        console_frame.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        
        # Consola
        self.console = scrolledtext.ScrolledText(console_frame, height=5, wrap=tk.WORD)
        self.console.pack(fill="both", expand=True)
        self.console.insert(tk.END, "Bienvenido al sistema de procesamiento de facturas.\n")
        self.console.config(state=tk.DISABLED)
    
    def show_regime_menu(self, regime):
        """Mostrar menú de opciones del régimen"""
        # Limpiar ventana principal
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(3, weight=0)
        
        # Título
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, pady=(0, 10))
        ttk.Label(title_frame, text=f"Régimen {regime}", 
                 font=("Arial", 16, "bold")).pack()
        
        # Frame de configuración
        config_frame = ttk.LabelFrame(main_frame, text="Configuración Actual", padding="10")
        config_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        
        # Información de configuración
        config_info = ttk.Frame(config_frame)
        config_info.pack(fill="x", expand=True)
        
        # Crear etiquetas de configuración
        ttk.Label(config_info, text=f"NIT: {self.nit}", 
                 font=("Arial", 9)).pack(anchor="w", pady=2)
        ttk.Label(config_info, text=f"Contrato: {self.contract_number}", 
                 font=("Arial", 9)).pack(anchor="w", pady=2)
        ttk.Label(config_info, text=f"Prefijo: {self.prefix}", 
                 font=("Arial", 9)).pack(anchor="w", pady=2)
        
        # Frame para botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, sticky="nsew", pady=10)
        
        # Configurar grid para dos columnas
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        # Botones
        options = [
            "Verificación de Facturas",
            "Empaquetar Facturas",
            "Verificar Soportes",
            "Empaquetar soportes",
            "Empaquetar facturas de un rango específico",
            "Empaquetar soportes del rango específico"
        ]
        
        # Organizar botones en dos columnas
        for i, option in enumerate(options):
            row = i // 2
            col = i % 2
            ttk.Button(button_frame, text=option, 
                      command=lambda opt=option: self.show_test_message(opt),
                      style='Regime.TButton').grid(row=row, column=col, 
                                                 padx=5, pady=5, 
                                                 sticky="ew")
        
        # Frame para el botón de regreso
        back_frame = ttk.Frame(main_frame)
        back_frame.grid(row=3, column=0, pady=10)
        
        # Botón de regreso
        ttk.Button(back_frame, text="Volver al Menú Principal", 
                  command=self.show_main_menu,
                  style='Back.TButton').pack(pady=10)
        
        # Frame para la consola
        console_frame = ttk.LabelFrame(main_frame, text="Consola", padding="5")
        console_frame.grid(row=4, column=0, sticky="ew", pady=(10, 0))
        
        # Consola
        self.console = scrolledtext.ScrolledText(console_frame, height=5, wrap=tk.WORD)
        self.console.pack(fill="both", expand=True)
        self.console.insert(tk.END, f"Régimen {regime} seleccionado.\n")
        self.console.config(state=tk.DISABLED)
    
    def show_test_message(self, option):
        """Mostrar mensaje de prueba para cada opción"""
        messagebox.showinfo("Prueba", f"Has seleccionado: {option}\nEsta función será implementada próximamente.")
    
    def show_directory_structure(self):
        """Mostrar la estructura de directorios en una ventana"""
        try:
            # Crear ventana
            dir_window = tk.Toplevel(self.root)
            dir_window.title("Estructura de Directorios")
            dir_window.geometry("800x600")
            
            # Configurar grid
            dir_window.grid_columnconfigure(0, weight=1)
            dir_window.grid_rowconfigure(0, weight=1)
            
            # Frame principal con padding
            frame = ttk.Frame(dir_window, padding="20")
            frame.grid(row=0, column=0, sticky="nsew")
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_rowconfigure(1, weight=1)
            
            # Título
            ttk.Label(frame, text="Estructura de Directorios", 
                     font=("Arial", 14, "bold")).grid(row=0, column=0, pady=(0, 20))
            
            # Área de texto con scroll
            text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=("Consolas", 10))
            text_area.grid(row=1, column=0, sticky="nsew")
            
            # Mostrar estructura
            text_area.insert(tk.END, "=" * 50 + "\n")
            
            for regime, paths in self.directories.items():
                text_area.insert(tk.END, f"\n{regime}:\n")
                for dir_type, path in paths.items():
                    if os.path.exists(path):
                        text_area.insert(tk.END, f"  ✓ {dir_type}: {path}\n")
                    else:
                        text_area.insert(tk.END, f"  ✗ {dir_type}: {path} (No existe)\n")
            
            text_area.insert(tk.END, "\n" + "=" * 50)
            
            # Hacer el texto de solo lectura
            text_area.config(state=tk.DISABLED)
            
            # Centrar la ventana
            dir_window.update_idletasks()
            width = dir_window.winfo_width()
            height = dir_window.winfo_height()
            x = (dir_window.winfo_screenwidth() // 2) - (width // 2)
            y = (dir_window.winfo_screenheight() // 2) - (height // 2)
            dir_window.geometry(f'{width}x{height}+{x}+{y}')
            
            # Hacer la ventana modal
            dir_window.transient(self.root)
            dir_window.grab_set()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar la estructura: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = IPSApplication(root)
    root.mainloop() 