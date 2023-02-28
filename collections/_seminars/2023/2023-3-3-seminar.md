---
layout: post
speaker: "Dan Plyukhin"
title: "A Language For Low-Latency Distributed Systems (WIP)"
time: 12p EST
location: "WANG 1004"
category: seminar
invited: true
link_abstract: true
bio: "Dan Plyukhin is a 6th year PhD candidate at the University of Illinois at Urbana-Champaign (UIUC) and a research assistant at the University of Southern Denmark (SDU). His research applies programming language methodologies to increase reliability and efficiency in distributed systems. His dissertation research investigates fault-tolerant distributed resource management in actor systems such as Akka and Erlang."
---
Building latency-critical distributed systems such as IoT and microservices is tedious and error-prone. Large systems can consist of thousands of independent components that must coordinate in order to complete various protocols. Implementations of such protocols must take advantage of all available parallelism and minimize latency, yet be easy to reason about and compose into larger protocols. These requirements appear to be at odds: minimizing latency is best achieved with a decentralized approach, yet reasoning is easiest from a logically centralized perspective.

In this talk, I will propose a new abstraction: poroutines. A poroutine is a logically centralized procedure that encodes a distributed dataflow graph. Poroutines are first-class, deadlock-free by construction, and composable like functions. Moreover, poroutines can be compiled to produce decentralized message-passing code.

Poroutines build on three independent lines of work: distributed futures, used in data-intensive applications such as Ray and PyTorch; choreographies, used in service-oriented computing; and lenient dataflow languages, which have been used for shared memory parallelism. I will show that several long-standing problems in each of these areas can be solved with insights from the others.

This talk describes a work in progress, developed in collaboration with SDU.
