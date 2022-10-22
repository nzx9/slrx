# SLRX (_Sign Language Recorder X_)

* Originally developed as [DSC](<https://github.com/nzx9/DSC>)
* Improved DSC by adding video of sign need to record and released [SLRX][slrx].

[![SLRX Repo Card](https://github-readme-stats.vercel.app/api/pin/?username=nzx9&repo=slrx&show_owner=true)](https://github.com/nzx9/slrx)

## Hosted On

[![Heroku](https://img.shields.io/static/v1?message=heroku&logo=Heroku&labelColor=FFF&color=430098&logoColor=430098&style=for-the-badge&label=%20)](https://slrx-pro.herokuapp.com)

## Built for

SLRX is built for Collect Dynamic Signs Remotly for

* Machine Learning Tasks
* Validating Data
* Many More..

## Packages used

SLRX uses a number of open source projects to work properly:

* [Django] - Python Web Framework
* [Sementic UI] - awesome modern CSS
* [Firebase] - as file storage
* [jQuery] - for frontend actions

_For Python dependencies view [requirement.txt](https://github.com/nzx9/slrx/blob/main/requirements.txt)_

SLRX itself is open source with a [public repository][slrx] on GitHub.

## Installation

DSC requires [Python](https://python.org/) v3.6+ to run.

Install the requiements and start the server.

### **For Linux/ MacOS (BASH/ ZSH)**

```sh
git clone https://github.com/krypto-i9/slrx.git
cd slrx
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
./manage.py runserver
```

Then open browser and goto

```sh
127.0.0.1:8000
```

### **For Windows (CMD)**

Download and Extract the [SLRX][slrx].
Then run this in CMD

```cmd
cd slrx
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python manage.py runserver
```

Then open browser and goto

```sh
127.0.0.1:8000
```

### Docker

Docker Not Available Yet.

## License

[BSD-3-Clause License][license]

[django]: https://www.djangoproject.com/
[sementic ui]: https://semantic-ui.com/
[firebase]: https://firebase.com/
[jquery]: https://jquery.com
[license]: https://github.com/nzx9/dsc/blob/main/LICENSE
[slrx]: https://github.com/nzx9/slrx
