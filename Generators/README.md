CoTeTo: Generator Packages
==========================

CoTeTo generators are bundles of files that are specific to an output
configuration (like a special modelica library or a specific input data API).

Search Path
-----------
Generators are loaded from a list of folders (usually containing this folder).
When using the provided command line or graphical interface you may adjust
the folder search using different ways:

1. The environment variable `COTETO_GENERATORS` (path elements separated by ;)
2. An entry `GeneratorPath` in the section `DEFAULT` in the configuration file
  `.CoTeTo.cfg` in the users home folder
3. The `-d` switch on the CLI or GUI

Two more folders are searched by default (if they exist):
1. The folder `Generators` in the parent folder (one level up) of the CoTeTo 
   module package. This enables CoTeTo to run without installation.
2. The folder `CoTeTo_Generators` two levels up of the CoTeTo module package.
   This allows CoTeTo to be a submodule in git and the generators to be 
   stored in a parallel folder. 

Contents of a Generator
-----------------------
A generator may be:

1. a subfolder or
2. a zip file

containing a file Package.inf and a special folder structure.

Documentation will follow soon, please have a look at the examples for now. The
easiest way to create a generator is to make a copy of an existing generator
and adjust the contents.
