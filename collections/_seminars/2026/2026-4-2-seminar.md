---
layout: post
speaker: "Paschal Amusuo"
title: "Do Unit Proofs Work? An Empirical Study of Compositional Bounded Model Checking for Memory Safety Verification"
time: 12p EST
location: "DSAI 1069"
category: seminar
invited: false
link_abstract: true
bio: "Paschal Amusuo is a 5th-year PhD candidate in the school of Electrical and Computer Engineering, advised by Prof. James Davis. His research focuses on developing techniques that enable systematic and scalable memory safety assurance on embedded software systems. He combines empirical software engineering methodologies with program analysis and formal method techniques to understand how vulnerabilities manifests in embedded software and to design systematic workflows and systems that reliably discovers these vulnerabilities."
---
Memory safety defects pose a major threat to software reliability, enabling cyberattacks, outages, and crashes. To mitigate these risks, organizations adopt Compositional Bounded Model Checking (BMC), using unit proofs to formally verify memory safety.  However, methods for creating unit proofs vary across organizations and are inconsistent within the same project, leading to errors and missed defects.  In addition, unit proofing remains understudied, with no systematic development methods or empirical evaluations.

This work presents the first empirical study on unit proofing for memory safety verification. We introduce a systematic method for creating unit proofs that leverages verification feedback and objective criteria.  Using this approach, we develop unit proofs for 73 components across four embedded operating systems and evaluate their effectiveness, characteristics, cost, and generalizability.  Our results show unit proofs are cost-effective, detecting 74% of recreated defects, with an additional 9% found with increased BMC bounds, and 20 new defects exposed.  We also found that embedded software requires small unit proofs, which can be developed in 87 minutes and executed in 61 seconds on average.  These findings provide practical guidance for engineers and empirical data to inform tooling design.
