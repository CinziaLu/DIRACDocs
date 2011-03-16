============================
dirac-wms-job-get-jdl
============================

Usage::

  dirac-wms-job-get-jdl.py (<options>|<cfgFile>)* 

Example::

  $ dirac-wms-job-get-jdl 1
  {'Arguments': '-ltrA',
   'CPUTime': '86400',
   'DIRACSetup': 'EELA-Production',
   'Executable': '/bin/ls',
   'JobID': '1',
   'JobName': 'DIRAC_vhamar_602138',
   'JobRequirements': '[             OwnerDN = /O=GRID-FR/C=FR/O=CNRS/OU=CPPM/CN=Vanessa Hamar;            OwnerGroup = eela_user;            Setup = EELA-Production;            UserPriority = 1;            CPUTime = 0        ]',
   'OutputSandbox': ['std.out', 'std.err'],
   'Owner': 'vhamar',
   'OwnerDN': '/O=GRID-FR/C=FR/O=CNRS/OU=CPPM/CN=Vanessa Hamar',
   'OwnerGroup': 'eela_user',
   'OwnerName': 'vhamar',
   'Priority': '1'}

