<h1 align="center">
Summary-youtube
</h1>

## 💻 Projeto

Aplicação para resumo de vídeos no youtube utilizando ChatGPT da OpenAI por trás. Atenção que o token da OpenAI pode ficar limitado pela conta ser free e não irá retornar resumos!!

## 🔨 Implementações

- [x] Obter transcrição do vídeo
- [x] Pela quantidade máxima de tokens da versão free do ChatGPT 3.5 (~4000 tokens), a transcição foi dividida em partes
- [x] Retorno do resumo da transcrição

## 🎨 Layout

Para essa aplicação, não foi utilizado figma

## ✨ Tecnologias

- [x] Python
- [x] FastAPI
- [x] Youtube Transcript API
- [x] OpenAI Request

## 🌐 Deploy

[Link do deploy](https://summary-youtube.onrender.com)

## 👨🏻‍💻 Backlog

- [ ] Melhorar resumo com nova conta da OpenAI ou resumo dos resumos. Em alguns casos, a leitura não fica adequada pela divisão do transcição ficar curta
- [ ] Colocar opção para outros idiomas (prioritariamente inglês)

## 👨🏻‍💻 Rodar localmente

### Como rodar localmente?
#### Habilitar o .env de acordo com o example. O token da Api é obtido dentro do site pela sua conta. O Token é o mesma que vai no .env do seu front. Ele entra como token nos requests. Coloquei apenas obter uma trava dentro da próprio env se eu quiser.

#### Localmente:  Depois de criar seu venv e instalar os requirements: uvicorn app.main:app --reload

#### Docker:  

docker build -t 'nome-da-image' .

docker run -d --name 'nome-do-container' -p 80:80 'nome-da-imagem'

