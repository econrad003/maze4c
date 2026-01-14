# Inform folder

## Text adventures, the Z-machine, and Inform

Inform is a family of programming languages that are oriented to producing text adventures.  The languages were inspired by the games Cave (aka Adventure), originally written in Fortran, and Zork, a commercial adventure game based loosely on Cave, produced by a company called Activision, and released for a number of early microcomputers.

Since microcomputer architecture in the early 1980s varied considerable, Zork was written for a virtual machine (the Z-machine).  Instead of writing game code for a number of different computers, Activision wrote an assembler and an interpreter for the Z-machine and instead simply assembled Zork for the Z-machine.  This programming model was viable -- a number of other text adventure games were written for the Z-machine, including Zork 2, Zork 3, the leather goddesses of Phobos, and, based on the Douglass Adams book, the hitchhiker's guide to the galaxy.  The Z-machine was extended to incorporate media such as images and sound -- a game called King Arthur used one such extension.  But eventually text adventures were supplanted by games that used graphical interfaces.  Today, text adventures are mainly written for the pleasure of hobbyists.

The Inform language was designed to compile programs for the Z-machine.  Prior to version level 7, Inform was an object-oriented compiler, somewhat like C++ or Modula II.  Beginning with level 7, the language uses somewhat natural flavor of English syntax.  Inform 7 actually compiles into Inform 6 before being compiled into code for a virtual machine, such as the Z-machine.

(The Z-machine architecture dates to an era when 64kB (65536 bytes) and 256kB (262144 bytes or 1/4 of a megabyte) were considered to be a lot of memory, so the default architechure for inform uses a somewhat larger machine, but Inform can also compile to the Z-machine.)

## HELLO WORLD in Inform 7

Here is a simple hello-world program written in Inform 7:

```
"Hello.inform"

Start is a room.  The description of start is "Nothing ever happens here.".

When play begins:
    say "Hello, adventurer!".
```

Inform is a declarative language used primarily for room-based text adventures.  A "room" is just a node or vertex in a graph, or a cell in a maze.  So most Inform programs declare at least one room.  The first paragraph declares a room and gives it a description.

The second paragraph displays a message at startup.  After compiling this program and running the output in an interpreter, you would see somthing like this:

```
Hello, adventurer!

Hello.inform, compiled 7 August, 3025.

Start
Nothing ever happens here.
>
```
There isn't much that can be done at this point, because the program doesn't specify much, but a lot of material is compiled by default.  For example:
```
Hello, adventurer!

Hello.inform, compiled 7 August, 3025.

Start
Nothing ever happens here.
> go east
You can't go that way.
> examine me
You are handsome as ever.
```
The actual responses to the commands are slighly different, but perhaps you get the drift.  Apparently, by default, the compiled code includes a command parser with a lot of default responses.  It also includes a character (known as "the player") whose actions are guided by these commands.  By default, the player is an extension of the person who types the commands.

## Introduction to Inform programming

We could add a couple of lines to our "story" to make it slightly more interesting:
```
"Hello.inform"

Start is a room.  The description of start is "Nothing ever happens here.".

When play begins:
    say "Hello, adventurer!".

The magical chamber is east of start.  The description is "Shazam!".

There is an oak tree here.  It is fixed in place.

There is a pine tree here.  It is scenery.

There is a daisy here.  The description "It's very pretty.".

There is some gold here.

There is some poison here.

After taking the daisy:
    say "It crumbles in your rough hands!";
    now the daisy is nowhere.

After taking the gold:
    end the story finally saying "You win!".

After taking the poison:
    end the story finally saying "You lose!".
```

That gives one possible path to winning the game:
```
Hello, adventurer!

Hello.inform, compiled 7 August, 3025.

Start
Nothing ever happens here.
> go east
Shazam!

There is an oak tree, some gold, a daisy and some poison here.
> examine daisy
It's very pretty.
> take daisy
It crumbles in your rough hands!
> take oak
It is fixed in place.
> examine pine
There is nothing special about the pine.
> take gold
You win!
```



