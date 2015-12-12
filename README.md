# awstrabsd
Trabalho de Sistemas Distribuídos para aprender a usar alguns serviços do AWS, na qual um webservice em cherrypy hospedado em uma vm do EC2 se comunica com o S3 e com o DynamoDB

Passos para execultar esse projeto

1. Instale as bibliotecas

pip install cherrypy<br>
pip install jinja2<br>
pip instal awscli<br>

2. Configure o aws

aws configure<br>

3. Crie a tabela no DynamoDB

python create_table.py<br>

4. Execulte o projeto

python cherrySD.py<br>
