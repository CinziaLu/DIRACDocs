=====================
dirac-rss-sync
=====================

  ==============================================================================

  DIRAC v6r7

  dirac-rss-sync

  

    Script that synchronizes the resources described on the CS with the RSS.

    By default, it sets their Status to `Unknown`, StatusType to `all` and 

    reason to `Synchronized`. However, it can copy over the status on the CS to 

    the RSS. Important: If the StatusType is not defined on the CS, it will set

    it to Banned !

    

Usage::

      dirac-rss-sync

        --init                Initialize the element to the status in the CS ( applicable for StorageElements )

        --element=            Element family to be Synchronized ( Site, Resource or Node ) or `all`

    

    

    Verbosity:

        -o LogLevel=LEVEL     NOTICE by default, levels available: INFO, DEBUG, VERBOSE..        

  ==============================================================================

 

 

Options::

  -    --init            : Initialize the element to the status in the CS ( applicable for StorageElements ) 

  -    --element=        : Element family to be Synchronized ( Site, Resource or Node ) or `all` 


