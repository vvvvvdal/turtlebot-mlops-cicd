# 🐢 Turtlebot (MLOps - CI/CD)

![Python](https://img.shields.io/badge/Python-3.10-blue)
![ROS 2](https://img.shields.io/badge/ROS_2-Humble-22314E)
![CI/CD](https://img.shields.io/github/actions/workflow/status/vvvvvdal/mlops-cicd-turtlebot/pipeline.yml?label=CI%2FCD%20Pipeline)

A ideia aqui é simples, mas resolve um problema gigante: como garantir que a IA que controla o robô físico, Turtlebot, não alucine e não faça o robô bater na parede?

Criamos um sistema de CI/CD. Antes de qualquer código ou modelo de IA ir para o robô físico, ele passa por uma bateria de testes virtuais. Se o robô virtual "bater" na parede ou ignorar normas de segurança na simulação, o deploy é cancelado e o robô físico fica protegido.

---

## 🐳 Como testar via Docker (Recomendado)

Para manter sua máquina limpa e evitar conflitos de dependências, todo o ambiente de testes (ROS 2 Humble, Ollama, Turtlesim e OpenCV) está configurado via Docker Compose.

### 1. Inicializando o Ambiente

Primeiro, permita que os containers acessem a interface gráfica do seu host Linux (para abrir a janela do Turtlesim):

```bash
xhost +local:root
```

Suba os containers Ollama e ROS2 em background:

```bash
docker compose up --build -d
```

Na primeira vez, faça o pull do modelo LLM local (`qwen2.5:1.5b`) no container do Ollama:
Se for a primeira vez, aparecerá a mensagem ">>> Send a message". Digite "/bye" ou pressione "CTRL + d" para sair.
```bash
docker exec -it ollama_local ollama pull qwen2.5:1.5b
```


### 2. Executando a Simulação (Navegação Autônoma)

Para rodar a simulação interativa, você precisará de dois terminais abertos lado a lado.

**Terminal 1 — Iniciar o Turtlesim**

Isso abrirá a janela azul do simulador gráfico do ROS 2:

```bash
docker exec -it ros_turtlesim bash -c "source /opt/ros/humble/setup.bash && ros2 run turtlesim turtlesim_node"
```

**Terminal 2 — Iniciar o Agente de Decisão**

Execute o script de navegação autônoma. O terminal pausará e solicitará que você digite interativamente o peso (qualidade) do modelo Ollama:

```bash
docker exec -it ros_turtlesim bash -c "source /opt/ros/humble/setup.bash && python3 src/turtlesim_navegacao.py"
```

- ✅ **Teste rprovado:** Digite um peso `>= 8`. O modelo se comportará bem, evitará as paredes usando as leituras do LiDAR simulado, e o deploy será liberado.
- ❌ **Teste reprovado:** Digite um peso `< 8`. Isso simula um modelo com pesos ruins, que ignorará as ordens de segurança e colidirá. O deploy será bloqueado.

---

## 💻 Como testar localmente (Bare Metal)

Caso prefira rodar diretamente no seu sistema operacional (sem Docker), siga os passos abaixo.

### Testes Unitários de Segurança

1. Instale as dependências Python necessárias:

```bash
pip install -r requirements.txt
```

2. Rode a bateria de testes com o Pytest:

```bash
pytest tests/ -v --log-cli-level=INFO
```

### Testando na Simulação Visual (Frontend HTML)

Para validar apenas a lógica de decisão e o visual sem precisar carregar todo o ecossistema ROS 2, você pode usar o dashboard interativo:

```bash
xdg-open simulacao_mapa.html
```