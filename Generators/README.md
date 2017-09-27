# CoTeTo: Generator Packages

CoTeTo generators are bundles of files that are specific to an output
configuration (like a special modelica library or a specific input data API).

## Search Path
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

## Contents of a Generator
A generator may be:

1. a subfolder or
2. a zip file (not working correctly at the moment)

containing a file Package.inf and a special folder structure.

Documentation will follow soon, please have a look at the examples for now. The
easiest way to create a generator is to make a copy of an existing generator
and adjust the contents.

### Package.inf
This file uses the well-known INI format. It needs the sections and entries described here. All other information will be ignored by the CoTeTo system, but can be accessed in your loader, filter and template code (using `generatorCfg`).

#### Section GENERATOR
The entries `name`, `version`, `description` and `author` can be used to describe the generator.

#### Section REQUIRES
This section will currently not be evaluated, but can be used to define dependencies of this generator. Checks may be added in later versions.

#### Section LOADER
Define the `name` and versions (`minVer` and `maxVer`) of the loader here.

#### Section FILTER
You can specify a filter function by a `module` and a `function` to be executed after the data is loaded. The code is searched in the subfolder `Filters`.

#### Section TEMPLATEx
All sections starting with the string `TEMPLATE` define a template structure to use.
Such a section need at least one entry called `topFile` to specify the top level template file (located in the subfolder `Templates`). The type of the template can be specified with the entry `type`. At the moment only `mako` (default) and `jinja2` are supported.

If you use more than one TEMPLATE section you should use an entry `ext` to specify the file extension (appended to the base output file name).
