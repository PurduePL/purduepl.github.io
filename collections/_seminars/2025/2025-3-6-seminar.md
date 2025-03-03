---
layout: post
speaker: "Paschal Amusuo"
title: "Evaluating the Use of Unit Proofs for Verifying Memory Safety of Embedded Software"
time: 12:00p EST
location: "WANG 1004"
category: seminar
invited: false
link_abstract: true
bio: "Paschal is a 4th year PhD student in the school of electrical and computer engineering at Purdue University, working with Prof James Davis. His research explores the use of novel insights from empirical software measurements to improve the validation and verification of critical software components."
---
Bounded Model Checking (BMC) provides formal guarantees that a software satisfies functional and security properties.
To scale BMC to larger software, the software can be decomposed into units, and unit proofs created to verify each unit.
However, despite adoption by major organizations, unit proofing remains understudied in research and underutilized in practice.
Existing experience reports lack detailed insights into unit proofs, and empirical studies on formal verification do not address them.
 
This work presents the first empirical study on unit proofing for memory safety in embedded software.
We developed unit proofs for 100 functional units across four embedded operating systems, analyzing their complexity, cost, defect detection effectiveness, and generalizability to uncovered functions and embedded software.
Our results show that verifying memory safety often requires simple, fast unit proofs, and using verification coverage as a completeness metric exposes 85\% of known memory safety defects.
Additionally, unit proofs targeting previously exploitable components uncovered 21 new exploitable defects in them, highlighting the need for memory safety verification in these components.