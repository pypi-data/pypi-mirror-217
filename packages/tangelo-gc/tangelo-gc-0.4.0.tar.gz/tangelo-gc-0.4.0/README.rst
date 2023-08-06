|tangelo_logo|

.. |tangelo_logo| image:: ./docs/source/_static/img/tangelo_logo_gradient.png
   :width: 600
   :alt: tangelo_logo

|maintainer| |licence| |systems| |dev_branch|

..
    |build|

.. |maintainer| image:: https://img.shields.io/badge/Maintainer-GoodChemistry-blue
   :target: https://goodchemistry.com
.. |licence| image:: https://img.shields.io/badge/License-Apache_2.0-green
   :target: https://github.com/goodchemistryco/Tangelo/blob/main/LICENSE
.. |systems| image:: https://img.shields.io/badge/OS-Linux%20MacOS%20Windows-7373e3
.. |dev_branch| image:: https://img.shields.io/badge/DevBranch-develop-yellow
.. |build| image:: https://github.com/goodchemistryco/Tangelo/actions/workflows/continuous_integration.yml/badge.svg
   :target: https://github.com/goodchemistryco/Tangelo/actions/workflows/continuous_integration.yml

Welcome !

Tangelo is an open-source and free Python package maintained by `Good Chemistry Company <https://goodchemistry.com>`_, focusing on the development of end-to-end material simulation workflows on quantum computers.

Tackling chemical systems with quantum computing is not easy. Leveraging pre- and post-processing techniques as well as insights from classical calculations remain necessary, in order to make
non-trivial use cases computationally tractable, and develop efficient approaches returning accurate results on simulators or quantum devices.
Assembling the different building blocks to form and explore workflows that meet these constraints is where Tangelo strives to be of
help.

|workflow|

.. |workflow| image:: ./docs/source/_static/img/quantum_workflow.png
   :width: 700
   :alt: tangelo_workflow

This package provides a growing collection of algorithms and toolboxes, including problem decomposition, to support the development of new approaches and the design of successful experiments on quantum devices. Tangelo is backend-agnostic,
so that users can write code once and experiment with current and future platforms with minimal changes.

Tangelo is capable to perform quantum experiments that led to `peer-reviewed work <https://www.nature.com/articles/s42005-021-00751-9>`_
published in scientific journals, co-authored by professionals from the chemical industry and quantum hardware manufacturers.

|curve|

.. |curve| image:: ./docs/source/_static/img/curve_dmet_qcc.png
   :width: 400
   :alt: curve

We hope to grow a healthy community around Tangelo, collaborate, and together leverage the best of what the field has to offer.

- Our `release document on arXiv <https://arxiv.org/abs/2206.12424>`_.
- Our `Sphinx documentation <http://tangelo-docs.goodchemistry.com>`_.
- Our `examples repository <https://github.com/goodchemistryco/Tangelo-Examples>`_.

What will you do with Tangelo ?

Install
-------

This package requires a Python 3 environment. We recommend:

* using `Python virtual environments <https://docs.python.org/3/tutorial/venv.html>`_ in order to set up your environment safely and cleanly
* installing the "dev" version of Python3 if you encounter missing header errors, such as ``python.h file not found``.
* having good C/C++ compilers and BLAS libraries to ensure good overall performance of computation-intensive code.



Using pip
^^^^^^^^^

The easiest way to install Tangelo in your local environment. We recommend upgrading pip first:

.. code-block::

   python -m pip install --upgrade pip.
   pip install tangelo-gc

If you'd like to install via pip the code in a specific branch of this Github repository (let's say ``develop``)

.. code-block::

   pip install git+https://github.com/goodchemistryco/Tangelo.git@develop

From source, using setuptools
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This package can be installed locally by copying the contents of this repository to any machine. This can be useful if you need a bit more control on your install (such as installing from a particular branch, or tweaking the ``setup.py`` install to circumvent any issue on your system).
Type the following command in the root directory:

.. code-block::

   python -m pip install .

If the installation of a dependency fails and the reason is not obvious, we suggest installing that dependency
separately with ``pip``\ , before trying again.

With Docker
^^^^^^^^^^^

Use our Docker file to deploy Tangelo in a Linux environment, either retrieved from pip or mounted locally. Comment / uncomment the relevant sections of the Dockerfile to control installation and dependencies.

"No install" notebook method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Check out the tutorial section below to see how services such as Google Colab, Binder or JupyterLab may help you circumvent local installation challenges or go beyond the compute capabilities of your laptop.

Optional dependencies: Quantum Simulators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Tangelo enables users to target various backends. In particular, it integrates quantum circuit simulators such as ``qulacs``\ , ``qiskit``\ , ``cirq`` or ``qdk``. We leave it to you to install the packages of your choice, and refer to their own documentation. Most packages can be installed through pip or conda in a straightforward way.


Optional dependencies: Classical Quantum Chemistry Packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Tangelo can be used without having a classical quantum chemistry package installed but many algorithms, by default, depend on one being installed. The two quantum chemistry packages that are natively supported are `PySCF <https://pyscf.org/>`_ and `Psi4 <https://psicode.org/>`_.

You are also welcome to provide your own interface to a quantum chemistry package of your choice by defining a subclass of `IntegralSolver <https://github.com/goodchemistryco/Tangelo/blob/develop/tangelo/toolboxes/molecular_computation/integral_solver.py>`_. An example of this can be found in `this test <https://github.com/goodchemistryco/Tangelo/blob/develop/tangelo/toolboxes/molecular_computation/tests/test_molecule.py#L167>`_.


Quick note for Windows users
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Depending on your OS and environment, some of the optional packages may be more challenging to install. If you are using Windows, we recommend you install the `Windows Linux Subsystem <https://docs.microsoft.com/en-us/windows/wsl/install>`_, which allows you to run Ubuntu as an application. Once it has been installed, you can type ``explorer.exe`` in your Ubuntu terminal to drag and drop files between your Windows and Linux environment. Here are a few essentials to install inside a brand new Ubuntu environment, before trying to install Tangelo:

.. code-block::

   sudo apt update && sudo apt upgrade
   sudo apt-get install python3-dev
   sudo apt-get install python3-venv
   sudo apt-get install cmake unzip


Optional: environment variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some environment variables can impact performance (ex: using GPU for quantum circuit simulation, or changing the number of CPU threads used) or are used to connect to web services providing access to some compute backends.

See the list of relevant environment variables and their use in ``env_var.sh``. In order for these variables to be set to the desired values in your environment, you can run this shell script in Linux with the following command line:
``source env_var.sh`` (you may need to set execution permissions with ``chmod +x set_env_var.sh`` first), or you can set them in whatever way your OS supports it, or even inside your python script using the ``os`` package.

Tutorials and examples
----------------------

We have a `dedicated repository <https://github.com/goodchemistryco/Tangelo-Examples>`_ for examples and tutorials !

We wrote a number of them, and tried to provide material that doesn't just explain how to use the software, but provides insights into the complex topics of chemistry, quantum computing, and digs into the challenges we encountered in our previous hardware experiments. Nothing prevents users from contributing and showcasing what they have been doing with Tangelo.

You can visualize notebooks directly on Github, most of them have been pre-run.
If you'd like to be able to run them locally, we suggest you use `Jupyter notebooks inside a virtual environment <https://janakiev.com/blog/jupyter-virtual-envs/>`_.

- Install Jupyter and ipykernel in your environment:
.. code-block::

   pip install jupyter ipykernel

- To make sure the notebooks allow you to set the kernel corresponding to your virtual environment:
.. code-block::

   python -m ipykernel install --user --name=myenv

Jupyter notebooks can also be displayed and executed in the cloud, with services such as Google Colab. This removes the constraint of building a local development envrionement, and enables users to run interactive notebooks on machines that may provide a better configuration than their own (more RAM, compute power, access to GPUs...). This may come in handy for users who want to get started quickly, especially for quick tests, demos and tutorials.

Check out our `tutorials <./TUTORIALS.rst>`_ file for more details.

Tests
-----

Unit tests can be found in the ``tests`` folders, located in the various toolboxes they are related to. To automatically find and run all tests (assuming you are in the ``tangelo`` subfolder that contains the code of the package):

.. code-block::

   python -m unittest


Contributions
-------------

Thank you very much for considering contributing to this project; we'd love to have you on board !
You do not need to be a seasoned software developer or expert in your field to make contributions to this project: it will take various kinds of people and backgrounds to tackle the challenges that await us.

However we need some guidelines and processes to ensure that we build something of quality for the community. We describe them in the `contributions <./CONTRIBUTIONS.rst>`_ file.
There are many ways you can contribute, but in case you're considering contributing to the codebase: don't be scared of the infamous pull request process ! It can feel intimidating, but we've had a few researchers or high-schoolers go through their first one and... they came back for more ! Mostly.

You can use the `Issue tab <https://github.com/goodchemistryco/Tangelo/issues>`_ to open a bug report or feature request. If you're not sure, starting a discussion in the `Discussion tab <https://github.com/goodchemistryco/Tangelo/discussions>`_ is a good start: we'll figure it out from there.

By joining the Tangelo community and sharing your ideas and developments, you are creating an opportunity for us to learn and grow together, and take ideas to the finish line and beyond.

Citations
---------

If you use Tangelo in your research, please cite:

   Valentin Senicourt, James Brown, Alexandre Fleury, Ryan Day, Erika Lloyd, Marc P. Coons, Krzysztof Bieniasz, Lee Huntington, Alejandro J. Garza, Shunji Matsuura, Rudi Plesch, Takeshi Yamazaki, and Arman Zaribafiyan Tangelo: An Open-source Python Package for End-to-end Chemistry Workflows on Quantum Computers 2022 arXiv:2206.12424

© Good Chemistry Company 2023. This software is released under the Apache Software License version 2.0.
