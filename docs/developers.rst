Development
===========

How to install the requirements
-------------------------------

A list of all requirements is available in `REQUIREMENTS.txt 
<https://github.com/cidles/poio-corpus/blob/master/REQUIREMENTS.txt>`_.

Linux/Ubuntu only.


For the corpus generation and prepartion of language models
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Some packages are installed with apt-get:

* python-lxml
* python-numpy
* python-scipy
* python-presage

Example::

$ sudo apt-get install python-lxml

Some packages are installed with `easy_install 
<https://pypi.python.org/pypi/setuptools>`_:

* requests
* beautifulsoup
* poio-api
* graf-python
* rdflib
* config
* cython
* sparsesvd
* regex
* s3cmd

Example:: 

$ sudo easy_install requests


For the Webapp
++++++++++++++

This will install all requirements and prepare the Webapp for launch.


Initialize your enviroment
..........................

Bootstrap the buildout environment::

$ python bootstrap.py

Install all dependencies via buildout::

$ bin/buildout


Get language data from server
.............................

Download data from Amazon::

$ python s3get.py

At this moment an Amazon AWS account is required.


Run the tests
.............

::

$ bin/test


Launch the server in development mode
.....................................

Launch the server::

$ bin/flask-ctl debug fg
