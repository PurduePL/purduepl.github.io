---
layout: default
title:  "CS590 - Individual Study Projects"
permalink: cs690-suresh-fall16.html
---
<div class="center-align">
  <h2>CS590/CS690 - Projects</h2>
  <h3>Instructor: Suresh Jagannathan</h3>
</div>

<h3>MagLev</h3>

<div class="inline-img-div" id="maglev-img-div">
</div>
MagLev is a symbolic execution engine for Ruby-on-Rails. It is written
as a Ruby library (a gem) that runs Rails web applications on symbolic
inputs (instead of concrete inputs) and records the execution in form
of an abstract program that can be analyzed offline. A symbolic
execution of a program captures its behavior with respect to its
inputs, thus helps us analyze the program without having to analyze
its source code. For example, if a program calls `subString` method on
a symbolic string object provided to it as an input, then we know that
the program calls `subString` method on all its string inputs. By
performing enough such symbolic executions, we can thus analyze the
program completely without having to build sophisticated static
analyses on its source code. The novelty of MagLev is that it coaxes
Ruby's concrete interpreter (MRI) to also accept symbolic inputs, thus
getting symbolic execution effectively for free. More about MagLev in
this [short paper]({{ site.baseurl }}/docs/maglev.pdf).

MagLev has been under development for few months now, and we do have a
working prototype. However, there are still some important problems to
be solved before MagLev is fit to be used on real web applications.
For example:

+ MagLev does not yet have a robust approach of dealing with
  higher-order functions, such as `map` and `each`, which are used
  heavily in Rails applications to iterate over collections.
+ MagLev forks Unix processes to explore various control-flow paths
  that branch on a symbolic input. The approach works quite well for
  small-to-medium size web applications, but its scalability for
  large application is still an open question.

An independent study on MagLev is a good opportunity to work on the
above problems, while learning advanced PL and compiler techniques by
applying them to the real-world applications.

<h3>Quelea</h3>

<div class="inline-img-div" id="quelea-img-div">
</div>

In pursuit of high scalability and _always-on_ experience, large scale
web services, such as Facebook and Amazon, have embraced
[unconventional](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)
[storage](https://static.googleusercontent.com/media/research.google.com/en//archive/bigtable-osdi06.pdf)
[systems](https://www.cs.cornell.edu/projects/ladis2009/papers/lakshman-ladis2009.pdf)
with weak consistency guarantees. The widespread adoption of
cloud-based deployment model (i.e., deploying applications via
Amazon's EC2 or Google's Compute Engine) has incentivized the use of
weakly consistent data stores even for small-to-medium scale web
applications. Unfortunately, programming with such stores is
significantly more complicated than programming with conventional
relational databases, and much of this complexity can be attributed to
the lack of sufficient programming abstractions and concurrency
control mechanisms that provide strong enough guarantees. To address
this problem, we built [Quelea](https://gowthamk.github.io/Quelea/), a
programming framework
that simplifies the task of developing highly scalable web
applications on the top of eventually consistent NoSQL stores, such as
Cassandra. The utility of Quelea is demonstrated by the wealth of
applications written on top of Quelea, such as a Twitter-like
Microblog and an eBay-like auction site. Quelea is
[open-sourced](https://github.com/kayceesrk/Quelea), and version 1.0.0
is available on [Hackage](https://hackage.haskell.org/package/Quelea).
Quelea is under active development, and we are currently working on
including the support for:

+ Fine-grained consistency guarantees, such as
  [Read-Your-Writes](https://docs.oracle.com/cd/E17276_01/html/gsg_db_rep/C/rywc.html), and [Monotonic Reads](https://en.wikipedia.org/wiki/Consistency_model#Monotonic_read_consistency).
+ Approximate invariants, such as _an item cannot be
  oversold by 2% of the available stock_, or _the value of a video
  view counter should never be more than 1% off from the actual
  count_.
+ Consistency inference, i.e., automatically inferring appropriate
  consistency levels for various operations so as to preserve program
  invariants.

An independent study on Quelea is a good opportunity to work on the
above problems, while gaining advanced skills in Distributed Systems,
Databases and PL.

<h3>Irmin</h3>

<div class="inline-img-div" id="irmin-img-div">
</div>

Git version control is a widely used technology to manage concurrent
revisions to the source code, and to track the history of changes.
Can Git be used to manage, not just the source code, but also the
data accessed by concurrent processes? This is the essential idea
underlying [Irmin](https://mirage.io/blog/introducing-irmin). Irmin is
a library to persist and synchronize distributed data structures both
on-disk and in-memory. It enables a style of programming very similar
to the Git workflow, where distributed nodes fork, fetch, merge and
push data between each other. The general idea is that you want every
active node to get a local (partial) copy of a global database and
always be very explicit about how and when data is shared and
migrated.

Irmin is a subject of active research at
[Cambridge University OCaml
Labs](https://www.cl.cam.ac.uk/projects/ocamllabs/), and is part of an
umbrella of projects that includes [Unikernels](https://unikernel.org/) and
[Mirage OS](https://mirage.io/).

An independent study focused on Irmin is a great opportunity to
explore unconventional ways of engineering a NoSQL store or an
Internet-of-Things (IoT) based on the Git-based data model facilitated
by Irmin.
<br />
<br />

<h3>Contact</h3>

If you are interested in any of the aforementioned projects, please
contact [Prof. Suresh
Jagannathan](https://www.cs.purdue.edu/homes/suresh/) or [Gowtham
Kaki](https://gowthamk.github.io/) with the details about yourself that
you consider to be relevant to the project.
