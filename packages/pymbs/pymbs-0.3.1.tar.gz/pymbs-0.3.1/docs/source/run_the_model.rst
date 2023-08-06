.. _run_the_model:

=============
Run the Model
=============

PyMBS is intended to be a framework for modeling the structured cash flows
of Mortgage Backed Securities. In order to develop a Proof of Concept in a
rather short period of time, the decision was made to lean on Jupyter Lab as
the front end for the application.  It should be noted however that PyMBS
could just as easily be integrated into a Microservice framework to support
a RESTful API and a web front end. (Jupyter Lab itself relies in part
on `ReactJS <https://reactjs.org/>`_).

As with most things related to Microsoft Windows, running Jupyter Lab requires
a special workflow, which is dicussed further down, in Step #6.  If you are
working on a MacOS or Linux machine, the following steps will get you up and
running in Jupyter Lab:

**1. Open up a terminal window**

    Open a terminal window and ``cd`` into the fhl2618 directory that holds
    the cloned repo of the model files.

    Once inside the deal directory, type ``jupyter lab`` at the command line
    and hit ``Enter``. This should launch the Jupyter Lab server and open
    Jupyter Lab in you web browser.

**2. View Jupyter Lab in your web browser**

    Once Jupyter Lab is running, you should see something like this, although
    the theme in your view may be the light theme, rather than the dark theme
    shown here:

    .. figure:: _images/jupyter_lab_initial.jpg
        :width: 800px
        :height: 464px
        :align: center
        :alt: Jupyter Lab Home

        *Jupyter Lab Home*

**3. Open the 2618model.ipynb file**

    In the file list on the left-hand-side, double-click on the
    2618model.ipynb file.  This is the Jupyter Notebook that displays the
    model and it's output.

    If your not familiar with what you are seeing, there is an IPython
    interactive shell inside the notebook. Each numbered "cell" holds a
    command, a series of commands, or the output of a command:

    .. figure:: _images/model_in_jupyter_lab.jpg
        :width: 800px
        :height: 464px
        :align: center
        :alt: Model in Jupyter Lab

        *The fhl2618 model in Jupyter Lab*

**4. Analyze the Model**

    In the first cell, we find 4 import statements that load in some
    code that we wish to make use of inside the notebook. The first 2 imports
    are used to display the assumed collateral cash flows for Group 3 in
    cell #7 of the notebook. The thid statement imports the PyMBS API, which
    is really the only import statement we *need* from ``pymbs``. The fourth
    statement imports the PyMBS ``config`` object, which is imported here only
    so that we can query and update the configuration dynamically.

    In cell #2, we assign the string value ``'fhl2618'`` to the ``series``
    variable, soley as a convenience.

    In cell #3, we call the ``load_deal`` function from the ``pymbs.api``
    module and assign it's return value to the ``terms_sheet`` variable.

    In cell #4 we call the ``load_model`` function from the ``pymbs.api``
    module and assign it's return value to the ``model`` variable.

    At this point, the model is fully loaded and ready to be run.

    Generally speaking, when reverse-engineering a deal, the first thing that
    the modeler attempts to do is to "tie-out" the cash flows on the Principal
    flowing through the deal's "waterfall", or payment rule structure. This is
    most easily done by computing the Weighted Average Lives (WALs) for the
    tranches and checking to see if they match with the counterparty, or, in
    this case, the Prospectus Supplement.

    The WALs for Group 3 are calculated and displayed in cell #5 by calling
    the ``show_wals`` function from the ``pymbs.api`` module.

    The cashlfows can't truly be considered "tied-out" unless you are
    comparing WALs that are calculated to 10 decimal places.  In this case,
    however, the disclosure in the prosupp only shows the WALs calculated to
    1-decimal precision, so that will have to suffice.

    As noted in :ref:`caveats`, the WALs here don't quite tie-out with those
    in the prosupp, but they are reasonably close. Determining the
    cause of this discrepancy is incredibly difficult when working on this
    in isolation, without the benefit of discussion with other Subject
    Matter Experts and checking the calculations in PyMBS against those made
    by a counterparty. The WALs here however are "close enough" to give us
    some degree of confidence in the math used.

    In cells 6 & 7, I demonstrate further functionality of PyMBS by running
    and displayng the Collateral Cash Flows, using the 100 PSA prepayment
    benchmark. Actually, when the cash flows are run in cell #6, they are
    computed for **all** prepayment scenarios given in the
    ``fhl2618_pps.json`` file. I choose to **only** show the cash flows at
    100 PSA in the ``display`` function in cell #7.

    It is possible to take a look at the ``fhl2618_pps.json`` file in
    Jupyter Lab by double-clicking on the file in the file explorer, just
    like you did when you opened the notebook in the beginning.

**5. Explore the Model and the API**
    
    In order to better appreciate what's going on here, you are encouraged to
    further explaore the PyMBS API (:ref:`api`), as well as the model file,
    which can also be viewed in Jupyter Lab:

    .. figure:: _images/model_file.jpg
        :width: 800px
        :height: 464px
        :align: center
        :alt: Viewing the Model file in Jupyter Lab

        *Viewing the Model file in Jupyter Lab*


**6. Special Instructions for Microsoft Windows Users**

    If you are running Microsoft Windows, you can't just open a regular
    Command Prompt or Power Shell window and run ``jupyter lab`` from the
    command line.  You need to open the Start Menu and open one of the
    "Anaconda" versions of the Command Prompt or Power Shell, as shown in the
    screen shot, below:

    .. figure:: _images/freakin_windows.jpg
        :width: 800px
        :height: 464px
        :align: center
        :alt: Running Jupyter Lab in Windows

        *Running Jupyter Lab in Windows*

    After taking this special step to launch Jupyter Lab, it should open
    in your web browser just as it would on the other platforms and everything
    else should work the same from there. It's just this initial launch step
    that is different (as well as some of the file paths, duly noted in other
    parts of this documentation).