======================================
Setting up a development installation
======================================

-------------------------------------
Sharing your development
------------------------------------- 
 
Once you're familiar with the basics of how GIT works. You're ready to clone the DIRAC source repository. 
DIRAC repository is hosted at https://github.com/DIRACGrid/DIRAC . From there you have two options:

 - Easy way: 
 
  1. Register at *github.com* and set up your account
  2. On *github.com* fork the DIRAC repository by going to https://github.com/DIRACGrid/DIRAC and clicking the *Fork* button on 
     the top right part of the page.
  3. By forking a repository *github.com* will create a https://github.com/yourusername/DIRAC repository where you are the administrator.
  4. Clone that repository in your local work space
  5. Start working on the DIRAC code
  6. Push changes to your *github.com* repository
  7. Issue a pull request to DIRAC by going to https://github.com/yourusername/DIRAC, switching to the branch you want DIRAC to 
     pull changes from and clicking the pull request button. 
  
-------------------------------------------
Setting up your development installation
-------------------------------------------

DIRAC developers tend to use eclipse for developing DIRAC. It is not mandatory but it is recommended. The following steps 
will try to guide you on setting up a development installation for DIRAC in eclipse. If you don't need/want eclipse just 
follow the next section and skip the rest.

Checking out the source
=========================

First you need to check out all the sources you need to start working on DIRAC or on any extension. Go to a clean directory 
( from now on we will call that directory *devRoot* ) and:
 
 1. Go to your *devRoot* directory
 2. Check out DIRAC source code. DIRAC source is hosted on *github.com*. So, you have to do::
      
      git clone git@github.com:yourusername/DIRAC.git 
     
    This will create a *devRoot/DIRAC* for you.
      
    If you don't intend to develop DIRAC and just need it for developing extensions do::
     
      git clone https://github.com/DIRACGrid/DIRAC.git
 
 3. This will create a *remote* pointer ( in git terms ) in the local git repository called *origin* that points to your source repository. 
    In that repository you will publish your code to be released. But all the releases will be done in the 
    https://github.com/DIRACGrid/DIRAC repository. 
    You need to define a *remote* for that repository to be able to pull newly released changes into your working repo. 
    We will name that repository *upstream*::

     git remote add upstream https://github.com/DIRACGrid/DIRAC.git  
     git fetch upstream                                          
  
 4. If you need DIRACWeb extension, for example, do the same with the repo at https://github.com/DIRACGrid/DIRACWeb
 5. If you need to check out any extension do so in the *devRoot* directory. For instance::
 
       svn co svn+ssh://svn.cern.ch/reps/dirac/LHCbDIRAC/trunk/LHCbDIRAC LHCbDIRAC
 
 6. Repeat step 4 for each extension you need
 7. Deploy DIRAC scripts by running::
 
       DIRAC/Core/scripts/dirac-deploy-scripts.py


 8. Now you need to install the required python packages for DIRAC to be able to run. There are two ways of doing that:
 
   8.1 If you want to use your own python (it needs to be 2.6 or 2.7) you can install all the required packages by hand. Just do::
       
       pip install GSI
       pip install MySQL-python
 
   8.2 If you don't have python 2.6 ot 2.7 available for your system or you just want to get the DIRAC External binaries for you platform, run::
 
       scripts/dirac-install -X -t server -i 26
    
   This may take a while if there aren't externals available for your platform and they have to be compiled.
       

 9. Last step is to to configure DIRAC. 
 
   9.1 If you want to create an isolated installation just creaate a *etc/dirac.cfg* file with::
   
       DIRAC {
         Setup = Local
         Configuration {
           Servers = dips://localhost:9135/Configuration/Server
           Master = yes
         }
         Setups {
           Local {
             Configuration = Local
           }
         }
       }
       Registry {                                                                                                                                                                                                                                                                             
         Users {                                                                                                                                                                                                                                                                  
           yourusername {                                                                                                                                                                                                                                                                 
             DN = your/DN/here                                                                                                                                                                                                                     
           }                                                                                                                                                                                                                                                                          
         }
         Groups {                                                                                                                                                                                                                                                                      
           admin {                                                                                                                                                                                                                                                                    
             Users = yourusername                                                                                                                                                                                                                                                        
             Properties = CSAdministrator                                                                                                                                                                                                                                            
           }                                                                                                                                                                                                                                                                           
         }                                                                                                                                                                                                                                                                           
       }                                                                                                                                                                                                                                                                                
       Systems {                                                                                                                                                                                                                                                                  
         Configuration {                                                                                                                                                                                                                                                               
           Local {                                                                                                                                                                                                                                                                     
             Services {                                                                                                                                                                                                                                                               
               Configuration {                                                                                                                                                                                                                                                       
                 Port = 9135                                                                                                                                                                                                                                                         
                 Authorization {                                                                                                                                                                                                                                                      
                   Default = all                                                                                                                                                                                                                                                     
                 }                                                                                                                                                                                                                                                                   
               }                                                                                                                                                                                                                                                                     
             }                                                                                                                                                                                                                                                                       
           }                                                                                                                                                                                                                                                                         
         }                                                                                                                                                                                                                                                                           
       }  
   
   
   
   9.2 If you want to connect to an already existing installation:
 
       scripts/dirac-configure -S setupyouwanttorun -C configurationserverslist -n sitename -H

 10. From now on, every time you want to publish something to your public repository do::

       git push origin localbranch:remotebranch  
       
     if you want to push a new branch
  
     or just::

       git push origin 
       
     for an already pushed branch

 11. To bring changes from the release repository do::

       git fetch upstream
       git rebase upstream/integration
 
You're ready for DIRAC development !


