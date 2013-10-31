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
* python-matplotlib

Example::

$ sudo apt-get install python-lxml

Some packages are installed with `easy_install 
<https://pypi.python.org/pypi/setuptools>`_:

* requests
* beautifulsoup
* graf-python
* rdflib
* config
* cython
* sparsesvd
* regex
* s3cmd
* flask-mobility

Example:: 

$ sudo easy_install requests

Some must be downloaded from github:

* presagio
* poio-api

These are avaiable at: `https://github.com/cidles 
<https://github.com/cidles>`_

To install the packages run::

$ sudo python setup.py install


For the Webapp
++++++++++++++

This will install all requirements and prepare the Webapp for launch.


Initialize your enviroment
..........................

Bootstrap the buildout environment::

$ python bootstrap.py

Install all dependencies via buildout::

$ sudo bin/buildout


Get language data from server
.............................

Download data from Amazon::

$ python get_corpus_data.py


Run the tests
.............

::

$ bin/test


Launch the server in development mode
.....................................

Launch the server::

$ bin/flask-ctl debug fg
