# ModuLab

<div align="center">
  <img src="AddInIcon.svg" alt="ModuLab Logo" width="120" />
  <h3>Uma maneira simples de criar peças modulares iniciais para projetos de marcenaria</h3>
</div>

## 🔍 Sobre

ModuLab é um add-in para o Autodesk Fusion 360 que facilita a criação de componentes modulares para projetos de marcenaria, especialmente móveis e armários. Com uma interface intuitiva, o ModuLab permite que você crie rapidamente estruturas básicas que podem ser personalizadas de acordo com suas necessidades.

## ✨ Recursos

- **Criação rápida de armários básicos**: Defina largura, altura, profundidade e espessura do material para criar estruturas de armários com poucos cliques
- **Interface amigável**: Comandos intuitivos com parâmetros claros para facilitar o uso
- **Módulos extensíveis**: Estrutura modular que permite adicionar facilmente novos recursos

## 🚀 Instalação

1. Faça o download ou clone este repositório
2. No Fusion 360, vá para a guia "Ferramentas" > "Add-Ins" > "Scripts e Add-Ins"
3. Clique em "+" e navegue até a pasta do ModuLab
4. Selecione o arquivo "ModuLab.manifest"
5. Clique em "Executar" para iniciar o add-in

## 🛠️ Como Usar

### Armário Básico
1. Na barra de ferramentas, clique no ícone do ModuLab no painel "Inicial"
2. Defina as dimensões desejadas:
   - Largura (em cm)
   - Altura (em cm)
   - Profundidade (em cm)
   - Espessura do MDF (em cm)
3. Clique em "OK" para criar o armário básico

## 🧩 Estrutura do Projeto

```
ModuLab/
├── commands/               # Comandos disponíveis no add-in
│   ├── basicCabinet/      # Comando para criar armários básicos
│   └── inicialUi/         # Interface inicial 
├── lib/                   # Bibliotecas auxiliares
├── config.py              # Configurações do add-in
├── ModuLab.py             # Arquivo principal
└── ModuLab.manifest       # Manifesto do add-in
```

## 📝 Requisitos

- Autodesk Fusion 360 (suporta Windows e Mac)
- Python (incluído no Fusion 360)

## 👨‍💻 Desenvolvimento

Para adicionar novos recursos ao ModuLab:

1. Crie uma nova pasta em `commands/` com a estrutura necessária
2. Adicione o novo módulo ao arquivo `commands/__init__.py`
3. Implemente as funções `start()` e `stop()` no seu módulo

## 📄 Licença

Este projeto é distribuído sob a licença MIT.

## 👤 Autor

Vinicius Antoniassi Salgado

---

<div align="center">
  <p>Construído com ❤️ para marceneiros e designers</p>
</div> 