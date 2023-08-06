.. _setup_modeling:

================================
Set up your Modeling Environment
================================

In the previous section, you installed Anaconda, PyMBS, and Jupyter Lab.
Before we can make use of PyMBS though, we need a structured cash flow model
to explore.

Fortuantely, there is one that is already partially setup that you can clone
from a Git repository. This is the model that I have been using as my reference
for developing PyMBS.

**1. Clone the model from the GitLab repo**

    In your web browser, navigate to https://gitlab.trove.fm/btf/fhl2618
    This is the git repository for the cash flow model. You do not need
    an account on this GitLab server in order to access this repo. When you
    arrive at the URL, this is what you should see:

    .. figure:: _images/fhl2618_repo.jpg
        :width: 800px
        :height: 464px
        :align: center
        :alt: Anaconda Navigator

        *The fhl2618 GitLab Repository*

    In the upper-right-hand corner, click on the ``Clone`` button to copy the
    URL that you will need to clone the repository to your machine, using Git.
    The use of Git is really outside the scope of this document.  If you are
    unfamiliar with Git, there are plenty of resources available online to
    help you with it, including this one here:
    https://docs.gitlab.com/ee/gitlab-basics/start-using-git.html

**2. Configure PyMBS**

    Before you can open the model in Jupyter Lab, you need to tell PyMBS where
    to find it.  You can do this by specifying a project directory in a
    configuration file.

    The User is able to customize settings via the ``config.yaml`` file, which
    is located in a subdirectory of the User's HOME directory.

    This exact location of this directory differs by platform, as shown below:

    +------------+-----------------------------------------------------+
    | Platform   | Config Path                                         |
    +============+=====================================================+
    | Mac OSX    | ``~/.config/pymbs/config.yaml``                     |
    +------------+-----------------------------------------------------+
    | Linux      | ``~/.config/pymbs/config.yaml``                     |
    +------------+-----------------------------------------------------+
    | Windows    | ``C:\Users\<user>\AppData\Local\pymbs\config.yaml`` |
    +------------+-----------------------------------------------------+

    If desired, the configuration values may be set using environment variables,
    instead of using the ``config.yaml`` file.  Additionally, an alternate
    location for the ``config.yaml`` file itself may be specified in the
    **PYMBS_CONFIG_PATH** environment variable.

    See the :ref:`config_mod` section of this documentation for details, including
    the names of the other environment variables.

    Below is a sample ``config.yaml`` file similar to the one that you
    will need to prepare before attempting to open a model in Jupyter Lab.

    The **project directory** key is the only value that is **required**.

    .. code-block:: yaml

        ---
        pymbs:
            project directory: '/Users/username/Projects/finance/FRE/REMICs'

    You can copy and paste the code block above directly into a text file and
    save it as ``config.yaml`` at the path noted in the table above for your
    platform (or in another path, if you choose to specify one, using the
    **PYMBS_CONFIG_PATH** environment variable).

    Modify the path of the ``project directory`` key from that in the template
    above so that it points to the correct path on your machine. The project
    directory is actually the **parent** directory of the fhl2618 direcotry
    that was created when you cloned the fhl2618 Git repoistory.

    For illustrative purposes, suppose that you created a ``cmo`` directory
    inside of your ``HOME`` directory and that you cloned the fhl2618 repo
    into the ``cmo`` directory.

    Your directory structure would appear as so:

    .. code-block:: text

        HOME
            \__cmo
                  \__fhl2618

    In this case, your ``project directory`` would be
    ``'/HOME/cmo'``.  You can continue to place other deals inside the
    ``cmo`` directory and PyMBS will know how to find them.

**3. Download a copy of the Prospectus Supplement**

    When reverse-engineering a structured cash flow model, it's helpful to
    have a copy of the Prospectus Supplement, aka "Prosupp", or
    "Offering Circular", if one is available. In this case, one is available -
    go ahead and download a copy of the prosupp for
    `Freddie Mac REMIC Series 2618 <https://freddiemac.mbs-securities.com/api/download/FRE/135984/2618oc>`_

    At this point in development, PyMBS is only capable of modeling Group 3
    from this deal.  The payment rules for Group 3 can be found on page 6 of
    the prosupp.  The collateral cash flows can be run for **all** of the
    groups in this deal.  In the near future, I would expect PyMBS to be
    capable of handling the payment rules for Groups 1 and 4.

    The payment rules for Group 2 of this deal are the most difficult to
    handle at this time. This is due to the limited parsing ability of the
    initial implementation of PyMBS.  If this framework is to be able to
    handle more complex payment rules, I will need to develop a Domain
    Specific Language (DSL) for the payment rules and a parser for the DSL.
    This would require a level of effort that goes beyond the scope of a
    Proof of Concept (POC).

    Finally, as noted in the :ref:`caveats` section of this documentation,
    PyMBS is not yet capable of paying down the balance of Notional tranches,
    nor is there logic yet to handle MACR tranches (those outlined on page 45
    of the prosupp). These too were effectively out of scope for a POC.

    Now, let's open up Jupyter Lab and :ref:`run_the_model`!
