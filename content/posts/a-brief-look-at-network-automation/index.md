---
title: "A brief look at Network Automation"
date: 2017-06-06
categories: ["network", "automation"]
tags: ["network", "automation", "python"]
---

There is an incredible amount of hype these days discussing automation especially in the realm of networking. Some would say that this is relatively new but I would argue that we have been struggling with automating the network for many decades, it is however becoming critical today due to the massive dependencies on our communications facilities and shifting application architectures towards distributed computing.

As defined by Oxford the definition of automation:

> the use of machines to do work that was previously done by people

What are the benefits of automation:

1.  Increase the number of changes that can be performed by an individual
2.  Reduce the probability of errors
3.  Rollback to a sane state
4.  Optimize the network on attributes besides bandwidth and delay

## Goals of Automation

### Operational Transparency and Global Reasoning

What drives your vendor selection process? Is it your confidence in your vendor to provide the features which will make your business more efficient or competitive? Is it the flexibility of the system or its performance? or is it your familiarity with the devices interface coupled with the fact you don’t want to be slowed down to learn something new or possibly a combination of these?

*Operational Transparency* is defined as the ability to control, operate and manage the behavior of your infrastructure regardless of the underlying implementation. In other words, I want to choose the best-of-breed implementations to satisfy my business problems while operating it in a consistent way. Not just consistent with that particular device model and version but across all devices and versions.

*Global Reasoning* is a bit of a different goal, it is more in-line with the SDN movement but not reliant on it. SDN as originally envisioned relies on the normalization of the device through a specific control protocol and processing model i.e. the match/action processing model. This turns out to be quite difficult to do in practice (for varying reasons) but that’s a conversation for another day. The main point to take away here is that complex distributed systems cannot be understood from the point of view of one single element, but the entire system as a whole needs to be reasoned about to be effective. This is where machine learning will play a large role to identify trends, classify information and leverage advanced solvers to examine the solution space and make predictions. We will talk about solutions in this space in another post.

## The problem nobody is talking about

There are lots of people talking about network automation and asking if network engineers should study languages like Python. While I absolutely see benefits in learning to code I feel there is a deeper problem that still isn’t being addressed in the industry.

There are a few frameworks that have emerged such as [Napalm-automation](https://github.com/napalm-automation) and [Ansible Networking](https://www.ansible.com/network-automation) catering to the goals of providing network operations with an automated way of configuring networks. These frameworks either entwine low-level device details into the code or rely on another set of libraries to bind control channels, manipulate the device configuration and inspect operational state. Who owns these low-level libraries and how often are they updated, patched, etc..?

Unfortunately this is the bane of the problem. We are constantly needing to care and feed these low-level interfaces in order to keep up with deployments, security updates and new features.

What we need is a consistent and extensible data model to represent network configuration and operational state. We will continue hobbling across this path of incrementalism until the open source communities establish enough of a foothold that we can transition from these proprietary implementations towards a generalized set of models that brings us to fruition.

> A good example of building towards a thoughtful architecture can be seen in the [Arista Cloud Vision Architecture](https://www.arista.com/en/products/eos/eos-cloudvision). Arista had been very careful about designing how operational and configuration state was represented within the device OS, they easily were able to aggregate this to build features based on *Global Reasoning*. In addition Cumulus Networks just released ints [NetQ](https://finance.yahoo.com/news/cumulus-networks-launches-netq-telemetry-130000866.html) web-scale soultion for data center operations that allows for *Global Reasoning* of the data center network as a whole.

#### A small detour on why automation frameworks are not enough.

Ok, so we have all these different vendor products, interfaces and data representations how do we build up economies of scale to help communities be successful?

##### Reuse, Reuse and Reuse

It’s a well known fact in software engineering that reusable code is a highly desirable attribute. For the main reason that as others become dependant on that piece of code, there is more of a desire to maintain, evolve and optimize the code that others have grown so dependant on. And if the community is not happy with the maintainers, given the appropriate open source licenses, they are free to fork it off and maintain their own version of the code.

##### Openness and EcoSystems

So how does one get reuse? Afterall it’s fairly easy to structure a piece of code into a library that can be consumed by others. In fact there are vast dependency networks in place such as PIP, NPM, Crates.io, Maven, etc.. that provide repositories of libraries that others can consume these libraries. Providing access to these libraries and making the consumable is critical for a successful ecosystem.

##### A library is not a Service

One thing that people should recognize is that a library typically is written in a specific programming language. In most cases it is difficult to share these libraries across different programming languages unless it was written in C and the language provides for a Foreign Function Interface (FFI). So in other words, libraries we see in general use today are locked within the programming environment they were created in.

> This is unfortunate because it minimizes the broad population of developers who might find these solutions beneficial but cannot cross the language divide.

## Enter the Service

Services are a critical concept to understand in the realm of reusable software. They are paramount in the evolving microservice architectural style and a key tenant to functional programming. Services can be written in a way that they can easily be consumed by applications written in other programming languages.

##### How do I talk with a service?

It turns out that the major bulk of services exposed today leverage web based standards such as HTTP and JSON. This is a fairly well understood architectural style commonly known as REST although most implementations do not leverage the full HATEOAS style developed by Roy Fielding.

There are other methods however for communicating between services using common protocols such as messaging API’s like: ZeroMQ, AMQP, GRPC, Thrift, ProtoBuf, MessagePack, NATS. This decouples clients and services in both space and time. Meaning the clients do not care where the location of the services are and they don’t have to hang on the phone and wait for a reply.

## Summary

So as we have seen automation does not stop at delivering configuration payloads to devices. We must model the management plane, control plane and data plane in order to normalize information to remove implementation specific details and build up our reasoning about operational behavior.
