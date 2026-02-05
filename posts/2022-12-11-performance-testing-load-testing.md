---
title: "Software Performance Troubleshooting And Optimization"
slug: "performance-testing-load-testing"
description: "A complete guide to load testing will enhance the quality of software and show the direction of system optimization during the entire development cycle."
author: "Taylor Zhang"
date: 2022-12-11
tags: ["microservices", "performance", "web-development", "quality-assurance", "performance-testing"]
published: true
---

Performance improvement and optimization are one of the MUST steps during the software development life cycle. For a system with a performance bottleneck, a general solving procedure includes assessing the current performance of the system, targeting the performance bottleneck of the system, and doing specific optimization to improve the performance.

Here we mainly focus on the systems with frontend client and backend services. You may find answers to the following questions in this article:

*   <mark>How to measure the performance of a system?</mark>
    
*   <mark>How to design a suite of tests to assess the performance of a system?</mark>
    

# How to design a complete performance test

The end goal of a performance test is not just to test a system but to provide metrics or data under some level of pressure to optimize the system to meet a specific throughput or speed.

## Resource Baseline and Metrics

As we all know, the hardware resources like CPU, RAM, and Bandwidth is one of the core factors to impact service performance. So it's better to clarify the maximum hardware resource that the service can use.

| Resource Type | Considerations |
| --- | --- |
| CPU | The total CPU a service can use. This often refers to the actual **number of cores** on the machine if the software is a traditional service that runs directly on the host computer or **CPU Request and Limits** that a container can use if the software belongs to a cloud-native system. You may also want to consider the type of CPU as well. |
| Memory | This defines the max of RAM a service can use. Different frameworks may have varieties of configurations to control the max of memory to use to avoid OOM. |
| Storage | The disk space and disk type are other considerations as many frameworks use disks to store temporary data or cold data to reduce RAM usage. The I/O speed if the disk is a local storage and network speed if the disk is a remote cloud storage can impact the performance a lot. |
| Network | Most online services depend on the network to talk to each other. Whether it's an internal network on the same data center or it's a public network that connects multiple edge devices, the network bandwidth and ethernet card are important considerations. |

Given the hardware resources, the outer environment is set. To answer 'How good a system performance is' we need to collect some key metrics to measure it. In general, here are the metrics that we care about the most:

| Metrics | Meaning |
| --- | --- |
| Throughput | The number of processed requests per second(TPS) |
| Response time | The average response time of all the requests |
| Error Rate | The percentage of error response of all requests |
| Success Rate | The percentage of all successful requests |
| Concurrency | The number of requests that can be handled at the same time |
| Resource Utilization | CPU, Memory Utilization |
| Network In/Out | The Network bandwidth and rate |

In addition to response time, more people only focus on the average, [but P90, P95, or P99](https://docs.vmware.com/en/VMware-Tanzu-Service-Mesh/services/slos-with-tsm/GUID-20F1B2A2-7789-44DE-B193-352F8C4BAE23.html) is a better way to describe the performance of the system.

## Test Plan and Scenario

Before we run tests, we need to first design a test plan to clarify what to test and how to test. There are several focuses the test plan needs to be designed for.

### Single Endpoint

The simplest pressure test can be done by constantly calling one single endpoint for a certain duration. <mark>By changing the concurrency, frequency, and duration, the metrics can tell the performance of the service.</mark>

Concurrency

For a single endpoint, high concurrency could result in some weird issues that rarely happened in the development environment. For REST APIs, **high concurrent queries** might be much slower than normal. And **high concurrent writes** may trigger dirty writes together with slow queries. Simulating high concurrent requests for both one **identical resource** and **different resources** should be considered and tested to reveal data isolation and logic issues.

Frequency

The higher the TPS and success rate are, the better the service performance is. When designing the test plan, the **max throughput** of service could be found by analyzing the curve of the metrics. But sometimes a test that is **beyond the max throughput**(TPS) needs to be run to figure out **the crush point**, like when an OOM would happen. Then a rate limiter or scaler trigger can be better configured.

Duration

In most cases, a pressure test that lasts for seconds or minutes can meet our goal. However, in the case of a memory leak, only a long-running test can expose it. This kind of test is also called the stability test. A stability test that lasts for days should be considered when you think your service has a memory leakage, especially for the services that consume heavy traffics 24/7, and are likely to fail to trigger GC or data clean logic.

### End-to-end test

<mark>Beyond a single endpoint, the whole process needs to be pressure tested to make sure the relied components, like the message queue, gateway, database, and configuration system meet the requirements.</mark> You may find a lot of timeout and inconsistent issues that are caused by performance bottlenecks in those components.

### User Scenario Test Suit

In the real world, the software system is usually used by a lot of users at the same time. And all these users are using different functionalities. Some functions are stateful that depend on the previous actions and the current status of the resource. <mark>We can simulate this complex scenario by combining our single endpoint functional tests.</mark>

For example, an e-commerce website has some key functionalities:

*   Register a new user
    
*   Show a list of shopping Items
    
*   Add item to shopping cart
    
*   Place an order
    
*   Pay the order through a bank account
    

As we can tell, these operations depend on each other. If we want to build a complete test plan for this website we might need to perform many operations of all kinds at the same time. To make a better test plan, some key points need to be paid attention to.

Composition of tests

As we discussed above, this test suit wants to combine all kinds of requests to simulate real-world pressure. So the ratio for different kinds of endpoint calls should be as close to the real world as possible. For example, the following describes a normal Friday night scenario:

| Functionality | Ratio |
| --- | --- |
| Register a new user | 2% |
| Show a list of shopping Items | 80% |
| Add item to shopping cart | 10% |
| Place an order | 4% |
| Pay the order through a bank account | 4% |

But a Black Friday night scenario might look like this:

| Functionality | Ratio |
| --- | --- |
| Register a new user | 1% |
| Show a list of shopping Items | 30% |
| Add item to shopping cart | 19% |
| Place an order | 25% |
| Pay the order through a bank account | 25% |

Our assumptions are natural: on a normal Friday night, people just perform their usual behavior: first, browse a lot of items, then place an order when they find their favorite. But on Black Friday night, people already pre-added their favorite items to the shopping cart. What they want to do is just place the order right after the annual sale starts.

<mark>So if we use the wrong scenario to test our system, the system might not satisfy our real requirement thus resulting in a business loss.</mark>

## More Details of Performance Test

There are more details in the performance test, here we just discuss a little more about the issues and thoughts we might face in the production.

### The Whole Service Chain VS A Portion of The Service Chain

Our end goal is to make sure the end-to-end process line is stable and smooth under certain pressure. However, the whole process chain is long and complex.

For example, the step "Pay the order through a bank account" usually includes a series of logic like freezing the order, freezing the item stock, reading bank data, requesting the bank system, processing the response from the bank, checking back to stock, sending item data to merchant for delivering.

In practice, <mark>we may want to break the whole line backward into chunks to test portion by portion to narrow down the bottleneck point.</mark> If the backend system is using microservice infrastructure, this strategy is more efficient to apply in production since bottlenecks may be distributed among the entire system and microservices may have performance issues of their own kind.

### Test Environment VS Production Environment

We often think it's better to use the test environment to do a test. But the performance test is an exception. By fixing the performance issue, we may need to tweak the configurations of every component in the system. Below we compared the pros and cons of using different environments to do the test:

| Environment | Pros | Cons |
| --- | --- | --- |
| Production | 1\. The metrics and results are real | 1\. Since users are using the production environment, the performance test may slow down the online service which could affect the online users' experience. |
|  | 2\. Fix and verify can be done only once | 2\. The data that is generated by requests are not real online data. Some strategies like dyeing can be used to mark the test data and clean up after the test process. |
|  | 3\. Alert and support systems are more accurate and complete which is easier to troubleshoot and fix the root cause | 3\. Since pressure test always comes with a huge amount of requests or data flow, the alert system and on-call system may ring the bell and can fire strange tickets while the test is in progress. Some online important alarms could be ignored. |
| Test | 1\. The environment is set up for test purposes so is isolated from online users. | 1\. The optimizations need to do twice to be applied to the production after being completed in the test environment. |

### Bottlenecks of Test Client

We talked a lot about the system that is the test target. But <mark>some bottlenecks are on the client side that is sending the tests.</mark>

Assume we want to verify a system that could handle the peak of 1 million TPS for 5 seconds. Of course, one single machine can not send 1 million requests a once. We need to design or find a pressure test system or infrastructure to reach this goal. The followings are some considerations when selecting the pressure test tools and machines:

*   The **network bandwidth** and **compute resources** always need to be calculated carefully according to the budget and the criteria.
    
*   The load test tool needs to have a feature to **control all the request senders** to start and stop sending the requests **at the same time**.
    
*   Usually, all the request senders are identical. But if a complex scenario needs to be tested, the test tool controller needs to have the power to **orchestrate senders in different groups**. For example, sender 1-20 run tests for endpoints 1 and 2, and sender 21-50 run tests for endpoints 3, 4, and 5.
    

Since the software systems are different, we need to design and plan them case by case with a consideration of business growth, implementation, and dev team.

# Summary

We discussed a lot of things to consider when designing and performing a complete pressure test. By running the test plan, a lot of issues can be uncovered. Some are resource bottlenecks, some are structural problems. If you want to continue this topic and explore how to fix these issues, please check out my next article [<mark>software-performance-optimization-toolbox</mark>](https://taylorzyx.hashnode.dev/software-performance-optimization-toolbox)<mark>.</mark>

Thanks for reading.