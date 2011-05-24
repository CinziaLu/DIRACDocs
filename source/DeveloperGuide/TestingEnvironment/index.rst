==============================
Setting up testing environment
==============================

Every large enough software project needs to be carefully tested, monitored and evaluated to assure that minimum standards of 
quality are being attained by the development process. A primary purpose of that is to detect software and configuration failures so that 
defects may be discovered and corrected before making official release and to check if software meets requirements and works as 
expected. Testing itself could also speed up the development process rapidly tracing problems introduced with 
the new code. 

DIRAC is not different from that scenario, with the exception that service-oriented architecture paradigm, which is one of the basic 
concepts of the project, making the quality assurance and testing process the real challenge. However as DIRAC becomes more and more popular 
and now is being used by several different communities, the main question is not: *to test or not to test?*, but rather: *how to test in a 
efficient way?*

The topic of software testing is very complicated by its own nature, but depending on the testing method employed, the testing process itself
can be implemented at any time in the development phase and ideally should cover many different levels of the system: 

- *unit tests*, in which the responsible person for one source file is proving that his code is written in a right way,
- *integration tests* that should cover whole group of modules combined together to accomplish one well defined task, 
- *regression tests* that seek for errors in existing functionality after patches, functionality enhancements and/or configuration 
  changes have been made to the software,  
- *certification tests* (or *system tests*), which are run against the integrated and compiled system, treating it as a black box and trying 
  to evaluate the system's compliance with its specified requirements. 

In DIRAC project unit tests should be prepared for the developer herself, integration tests could be developed in groups of code responsible persons,
for regression tests the responsible person should be a complete subsystem (i.e. WMS, DMS, SMS etc.) manager, while certification tests should be 
prepared and performed by release managers.  

This document will try to formulate the basic requirements for the lowest level of testing: unit tests, on top of which any complicated 
and fully featured testing framework could be defined. 

Tools and methodology
---------------------

In DIRAC unit tests should be prepared for the developer herself. As the main implementation language is Python, the developers should 
use its default tool for unit testing, which is already a part of any Python distributions: the unittest_ module. 

This module provides a rich set of tools for constructing and running tests, supporting some very important concepts, like:

- *fixtures*: initialisation needed for setting up a group of tests together with appropriate clean-up after the execution
- *cases*: the smallest unit of testing for one use case scenario
- *suites*: collection of test cases for aggregation of test that should be executed together
- *runners*: classes for executing tests, checking all the spotted asserts and providing output results to the user.

The developers are encouraged to make themselves familiar with unittest module documentation, which could be found 
`here <http://docs.python.org/library/unittest.html>`_. It is suggested to read at least documentation for TestCase_, TestSuite_ 
and TestLoader_ classes and follow the examples over there.

Unit tests are typically created by the developer who will also write the code that is being tested. 
The tests may therefore share the same blind spots with the code: for example, a developer does not realize that certain 
input parameters must be checked, most likely neither the test nor the code will verify these input parameters. 
If the developer misinterprets the requirements specification for the module being developed, both the tests and the code will be wrong. 
Hence if the developer is going to prepare her own unit tests, she should pay attention and take extra care to implement proper testing 
suite, checking for every spot of possible failure (i.e. interactions with other components) and not trusting that someone else's code is 
always returning proper type and/or values. 

Testing the code, and so proper code developing cycle, can be done in four well defined steps:

Step 1. **Preparation**

The first step on such occasions is to find all possible use cases scenarios. The code [#]_ should be read carefully to isolate
all the paths of executions. For each of such cases the developer should prepare, formulate and define all required inputs and outputs,  
configurations, internal and external objects states, underlying components etc. Spending more time on this preparation phase will help to 
understand all possible branches, paths and points of possible failures inside the code and accelerate the second step, which is the test suite
implementation. 

Amongst all scenarios one is very special - so special, that it even has got its own name: *the main success scenario*. This is the path 
in execution process, in which it is assumed that all components are working fine so the  system is producing results correct to the last bit. 
The developer should focus on this scenario first, as all the others are most probably branching from it if some error condition would appear. 

Step 2. **Implementation**

Once the set of use cases is well defined, the developer should prepare and implement test case for each of use cases which should define:

- initial and final states of the system being tested, 
- runtime configuration, 
- set of input values, associated objects and their internal states,
- correct behaviour, 
- set of output results. 

Each test case should be instrumented with a special method: *setUp*,  which is preparing the testing environment. This is the correct place 
for constructing input and output data stubs, mock objects that the production code is using from the outside world and initial state of object
being tested. It is a good practice to implement also second special method: *tearDown*, which is doing a clean up after the tests execution, destroying all
objects created inside *setUp* function.

A test case should try to cover as much as possible the API of software under test and the developer is free to decide how many tests 
and asserts she would be implementing and executing, but of course there should be at least one test method inside each of test cases and at least 
one assert in every test method. The developer should also keep in her mind that being greedy is not a good practice: her test cases should check 
only her own code and nothing else. 

Step 3. **Test execution** 

Every developer is encouraged to execute her test suites by herself. Execution code of test suite should be put into unit test module 
in a various ways. Of course once the test results are obtained, it is the high time for fixing all places in the tested code, in which 
tests have failed.

Step 4. **Refactoring**

Once the code is tested and all tests are passed, the developer can start thinking about evolution of the code. This includes 
performance issues, cleaning up the code from repetitions, new features, patching, removing obsolete or not used methods. 
So from this point the whole developing cycle can start again and again and again...

Test doubles
------------

To isolate the code being tested from depended-on components it is convenient and sometimes necessary to use *test doubles*: 
simplified objects or procedures, that behaves and looks like the their real-intended counterparts, but are actually simplified versions 
that reduce the complexity and facilitate testing [#]_. Those fake objects meet the interface requirements of, and stand in for, more complex real ones,  
allowing programmers to write and unit-test functionality in one area without actually calling complex underlying or collaborating classes.
The isolation itself help developers to focus their tests on the behaviour of their classes without worrying about its dependencies, but also may be 
required under many different circumstance, i.e.:

- if depended-on component may return values or throw exceptions that affect the behaviour of code being tested, but it is impossible or 
  difficult for such cases to occur, 
- if results or states from depended-on component are unpredictable (like date, weather conditions, absence of certain records in database etc.),
- if communication with internal states of depended-on component is impossible,
- if call to depended-on component has unacceptable side effects ,
- if interactions with depended-on component is resource consuming operation (i.e. database connections and queries),
- if depended-on component is not available or even not existing in the test environment (i.e. the component's implementation hasn't stared yet, 
  but its API is well defined). 

It is clear that in such cases the developer should try to instrument the test suite with a set doubles, which come is several flavours:

**Dummy**
   A *dummy object* is an object that is used when method being tested has required object of some type as a parameter, but apart of 
   that neither test suite nor code being tested care about it.

**Stub**
   A *test stub* is a piece of code that doesn't actually do anything other than declare itself and the parameters it accepts 
   and returns something that is usually the values expected in one of the scenarios for the caller. This is probably the most popular double
   used in a test-driven development.

**Mock**
   A *mock object* is a piece of code, that is used to verify the correct behaviour of code that undergo tests, paying more attention 
   on how it was called and executed inside the test suite. Typically it also includes the functionality of a test stub in that it must return 
   values to the test suite, but the difference is it should also validate if actions that cannot be observed through the public API of code being 
   tested are performed in a correct order. 

In a dymanically typed laguage like Python_ every test double is easy to create as there is no need to simulate the full API of depended-on 
components and the developer can freely choose only those that are used in her own code. 

Example
-------

Let's assume we are coding a client to the CheesShopSystem [#]_ inside DIRAC. The depended-on components are CSS.Service.CheesShopOwner with 
CSS.DB.CheesShopDB database behind it. Our CSS.Client.CheesShopClient could only ask the owner for a specific chees [#]_ and eventually is killing 
him with a gun. We know the answers for all question that have been asked already, there was no chees at all in original script, but here for teaching
purposes we can just pretend for a while that the owner is really checking the shop's depot and even more, the Cheddar is present. The code 
for ``CheesShopOwner``::

  from types import *
  from DIRAC import S_OK, S_ERROR, gLogger, gConfig
  from DIRAC.Core.DISET.RequestHandler import RequestHandler  
  from DIRAC.CheesShopSystem.DB.CheesShopDB import CheesShopDB
  
  # global instance of a chees shop database
  cheesShopDB = False

  # initialize it first
  def initializeCheesShopOwner( serviceInfo ):
    global cheesShopDB
    cheesShopDB = CheesShopDB()
    return S_OK()
  
  class CheesShopOwner( RequestHandler ):
  
    types_isThere = [ StringType ]
    def export_isThere( self, chees ):
      return cheesShopDB.isThere( chees ) 
  
    types_buyChees = [ StringType, FloatType ]
    def export_buyChees( self, chees, quantity ):
      return cheesShopDB.buyChees( chees, quantity )
  
    # ... and so on, so on and so on, i.e:
    types_insertChees = [ StringType, FloatType, FloatType ]
    def export_insertChees( self, cheesName, price, quantity ):
      return cheesShopDB.insertChees( cheesName, price, quantity )


And here for ``CheesShopClient`` class::

  from DIRAC import S_OK, S_ERROR, gLogger, gConfig
  from DIRAC.Core.Base.Client import Client

  class Chees( object ):

    def __init__( self, name ):
      self.name = name

  class SpanishInquisitionError( Exception ):
    pass

  class CheesShopClient( Client ):

    def __init__( self, money, shopOwner = None ):
      self.__money = money
      self.shopOwner = shopOwner

    def buy( self, chees, quantity = 1.0 ):

      # is it really chees, you're asking for?
      if not isinstance( chees, Chees ):
        raise SpanishInquisitionError( "It's stone dead!" )

      # and the owner is in?
      if not self.shopOwner:
        return S_ERROR("Shop is closed!")

      # and chees is in the shop depot? 
      res = self.shopOwner.isThere( chees.name )   
      if not res["OK"]:
        return res

      # and you are not asking for too much?
      if quantity > res["Value"]["Quantity"]:
        return S_ERROR( "Not enough %s, sorry!" % chees.name )

      # and you have got enough money perhaps?
      price = quantity * res["Value"]["Price"]
      if self.__money < price:
        return S_ERROR( "Not enough money in your pocket, get lost!")

      # so we're buying
      res = self.shopOwner.buyChees( chees.name, quantity )
      if not res["OK"]:
        return res
      self.__money -= price

      # finally transaction is over 
      return S_OK( self.__money )


This maybe oversimplified code example already has several hot spots of failure for chess buying task: first of all, your input parameters 
could be wrong (i.e. you want to buy rather parrot, not chees); the shop owner could be out; they haven't got chees you are asking for in the store;
or maybe it is there, but not enough for your order; or you haven't got enough money to pay and at least the transaction itself could be interrupted 
for some reason (connection lost, database operation failure etc.).

We have skipped ``CheesShopDB`` class implementation on purpose: our ``CheesShopClient`` directly depends on ``CheesShopOwner`` and we shoudn't 
care on any deeper dependencies. 

Now for our test suite we will assume that there is a 20 lbs of Cheddar priced 9.95 pounds, hence the test case for success is i.e. asking for 
1 lb of Cheddar (the main success scenario) having at least 9.95 pounds in a wallet:

  - input: ``Chees("Cheddar")``, 1.0 lb, 9.95 pounds in your pocket
  - expected output: ``S_OK = { "OK" : True, "Value" : 0.0 }``

Other scenarios are:

1. Wrong order [#]_:

  * Want to buy Norwegian blue parrot:

    - input: ``Parrot("Norwegian Blue")`` 
    - expected output: an exception ``SpanishInquisitionError("It's stone dead!")`` thrown in a client

  * Asking for wrong quantity:

    - input: ``Chees("Cheddar")``, ``quantity = "not a number"`` or ``quantity = 0``
    - expected output: an exception ``SpanishInquisitionError("It's stone dead!")`` thrown in a client

3. The shop is closed:

  - input: ``Chees("Cheddar")``
  - expected output: ``S_ERROR = { "OK" : False, "Message" : "Shop is closed!" }``

4. Asking for any other chees:

  - input: ``Chees("Greek feta")``, 1.0 lb
  - expected output: ``S_ERROR = { "OK" : False, "Message" : "Ah, not as such!" }``

5. Asking for too much of Cheddar: 

  - input: ``Chees("Cheddar")``, 21.0 lb
  - expected output: ``S_ERROR = { "OK" : False, "Message" : "Not enough Cheddar, sorry!" }``

6. No money on you to pay the bill:

  - input: ``Chees("Cheddar")``, 1.0 lb, 8.0 pounds in your pocket 
  - expected output: ``S_ERROR = { "OK" : False, "Message" : "Not enough money in your pocket, get lost!" }``

7. Some other unexpected problems in underlying components, which by the way we are not going to be test or explore here. *You just can't test everything, 
keep track on testing your code!*

The test suite code itself follows::

  import unittest
  from mock import Mock

  from DIRAC import S_OK, S_ERROR
  from DIRAC.CheesShopSystem.Client.CheesShopClient import Chees, CheesShopClient
  from DIRAC.CheesShopSystem.Service.CheesShopOwner import CheesShopOwner

  class CheesClientMainSuccessScenario( unittest.TestCase ):

    def setUp( self ):
      # stub, as we are going to use it's name but nothing else 
      self.chees = Chess( "Cheddar" )
      # money, dummy 
      self.money = 9.95
      # amount, dummy
      self.amount = 1.0
      # real object to use
      self.shopOwner = CheesShopOwner( "CheesShop/CheesShopOwner" )
      # but with mocking of isThere
      self.shopOwner.isThere = Mock( return_value = S_OK( { "Price" : 9.95, "Quantity" : 20.0 } ) )
      # and buyChees methods
      self.shopOwner.buyChees = Mock() 
    
    def tearDown( self ):
      del self.shopOwner
      del self.money
      del self.amount
      del self.chees 

    def test_buy( self ):
       client = CheesShopClient( money = self.money, shopOwner = self.shopOwner )
       # check if test object has been created
       self.assertEqual( isinstance( client, CheesShopClient), True )     
       # and works as expected       
       self.assertEqual( client.buy( self.chees, self.amount ), { "OK" : True, "Value" : 0.0 } )
       ## and now for mocked objects
       # asking for chees
       self.shopOwner.isThere.assert_called_once_with( self.chees.name )
       # and buying it
       self.shopOwner.buyChees.assert_called_once_with( self.chees.name, self.amount )
      
      
  if __name__ == "__main__":
    unittest.main()
    #testSuite = unittest.TestSuite( [ "CheesClientMainSuccessScenario" ] )
    

Conventions
-----------

All test modules should follow those conventions:

**T1**
  Test environment should be shielded from the production one and the same time should mimic it as far as possible. 

**T2**
  All possible interactions with someone else's code or system components should be dummy and artificial. This could be obtained by proper use of 
  stubs, mock objects and proper set of input data. 

**T3**
  Tests defined in one unit test module should cover one module (in DIRAC case one class) and nothing else.

**T4**
  The test file name convention should follow the rule: *test* word concatenated with module name, i.e. in case of *CheesClient* module, 
  which implementation is kept *CheesClient.py* disk file, the unit test file should be named *testCheesClient.py*  

**T5**
  Each TestCase_ derived class should be named after module name and scenario it is going to test and *Scenario* world, i.e.:
  *CheesClientMainSuccessScenario*, *CheesClientWrongInputScenario* and so on. 

**T6**
  Each unit test module should hold at least one TestCase_ derived class, ideally a set of test cases or test suites.

**T7**
  The test modules should be kept as close as possible to the modules they are testing, preferably in a *test* subdirectory on DIRAC subsystem
  package directory, i.e: all tests modules for WMS should be kept in *DIRAC/WMS/tests* directory.

Footnotes
---------

.. [#] Or even better software requirements document, if any of such exists. Otherwise this is a great opportunity to prepare one.
.. [#] To better understand this term, think about a movie industry: if a scene movie makers are going to film is potentially dangerous and unsafe 
       for the leading actor, his place is taken over by a stunt double.
.. [#] A real pity if you have missed this show.
.. [#] and eventually is killing him with a gun. But not here, sorry if we disapoint you.
.. [#] You may ask: *isn't it silly?* No, in fact it isn't. Validation of input parameters is one of the most important tasks during testing. 


.. _Python: http://www.python.org/
.. _unittest: http://docs.python.org/library/unittest.html
.. _TestCase: http://docs.python.org/library/unittest.html#unittest.TestCase
.. _TestSuite: http://docs.python.org/library/unittest.html#unittest.TestSuite
.. _TestLoader: http://docs.python.org/library/unittest.html#unittest.TestLoader
