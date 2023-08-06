.. _caveats:

=======================
Caveats and Limitations
=======================
* Collat replines must consist of assumptions only - PyMBS cannot yet make the
  calculations necessary for Known Collateral (Pool IDs) or Securitzed Collateral (ReREMICs).


* Payment functions for all of the possible types of rules to be found in a deal's
  waterfall have not yet been implemented. In part, this is because the current
  implementation is designed merely to serve as a POC.


* PyMBS cureently makes use of the ``eval`` function to translate a payment
  rule from the waterfall into a function call in the library. Use of ``eval``
  *can* be dangerous and is generally discouraged, especially in a production
  environment. This is mitigated to some extent by the fact that the eval
  statement is only used to call functions in the payment_rules module, however,
  it will be removed competely in a future release. In a production environment,
  PyMBS would implement a Domain Specific Language (DSL) that would allow for
  (relatively) simple syntax to be mapped to robust functionality behind the scenes.
  This task is non-trivial, if it is to be implemented correctly.


* Floating rate and Inverse Floating rate tranches are similarly limited in the types of
  floater formulas that can be created. Basically, the formula must take the form of a
  spread to a benchmark, limited by a cap and a floor. The benchmark is limited to a
  static value at this time, although providing for benchmark scenarios or live, online
  lookups for historical data should be relatively easy to implement.


* Prepayment scenarios are limited to multiples of the PSA benchmark. Allowing for CPR and
  SMM scenarios, as well as custom prepayment vectors should also be relatively easy to
  implement.


* The refence deal that is being used during initial development is the `Freddie Mac REMIC
  Series 2618 <https://freddiemac.mbs-securities.com/api/download/FRE/135984/2618oc>`_,
  issued in May of 2003. At the moment, the Weighted Average Lives (WALs) for
  the tranches are within a slight variance of those disclosed in the Prospectus Supplement.
  At this point, working in isolation, without the beenfit of input from other Subject Matter
  Experts (SMEs), it is thought that these calculations are as close as can be achieved.


* Freddie Mac does not offer a RESTful API for accessing Security-related
  information from their website. The files that they offer are in antiquated formats that
  would require customized parsers to be built in order to read-in the data disclosed on their
  website. In order to avoid writing custom parsers at this stage, and as a means to show
  a better way, the deal-related data required for modeling the reference deal was converted
  into a JSON format. This is what would be expected from a REST API, and has the added benefit
  of not needing a custom parser. In addition, the JSON files are much smaller in size.


* MACRs and Notional Classes are loaded into the model, but are not yet handled by the payment
  functions. These classes will not be displayed in the Weighted Average Lives table. The cash
  flows for notional classes can be run, but they will NOT be correct.
  

* In addition to the Prospectus Supplement, the reference material used includes two books on the
  subject matter:

    * **Collateralized Mortgage Obligations: Structures and Analysis, 3rd Edition**,
      by Frank J. Fabozzi and Chuck Ramsey [#f1]_

    * **Fixed Income Mathematics: Analytical and Statistical Techniques, 3rd Edition**,
      by Frank J. Fabozzi [#f2]_

.. rubric:: Footnotes

.. [#f1] | `Publisher Website for Collateralized Mortgage Obligations: Structures and Analysis <https://www.wiley.com/en-us/Collateralized+Mortgage+Obligations%3A+Structures+and+Analysis%2C+3rd+Edition-p-9781883249625>`_

.. [#f2] | `Amazon Website for Fixed Income Mathematics: Analytical and Statistical Techniques <https://www.amazon.com/Fixed-Income-Mathematics-Analytical-Statistical/dp/007146073X/ref=sr_1_1?keywords=Fixed+Income+Mathematics%3A+Analytical+and+Statistical+Techniques&qid=1566797581&s=books&sr=1-1>`_
