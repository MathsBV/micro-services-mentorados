#!/bin/bash

# Atualizar o sistema
sudo apt-get update
sudo apt-get upgrade -y

# Instalar dependências
sudo apt-get install -y python3-pip python3-venv nginx

# Criar diretório da aplicação
mkdir -p /home/ubuntu/app
cd /home/ubuntu/app

# Criar e ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências Python
pip install -r requirements.txt

# Configurar Nginx
sudo tee /etc/nginx/sites-available/mentorados << EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }

    location /static {
        alias /home/ubuntu/app/frontend;
    }
}
EOF

# Habilitar o site
sudo ln -s /etc/nginx/sites-available/mentorados /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# Configurar serviço systemd
sudo tee /etc/systemd/system/mentorados.service << EOF
[Unit]
Description=Mentorados Microservice
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/app
Environment="PATH=/home/ubuntu/app/venv/bin"
ExecStart=/home/ubuntu/app/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
EOF

# Iniciar o serviço
sudo systemctl daemon-reload
sudo systemctl enable mentorados
sudo systemctl start mentorados 