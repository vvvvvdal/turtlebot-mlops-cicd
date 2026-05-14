# Usando a imagem oficial e "leve" do ROS 2
FROM ros:humble-ros-core-jammy

# Evita que o Ubuntu faça perguntas (como fuso horário) travando a instalação
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Instala o pip do Python e as dependências graficas que o OpenCV exige
RUN apt-get update && apt-get install -y \
    python3-pip \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copia a lista de bibliotecas do seu repositório
COPY requirements.txt .

# Instala o Pytest, Numpy e OpenCV
# A flag --break-system-packages é necessária no Ubuntu 22.04 (base do Humble) 
# ao rodar pip como root dentro de containers
RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages

# Copia todo o seu código para dentro do container do robô
COPY . .

# Simula a inicialização do nó de visão do robô
CMD ["python3", "visao_mock.py"]