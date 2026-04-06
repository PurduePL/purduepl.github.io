---
layout: post
speaker: "Sam Estep (MWPLS)"
title: "Contextual Monomorphization"
time: 12p EST
location: "DSAI 1069"
category: seminar
invited: true
link_abstract: true
bio: "Sam Estep is a PhD student at Carnegie Mellon University, with a focus on programming language design and compiler implementation. His research centers around heterogeneous programs where some parts are more performance-sensitive than others, such as documents using numerical optimization for diagram layout, or differentiable graphics pipelines spanning multiple kernels."
---
A flamechart models a program's execution as a hierarchy of nested calls. This is a very natural view, which is why dynamic scoping was invented before lexical scoping, and is still around today in more constrained forms despite its flaws. However, dynamic scoping has limited applicability to performance-sensitive programming, because dynamism makes it difficult for the compiler to perform the usual tricks that get unlocked by inlining. This talk presents a new programming language mechanism for managing context, allowing the programmer to make different choices for different sections of the same program, then letting the compiler optimize separately for each choice. Many common language features can be subsumed under this, including compilation flags, parametric polymorphism, ad-hoc polymorphism, and Lisp-style dynamic scoping. Applications include arena-style memory management, instrumentation for debugging individual parts of a program, and generic libraries for numerical computation.
