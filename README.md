# Invoice-Generator-APP
Invoice generator made on Flask.

## Project description

Hi everyone! This is my first flask project. Its web application which allows you create and download invoice in PDF format.

### Functionality
* Create invoice
* Invoice payment counter
* Preview all invoices
* Delete invoice
* Transfer invoice from html to PDF and download it


### Stack
* Python 3
* Flask



### Installation

Download or clone repository from GH. Install libraries from requirements.txt, to do this open your terminal and type:
```
pip install -r requirements.txt
```

After that you have to create database, to do this type in python console:
```
from app import db, app
db.create_all(app=app)
```

Finally you can start application, to do this you must do following steps:

Linux:

```
$ export FLASK_DEBUG=1
$ export FLASK_APP=app
$ flask run
```

Windows:

```
> set FLASK_DEBUG=1
> set FLASK_APP=app
> flask run
```

Account name and password for testing application is : admin/admin

If you want create your own user you have to add it manually to database.

### Sample photos of application
#### Login:
<img src="https://i.ibb.co/b1CW1Mn/login-page.jpg" alt="login-page" height="280" width="600">

#### Admin panel:
<img src="https://i.ibb.co/7JYcCQg/admin-panel-page.jpg" alt="admin-panel-page" height="280">

#### Add invoice:
<img src="https://i.ibb.co/NYLDr3q/add-invoice-page.jpg" alt="add-invoice-page" height="280">

#### Preview:
<img src="https://i.ibb.co/7jQt3fw/preview-invoice-page.jpg" alt="preview-invoice-page" height="280">

#### Preview pdf format:
<img src="https://i.ibb.co/1JTDzGk/pdf-preview-page.jpg" alt="pdf-preview-page" width="600">


__Enjoy!__

__Contact:__

>zitarukm@gmail.com
