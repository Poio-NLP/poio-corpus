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


For the Server
++++++++++++++

This will install all requirements and prepare the Server (`Flask webapp`) for launch.


Initialize your enviroment
..........................

Start by bootstraping the buildout environment::

$ python bootstrap.py

Next you have to install all dependencies using the buildout script::

$ sudo bin/buildout


Get language data from server
.............................

You have to download all the language data from our Amazon server (this may take a while)::

$ python get_corpus_data.py


Run the tests
.............

Before starting the server you should run our tests to ensure that everything is working properly::

$ bin/test


Launch the server in development mode
.....................................

Finally you can launch the server::

$ bin/flask-ctl debug fg



How to get Poio Corpus working on Pycharm
-----------------------------------------

1. Start by creating a new project with the following settings:

   * Project name: Poio Corpus
   * Location: ~/poio-corpus/site/flask-app/src/main/
   * Project type: Flask Project
   * Interpreter: Python 2.7

2. After you press ``Ok`` PyCharm will prompt if you want to create a project from existing sources, press Yes.

3. In order to run the server from PyCharm you need to add a new confguration for the server, to do this: 
	
   * On the menu bar go to ``Run`` and open ``Edit Configurations...``;
   * Press the ``+`` sign and from the dropdown menu choose ``Python``.

4. Fill in the new confifuration with the following settings and press ``Ok``:

   * Name: Poio Corpus Server
   * Script: ``bin/flask-ctl``
   * Script parameters: ``debug fg``
   * Working directory: ``~/poio-corpus/site/flask-app/``

Now every time you want to start the server make sure that the selected configuration on the menu bar is ``Poio Corpus Server`` and just press ``Run`` (play button).