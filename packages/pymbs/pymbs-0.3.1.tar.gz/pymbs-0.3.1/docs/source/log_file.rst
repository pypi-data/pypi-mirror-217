
By default, the log file itself is located in platform-specific locations,
as shown below:

+------------+-----------------------------------------------------+
| Platform   | Log File Path                                       |
+============+=====================================================+
| Mac OSX    | ``~/.local/log/pymbs/pymbs.log``                    |
+------------+-----------------------------------------------------+
| Linux      | ``~/.local/log/pymbs/pymbs.log``                    |
+------------+-----------------------------------------------------+
| Windows    | ``C:\Users\<user>\AppData\Local\pymbs\pymbs.log``   |
+------------+-----------------------------------------------------+

If you would like to specify your own log file location, you can specify
the location with the ``PYMBS_LOG_FILE`` environment variable.
