"""
Utilice el modulo nativo 'http.server' (BaseHTTPRequestHandler y HTTPServer) 
por las siguientes razones de arquitectura y entorno:

1. PORTABILIDAD: Al ser una libreria estandar de Python, el microservicio 
   funciona en cualquier entorno sin necesidad de instalar dependencias 
   externas (como Flask o Django), ideal para despliegues rapidos y ligeros.
   tome esta decision ya que el pc del laboratorio debia instalar node.js y se requeria la contraseña del administrador del sistema 
 
2. CERO DEPENDENCIAS: Resuelve la limitacion de permisos de administrador 
   en el entorno local, cumpliendo con el requerimiento de operatividad inmediata.

3. BAJO NIVEL (EDUCATIVO): Permite demostrar el manejo manual de los 
   verbos HTTP (GET/POST), las cabeceras (Headers) y los codigos de estado (200, 201), 
   elementos fundamentales en la comunicacion entre microservicios.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
# Se utiliza un array en memoria para representar la persistencia del inventario.
productos = [
    {"id": 1, "nombre": "PlayStation 5", "stock": 10, "precio": 549990},
    {"id": 2, "nombre": "Switch Pro", "stock": 50, "precio": 23690}
]

class ShopSmartHandler(BaseHTTPRequestHandler):
    # Manejador de peticiones GET: Lectura de inventario
    def do_GET(self):
        if self.path == '/productos':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(productos).encode())
        else:
            self.send_error(404, "Ruta no encontrada")
   # peticiones post para poder actualizar el innventario 
    def do_POST(self):
        if self.path == '/productos':
            
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            nuevo_prod = json.loads(post_data)
            
            # asignamos un id al agregar el producto 
            nuevo_prod['id'] = len(productos) + 1
            productos.append(nuevo_prod)
            
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"mensaje": "Producto agregado", "producto": nuevo_prod}
            self.wfile.write(json.dumps(response).encode())

# ejecutamos eel servidor
if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, ShopSmartHandler)
    print("Microservicio ShopSmart corriendo en http://localhost:8000")
    httpd.serve_forever()