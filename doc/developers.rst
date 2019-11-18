.. _developers:

Deploy and develop Poio
=======================

Poio Website
------------

The repository is here:

https://github.com/Poio-NLP/poio-site


This will install all requirements and prepare the server (`Flask webapp`) for
launch.

.. _initialize_env:

Initialize your enviroment
..........................

Start creating a virtualenv environment:

.. code-block:: console

  $ virtualenv venv
  $ source venv/bin/activate

Next you have to install all dependencies using pip:

.. code-block:: console

  $ pip install -r requirements.txt


Start the server in development mode
.....................................

Finally you can start the server:

.. code-block:: console

  $ cd src
  $ export FLASK_APP=main
  $ flask run


Poio Corpus
-----------

The repository is here:

https://github.com/Poio-NLP/poio-corpus


Install the requirements for Poio Corpus
........................................

We recommend to create a virtualenv and install all requirements via pip:

.. code-block:: console

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
