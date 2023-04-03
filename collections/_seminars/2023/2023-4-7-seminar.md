---
layout: post
speaker: "Vani Nagarajan"
title: "RT-DBSCAN: Accelerating DBSCAN using Ray Tracing Hardware"
time: 12p EST
location: "WANG 1004"
category: seminar
link_abstract: true
bio: "Vani Nagarajan is a 4th year PhD student in the department of ECE advised by Prof. Milind Kulkarni. She works on accelerating irregular applications using Ray Tracing hardware."
---
General Purpose computing on Graphical Processing Units (GPGPU) has resulted in unprecedented levels of speedup over its CPU counterparts, allowing programmers to harness the computational power of GPU shader cores to accelerate other computing applications. But this style of acceleration is best suited for regular computations (e.g., linear algebra). Recent GPUs feature new Ray Tracing (RT) cores that instead speed up the irregular process of ray tracing using Bounding Volume Hierarchies. While these cores seem limited in functionality, they can be used to accelerate n-body problems by leveraging RT cores to accelerate the required distance computations. In this work, we propose RT-DBSCAN, the first RT-accelerated DBSCAN implementation. We use RT cores to accelerate Density-Based Clustering of Applications with Noise (DBSCAN) by translating fixed-radius nearest neighbor queries to ray tracing queries. We show that leveraging the RT hardware results in speedups between 1.3x to 4x over current state-of-the-art, GPU-based DBSCAN implementations.
