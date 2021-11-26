# Team-Project-CMPUT404
## Team Member
CCID | NAME
---- | ---- 
wwu3|Weiyi Wu
hhong1|Haoyang Hong
bingran1|Bingran Huang
zhengyao|Zhengyao Zhang
liu9|Hao Liu

https://github.com/CMPUT404FaLL2021/team-project-404

### LAB Section
LAB 802 Team-13

## The project is running on Heroku

https://cmput404-team13-socialapp.herokuapp.com/socialapp/index

## Wiki
>  include API Document and Test Document

https://github.com/CMPUT404FaLL2021/team-project-404/wiki/Home-Wiki

>  Here is the swagger includes API Overview

https://cmput404-team13-socialapp.herokuapp.com/swagger/

## Installation
> Create a virtualenv and activate the python virtual environment

```
>$ virtualenv venv --python=python3

>$ source venv/bin/activate
```
> Download the project and install all libraries that are needed

```
>$ git clone https://github.com/CMPUT404FaLL2021/team-project-404.git

>$ pip install -r requirements.txt
```
> Migrate all the changes if there are any
> 
> Create superuser (this will be the admin on server)
> 
> Run the server on localhost
```
>$ python manage.py migrate

>$ python manage.py createsuperuser

>$ python manage.py runserver
```
> If you made any changes to the Django model, please run the follow to commiting all those changes to the actual SQL database

```
>$ python manage.py makemigrations

>$ python manage.py migrate
```
## How To Use?
### Some Idea and Design about this Project

This project theme is distributive social network, so we follow the specification idea that each server is independent from each other and hosting only the posts information that is made by its own server user and also hosting each own server user's userprofile. Each server does not store any extra information about other server's user and posts except we store the url(api) that we can request for the data.

### How to get an account?

You will first need to get into the signup page and register an account. And then you will need to wait for one of the Admin to give you permission to log into the main home page. Or you can create a super user which will be the admin on the server as default. But other new sign up users will still need to grant permission to access the home page(login).

For accepting new sign up user's request for granting permission to access homepage(login), you must first have a super user account and then go to the admin page by "/admin" and then go to the User table and find the users you want to grant permission to and click into it and check the active.

### How to be friends?

In this project, the definition of real friend is if two users are following each other. Our way of handling friend is to only keep one direction followship in each server. Each server will only store who their user is following but does not know who is following them since the other server will have that. In such way, handling friends across different servers are actually way easier. When validating friend lists we send request to other servers to verify if that user is also following him/her to get the two diretion followships.

## Collaboration

## External Source Referenced
### Reference link:

#### API Related:

https://www.django-rest-framework.org/

https://docs.djangoproject.com/en/3.2/ref/

REST API: https://www.youtube.com/playlist?list=PLgCYzUzKIBE9Pi8wtx8g55fExDAPXBsbV

***

#### CSS Related:

color and desige : https://uigradients.com/#CalmDarya

https://codepen.io/ChynoDeluxe/ Chyno Deluxe August 24, 2015 Dependencies:font-awesome.css

***

#### Function Related:

login function: 

https://learndjango.com/tutorials/django-login-and-logout-tutorial

Register function:

https://wsvincent.com/django-user-authentication-tutorial-signup/

Edit Prifrofile:

https://wsvincent.com/django-user-authentication-tutorial-password-reset/

Like function: 

https://morioh.com/p/626428a91af5





