from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

# Mudar para o diretório do frontend
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Configurar o servidor
port = 3000
server_address = ('', port)

# Criar o servidor
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

print(f'Servidor rodando em http://localhost:{port}')
print('Pressione Ctrl+C para parar o servidor')

# Iniciar o servidor
httpd.serve_forever() 