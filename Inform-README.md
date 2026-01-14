# Interactive fiction and the Inform language

## Inform information

Inform 7 is a descriptive programming language which is used primarily for writing text adventure games.  By default, it organizes a program into *somewhat natural* English language paragraphs.  As the programming requirements get more complicated, the language required becomes a bit less natural.

In any case, here is a sample program that describes a silly game with just two rooms -- the object of the game is to pick up something that is found in the second room:

> Section 1 - the campsite
>
> The campsite is a room.  The description is "a typical campsite in a state park.  Trees line the site, and a picnic table is free.  There is a path leading east.".
>
> The huge van is a vehicle.  The description is "a veritable gas guzzler".  It is closed.
>
> Instead of opening the huge van:
> > say "You seem to have misplaced the keys.".
>
> The park ranger is a woman.  The description is "She seems to be interested in the trees".  She is here.
>
> The trees are a backdrop.  They are everywhere.
>
> The picnic table is an enterabble supporter.  It is here. It is scenery.
>
> The bench is an enterable supporter. It is part of the picnic table.
>
> Instead of entering the picnic table:
> > try entering the bench.
>
> Section 2 - lakeside
>
> The lakeside is a room.  The description is "a beach bordering a large lake. Trees line the border. There is a path leading west.".  It is east of the campsite.
>
> The lake is here. It is scenery.  The beach is here.  It is scenery.
>
> The lucky penny is here.  The description is "It is probably worth about one cent!".
>
> The epilogue is a scene.  The epilogue begins when the player is carrying the lucky penny.
>
> When the epilogue begins:
> > end the story finally saying "Congratulations. The penny is actually a very rare one cent coin with a market value of 25 cents!".

(**NOTE:** I haven't actually compiled and tested the code, so there may be a few bugs.)

Note the style of the code.  Most of the statements simply describe various objects that exist in the game world.  This is quite characteristic of a descriptive programming language,  When the code is compiled, it is translated into an object-oriented language (Inform 6) which is then compiled into code for a target machine (*e.g.*, the Z-machine) which is then run in an interpreter.

If we were playing this game, the interpreter output would look something like this:
```
   "Campsite Blues".
   December 25, 2025.

   campsite.
   a typical campsite in a state park.  Trees line the site, and a picnic table is free.  There is a path leading east.

   A huge van and a park ranger are here.
   > examine trees
   There is nothing special about the trees.
   > east
   lakeside
   a beach bordering a large lake. Trees line the border. There is a path leading west.

   There is a lucky penny here.
   > examine lake
   There is nothing special about the lake.
   > take lake
   It is scenery.
   > examine penny
   It is probably worth about one cent!
   > take penny
   Taken.
    *** Congratulations. The penny is actually a very rare one cent coin with a market value of 25 cents! ***
```

## Interactive fiction

Here are some links for more information:

* The Interactive Fiction Archive: <https://www.ifarchive.org/>.
* The Interactive Fiction Wiki: <https://www.ifwiki.org/Archive>.
* The IfWiki starter links: <https://www.ifwiki.org/Starters>.
* The Interactive Fiction Community Forum: <https://intfiction.org/>.

