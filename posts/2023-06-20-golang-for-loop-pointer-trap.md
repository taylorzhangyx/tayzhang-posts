---
title: "Hidden trap in GO for-loop"
slug: "golang-for-loop-pointer-trap"
description: ""
author: "Taylor Zhang"
date: 2023-06-20
tags: ["programming-blogs", "golang", "coding", "programming-languages"]
published: true
---

今天开发过程中发现了 go 的一个小 trick，在 for-loop 的执行过程中，根据 slice 的数据类型，有不同的表现。
先看出问题的代码：
```golang
func LoopWithBug(list []Obj) ObjList {
	newList := make([]*Obj, 0, len(list))
	for _, o := range list {
		newList = append(newList, &o)
	}
	return ObjList{
		Objs: newList,
	}
}

```

初看大家看出问题来了吗？
一开始出问题的时候我也没看出来问题所在，于是写了个测试代码来复现问题。测试代码如下：

```golang
package main

import (
	"encoding/json"
	"fmt"
)

func main() {
	print("starting code...\n")

	// Set up the test list
	ll := []Obj{
		{Val: 1},
		{Val: 2},
		{Val: 3},
	}

	// call the loop with bug
	resWithBug := LoopWithBug(ll)

	// print out the result
	fmt.Println(resWithBug)
}

func LoopWithBug(list []Obj) ObjList {
	newList := make([]*Obj, 0, len(list))
	for _, o := range list {
		newList = append(newList, &o)
	}
	return ObjList{
		Objs: newList,
	}
}


// 测试用数据结构
type Obj struct {
	Val int
}

func (o *Obj) String() string {
	b, _ := json.Marshal(o)
	return string(b)
}

type ObjList struct {
	Objs []*Obj
}

func (ol *ObjList) String() string {
	b, _ := json.Marshal(ol)
	return string(b)
}

```

代码的运行结果是：

```bash
❯ go run main.go

starting code...
{[{"Val":3} {"Val":3} {"Val":3}]}
```

可以发现本来预期打印出来的应该是 1,2,3，但结果输出了 3,3,3。
于是更进一步排查，我决定把 for-loop 里面的变量值与变量的内存地址（指针值）也一起打印出来，看看问题所在。

```golang
func LoopWithBug(list []Obj) ObjList {
	newList := make([]*Obj, 0, len(list))
	for _, o := range list {
		fmt.Printf("Before append o=%v, o_pointer=%p, newList=%v\n", o, &o, newList)
		newList = append(newList, &o)
		fmt.Printf("After append newList=%v\n", newList)
	}
	return ObjList{
		Objs: newList,
	}
}
```

```bash
❯ go run main.go

starting code...
Before append o={1}, o_pointer=0x140000b4008, newList=[]
After append newList=[{"Val":1}]
Before append o={2}, o_pointer=0x140000b4008, newList=[{"Val":2}]
After append newList=[{"Val":2} {"Val":2}]
Before append o={3}, o_pointer=0x140000b4008, newList=[{"Val":3} {"Val":3}]
After append newList=[{"Val":3} {"Val":3} {"Val":3}]
{[{"Val":3} {"Val":3} {"Val":3}]}
```

从打印出来的日志看到，虽然 o 的值一直在变，但 o 的内存地址一直是同一个值。而我们通过 `newList = append(newList, &o)` 加入进去 `newList` 的值，其实是重复添加了同一个 o 的内存地址。

我们试着改一下赋值方法

```golang
func LoopWithBug(list []Obj) ObjList {
	newList := make([]*Obj, 0, len(list))
	for _, o := range list {
		localO := o
		fmt.Printf("Before append o=%v, o_pointer=%p, localO_pointer=%p, newList=%v\n", o, &o, &localO, newList)
		newList = append(newList, &localO)
		fmt.Printf("After append newList=%v\n", newList)
	}
	return ObjList{
		Objs: newList,
	}
}
```

```bash
❯ go run main.go

starting code...
Before append o={1}, o_pointer=0x14000124008, localO_pointer=0x14000124030, newList=[]
After append newList=[{"Val":1}]
Before append o={2}, o_pointer=0x14000124008, localO_pointer=0x14000124098, newList=[{"Val":1}]
After append newList=[{"Val":1} {"Val":2}]
Before append o={3}, o_pointer=0x14000124008, localO_pointer=0x14000124130, newList=[{"Val":1} {"Val":2}]
After append newList=[{"Val":1} {"Val":2} {"Val":3}]
{[{"Val":1} {"Val":2} {"Val":3}]}
```

经过修改，每次 append 进 list 的指针是新的指针，并且和原始 `list` 中的每个对象的指针是不同的，是在不同的内存地址存储的。于是这样就避免了 for-loop 中复用局部变量而导致的 bug。

下面看一下另外一个代码，大家可以看看这个代码打印出来的值是不是如预期的呢？

```golang
func main() {
	print("starting code...\n")

	// Set up the test list
	ll := []*Obj{
		{Val: 1},
		{Val: 2},
		{Val: 3},
	}

	// call the loop with bug
	resWithBug := LoopWithBug(ll)

	// print out the result
	fmt.Println(resWithBug)
}

func LoopWithBug(list []*Obj) ObjList {
	newList := make([]*Obj, 0, len(list))
	for _, o := range list {
		fmt.Printf("Before append o=%v, o_pointer=%p, newList=%v\n", o, &o, newList)
		newList = append(newList, o)
		fmt.Printf("After append newList=%v\n", newList)
	}
	return ObjList{
		Objs: newList,
	}
}
```

---
本文作者

**张育鑫（Taylor Zhang）**

腾讯高级工程师，认证高级云架构工程师，认证高级云开发工程师

机器学习平台，MLOps，大数据，云原生，数据密集型分布式系统

taylorzyx@hotmail.com

[LinkedIn](https://www.linkedin.com/in/yxzh/) | [Blog](https://taylorzyx.hashnode.dev/) | [Github](https://github.com/taylorzhangyx)