# AFCARS Database Tool

The AFCARS Database Tool is an editor for the XML data to be submitted to the AFCARS system.


## Building an executable

Windows:

    C:> pyinstaller --clean -F -n AXE -w --add-data "ui/style.qss;ui" --add-data "assets/*.*;assets" --add-data "ui/*.ui;ui" main.py

MacOS:

    $ pyinstaller --clean -F -n AXE -w --add-data "ui/style.qss:ui" -w main.py

