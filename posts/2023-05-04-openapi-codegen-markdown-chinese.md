---
title: "基于 OpenAPI 自动生成接口文档和 API 逻辑代码"
slug: "openapi-codegen-markdown-chinese"
description: "Introducing an open-source project to demonstrate how to set up a workflow to use openapi with auto markdown generator and codegen in golang gin."
author: "Taylor Zhang"
date: 2023-05-04
tags: ["documentation", "apis", "developer", "automation", "devops"]
published: true
---

大家好，我是 靠谱的 Taylor。最近工作上在研究接口设计相关的规范和工具，小有所成，跟大家分享一下。

---

## 关于作者

张育鑫（Taylor Zhang）

腾讯高级工程师，认证高级云架构工程师，认证高级云开发工程师  
机器学习平台，MLOps，大数据，云原生，数据密集型分布式系统

Find Me: taylorzyx@hotmail.com

[LinkedIn](https://www.linkedin.com/in/yxzh/) | [Blog](https://taylorzyx.hashnode.dev/) | [Github](https://github.com/taylorzhangyx)

---

# TAKEAWAY

| 条目 | 内容 |
| --- | --- |
| 场景痛点 | 服务 API 的变更需要维护服务端代码，客户端代码和接口文档三份文档，同步，修改和调试耗费精力且容易出错。 |
| [解决方法](https://github.com/taylorzhangyx/openapi-codegen-go) | [通过 OpenAPI 规范定义 API 并使用自动化脚本和工具自动生成服务端，客户端代码和 API 文档 Markdown](https://github.com/taylorzhangyx/openapi-codegen-go) |
| 依赖工具 | OpenAPI，oapi-codegen，widdershins |

## 场景痛点

在服务开发的时候，服务的接口 API 设计决定着这个服务与其他服务的调用方式以及和网页之间的交互联动难易程度。被外部服务调用的时候，接口 API 的设计和字段含义是不可缺少的一部分。

服务端，客户端以及接口文档三方都需要明确对于 API 的定义及含义。而实际生产当中，随着需求不断丰富，开发当中的场景细节不断增多，API 会不断地修改，其对应的定义和字段含义也会不断变化。这时候要想基于服务端的逻辑变化来同步客户端以及接口文档的修改，需要额外的工作量。

<mark>如果能有对 API 统一的定义，自动根据 API 定义和描述生成代码、注释以及接口文档，则免去了维护的工作。</mark>

## 解决方法

<mark>基于 </mark> [<mark>OpenAPI</mark>](https://swagger.io/specification/) <mark>的规范来定义接口及用例，并通过 </mark> [<mark>oapi-codegen</mark>](https://github.com/deepmap/oapi-codegen) <mark>和 </mark> [<mark>widdershins</mark>](https://github.com/Mermade/widdershins) <mark>自动生成服务 API 层代码及对应 Markdown 文档。</mark>

### OpenAPI specification

OpenAPI 规范（原称为 Swagger 规范）是一种用于描述、设计和编写 RESTful API 的标准。通过它开发人员可以定义 API 的地址、请求参数、响应参数等信息，提高 API 的开发、测试和集成效率。OpenAPI 规范旨在提供一种可读性高、易于维护的方式来描述 API，以便更直观和便捷地描述 API 的功能，让开发者更方便地使用。

OpenAPI 规范的前身是 Swagger 规范，由 Tony Tam 在 2010 年创建。Swagger 规范从一开始就非常受欢迎，因为它提供了一种简单、易于理解的方式来描述 RESTful API，并且支持生成客户端和服务器端代码。

随着 Swagger 规范的发展，2015 年 SmartBear Software 收购了 Swagger 项目，并与 IBM、Microsoft、PayPal 等公司一起成立了 OpenAPI Initiative。这个组织的目标是维护和推广 OpenAPI 规范并推广其成为一种行业标准。

2016 年，Swagger 规范被更名为 OpenAPI 规范，以表示其在 OAI 组织下的地位。从此，OpenAPI 规范作为一个独立的项目继续发展。

OpenAPI主要版本包括 OpenAPI 2.0：基于原始的 Swagger 2.0 规范，2014 年发布。 OpenAPI 3.0：2017 年发布，这一版本带来了许多重要的改进，如更好的组件重用、新的响应类型和示例、新的安全方案等。 OpenAPI 3.1：2021 年初发布，这个版本与 JSON Schema 规范更紧密地集成，增加了对 Webhooks 的支持，以及诸如 if、then 和 else 等条件语句的支持。

OpenAPI 规范有助于提高 API 设计的质量和一致性，降低开发和维护 API 的成本。许多流行的 API 设计工具和框架（如 Swagger、Postman、Stoplight 等）都支持 OpenAPI 规范。

### oapi-codegen

[oapi-codegen](https://github.com/deepmap/oapi-codegen) 是一个用于从 OpenAPI 规范生成 Go 语言代码的开源工具。它可以根据 OpenAPI 规范自动生成 Go 语言的客户端、服务器端代码、类型定义和相关接口。

### widdershins

[widdershins](https://github.com/Mermade/widdershins) 可以将 OpenAPI、AsyncAPI 和 Semoasa 规范转换为各种可读文档格式，例如 Markdown、AsciiDoc 和 HTML。它允许开发人员将 API 规范文件（通常为 YAML 或 JSON 格式）转换为具有良好可读性和可维护性的文档，以便于开发者和最终用户了解 API 的功能和使用方法。它还可以通过修改文档模版自定义生成的文档格式和内容。

## 实操案例

### 开源代码

[<mark>openapi-codegen-go</mark>](https://github.com/taylorzhangyx/openapi-codegen-go) <mark>提供了可运行的例子</mark>，将 OpenAPI3.0，oapi-codegen 和 widdershins 有机地结合起来，通过简单的指令生成可以直接基于 [gin](https://github.com/gin-gonic/gin) 框架运行的代码，并生成 client 和接口文档。

[![](https://cdn.hashnode.com/res/hashnode/image/upload/v1683214378635/ebecc783-79f9-429c-94b7-4819733bea1a.png align="center")](https://github.com/taylorzhangyx/openapi-codegen-go)

### 自定义模版

通过简单修改模板，实现了中文文档的输出：[中文自定义模板](https://github.com/taylorzhangyx/openapi-codegen-go/commit/717d38b52fa500d5300a74f0afa21a885e645acf)

[![](https://cdn.hashnode.com/res/hashnode/image/upload/v1683212636345/7a6b028a-7fd6-4546-a8a2-e0d8fc816eda.png align="center")](https://github.com/taylorzhangyx/openapi-codegen-go/commit/717d38b52fa500d5300a74f0afa21a885e645acf)

### 开发环境调试插件

OpenAPI 的生态已经比较健全，在多个 IDE 上都有插件可以直接解析 API 的定义文件并生成相应的接口调试页面直接进行本地调试

|  | Editor | Viewer |
| --- | --- | --- |
| VS Code | [OpenAPI (Swagger) Editor](https://marketplace.visualstudio.com/items?itemName=42Crunch.vscode-openapi) | [vscode-openapi-viewer](https://marketplace.visualstudio.com/items?itemName=AndrewButson.vscode-openapi-viewer) |
| JetBrains | [OpenAPI (Swagger) Editor](https://plugins.jetbrains.com/plugin/14837-openapi-swagger-editor) | [OpenAPI Specifications](https://plugins.jetbrains.com/plugin/14394-openapi-specifications) |

如下图，可直接通过 IDE 中的插件来打开 OpenAPI 定义文件来直接对接口进行调试。

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1683212647935/01f0628a-b993-4f22-8ace-dd189ce8e603.png align="center")

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1683212655737/cff3806d-38f5-4a82-aab0-87d9323bbcb6.png align="center")

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1683212663041/b484123f-055c-4f03-99b1-4265507998bb.png align="center")

---

## 关于作者

张育鑫（Taylor Zhang）

腾讯高级工程师，认证高级云架构工程师，认证高级云开发工程师  
机器学习平台，MLOps，大数据，云原生，数据密集型分布式系统

Find Me: taylorzyx@hotmail.com

[LinkedIn](https://www.linkedin.com/in/yxzh/) | [Blog](https://taylorzyx.hashnode.dev/) | [Github](https://github.com/taylorzhangyx)