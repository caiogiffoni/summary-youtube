# summary-youtube

docker build -t summarize-it .

docker run -d --name summarize-it -p 80:80 summarize-it

uvicorn app.main:app --reload
