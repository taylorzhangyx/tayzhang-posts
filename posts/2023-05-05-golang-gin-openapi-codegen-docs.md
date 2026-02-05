---
title: "Auto Documentation Generation And Code-gen with Golang Gin Based on OpenAPI"
slug: "golang-gin-openapi-codegen-docs"
description: "Introducing an open-source project to demonstrate how to set up a workflow to use openapi with auto markdown generator and codegen in golang gin."
author: "Taylor Zhang"
date: 2023-05-05
tags: ["documentation", "apis", "developer", "automation", "devops"]
published: true
---

Greetings everyone, this is Taylor. Lately, I have been conducting research on API design standards and tools in my professional endeavors, achieving modest success. I would like to share my findings with you all.

---

## Author

Yuxin(Taylor) Zhang

Senior Software Engineer, Certified Professional Cloud Software Engineer, Professional Cloud Architect

ML Platform | MLOps | Big Data | Data Intensive Distributed System

Find Me: taylorzyx@hotmail.com

[LinkedIn](https://www.linkedin.com/in/yxzh/) | [Blog](https://taylorzyx.hashnode.dev/) | \[Github\](https://github.com/taylorzh

---

## TAKEAWAY

| Entry | Content |
| --- | --- |
| Pain Point | Maintaining server-side code, client-side code, and API documentation for service API changes is time-consuming, error-prone, and requires synchronization. |
| [Solution](https://github.com/taylorzhangyx/openapi-codegen-go) | [<mark>Utilize OpenAPI specifications to define APIs and employ automated scripts and tools to generate server-side, client-side code, and API documentation in Markdown format.</mark>](https://github.com/taylorzhangyx/openapi-codegen-go) |
| Tools | OpenAPI, oapi-codegen, widdershins |

## Pain Point

During service development, the design of a service's API determines the way it interacts with other services, as well as the ease of interactivity between the service and web pages. The design and field definitions of an API are indispensable when being called by external services.

Server-side, client-side, and API documentation all require clear definitions and meanings of APIs. In reality, as requirements become increasingly complex and development scenarios continue to expand, APIs undergo constant modifications, and their corresponding definitions and field meanings change accordingly. Synchronizing client-side and API documentation based on server-side logic changes necessitates additional effort.

<mark>A unified API definition that automatically generates code, comments, and API documentation based on the API definition and description would eliminate the need for maintenance.</mark>

## Solution

Leverage [OpenAPI](https://swagger.io/specification/) specifications to define interfaces and use cases, and generate service API layer code and corresponding Markdown documentation using [oapi-codegen](https://github.com/deepmap/oapi-codegen) and [widdershins](https://github.com/Mermade/widdershins).

### OpenAPI Specification

The OpenAPI Specification (formerly known as Swagger Specification) is a standard for describing, designing, and documenting RESTful APIs. Developers can define API endpoints, request parameters, and response parameters through it, enhancing the efficiency of API development, testing, and integration. <mark>The OpenAPI Specification aims to provide a highly readable and maintainable way to describe APIs, making it more intuitive and convenient for developers to understand and use the API.</mark>

The OpenAPI Specification was preceded by the Swagger Specification, created by Tony Tam in 2010. Swagger was popular from the beginning, as it provided a simple and comprehensible way to describe RESTful APIs, with support for generating client and server-side code.

As the Swagger Specification evolved, SmartBear Software acquired the Swagger project in 2015 and established the OpenAPI Initiative alongside IBM, Microsoft, and PayPal. The organization's goal is to maintain and promote the OpenAPI Specification and establish it as an industry standard.

In 2016, the Swagger Specification was renamed to the OpenAPI Specification to signify its status within the OAI organization. Since then, the OpenAPI Specification has continued to evolve as an independent project.

Key OpenAPI versions include:

**OpenAPI 2.0**: Released in 2014, based on the original Swagger 2.0 Specification.

**OpenAPI 3.0**: Released in 2017, this version introduced many significant improvements, such as enhanced component reuse, new response types and examples, and new security schemes.

**OpenAPI 3.1**: Released in early 2021, this version features closer integration with the JSON Schema Specification, adds support for Webhooks, and incorporates conditional statements such as if, then, and else.

The OpenAPI Specification helps improve the quality and consistency of API design while reducing the cost of developing and maintaining APIs. Many popular API design tools and frameworks (e.g., Swagger, Postman, Stoplight) support the OpenAPI Specification.

### oapi-codegen

[oapi-codegen](https://github.com/deepmap/oapi-codegen) is an open-source tool for generating Go code from OpenAPI specifications. It can automatically generate client-side, server-side code, type definitions, and related interfaces for Go based on the OpenAPI Specification.

### widdershins

[widdershins](https://github.com/Mermade/widdershins) converts OpenAPI, AsyncAPI, and Semoasa specifications into various human-readable documentation formats, such as Markdown, AsciiDoc, and HTML. Developers can convert API specification files (usually in YAML or JSON format) into readable and maintainable documentation to help both developers and end-users understand the API's functionality and usage. The generated documentation format and content can be customized by modifying document templates.

## Practical Example

### Open Source Code

[openapi-codegen-go](https://github.com/taylorzhangyx/openapi-codegen-go) provides a runnable example that combines OpenAPI 3.0, oapi-codegen, and widdershins. It generates code that can be directly run on the [gin](https://github.com/gin-gonic/gin) framework, as well as client-side code and API documentation, through simple commands.

[![](https://cdn.hashnode.com/res/hashnode/image/upload/v1683280664488/ff33d744-a547-4c3a-a83a-7993298287a2.png align="center")](https://github.com/taylorzhangyx/openapi-codegen-go)

### Custom Templates

By simply modifying the template, Chinese documentation output is achieved: [Custom Chinese Template](https://github.com/taylorzhangyx/openapi-codegen-go/commit/717d38b52fa500d5300a74f0afa21a885e645acf)

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1683280692137/4e118d07-23f0-4a58-a7f1-89e73cb1e565.png align="center")

### Development Environment Debugging Plugins

The OpenAPI ecosystem is robust, with plugins available for multiple IDEs that can directly parse API definition files and generate corresponding interface debugging pages for local debugging. These plugins streamline the API development process and make it more efficient by allowing developers to test and refine their APIs directly within their development environment.

|  | Editor | Viewer |
| --- | --- | --- |
| VS Code | [OpenAPI (Swagger) Editor](https://marketplace.visualstudio.com/items?itemName=42Crunch.vscode-openapi) | [vscode-openapi-viewer](https://marketplace.visualstudio.com/items?itemName=AndrewButson.vscode-openapi-viewer) |
| JetBrains | [OpenAPI (Swagger) Editor](https://plugins.jetbrains.com/plugin/14837-openapi-swagger-editor) | [OpenAPI Specifications](https://plugins.jetbrains.com/plugin/14394-openapi-specifications) |

As shown below, you can directly open the OpenAPI definition file within the IDE using a plugin and debug the API interfaces seamlessly. <mark>This integrated approach makes it easier for developers to test, modify, and refine their APIs without leaving their preferred development environment.</mark>

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1683280716541/7a7f98fd-fdec-4eb5-97a3-fb2c740450c6.png align="center")

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1683280727276/a804e85e-f84b-4ae8-b5ef-13e43655b445.png align="center")

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1683280734984/f38863ed-476b-4633-8503-145f399ac67f.png align="center")

---

## Author

Yuxin(Taylor) Zhang

Senior Software Engineer, Certified Professional Cloud Software Engineer, Professional Cloud Architect

ML Platform | MLOps | Big Data | Data Intensive Distributed System

Find Me: taylorzyx@hotmail.com

[LinkedIn](https://www.linkedin.com/in/yxzh/) | [Blog](https://taylorzyx.hashnode.dev/) | [Github](https://github.com/taylorzhangyx)