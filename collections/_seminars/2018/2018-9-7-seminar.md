---
layout: post
speaker: "Fei Wang"
title:  "Lantern, a Machine Learning framework built on Delimited Continuations and Staging"
location: "LWSN 3102A/B"
category: seminar
link_abstract: true
---

Deep learning rests in crucial ways on gradient-descent optimization and end-to-end differentiation. Under the slogan of differentiable programming, there is an increasing demand for efficient automatic gradient computation for emerging network architectures that incorporate dynamic control flow (especially in NLP).

In this talk, we take a fresh look at backpropagation, and propose an implementation using Delimited Continuations. We also combine it with native code generation techniques called Multi-Stage Programming (staging), which leads to a highly efficient implementation that combines the performance benefits of software frameworks based on explicit reified computation graphs (e.g.,TensorFlow) with the expressiveness of pure library approaches (e.g., PyTorch).
