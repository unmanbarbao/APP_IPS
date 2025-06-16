import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import re
import sys

class IPSApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("IPS - Procesador de Facturas")
        self.root.geometry("800x700")
        
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
            
            # Obtener el directorio base
            if getattr(sys, 'frozen', False):
                # Si estamos ejecutando como .exe
                base_dir = os.path.dirname(sys.executable)
            else:
                # Si estamos ejecutando como script
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
            if option == "Verificación de Facturas":
                ttk.Button(button_frame, text=option, 
                          command=lambda r=regime: self.verify_invoices(r),
                          style='Regime.TButton').grid(row=row, column=col, 
                                                     padx=5, pady=5, 
                                                     sticky="ew")
            else:
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
    
    def log_to_console(self, message):
        """Agregar mensaje a la consola"""
        try:
            self.console.config(state=tk.NORMAL)
            self.console.insert(tk.END, f"{message}\n")
            self.console.see(tk.END)
            self.console.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Error al escribir en la consola: {str(e)}")
    
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

    def verify_invoices(self, regime):
        """Verificar facturas del régimen seleccionado"""
        try:
            # Obtener la ruta de la carpeta de facturas
            facturas_path = self.directories[regime]['FACTURAS']
            
            # Verificar si la carpeta existe
            if not os.path.exists(facturas_path):
                self.log_to_console(f"Error: La carpeta de facturas no existe en {facturas_path}")
                return
            
            # Obtener todas las carpetas de facturas
            invoice_folders = [f for f in os.listdir(facturas_path) 
                             if os.path.isdir(os.path.join(facturas_path, f))]
            
            if not invoice_folders:
                self.log_to_console("No se encontraron carpetas de facturas.")
                return
            
            # Crear ventana de resultados
            results_window = tk.Toplevel(self.root)
            results_window.title(f"Verificación de Facturas - {regime}")
            results_window.geometry("1200x600")
            
            # Configurar grid
            results_window.grid_columnconfigure(0, weight=1)
            results_window.grid_rowconfigure(0, weight=1)
            
            # Frame principal
            frame = ttk.Frame(results_window, padding="20")
            frame.grid(row=0, column=0, sticky="nsew")
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_rowconfigure(1, weight=1)
            
            # Título
            ttk.Label(frame, text=f"Verificación de Facturas - {regime}", 
                     font=("Arial", 14, "bold")).grid(row=0, column=0, pady=(0, 20))
            
            # Crear Treeview con scrollbar
            tree_frame = ttk.Frame(frame)
            tree_frame.grid(row=1, column=0, sticky="nsew")
            tree_frame.grid_columnconfigure(0, weight=1)
            tree_frame.grid_rowconfigure(0, weight=1)
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(tree_frame)
            scrollbar.grid(row=0, column=1, sticky="ns")
            
            # Treeview
            tree = ttk.Treeview(tree_frame, columns=("carpeta", "json", "xml", "cuv", "contrato", "mensaje"),
                               show="headings", yscrollcommand=scrollbar.set)
            
            # Configurar columnas
            tree.heading("carpeta", text="Carpeta")
            tree.heading("json", text="JSON")
            tree.heading("xml", text="XML")
            tree.heading("cuv", text="CUV")
            tree.heading("contrato", text="Contrato")
            tree.heading("mensaje", text="Mensaje")
            
            # Configurar anchos de columna
            tree.column("carpeta", width=150)
            tree.column("json", width=50, anchor="center")
            tree.column("xml", width=50, anchor="center")
            tree.column("cuv", width=50, anchor="center")
            tree.column("contrato", width=50, anchor="center")
            tree.column("mensaje", width=800)
            
            # Configurar scrollbar
            scrollbar.config(command=tree.yview)
            
            # Grid del Treeview
            tree.grid(row=0, column=0, sticky="nsew")
            
            # Verificar cada carpeta
            for folder in invoice_folders:
                folder_path = os.path.join(facturas_path, folder)
                results = self.verify_folder(folder_path, folder)
                
                # Inicializar estados
                json_status = "✓"
                xml_status = "✓"
                cuv_status = "✓"
                contract_status = "✓"
                message = "OK"
                
                # Procesar resultados
                for result in results:
                    if result['tipo'] == 'ERROR':
                        if 'JSON principal' in result['mensaje']:
                            json_status = "✗"
                        elif 'XML' in result['mensaje']:
                            xml_status = "✗"
                        elif 'CUV' in result['mensaje']:
                            cuv_status = "✗"
                        elif 'número de contrato' in result['mensaje'].lower():
                            contract_status = "✗"
                        message = result['mensaje']
                
                # Insertar en el Treeview
                tree.insert("", "end", values=(folder, json_status, xml_status, cuv_status, contract_status, message))
            
            # Frame para botones
            button_frame = ttk.Frame(frame)
            button_frame.grid(row=2, column=0, pady=20)
            
            # Botón para corregir contratos
            ttk.Button(button_frame, text="Corregir Números de Contrato", 
                      command=lambda: self.correct_contract_numbers(regime, tree),
                      style='Main.TButton').pack(side="left", padx=5)
            
            # Botón para cerrar
            ttk.Button(button_frame, text="Cerrar", 
                      command=results_window.destroy,
                      style='Main.TButton').pack(side="right", padx=5)
            
            # Centrar la ventana
            results_window.update_idletasks()
            width = results_window.winfo_width()
            height = results_window.winfo_height()
            x = (results_window.winfo_screenwidth() // 2) - (width // 2)
            y = (results_window.winfo_screenheight() // 2) - (height // 2)
            results_window.geometry(f'{width}x{height}+{x}+{y}')
            
            # Hacer la ventana modal
            results_window.transient(self.root)
            results_window.grab_set()
            
            self.log_to_console(f"Verificación de facturas completada para {regime}")
            
        except Exception as e:
            self.log_to_console(f"Error durante la verificación: {str(e)}")
            messagebox.showerror("Error", f"Error durante la verificación: {str(e)}")

    def correct_contract_numbers(self, regime, tree):
        """Corregir los números de contrato en los archivos XML"""
        try:
            # Obtener la ruta de la carpeta de facturas
            facturas_path = self.directories[regime]['FACTURAS']
            
            # Contador de correcciones
            corrected = 0
            errors = 0
            skipped = 0
            
            self.log_to_console(f"\nIniciando corrección de números de contrato para {regime}...")
            self.log_to_console(f"Número de contrato configurado: {self.contract_number}")
            
            # Recorrer todos los items en el Treeview
            for item in tree.get_children():
                values = tree.item(item)['values']
                folder = values[0]
                contract_status = values[4]  # Estado del contrato
                message = values[5]  # Mensaje
                
                # Verificar si necesita corrección (ya sea por estado o mensaje)
                needs_correction = (contract_status == "✗" or 
                                  "número de contrato" in message.lower() or 
                                  "contrato" in message.lower())
                
                if needs_correction:
                    folder_path = os.path.join(facturas_path, folder)
                    files = os.listdir(folder_path)
                    
                    # Buscar el archivo XML
                    xml_files = [f for f in files if f.endswith('.xml')]
                    if xml_files:
                        xml_path = os.path.join(folder_path, xml_files[0])
                        try:
                            # Leer el contenido del archivo XML
                            with open(xml_path, 'r', encoding='utf-8') as file:
                                content = file.read()
                            
                            # Buscar el número de contrato actual
                            pattern = r'<Value>([^<]+)</Value>'
                            match = re.search(pattern, content)
                            
                            if match:
                                current_contract = match.group(1).strip()
                                self.log_to_console(f"\nProcesando {folder}:")
                                self.log_to_console(f"- Número de contrato actual: {current_contract}")
                                
                                # Reemplazar el número de contrato
                                new_content = re.sub(pattern, f'<Value>{self.contract_number}</Value>', content)
                                
                                # Guardar el archivo modificado
                                with open(xml_path, 'w', encoding='utf-8') as file:
                                    file.write(new_content)
                                
                                # Actualizar el Treeview con todos los valores
                                current_values = list(tree.item(item)['values'])
                                current_values[4] = "✓"  # Actualizar estado del contrato
                                current_values[5] = "OK"  # Actualizar mensaje
                                tree.item(item, values=current_values)
                                
                                corrected += 1
                                self.log_to_console(f"✓ Contrato corregido en {folder}")
                            else:
                                skipped += 1
                                self.log_to_console(f"✗ No se encontró el número de contrato en {folder}")
                            
                        except Exception as e:
                            errors += 1
                            self.log_to_console(f"✗ Error al corregir {folder}: {str(e)}")
                else:
                    skipped += 1
            
            # Mostrar resumen
            self.log_to_console(f"\nResumen de la corrección:")
            self.log_to_console(f"- Carpetas corregidas: {corrected}")
            self.log_to_console(f"- Carpetas omitidas: {skipped}")
            self.log_to_console(f"- Errores: {errors}")
            
            message = f"Corrección completada:\n"
            message += f"- Corregidos: {corrected}\n"
            message += f"- Omitidos: {skipped}\n"
            message += f"- Errores: {errors}"
            messagebox.showinfo("Corrección de Contratos", message)
            
        except Exception as e:
            error_msg = f"Error durante la corrección: {str(e)}"
            self.log_to_console(f"✗ {error_msg}")
            messagebox.showerror("Error", error_msg)

    def verify_folder(self, folder_path, folder_name):
        """Verificar una carpeta de factura individual"""
        results = []
        
        # Extraer la parte numérica del nombre de la carpeta
        numeric_part = ''.join(filter(str.isdigit, folder_name))
        
        # Verificar archivos requeridos
        required_files = {
            'json': f"{folder_name}.json",
            'xml': None,  # Se verificará que exista un XML con la parte numérica
            'cuv': None  # Se verificará que contenga "CUV" en el nombre
        }
        
        # Verificar archivo JSON principal
        json_path = os.path.join(folder_path, required_files['json'])
        if not os.path.exists(json_path):
            results.append({
                'carpeta': folder_name,
                'tipo': 'ERROR',
                'mensaje': f'Falta el archivo JSON principal: {required_files["json"]}'
            })
        
        # Verificar archivo XML (cualquier XML que contenga la parte numérica)
        xml_files = [f for f in os.listdir(folder_path) 
                    if f.endswith('.xml') and numeric_part in f]
        if not xml_files:
            results.append({
                'carpeta': folder_name,
                'tipo': 'ERROR',
                'mensaje': f'Falta el archivo XML que contenga el número {numeric_part}'
            })
        else:
            # Verificar el número de contrato en el XML
            xml_path = os.path.join(folder_path, xml_files[0])
            contract_error, contract_element = self.verify_contract_number(xml_path)
            if contract_error:
                results.append({
                    'carpeta': folder_name,
                    'tipo': 'ERROR',
                    'mensaje': contract_error
                })
        
        # Verificar archivo JSON con CUV
        cuv_files = [f for f in os.listdir(folder_path) 
                    if f.endswith('.json') and 'CUV' in f.upper()]
        if not cuv_files:
            results.append({
                'carpeta': folder_name,
                'tipo': 'ERROR',
                'mensaje': 'Falta el archivo JSON con CUV'
            })
        
        # Si no hay errores
        if not results:
            results.append({
                'carpeta': folder_name,
                'tipo': 'OK',
                'mensaje': 'Carpeta verificada correctamente'
            })
        
        return results

    def verify_contract_number(self, xml_path):
        """Verificar el número de contrato en el archivo XML"""
        try:
            # Leer el archivo como texto
            with open(xml_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Buscar el patrón Name/Value para el número de contrato
            contract_found = False
            xml_contract = None
            
            # Buscar el patrón <Name>NUMERO_CONTRATO</Name> seguido de <Value>
            pattern = r'<Name>NUMERO_CONTRATO</Name>\s*<Value>([^<]+)</Value>'
            match = re.search(pattern, content)
            
            if match:
                xml_contract = match.group(1).strip()
                contract_found = True
            
            if not contract_found:
                return 'No se encontró el número de contrato en el archivo XML', None
            
            # Normalizar el número de contrato encontrado
            if '.' not in xml_contract:
                xml_contract = f"{xml_contract[:3]}.{xml_contract[3:]}"
            
            # Validar el formato del número de contrato
            if not re.match(r'^\d{3}\.2025$', xml_contract):
                return f'El número de contrato encontrado ({xml_contract}) no tiene el formato correcto (XXX.2025)', None
            
            # Comparar con el número de contrato configurado
            if xml_contract != self.contract_number:
                return f'El número de contrato en el XML ({xml_contract}) no coincide con el configurado ({self.contract_number})', None
            
            return None, None
            
        except Exception as e:
            return f'Error al verificar el número de contrato: {str(e)}', None

if __name__ == "__main__":
    root = tk.Tk()
    app = IPSApplication(root)
    root.mainloop() 