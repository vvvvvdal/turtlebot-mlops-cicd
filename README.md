# 🐢 Turtlebot (MLOps - CI/CD)

![Python](https://img.shields.io/badge/Python-3.10-blue)
![ROS 2](https://img.shields.io/badge/ROS_2-Humble-22314E)
![CI/CD](https://img.shields.io/github/actions/workflow/status/vvvvvdal/mlops-cicd-turtlebot/pipeline.yml?label=CI%2FCD%20Pipeline)

A ideia aqui é simples, mas resolve um problema gigante: como garantir que a IA que controla o robô físico, Turtlebot, não alucine e não faça o robô bater na parede?

Criamos um sistema de CI/CD. Antes de qualquer código ou modelo de IA ir para o robô físico, ele passa por uma bateria de testes virtuais. Se o robô virtual "bater" na parede ou ignorar normas de segurança na simulação, o deploy é cancelado e o robô físico fica protegido.

---

## 🐳 Como testar

Para manter sua máquina limpa e evitar conflitos de dependências, todo o ambiente de testes (ROS 2 Humble, Ollama, Turtlesim e OpenCV) está configurado via Docker Compose.

### 1. Inicializando o Ambiente:

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

### 2. Executando a Simulação:

**Iniciar o Teste**

Execute o script de navegação autônoma. O terminal pausará e solicitará que você digite interativamente o peso (qualidade) do modelo Ollama:

```bash
docker exec -it ros_turtlesim bash -c "source /opt/ros/humble/setup.bash && python3 src/turtlesim_teste.py"
```

- ✅ **Teste rprovado:** Digite um peso `>= 8`. O modelo se comportará bem, evitará as paredes usando as leituras do LiDAR simulado, e o deploy será liberado.
- ❌ **Teste reprovado:** Digite um peso `< 8`. Isso simula um modelo com pesos ruins, que ignorará as ordens de segurança e colidirá. O deploy será bloqueado.

**Finalizar o Teste: encerrar o container**
```bash
docker compose down
```

---

### 4. Testar visualmente

Para validar a lógica de navegação e o visual sem precisar do ecossistema ROS 2 completo, abra o dashboard interativo:

```bash
xdg-open simulacao_mapa.html
```