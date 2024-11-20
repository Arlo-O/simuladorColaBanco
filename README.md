# Simulador Banco cola circular-dinamica

Este es un proyecto que tiene como objetivo desarrollar un simulador de lo que sería la cola (usualmente llamada fila) hacia el cajero de un banco, el sistema implementa una cola dinamica y ciruclar para la representación de los clientes en espera y el cliente que esta haciendo atendido.

_¿Por qué circular y dinamica?_ El circular se debe a que se tiene como proposito que si un cliente necesita realizar un número mayor de transacciones al limite definido, entonces el cliente debe de ir a la cola de la fila con sus transacciones restantes, y dinamica, porque los clientes se agregan a la cola en tiempo de ejecución.

## Para ejecutar el código 🚀

Asegurese de tener instaladas las librerias:
* Tkinter
* Pillow
Y de descargar no solo el código sino tambien la imagen incluida en el proyecto.

## Contexto del proyecto.

El proyecto consta de una interfaz grafica de usuario (GUI) en la cual no es necesaria la interacción del usuario para el desarrollo del programa.

Como se dijo anteriormente el proyecto simula ser la cola de un banco, para ello se tomaron como requerimientos los siguientes items:
- Cada cliente tiene un id y un número de transacciones a realizar.
- Limite máximo de transacciones por turno = 5.
- La cola debe de ser dinamica.
- El cajero debe ser representado en la cola circular.
- El uso de hilos es necesario para garantizar la ejecución simultanea de creacion de clientes y el que sean atendidos.
- Se debe de presentar en una interfaz grafica de usuario.
- El cliente que supere el número de transacciones debe ser enviado al final de la cola con sus transacciones restantes.

## Construido con 🛠️

_Como lenguaje se uso Python_

* Libreria Tkinter
* Libreria Pillow
* Modulo Time
* Modulo Random
* Modulo Threading


## Autores ✒️



* **Arlo Ocampo** - [Arlo-O](https://github.com/Arlo-O)

