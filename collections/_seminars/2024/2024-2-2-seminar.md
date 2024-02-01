---
layout: post
speaker: "Qianchuan Ye"
title: "Language-based Techniques for Policy-Agnostic Oblivious Computation"
time: 12p EST
location: "LWSN 3102A/B"
category: seminar
invited: false
link_abstract: true
bio: "Qianchuan Ye is a PhD candidate at Purdue University, working with Prof. Ben Delaware. He is interested in proof assistants, type theory and programming languages."
---

Protecting personal information is growing increasingly important to the general public, to the point that major tech companies now advertise the privacy features of their products. Despite this, it remains challenging to implement applications that do not leak private information either directly or indirectly, through timing behavior, memory access patterns, or control flow side channels. Existing security and cryptographic techniques such as secure multiparty computation (MPC) provide solutions to privacy-preserving computation, but they can be difficult for non-experts to use.
In this talk, I will discuss the design of a high-level programming language that aims to help programmers write privacy-critical applications under a strong threat model (as in MPC). This language supports private structured data, such as trees, and complex policies that go beyond whether a particular field of a record is private. More crucially, it allows programmers to implement privacy-preserving applications modularly, i.e. to independently develop application logic and independently update and audit privacy policies. I will introduce the key ideas behind this language, a security type system that employs dependent types to provide strong guarantees about information leakage and a evaluation strategy that repairs unsafe computation dynamically. I will then discuss how employing a static policy enforcement approach enables exponential performance improvements on a variety of secure applications involving structured data and complex privacy policies.
