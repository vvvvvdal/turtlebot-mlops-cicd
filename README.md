# 🐢 Turtlebot (MLOps - CI/CD)

![Python](https://img.shields.io/badge/Python-3.10-blue)
![ROS 2](https://img.shields.io/badge/ROS_2-Humble-22314E)
![CI/CD](https://img.shields.io/github/actions/workflow/status/vvvvvdal/mlops-cicd-turtlebot/pipeline.yml?label=CI%2FCD%20Pipeline)

A ideia aqui é simples, mas resolve um problema gigante: como garantir que a IA que controla o robô físico (o Turtlebot) não tome decisões absurdas (alucinações) e faça o robô bater na parede? 

Criamos uma esteira de **Integração Contínua (CI/CD)**. Antes de qualquer código ou modelo de IA ir para o robô, ele passa por uma bateria de testes virtuais. Se o robô virtual "bater" na parede, o deploy é cancelado e o hardware físico fica a salvo.

## 💻 Como testar

1. Instale as dependências necessárias:
```bash
pip install -r requirements.txt
```

2. Rode a bateria de testes de segurança com o Pytest:
```bash
pytest tests/ -v --log-cli-level=INFO
```
