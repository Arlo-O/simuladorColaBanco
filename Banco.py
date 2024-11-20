import tkinter as tk
from PIL import Image, ImageTk
import threading, time, random

class Cliente:
    def __init__(self, identificacion, transacciones):
        self.identificacion = identificacion
        self.transacciones = transacciones
        self.siguiente = None

class ColaCircular:
    def __init__(self):
        self.ultimo = None
        self.lock = threading.Lock()

    def agregarClientes(self, cliente : Cliente):
        with self.lock:
            if not self.ultimo:
                self.ultimo = cliente
                cliente.siguiente = cliente
            else:
                cliente.siguiente = self.ultimo.siguiente
                self.ultimo.siguiente = cliente
                self.ultimo = cliente
    
    def atenderClientes(self):
        with self.lock:
            if not self.ultimo:
                return None
            primero = self.ultimo.siguiente
            if primero == self.ultimo:
                self.ultimo = None
            else:
                self.ultimo.siguiente = primero.siguiente
            return primero
    
    def estaVacia(self):
        with self.lock:
            return self.ultimo is None 
    
class GUIBanco:
    def __init__(self, master):
        self.master = master
        self.cola = ColaCircular()
        self.cajero = Cajero(5,self.cola, self)
        self.clienteId = 1
        self.generarClientes = True
        self.clientes = []
        self.circulos = []

        self.inicializarVentana()
        self.crearComponentes()
        self.iniciarHilos()

    def inicializarVentana(self):
        self.master.title("Simulador Banco")
        self.master.geometry("800x500")
    
    def crearComponentes(self):
        self.canva = tk.Canvas(self.master, width=800, height=500, background="white")
        self.canva.pack()

        self.imagen = Image.open("cajero.png").resize((200, 200))
        self.cajeroTk = ImageTk.PhotoImage(self.imagen)
        self.canva.create_image(50, 50, image=self.cajeroTk, anchor= tk.NW)

        self.dibujarFila()
        self.dibujarCirculos()

        self.btnCerrar = tk.Button(self.master, text="Parar creación clientes", command=self.cerrarBanco)
        self.btnCerrar.place(x = 80, y= 310)

        self.btnReanudar = tk.Button(self.master, text="Reanudar creación clientes", command=self.reanudarCreacion)
        self.btnReanudar.place(x= 80, y= 350)

    def dibujarFila(self):
        # Horizontal 1
        self.canva.create_line(320, 100, 700, 100, width=4)  # Borde superior
        self.canva.create_line(320, 150, 650, 150, width=4)  # Borde inferior
        # Vertical 1
        self.canva.create_line(650, 150, 650, 200, width=4)  # Borde izquierdo
        self.canva.create_line(700, 100, 700, 250, width=4)  # Borde derecho
        # Horizontal 2
        self.canva.create_line(320, 200, 650, 200, width=4)  # Borde superior
        self.canva.create_line(370, 250, 700, 250, width=4)  # Borde inferior
        # Vertical 2
        self.canva.create_line(370, 250, 370, 300, width=4)  # Borde derecho
        self.canva.create_line(320, 200, 320, 350, width=4)  # Borde izquierdo
        # Horizontal 3
        self.canva.create_line(370, 300, 700, 300, width=4)  # Borde superior
        self.canva.create_line(320, 350, 650, 350, width=4)  # Borde inferior
        # Vertical 3
        self.canva.create_line(650, 350, 650, 400, width=4)  # Borde izquierdo
        self.canva.create_line(700, 300, 700, 400, width=4)  # Borde derecho

        self.canva.create_text(300, 80, text="Inicio", font=("Helvetica", 14))

    def dibujarCirculos(self):
        radio = 20
        diametro = radio * 2
        margen = 7
        x_inicio, x_fin = 320, 700
        y_inicio, y_medio, y_fin = 125, 225, 325

        self.circulo_atendido = self.canva.create_oval(250, 105, 290, 145, fill="gray")
        self.texto_atendido = self.canva.create_text(270, 125, text="", font=("Arial", 12))
        self.circulos.append((self.circulo_atendido, self.texto_atendido))

        for x in range(x_inicio + radio, x_fin - radio + 1, diametro + margen):
            circulo = self.canva.create_oval(
                x - radio, y_inicio - radio, x + radio, y_inicio + radio, fill="gray")
            texto = self.canva.create_text(x, y_inicio, text=f"", font=("Arial", 12))
            self.circulos.append((circulo, texto))

        circulo = self.canva.create_oval(
            x_fin -diametro - margen, y_inicio + radio + 10, x_fin - margen, y_inicio + diametro + radio + 10, fill="gray")
        texto = self.canva.create_text(x_fin-radio-margen, y_inicio + diametro+10, text="", font=("Arial", 12))
        self.circulos.append((circulo, texto))
            
        for x in range(x_fin - radio - margen, x_inicio + radio - 1, -diametro-margen):
            circulo = self.canva.create_oval(
                x - radio, y_medio -radio, x + radio, y_medio + radio, fill="gray")
            texto = self.canva.create_text(x, y_medio, text=f"", font=("Arial", 12))
            self.circulos.append((circulo, texto))

        circulo = self.canva.create_oval(
                x_inicio + margen, y_medio + radio + margen, x_inicio +margen + diametro, y_medio + margen + radio + diametro, fill="gray")
        texto = self.canva.create_text(x_inicio+radio+margen, y_medio+diametro+margen, text="", font=("Arial", 12))
        self.circulos.append((circulo, texto))

        for x in range(x_inicio + radio, x_fin - radio + 1, diametro + margen):
            circulo = self.canva.create_oval(
                x - radio, y_fin - radio, x + radio, y_fin + radio, fill="gray")
            texto = self.canva.create_text(x, y_fin, text=f"", font=("Arial", 12))
            self.circulos.append((circulo, texto))
    
    def iniciarHilos(self):
        threading.Thread(target=self.generarClienteAuto, daemon=True).start()
        threading.Thread(target=self.cajero.atenderClientes, daemon=True).start()

    def generarClienteAuto(self):
        while self.generarClientes:
            if len(self.clientes) < 20:
                cliente = Cliente(self.clienteId, random.randint(1,10))
                self.cola.agregarClientes(cliente)
                self.clientes.append(cliente)
                self.clienteId += 1
                self.actualizarCirculos()
            time.sleep(random.randint(1,3))

    def actualizarCirculos(self):
        for i in range(len(self.circulos)):
            if i < len(self.clientes):
                self.canva.itemconfig(self.circulos[i][0], fill="green")
                self.canva.itemconfig(self.circulos[i][1], text=self.clientes[i].identificacion)
            else:
                self.canva.itemconfig(self.circulos[i][0], fill="gray")
                self.canva.itemconfig(self.circulos[i][1], text="")
    
    def actualizarGUI(self):
        self.canva.itemconfig(self.circulos[0][0], fill="blue")
        self.canva.itemconfig(self.circulos[0][1], text=self.clientes[0].identificacion)
        self.master.update()

    def cerrarBanco(self):
        self.generarClientes = False
    
    def reanudarCreacion(self):
        if not self.generarClientes:
            self.generarClientes = True
            threading.Thread(target=self.generarClienteAuto, daemon=True).start()
            print("Creación de clientes reanudada")

class Cajero:
    def __init__(self, limiteTransacciones, cola : ColaCircular, gui : GUIBanco):
        self.limiteTransacciones = limiteTransacciones
        self.cola = cola
        self.gui = gui

    def atenderClientes(self):
        while not self.cola.estaVacia():
            cliente = self.cola.atenderClientes()
            if cliente:
                self.gui.actualizarGUI()
                transaccionesRestantes = self.procesarTransacciones(cliente)
                if transaccionesRestantes > 0:
                    cliente.transacciones = transaccionesRestantes
                    self.cola.agregarClientes(cliente)
                    self.gui.clientes.remove(cliente)
                    self.gui.clientes.append(cliente)
                else:
                    self.gui.clientes.remove(cliente)

                self.limpiarGUI()
            # else:
            #     time.sleep(1)

    def procesarTransacciones(self, cliente : Cliente):
        for i in range(cliente.transacciones):
            time.sleep(1)
        return max(0, cliente.transacciones - self.limiteTransacciones)
    
    def limpiarGUI(self):
        self.gui.canva.itemconfig(self.gui.circulos[0][0], fill="gray")
        self.gui.canva.itemconfig(self.gui.circulos[0][1], text="")
        self.gui.master.update()
        self.gui.actualizarCirculos()


if __name__ == "__main__":
    ventana = tk.Tk()
    programa = GUIBanco(ventana)
    ventana.mainloop()