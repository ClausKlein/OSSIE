README.TXT

------------
Instructions
------------

1. Start the Waveform Developer python interface from the /wavedev/ directoy.

       python wd.py

2. To create the sample application, click on Help->Sample Waveform from the menu.
   A basic application will be shown with a component list and related connections.

3. Click Waveform->Generate from the menu and select the desired output directory.

4. The waveform is now ready to be populated. Exit the Waveform Developer

5. To build the waveform:
   >> cd /path/to/generated_code/

   enter each of the top-level directories created and type:
   >> ./reconf
   >> ./configure
   >> make
   >> make install

7. To run:

  - go to the base sdr installation directory: /sdr (default)

  - start the naming service and the event service
    (usually omniNames.sh)

  - run the nodeBooter
    >> nodeBooter -D -d /nodes/default_GPP_node.dcd.xml -P /sdr/dom -p /sdr/dev

  - run your waveform from the base waveforms directory (default is
    /sdr/dom/waveforms)
    >> wavLoader.py <your waveform>_DAS.xml

