Systems / WorkloadManagement / <SETUP> / Databases - Sub-subsection
===================================================================

Databases used by WorkloadManagement System. Note that each database is a separate subsection.

+--------------------------------+----------------------------------------------+----------------------+
| **Name**                       | **Description**                              | **Example**          |
+--------------------------------+----------------------------------------------+----------------------+
| *<DATABASE_NAME>*              | Subsection. Database name                    | JobDB                |
+--------------------------------+----------------------------------------------+----------------------+
| *<DATABASE_NAME>/DBName*       | Database name                                | DBName = JobDB       |
+--------------------------------+----------------------------------------------+----------------------+
| *<DATABASE_NAME>/Host*         | Database host server where the DB is located | Host = db01.in2p3.fr |
+--------------------------------+----------------------------------------------+----------------------+
| *<DATABASE_NAME>/MaxQueueSize* | Maximum number of queries??                  | MaxQueueSize = 10    |
+--------------------------------+----------------------------------------------+----------------------+

The databases associated to WorkloadManagement System are:
- JobDB
- JobLoggingDB
- MPIJobDB
- PilotAgentDB
- SandboxMetadataDB
- TaskQueueDB