# KiCommand - Kicad Command Line

KiCommand allows simple command strings to be executed within pcbnew.
Command strings consist of a variety commands that retrieve, filter, and
process Kicad objects. Commands are very easily added with a simple syntax.

[Development and discussion thread](https://forum.kicad.info/t/7694) on KiCAD forums.

[Tutorial and Wiki](https://forum.kicad.info/t/21008). The tutorial assumes no prior knowledge and will teach you step by step how to use KiCommand.

Here are a few short examples:

- **pads setselect**
    - select all pads
- **: selectallpads pads setselect ;**
    - define a new command called **SELECTALLPADS** that select all pads
- **modules U1 matchreference getpads setselect**
    - select the pads of the module with reference 'U1'
- **: selectmodpads modules swap matchreference getpads setselect ;**
    - define a command that select the pads of the module indicated by the argument.
    - Use the command like this: **U1 selectmodpads**
- **valuetextobj DeleteStructure call**
    - Delete all value objects on the modules
- **valuetextobj selected DeleteStructure call**
    - Delete all selected value objects on the modules

## Getting Started
### Installation

- Place the entire kicommand folder in 
**C:\Program Files\KiCad\share\kicad\scripting\plugins**
Or the equivalent in MacOS or Linux
(*there may be a user-level directory for such files, but I am not aware of it at the moment.*)

#### For KiCad (5.1.5)-3 release:
KiCommand is an ActionPlugin and is installed similarly to other Action Plugins:

1) Within KiCad pcbnew, select the Tools > External Plugins > Refresh Plugins
2) The next time you start pcbnew, the *KiCommand* menu item will already be in the *External Plugins* menu so there should be no need to *Refresh Plugins*.

KiCommand dialog box is shown when the Tools > External Plugins > KiCommand menu item is selected.

#### From the Scripting Console

Select *Tools > Scripting Console...* then enter

    import kicommand
    kicommand.KiCommandAction.getInstance().Run()
    from kicommand.kicommand import kc
    
This will show the KiCommand dialog, and is exactly what is run when KiCommand is selected from the "External Tools..." menu. The last line will allow you to enter *KiCommand* commands from the console using the *kc* command:

    kc('board print')

### Testing Your Installation
Select *Tools > Scripting Console...* then enter

    import kicommand.test

This will execute a series of tests, running a series of *KiCommand* commands and verifying the results. You should see all of the tests return *OK*.

### Self Documented Help
When KiCommand starts up, it displays help information to get you started.

Essentially, how to get more help with a variety of help commands.

Commands are organized by category, and the main help commands display general
help (**help**), command categories (**helpcat**), detail help on specific commands (**explain**),
or detailed help of all commands (**helpall**)

# Overview

With KiCommand, arguments to commands are entered *before* the command. Any results
from the command are then used as an argument to the *next* command. This way,
you can chain together commands in a way that often makes sense. This 
programming structure is
called *[stack-based programming](https://en.wikipedia.org/wiki/Stack-oriented_programming_language)*.

KiCommand has several advantages over Python Scripting:

- Simplicity in programming and argument type handling make KiCommand more
accessible than the equivalent KiCad Python scripting.
- Command strings mean less worrying about variables.
- Command strings are often short and easily sharable.
- Many commands accept a variety of input types, and still work as you would expect.
- Programming structure means you don't have to worry as much about variables.
- KiCommand naturally handles lists of objects, so looping over objects is not
needed: it just happens.
- Being able use pcbnew Python object attributes and functions gives
KiCommand a lot of access to the Kicad object model.
- Defining new commands is simple.
- With KiCommand handling of argument types, there's less worrying about
exact types.

And several disadvantages:

- Built in commands have flexible argument types, while Python commands
(accessed with **callargs**) may require careful argument manipulation.
- Many commands are simple and straightforward, while complex commands are
possible. The stack-based structure makes some complex strings difficult to
decipher or create, even for experienced programmers.
- While creating entirely new elements from scratch is usually possible,
command strings are sometimes wordy.
- There are currently no looping or conditional commands.
- Full flexibility is only available with Python scripting. Command strings
are a short simple interface for some object manipulation or interrogation.

## Introduction to Command Strings and Programming Structure

In KiCommand, a *Command String* contains a sequence of arguments and commands
that are executed sequentially. Arguments occur before the command that uses 
them. The arguments are *consumed* by a command and the results of the command
are stored on top of any previously unused arguments or results, making those 
arguments and results available to future commands. 

This is implemented and often imagined as a *stack* structure.
In this structure, the stack holds *values* (aka *operands* or *arguments*) that are used in
subsequent *commands*.

Several important characteristics of the stack structure of programming:

- operands are placed **on top of the** ***stack*** when encountered in the 
*command string*
- operands are removed **from the top of the** ***stack*** when commands are encountered in the command string
- results from commands are placed **on top of the** ***stack***, to be used as operands in future commands.
- results from previous commands continue to exist on the stack until used.
In this way, results from past commands build up to become arguments for future commands.
- again, commands generally remove their arguments from the stack and return their results
to the stack. If you need to execute several commands on the same argument, the
**copy** and **swap** commands will be useful.

## Examples

- **modules**
    - return the list of modules
- **modules selected**
    - return the list of selected modules
- **modules selected clearselect**
    - unselect all selected modules
- **modules setselect**
    - select all modules (this seems to have no visual effect)
- **pads setselect**
    - select all pads
- **pads clearselect**
    - unselect all pads
- **modules getpads setselect**
    - select all pads of all modules
- **modules getpads clearselect**
    - unselect all pads of all modules
- **modules U1 matchreference getpads setselect**
    - select the pads of the module with reference 'U1'

### Defining commands

KiCommand allows you to define your own commands, too, using a colon (**:**) to begin the command definition. More information on defining commands can be found in the [Tutorial and Wiki](https://forum.kicad.info/t/21008).

### General Conventions

KiCommand follows a general set of conventions:

- Commands are all lower case.
- Arguments are usually Mixed Case.
- Python commands within Command Stack are whatever is needed, but mostly will be Mixed Case or UPPER CASE.
- To enter a string argument that also happens to be a command, use the single quote mark (') such as in the following string: **'calllist help**
- To enter an argument that requires any spaces (such as a filename or command help text),
use double quotes around the argument (i.e. **"argument with spaces"**).
- Access to Python functions and attributes are exactly as documented in the [Python pcbnew documentation](http://docs.kicad-pcb.org/doxygen-python/namespacepcbnew.html), which are often in either mixed case or all caps. Example: **modules GetCenter call**
- Arguments are handled slightly differently in the **call** and **callargs** commands. They operate fairly seamlessly with, and often require lists. Calling a Python function on list executes that function on each member of the list. 
- Define a new command with the colon, and end with the semicolon.
    - **: newcommand ARG Arg command ARG command ;**
- Core commands either place objects on the stack or operate on objects on the stack. The commands that place a list of objects on the stack are in the category *Elements* and are listed with the command **Elements helpcat**:
    - **modules**
    - **pads**
    - **tracks** - includes vias
    - **drawings**
- From these core commands, other commands are defined to retrieve certain objects.    
    - **textobj**
    - **valuetextobj**
    - **referencevalueobj**
    - **toptext**
- And in case there is anything missing, you can access the top-level board and pcbnew objects.
    - **pcbnew** - top level pcbnew Python object
    - **board** - top level Board Python object from **pcbnew.GetBoard()**
- And finally, you can filter each of the above objects to choose exactly the objects you want, or get at them in slightly different ways.
    - **pads selected**
    - **modules U1 matchreference getpads**
    - **tracks VIA filtertype**

### Calling Python commands

Calling Python within a *Command String* is possible and there are several commands
designed to do so within the *Programming* category, with commands in the 'Conversion'
category being useful to convert arguments to the correct format and type.

- **call** - used to call a Python object's function that requires no arguments (such as a call to GetShapeStr on a DRAWSEGMENT object)
- **callargs** - used to call a Python object's function that requires arguments. Arguments
are in the single argument as a list of lists, where each inner list contains the arguments
for a single call. The inner list contains as many members as arguments necessary
for the command. The commands **zip2**, **float**, **list** and **delist** might be useful here.
- **attr** - retrieves an attribute from an object. This can be a value or a function, though
if it were a function, it's probably more useful with the **call** or **callargs** commands to actually call the function.

### Lists
Many commands can use lists as arguments. Often, lists as
arguments are used in parallel, and the results are in parallel
as well. For example, if there is a list of DRAWSEGMENTs at
the top of the stack, the command string **GetShapeStr call**
will result in a parallel list of outputs from the corresponding
DRAWSEGMENT. The command is repeated for each member of the list.

To filter lists, try using the **filtertype**, **filter**, 
and commands in the *Comparison* category.

### About Capitalization

- The capitalization convention works well with most text on the board in uppercase and most Python functions and variables being upper or mixed case.
- Mixed Case items are all arguments (Python functions and objects look like arguments in the Command String). Mixed case arguments means they also do not get interpreted as commands.
- Lower case commands do not conflict with the namespaces of most Python commands/variables nor do they conflict with arguments.
- Note that these capitalization conventions almost eliminate the need for using single quote (it still may be necessary in some cases).
