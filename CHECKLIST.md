# Checklist

## 🏗️ Estrutura Principal
- [x] **O Script de Inferência**: Lógica de leitura de sensores e processamento com IA Local (Ollama + Visão Mock).
- [x] **A Bateria de Testes**: Cobertura de testes (`Pytest`) para barrar alucinações e checar confiança da visão.
- [x] **O Container Docker**: Infraestrutura (Dockerfile) que empacota as dependências de sistema e o Python.
- [x] **O Arquivo YAML**: GitHub Actions que orquestra a automação do CI/CD na nuvem.

---

## 🛠️ Tarefas Extras

- [x] **Tarefa 1: Parametrização de Robótica**
  - O que: Mudar a distância da IA de "hardcoded" (`1.0`) para uma variável global configurável (`DISTANCIA_SEGURA = 1.0`).
- [x] **Tarefa 2: Observabilidade e Auditoria**
  - O que: Adicionar um `FileHandler` no logging do Ollama para salvar um arquivo `.log`.
- [x] **Tarefa 3: Automação da Experiência (DevOps)**
  - O que: Criar um arquivo `Makefile` com atalhos fáceis para instalar, testar e rodar o projeto.
- [x] **Tarefa 4: Failsafe de Latência**
  - O que: Colocar um *timeout* de segurança de 1.5s na requisição da IA. Se demorar, o robô para.
- [x] **Tarefa 5: Sanitização da Saída da IA**
  - O que: Criar uma regra (regex/split) para garantir que a saída enviada ao robô é *apenas* o comando, ignorando falas extras da IA.
- [ ] **Tarefa 6: Otimização da Esteira (Opcional)**
  - O que: Adicionar o passo de *Cache* no GitHub Actions para acelerar o tempo de build do pipeline.

# Checklist

## 🏗️ Estrutura Principal
- [x] **O Script de Inferência**: Lógica de leitura de sensores e processamento com IA Local (Ollama + Visão Mock).
- [x] **A Bateria de Testes**: Cobertura de testes (`Pytest`) para barrar alucinações e checar confiança da visão.
- [x] **O Container Docker**: Infraestrutura (Dockerfile) que empacota as dependências de sistema e o Python.
- [x] **O Arquivo YAML**: GitHub Actions que orquestra a automação do CI/CD na nuvem.

---

## 🛠️ Tarefas Extras

- [ ] **Tarefa 1: Parametrização de Robótica**
  - O que: Mudar a distância da IA de "hardcoded" (`1.0`) para uma variável global configurável (`DISTANCIA_SEGURA = 1.0`).
- [ ] **Tarefa 2: Observabilidade e Auditoria**
  - O que: Adicionar um `FileHandler` no logging do Ollama para salvar um arquivo `.log`.
- [ ] **Tarefa 3: Automação da Experiência (DevOps)**
  - O que: Criar um arquivo `Makefile` com atalhos fáceis para instalar, testar e rodar o projeto.
- [ ] **Tarefa 4: Failsafe de Latência**
  - O que: Colocar um *timeout* de segurança de 1.5s na requisição da IA. Se demorar, o robô para.
- [ ] **Tarefa 5: Sanitização da Saída da IA**
  - O que: Criar uma regra (regex/split) para garantir que a saída enviada ao robô é *apenas* o comando, ignorando falas extras da IA.
- [ ] **Tarefa 6: Otimização da Esteira (Opcional)**
  - O que: Adicionar o passo de *Cache* no GitHub Actions para acelerar o tempo de build do pipeline.
