#!/usr/bin/env python
''' buildCodeDOC
  
  It accepts as argument the DIRAC version ( or branch name )

'''

# defined on DIRACDocs/source/Tools/fakeEnvironment
import fakeEnvironment

import DIRAC

import os
import pkgutil
import sys
import tempfile

DOCMODULES = [ 'API', 'Client', 'Service', 'Utilities' ]

def getTmpDir():
  ''' Creates a temporary dir and adds it to sys.path so that we can import
      whatever lies there.
  '''

  try:
    tmpDir = tempfile.mkdtemp()
  except IOError:
    sys.exit( 'IOError creating tmp dir' )
      
  sys.path.append( tmpDir )

  return tmpDir

#...............................................................................
# Functions generating rst files

def getCodeDocumentationPath():

  whereAmI = os.path.dirname( os.path.abspath( __file__ ) )
  relativePathToWrite = '../source/CodeDocumentation'
  
  codeDocumentationPath = os.path.abspath( os.path.join( whereAmI, 
                                                         relativePathToWrite ) )

  try:
    os.mkdir( codeDocumentationPath )
  except OSError:
    sys.exit( 'Cannot create %s' % codeDocumentationPath )

  return codeDocumentationPath  

def getDIRACPackages():
  
  pkgpath = os.path.dirname( DIRAC.__file__ )
  packages = [ name for _, name, _ in pkgutil.iter_modules([pkgpath]) ]
  
  packages.sort()
  
  return packages

def getPackageModules( package ):

  diracPackage = __import__( 'DIRAC.%s' % package, globals(), locals(), [ '*' ] )

  pkgpath = os.path.dirname( diracPackage.__file__ )
  modules = [ name for _, name, _ in pkgutil.iter_modules([pkgpath]) ]
  
  modules.sort()
  
  return modules

def writeIndexHeader( indexFile, title ):

  indexFile.write( '=' * len( title ) )
  indexFile.write( '\n%s\n' % title )
  indexFile.write( '=' * len( title ) )
  indexFile.write( '\n\n.. toctree::' )
  indexFile.write( '\n   :maxdepth: 2\n' )

def writeCodeDocumentationIndexRST( codeDocumentationPath, diracPackages ):
  '''
  '''
    
  indexPath = os.path.join( codeDocumentationPath, 'index.rst' )
  with open( indexPath, 'w' ) as index:
    writeIndexHeader( index, 'Code Documentation |release|' )    
    for diracPackage in diracPackages:
      index.write( '\n   %s/index.rst\n' % diracPackage )  

def writePackageDocumentation( tmpDir, codeDocumentationPath, diracPackage ):
  
  packageDir = os.path.join( codeDocumentationPath, diracPackage ) 
  try:
    os.mkdir( packageDir )
  except OSError:
    sys.exit( 'Cannot create %s' % packageDir )

  modulePackages = getPackageModules( diracPackage )

  indexPath = os.path.join( packageDir, 'index.rst' )
  with open( indexPath, 'w' ) as index:
    writeIndexHeader( index, diracPackage )
    
    for modulePackage in modulePackages:
      if not modulePackage in DOCMODULES:
        continue
      index.write( '\n\n   %s/index.rst' % modulePackage )
      packageModPath = os.path.join( packageDir, modulePackage )
        
      try:
        os.mkdir( packageModPath )
      except OSError:
        sys.exit( 'Cannot create %s' % packageModPath )

      packModPackages = getPackageModules( '%s.%s' % ( diracPackage, modulePackage ) )

      packageModPathIndex = os.path.join( packageModPath, 'index.rst' )
      with open( packageModPathIndex, 'w' ) as packModFile:
        writeIndexHeader( packModFile, modulePackage )
                    
        for packModPackage in packModPackages:
          
          if 'lfc_dfc_copy' in packModPackage:
            continue 
          if 'TransformationCLI' in packModPackage:
            continue
            
          route = 'DIRAC/%s/%s/%s.py' % ( diracPackage, modulePackage, packModPackage )
        
          route2 = tmpDir + '/../../' + route
           
          if not os.path.isfile( route2 ):
            print route2
            print 'Was a dir... skipping !'
            continue
              
          packModFile.write( '\n\n   %s' % packModPackage )
          packModPackagePath = os.path.join( packageModPath, '%s.rst' % packModPackage )
          f = open( packModPackagePath, 'w' )
          f.write( '=' * len( packModPackage ) )
          f.write( '\n%s\n' % packModPackage )
          f.write( '=' * len( packModPackage ) )
          f.write( '\n' )
          f.write( '\n.. automodule:: DIRAC.%s.%s.%s' % ( diracPackage, modulePackage, packModPackage ) )
          f.write( '\n   :members:' )
          f.close() 
#...............................................................................
# run

def run( diracVersion, tmpDir = None ):

  if tmpDir is None:
    tmpDir = getTmpDir()

  diracPackages         = getDIRACPackages()    
  codeDocumentationPath = getCodeDocumentationPath()
  
  writeCodeDocumentationIndexRST( codeDocumentationPath, diracPackages )
  
  for diracPackage in diracPackages:
    writePackageDocumentation( tmpDir, codeDocumentationPath, diracPackage )
  
#...............................................................................
# main

if __name__ == "__main__":

  try:
    tmpdir = sys.argv[ 1 ]
  except IndexError:  
    tmpdir = None

  try:
    diracVersion = sys.argv[ 2 ]
  except IndexError:  
    diracVersion = 'integration'
  
  run( diracVersion, tmpdir )
  
#...............................................................................  
#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF  