# AFCARS Database Tool

The AFCARS Database Tool is an editor for the XML data to be submitted to the AFCARS system.


## Building an executable

Windows:

    C:> pyinstaller --clean --onefile --name AXE -w --icon=assets/favicon.ico --add-data "ui/style.qss;ui" --add-data "assets/pexels-negative-space-97077.jpg;assets" --add-data "templates/*.xml;templates" --add-data "ui/*.ui;ui" main.py

MacOS:

    $ pyinstaller --clean --onefile --name AXE -w \
        --icon "assets/app_icon.icns" \
        --add-data "ui/style.qss:ui" \
        --add-data "assets/pexels-negative-space-97077.jpg:assets" \
        --add-data "ui/*.ui:ui" \
        main.py

