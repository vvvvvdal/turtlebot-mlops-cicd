# 🐢 Turtlebot (MLOps - CI/CD)

![Python](https://img.shields.io/badge/Python-3.10-blue)
![ROS 2](https://img.shields.io/badge/ROS_2-Humble-22314E)
![CI/CD](https://img.shields.io/github/actions/workflow/status/vvvvvdal/mlops-cicd-turtlebot/pipeline.yml?label=CI%2FCD%20Pipeline)

A ideia aqui é simples, mas resolve um problema gigante: como garantir que a IA que controla o robô físico, Turtlebot, não alucine e não faça o robô bater na parede?

Criamos um sistema CI/CD. Antes de qualquer código ou modelo de IA ir para o robô, ele passa por uma bateria de testes virtuais. Se o robô virtual "bater" na parede, o deploy é cancelado e o robô físico fica protegido.

## 💻 Como testar

### Testando no terminal:
1. Instale as dependências necessárias:
```bash
pip install -r requirements.txt
```

2. Rode a bateria de testes de segurança com o Pytest:
```bash
pytest tests/ -v --log-cli-level=INFO
```

### Testando no Turtlesim com Ollama (navegação autônoma):
1. Inicie o Turtlesim (Terminal 1):
```bash
ros2 run turtlesim turtlesim_node
```

2. Rode a navegação com um peso de modelo (Terminal 2):
```bash
# Peso bom (peso >= 8): Aprovado
python3 src/turtlesim_navegacao.py 10

# Peso ruim (peso < 8): Reprovado
python3 src/turtlesim_navegacao.py 3
```

### Testando na simulação visual com HTML:
1. Abra o arquivo `simulacao_mapa.html` no seu navegador:
```bash
xdg-open simulacao_mapa.html
```
