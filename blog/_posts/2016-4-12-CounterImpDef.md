---
layout: post
title: Definitions VS Implementation
---

Let's dive into the problem. Consider the following code, which is a definition of a simple counter with two functions, query and incerement: 


``` coq
Definition GCounter_State : Set := nat.

Inductive GCounter : Type :=
|ConsGCounter : GCounter_State -> GCounter.

Definition GCounter_read (c: GCounter): GCounter_State:=
  match c with
    |ConsGCounter n => n
  end.

Definition GCounter_inc (c: GCounter): GCounter :=
  match c with
    |ConsGCounter n => ConsGCounter (n+1)
  end.
```
We could make it even simpler: 

``` coq
Definition GCounter' := nat.
Definition GCounter'_read (c:GCounter'): nat := c.  
Definition GCounter'_inc (c:GCounter'): GCounter' := c+1.
```
Consider either of the definitions above. They both specify what you (as a programmer) expect from a counter datatype; it preserves a natural number for you, and lets you to increment it.
<br>
Now imagine you (as a language designer) are given one the above definitions and asked to equip your language with such a datatype. In an isolated system with no failure, this would be a piece of cake. 
But what if you are asked to implement it as a replicated data object?<br> 
Considering the amzing capabalities of CRDTs (Which in my opinion, are the best things you can get, within limitation of CAP theorem, [read more](https://vaughnvernon.co/?p=1012))
you decide to implement the counter as a CRDT as follows:

``` coq
Inductive GCtr_Eff: Type := |inc.

Definition GCtr:Type := list GCtr_Eff.

Definition GCtr_read (c:GCtr) : nat := length c.

Definition GCtr_inc (c:GCtr) : GCtr := (cons inc c).

Definition Gctr_resolve  (c1 : GCtr_Eff) (c2 : GCtr_Eff) :list GCtr_Eff :=
  match (c1,c2) with
    | (inc,inc) => cons inc (cons inc nil)
  end.

``` 
You are done, Congradulations! <br>
But wait... this transformation is not intuitive at all. You have implemented a natueal counter as a list of objects! 
Now you need to prove that your implementation is correct (i.e. behaves the same as the specifications given to you).
<br> How are you going to proceed? 





