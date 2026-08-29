---
layout: post
speaker: "Matthew Borland"
title: "IEEE 754 Decimals for C++: The Boost.Decimal Library"
time: 12p EST
location: "WANG 1004"
vc_link: "https://purdue-edu.zoom.us/j/91273616257?pwd=5lIin8gdpX9canY0DYOoNpIFglqRU3.1"
category: seminar
invited: false
link_abstract: true
bio: "Matt Borland earned his bachelor's from the University of Michigan and his master's from the Georgia Institute of Technology, and is currently a doctoral candidate in Electrical and Computer Engineering at Purdue University. He is the author of Boost.Charconv and Boost.Decimal, both developed at the C++ Alliance. He is also a core maintainer of several other Boost libraries, including Boost.Math and Boost.Multiprecision."
---

Why does 0.1 + 0.2 not equal 0.3? Because binary floating-point cannot exactly represent most decimal fractions, the value 0.1 simply does not exist in IEEE 754 binary. For applications where rounding errors are unacceptable, finance, billing, regulatory reporting, scientific data interchange, this is a structural problem, not a precision setting that can be tuned away. IEEE 754-2008 introduced a decimal floating-point alternative that stores the significand in base 10, and ISO/IEC TR 24733 sketched a C++ binding for it. Compiler support, however, has remained uneven across vendors and architectures.

Boost.Decimal is a header-only, dependency-free, C++14 implementation of IEEE 754-2008 and TR 24733 decimal floating-point. It provides three IEEE-conformant types, decimal32_t, decimal64_t, and decimal128_t, and three companion decimal_fast*_t types that trade strict bit-layout conformance for speed where you don't need on-the-wire interoperability. All six types behave like built-in floating-point: they're constexpr-friendly throughout, support mixed arithmetic and promotion, and ship with their own implementations of `<cmath>`, `<charconv>`, `<format>`, `<cstdio>`, `<cfenv>`, `<functional>` hashing, `<limits>`, and Boost.Math integration. The library is tested natively on x86_64, ARM64, and s390x, and under emulation on PPC64LE and ARM Cortex-M.

This talk is the introduction to decimal floating-point that most C++ programmers never got. We'll cover what decimal floating-point actually is at the bit level (BID vs. DPD encodings, the cohort concept that has no analogue in binary), why the standard library's defaults are what they are (e.g. Rounding), and how Boost.Decimal's API maps onto familiar `<cmath>` and `<charconv>` patterns. We'll work through worked examples, parsing a price feed, computing financial summary statistics through Boost.Math, round-tripping values through `<charconv>` while preserving cohort information, and walk through the library's deliberate deviations from both IEEE 754 and the C++ standard, including why floating-point exception flags were sacrificed to keep constexpr and how from_chars was extended to distinguish overflow from underflow as well as preserve cohorts. We'll close with reviews of the benchmarks versus binary floating point, as well as other existing libraries.

By the end, attendees will know when reaching for decimal is the right call, which of the six types fits their workload, and what trade-offs the library made on their behalf.
