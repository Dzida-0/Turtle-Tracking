# Plan
- host app using docker and aws
- use cd on marge to main for deployment
- use ECR free tier
- use EC2 free tier
- use RDS Postgate free tier
- use ECS Monitoring free tier
- use adiciopnal storage for photos and json
- use aws lambda free tier for updating database and sending emails

# Curent project shemat:
## run.py <- run app 
## config.py <- configurate app 
## data
### raw <- json
### __init__.py
### data_parsing.py <- should be operated by lambda
### data_download.py <- should be operated by lambda
## instance
### database.db <- local database
## tests <- folder with pytest
## app
### __init__.py <- app initialisation
### errors.py <- 404, 500 errors handeling
### extensions.py
### models.py <- database models
### forms.py <- Login , register forms
### routes <- flask blueprints
### static <- scss files, .js files, photos
### templates <- html templates