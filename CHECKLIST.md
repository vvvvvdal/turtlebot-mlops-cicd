# Checklist

## 🏗️ Estrutura Principal
- [x] **O Script de Inferência**: Lógica de leitura de sensores e processamento com IA Local (Ollama + Visão Mock).
- [x] **A Bateria de Testes**: Cobertura de testes (`Pytest`) para barrar alucinações e checar confiança da visão.
- [x] **O Container Docker**: Infraestrutura (Dockerfile) que empacota as dependências de sistema e o Python.
- [x] **O Arquivo YAML**: GitHub Actions que orquestra a automação do CI/CD na nuvem.

---

## 🛠️ Tarefas Extras

- [x] **Tarefa 1: Automação da Experiência (DevOps)**
  - O que: Colocar um *timeout* de segurança de 1.5s na requisição da IA. Se demorar, o robô para.
- [ ] **Tarefa 2: Otimização da Esteira (Opcional)**
  - O que: Adicionar o passo de *Cache* no GitHub Actions para acelerar o tempo de build do pipeline.