---
layout: post
speaker: "Yuantian Ding"
title: "Enhanced Enumeration of Techniques for Syntax-Guided Synthesis of Bit-Vector Manipulations"
time: 12p EST
location: "LWSN 3102A/B"
category: seminar
invited: false
link_abstract: true
bio: "[Yuantian Ding](https://dnailz.github.io) is a second-year PhD student from Purdue ECE, working with Prof. [Xiaokang Qiu](https://engineering.purdue.edu/~xqiu/). He's primarily interested in various program synthesis tasks, with a particular focus on syntax-guided synthesis."
---
Syntax-guided synthesis has been a prevalent theme in various computer-aided programming systems. However, the domain of bit-vector synthesis poses several unique challenges that have not yet been sufficiently addressed and resolved. In this paper, we propose a novel synthesis approach that incorporates a distinct enumeration strategy based on various factors. Technically, this approach weighs in subexpression recurrence by term-graph-based enumeration, avoids useless candidates by example-guided filtration, prioritizes valuable components identified by large language models. This approach also incorporates a bottom-up deduction step to enhance the enumeration algorithm by considering subproblems that contribute to the deductive resolution. We implement all the enhanced enumeration techniques in our SyGuS solver DryadSynth, which outperforms state-of-the-art solvers in terms of the number of solved problems, execution time, and solution size. Notably, DryadSynth successfully solved 31 synthesis problems for the first time, including 5 renowned Hacker's Delight problems.
