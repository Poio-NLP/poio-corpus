Development
===========

How to install the requirements
-------------------------------

You can find a list of all requirements in `REQUIREMENTS.txt 
<https://github.com/cidles/poio-corpus/blob/master/REQUIREMENTS.txt>`_.

This documentation is for Linux/Ubuntu only.


For the corpus generation and prepartion of language models
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

You need to install the following packages with `apt-get`:

* python-lxml
* python-numpy
* python-scipy

For example::

$ sudo apt-get install python-lxml

You need to install the following packages with `easy install
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

For example:: 

$ sudo easy_install requests

In addition, some packages must be downloaded from github:

* presagio
* poio-api

These are avaiable at: `https://github.com/cidles 
<https://github.com/cidles>`_

To install the packages run::

$ sudo python setup.py install