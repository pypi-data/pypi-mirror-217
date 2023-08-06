.. _anaconda_jupyter:

===============================
Set up Anaconda and Jupyter Lab
===============================

Most computer languages are supported by a plethora of 3rd-party libraries,
frameworks, and extensions.  These packages of code are in turn supported by
package managers.  With Python, there are several package managers available,
including the long used Pip, and the ascendent Pipenv.  In additon, many
platform package managers, like DNF and APT on Linux, and Homebrew on MacOS,
support the installation of a subset of Python packages.

In the Data Science community, the most commonly used package manager is
Anaconda.  There's good reason for this - Anaconda supports over 1,500 Data
Science packages, written in Python and R, and optimized for delivery across
MacOS, Linux, and Windows.  It also comes with the Anaconda Navigator
Graphical User Interface, which some will find a refreshing alternative to
managing their computing environments from the Command Line Interface.  If
you prefer the CLI - don't worry - your Anconda installation will provide that
too.  Now, let's get started!

**1. Download Anaconda for your platform**

    Go to https://www.anaconda.com/download and download the appropriate
    version of Anaconda for your platform.

**2. Install Anaconda**

    On MacOS and Windows, the file you downloaded above will launch an install
    wizard that will quickly step you through the install process.  As with
    most things Linux, a wizard installer is not available, but if you're
    using Linux, you won't find this install particularly taxing.  Anaconda
    provides a self-extracting shell script for installation on Linux.  If you
    would like to see the Anconda Documentation on the Installation process,
    it is available here: https://docs.anaconda.com/free/anaconda/install/

**3. Launch Anaconda Navigator and Sign-in to Anaconda Cloud**

    When you lauch Anaconda Navigator, you will be presented with a window
    similar to this one, below.  Yours will probably look slightly different,
    as I have been using mine during the development of of PyMBS.


    .. figure:: _images/anaconda_navigator.jpg
        :width: 800px
        :height: 464px
        :align: center
        :alt: Anaconda Navigator

        *Anaconda Navigator*

    In the upper-right corner, you see a button that will allow you to sign-in
    to Anaconda Cloud. You don't need to an Anaconda Cloud account to use
    Jupyter and PyMBS, but sign-up is free.  If you don't have an account,
    navigate over to https://anaconda.org/ in your web browser and sign-up for
    one.  After you've done that, come back to the Anaconda Navigator and
    Sign-in.

**4. Create a new environment for your modeling work**

    In Anaconda Navigator, click on the *Environments* tab in the left-hand
    navigation bar.  You should see something similar to the image below.  If
    this is your first time using Anaconda, you will only see the
    ``base (root)`` environment.  In the picture below, you'll see a second
    one called ``pymbs``, which is the one that I use for developing this
    framework.


    .. figure:: _images/anaconda_environments.jpg
        :width: 800px
        :height: 464px
        :align: center
        :alt: Anaconda Environments

        *Anaconda Environments*

    Click on the ``Create`` button at the bottom of the environments list and
    create an environment to use for running the MBS models.  You can call it
    anything you like, such as ``MBS`` or ``cmo_modeling`` or
    ``the_puzzle_factory`` (spaces in the name are not allowed, but underscores
    are).  Select ``Python 3.7`` as your interpreter.  After you create this,
    you will add some packages to it to help run your models.

    .. figure:: _images/create_new_env.jpg
       :width: 480px
       :height: 265px
       :align: center
       :alt: Create New Environment

       *Create New Environment*

**5. Add some packages to your environment.**

    After creating your new environment, you'll find that Anaconda went ahead
    and added about 17 packages or so as part of the initial setup. These are
    basic packaages that most if not all environments are going to need.
    To model structured cash flows in Jupyter Lab, we'll need to add a few
    more.

    First, let's add the PyMBS package.  As a package manager, Anaconda will
    be aware of any packages that ``pymbs`` is dependent upon, so adding
    ``pymbs`` will add those packages that it depends on as well.

    With so many packages out there, the possibility of two (or more) developers
    choosing the same name for their package is not unrealistic.  In order to
    handle these name collisions gracefully, Anaconda employs *channels*, aka
    *namespaces*. There are two main channels included in the initial install
    of Anaconda.  These channels contain most of the heavily used, well-known
    packages, like OpenSSL, Pandas, and NumPy.

    For newer, lesser known packages like ``pymbs``, the developer creates their
    own channel and supplies the package through that.  In order to download
    ``pymbs``, click on the ``Channels`` button in the top center of the
    Anaconda Navigator window. When the new window opens, click on the
    ``Add`` button and enter ``btf``, then click the ``Update Channels`` button
    to complete the addition.

    .. figure:: _images/add_channel.jpg
       :width: 465px
       :height: 334px
       :align: center
       :alt: Create New Environment

       *Add the btf Channel*

    Now that you've added the ``btf`` channel, Anaconda has access to the
    ``pymbs`` package.

    In the pull-down menu to the left of the ``Channels`` button, select
    ``Not installed``.  In the ``Search Packages`` field on the right,
    search for ``pymbs``.  When ``pymbs`` shows-up in the results, check
    the box on the left side of its row and click on the ``Apply`` button,
    in the lower-right-hand corner of the window.

    .. figure:: _images/install_pymbs.jpg
       :width: 800px
       :height: 464px
       :align: center
       :alt: Install PyMBS

       *Install PyMBS*

    Some machinations will ensue, as Anaconda determines the dependencies for
    ``pymbs`` that will also need to be installed.  In the end, you will be
    presented with a list of the packages to be installed.  Click ``Apply``.

    .. figure:: _images/install_packages.jpg
       :width: 428px
       :height: 409px
       :align: center
       :alt: Install Packages

       *Install Packages*

    Even though we are using Jupyter Lab to explore PyMBS, ``pymbs`` is not
    not actually dependent on ``jupyterlab``, so ``jupyterlab`` is still not
    installed. Go ahead and run through the steps above again that you used to
    install ``pymbs``, this time searching for and installing ``jupyterlab``.

    That's it! But it's not time to start up Jupyter Lab just yet.  In the
    next section, we'll clone the repo for the cash flow model and then things
    will really start humming along...

:ref:`setup_modeling`
