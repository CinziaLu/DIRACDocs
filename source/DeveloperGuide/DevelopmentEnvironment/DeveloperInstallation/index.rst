.. _developer_installation:

======================================
Setting up a development installation
======================================

-------------------------------------
Sharing your development
-------------------------------------

Once you're familiar with the basics of how GIT works. You're ready to clone the DIRAC source repository.
DIRAC repository is hosted at https://github.com/DIRACGrid/DIRAC. This has been already outlined in the previous sections, so we will not repeat it here.

In any case, it's now time to setup a developer installation. A developer installation is a "closed" installation: an installation that can, even, be used while being disconnected from the network.

-------------------------------------------
Setting up your development installation
-------------------------------------------

DIRAC developers tend to use eclipse for developing DIRAC. It is not mandatory but it is recommended. The following steps
will try to guide you on setting up a development installation for DIRAC in eclipse. If you don't need/want eclipse just
follow the next section and skip the rest.

Checking out the source
=========================

First you need to check out all the sources you need to start working on DIRAC or on any extension. Go to a clean directory
( from now on we will call that directory *$DEVROOT* ) and:

  1. Go to your *$DEVROOT* directory
  2. Check out DIRAC source code. DIRAC source is hosted on *github.com*. So, you have to do::

      git clone git@github.com:yourusername/DIRAC.git

    This will create a *$DEVROOT/DIRAC* for you.
    If you don't intend to develop DIRAC and just need it for developing extensions do::

      git clone https://github.com/DIRACGrid/DIRAC.git

  3. This will create a *remote* pointer ( in git terms ) in the local git repository called *origin* that points to your source repository. In that repository you will publish your code to be released. But all the releases will be done in the https://github.com/DIRACGrid/DIRAC repository. You need to define a *remote* for that repository to be able to pull newly released changes into your working repo. We will name that repository *release*::

      git remote add release https://github.com/DIRACGrid/DIRAC.git
      git fetch release

  4. If you need DIRACWeb extension, for example, do the same with the repo at https://github.com/DIRACGrid/DIRACWeb
  5. If you need to check out any extension do so in the *$DEVROOT* directory. For instance::

      svn co svn+ssh://svn.cern.ch/reps/dirac/LHCbDIRAC/trunk/LHCbDIRAC LHCbDIRAC

  6. Repeat step 4 for each extension you need
  7. Deploy DIRAC scripts by running::

      DIRAC/Core/scripts/dirac-deploy-scripts.py

    It is a good idea to add the scripts directory to your $PATH.

  8. We now add MySQL. DIRAC mainly uses *MySQL* as its database engine. There are many database structures used by DIRAC. Each system tipically has more than one database structure to keep its state. The first step is to install *MySQL* from your distribution. For rpm based distributions execute::

      yum install mysql mysql-server
      service mysqld start
  
    For debian based distributions execute::
  
      apt-get install mysql-server
    
    If you have either another distribution or another operative system please head to `MySQL <http://www.mysql.com/>`_ to check how to install MySQL in your host.  Once MySQL is installed you need to create a user to interact with the DB, e.g. the user *Dirac*::

      > mysql -u root
      
      mysql> CREATE USER 'Dirac'@'localhost' IDENTIFIED BY 'yourpasswd';
      Query OK, 0 rows affected (0.00 sec)


    Now, you will need to create a database in MySQL for each database you want to use or develop. First create the database::

      mysqladmin -u root create yourdbname
  
    Once the database has been created::

      > mysql -u root yourdbname
      ...

      mysql> GRANT SELECT,INSERT,LOCK TABLES,UPDATE,DELETE,CREATE,DROP,ALTER ON yourdbname.* TO Dirac@'%' IDENTIFIED BY 'yourpasswd';
      Query OK, 0 rows affected (0.01 sec)
      mysql> flush privileges;
      Query OK, 0 rows affected (0.01 sec)
  
    With the previous steps you've created a database called *yourdbname* and authorized user *yourusername* with password *yourpasswd* to use it. 

  9. Now you need to install the required python packages for DIRAC to be able to run. There are two ways of doing that:

    9.1. If you want to use your own python (you can use versions 2.6 or 2.7, but it is highly suggested to use python 2.7) you can install all the required packages by hand. First, you'll need to install few packages for your distrubution, e.g. you will need gcc, python-devel, openssl-devel, mysql, mysql-devel, python-pip. Then, you can use pip to install specifc python tools::

          pip install GSI
          pip install MySQL-python
          pip install mock

    Now, remember to update the $PYTHONPATH with the directory where you put your DIRAC code (and the code of possible extensions). Note: for those of you with OSX Lion or newer take a look `here <http://bruteforce.gr/bypassing-clang-error-unknown-argument.html>`_ if you can't install MySQL-python...

    9.2. The second possibility is to use the same script that is used for the server installations. This is needed if you don't have python 2.6 ot 2.7 available for your system or you just want to get the DIRAC External binaries for you platform::

          scripts/dirac-install -X -t server -i 26

    This may take a while if there aren't externals available for your platform and they have to be compiled. In any case, we suggest to try with the first alternative.


  10. Last step is to to configure DIRAC. There are 2 ways to do that: the first, and suggested way, is to work in isolation. At this point, the key becomes understanding how the DIRAC `Configuration Service (CS) <http://diracgrid.org/files/docs/AdministratorGuide/Configuration/ConfigurationStructure/index.html>`_ works. I'll explain here briefly. The CS is a layered structure: whenever you access a CS information (e.g. using a "gConfig" object, see later), DIRAC will first check into your local "dirac.cfg" file (it can be in your home as .dirac.cfg, or in etc/ directory, see the link above). If this will not be found, it will look for such info in the CS servers available.

    When you develop locally, you don't need to access any CS server: instead, you need to have total control. So, you need to work a bit on the local dirac.cfg file. There is not much else needed, just create your own etc/dirac.cfg. The example that follows might not be easy to understand at a first sight, but it will become easy soon. The syntax is extremely simple, yet verbose: simply, only brackets and equalities are used.

    10.1. If you want to create an isolated installation just creaate a *$DEVROOT/etc/dirac.cfg* file with (create the etc directory first)::

      DIRAC
      {
        Setup = DeveloperSetup
        Setups
        {
          DeveloperSetup
          {
            Framework = DevInstance
            Test = DevInstance
          }
        }
      }
      Systems
      {
         Framework
         {
           DevInstance
           {
             URLs
             {
             }
             Services
             {
             }
           }
        }
        Test
        {
          DevInstance
          {
            URLs
            {
            }
            Services
            {
            }
          }
        }
      }
      Registry
      {
        Users
        {
          yourusername
          {
            DN = /your/dn/goes/here
            Email = youremail@yourprovider.com
          }
        }
        Groups
        {
          devGroup
          {
            Users = yourusername
            Properties = CSAdministrator, JobAdministrator, ServiceAdministrator, ProxyDelegation, FullDelegation
          }
        }
        Hosts
        {
          mydevbox
          {
            DN = /your/box/dn/goes/here
            Properties = CSAdministrator, JobAdministrator, ServiceAdministrator, ProxyDelegation, FullDelegation
          }
        }
      }

    10.2. The second possibility (ALTERNATIVE to the previous one, and not suggested) is to issue the following script::

        scripts/dirac-configure -S setupyouwanttorun -C configurationserverslist -n sitename -H

    This is a standard script, widely used for non-developer installations, that will connect to an already existing installation when the configuration servers list is given


  11. Now, it's time to deal with certificates. DIRAC understands certificates in *pem* format. That means that certificate set will consist of two files. Files ending in *cert.pem* can be world readable but just user writable since it contains the certificate and public key. Files ending in *key.pem* should be only user readable since they contain the private key. You will need two different sets certificates and the CA certificate that signed the sets. *Note: if any of the paths mentioned here does not yet exist, just create it with mkdir*

    11.1. CA certificates: Place them under *$DEVROOT/etc/grid-security/certificates*. You can install them following the instructions `here <https://wiki.egi.eu/wiki/EGI_IGTF_Release>`_. In case you can't use a package manager like *apt* or *yum* there are tarballs available to download the CA certificates, so in that case you can use this script


      .. literalinclude:: downloadCAs.sh


      11.1.1. Dummy CA certificate. If you have your own user and host certificates you can skip this step, otherwise you'll need to create a dummy CA to generate user and host certificates::

         openssl genrsa -out cakey.pem 2048
         openssl req -new -x509 -days 3650 -key cakey.pem -out cacert.pem -subj "/O=$(whoami)-dom/OU=PersonalCA"

      Place both files in *$DEVROOT/etc/grid-security* and copy *cacert.pem* to *$DEVROOT/etc/grid-security/certificates*. 

    11.2 Server certificate: If you have access to a server certificate from another installation or service, you can use that for your development instance.

      11.2.1. In case you don't have access to any host or service certificates you can create one by doing::

          openssl genrsa -out hostkey.pem 2048
          openssl req -new -key hostkey.pem -out hostreq.csr -subj "/O=$(whoami)-dom/OU=PersonalCA/CN=$(hostname -f)"
          openssl x509 -req -in hostreq.csr -CA cacert.pem -CAkey cakey.pem -CAcreateserial -out hostcert.pem -days 500 

      Place them at *$DEVROOT/etc/grid-security/hostcert.pem* and *$DEVROOT/etc/grid-security/hostkey.pem*.

    11.3 User certificate: If you have your own user certificate you can use that one. Place your certificate in *$HOME/.globus/usercert.pem* and *$HOME/.globus/userkey.pem*.

      11.3.1. If you don't have a user certificate you will need to generate on like this::

         openssl genrsa -out userkey.pem 2048
         openssl req -new -key userkey.pem -out userreq.csr -subj "/O=$(whoami)-dom/OU=PersonalCA/CN=$(whoami)"
         openssl x509 -req -in userreq.csr -CA cacert.pem -CAkey cakey.pem -CAcreateserial -out usercert.pem -days 500 

      Now place them under *$HOME/.globus/usercert.pem* and *$HOME/.globus/userkey.pem*

  12. Now we need to register those certificates in DIRAC. To do you you must modify *$DEVROOT/etc/dirac.cfg* file and set the correct
      certificate DNs for you and your development box. For instance, to register the host replace "/your/box/dn/goes/here" (/Registry/Hosts/mydevbox/DN option) with the result of::

        openssl x509 -noout -subject -in etc/grid-security/hostcert.pem | sed 's:^subject= ::g'

You're ready for DIRAC development !

