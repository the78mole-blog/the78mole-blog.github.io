---
title: Getting Started Embedded – Part II – The Embedded Project
date: '2018-08-17'
description: ''
categories:
- General
- Project Management
tags: []
---

Start embedded projects in an ordered way using the right tools

For many people, "project" is a mysterious word and everybody understands something different about it. Sales department has a totally different understanding than engineers. Engineers see it quite similar to software developers, but there are facets their opinion differs. Just take a minute to think about what a project means to you.

So, after you got your own opinion, let's first define, what a project means to me. At first it means nothing more than a vision, e.g. a customer's product idea, to talk about. And with every vision, everybody has an individual understanding of it in the beginning.

## The Information Collection Project

Welp, what is that? It has at first nothing to do with software, hardware or an embedded project. We start to collect information. Since we are living in the 21st century, we try to avoid using paper and put everything into "the cloud". One way to organize such information is putting everything into a MS Word document... OK, this was a joke :-)

I tend to use "the Atlassian tools" (Jira, Confluence, Bitbucket) for that purpose. Not that I receive any revenue for that, but I did not find anything that can compete with it at the moment... Most important in my opinion at this stage is Confluence. But to start a "Space" in Confluence, the more effective workflow is to start with a Jira project (again this word...).

If you create a Jira project, I suggest you use a template that contains user stories and bugs (e.g. Scrum or Kanban), and then add issue types ([Tutorial](https://blog.the78mole.de/tutorials/creating-custom-issue-types-in-jira/)) for requirements and impediments. Don't try to optimize the workflow for every issue type, during the project is the perfect time to do it.

Now create a new Confluence space (Software Project Space template) and link it to your just created Jira project. This space is the container for all relevant project information. Neither is Jira only suited for software projects, nor is Confluence (with this software template). In fact, you can drive anything with it efficiently. I love it to steer my renovation projects around my house with it. (Yes, I'm a nerd :-) !) This is not classical project management with a tight schedule, it is simply collecting issues, linking them and pick them according to their priority and dependencies.

For those old stagers around us and for those new to agile principles or just interested people, I would recommend to have a look into [Design Thinking](https://en.wikipedia.org/wiki/Design_Thinking). It gives you some ideas on how to collect the relevant information, define stakeholders,...

## The Vision

One of the most important things, before we can talk about "the project", we need to get a common understanding, what the inventor of that vision had in mind. If, and only if, the vision can be realized with **hard- and software**, we have an embedded project starting and many developers already have an idea, how it can be "solved" as a collection of electronic parts and code. But this is the "solve a problem" approach (engineers like that) to start a project, but very often not leading to customer's satisfaction. We will start differently...

To get a common understanding, it is necessary to talk about the system's requirements, making the vision more clear to all involved parties. At this point, it is the right time, to list possible stakeholders and the users of the potential product. Don't forget to create meeting notes and other pages about your findings in Confluence and put every requirement into your Jira project. In Confluence you can create a nice page with a Jira-Table-Macro collecting requirements and also grouping them with filters for different stakeholders. You can use tags for that purpose or, even better, create Jira Service Desk accounts for your stakeholders (saving the costly developer accounts). For sure that requires the Jira Service Desk add-on (the smalles 3-Agent-Version should serve very well even for projects).

During this time of user and stakeholder analysis, the vision becomes more clear and a common understanding settles. Still it is not the time to carve the solution in stone, like many engineers/developers tend to (again, this is what they love). The vision will still evolve during "the project" and also system requirements will do. Now it's time for personas and use cases, to get an even better common understanding.

## Use Cases

When we talk about use cases, we often only talk about users or customers of the end product. But you should never forget the other stakeholders. Even the development team can be a stakeholder, because they (in an agile environment) should be the responsible for quality and they for sure have specific requrements regarding QA (Quality Assurance, e.g. testing). BTW: Don't forget a UART port in your hardware requirements if you go with headless embedded system. Otherwise the developers will kill you instantly when they move from eval board to prototype hardware.

If you have some uses cases collected, hopefully a few for every stakeholder, it's time to move on. Don't try to finalize the list, you will fail! It is much better to keep in mind, that the list will still evolve and steer your project to be agile. Try to prioritize them together with all stakehoders. Invite some avatars, if stakeholders can not be included (e.g. real end customers). Here personas come get handy.

## The Project's Disciplines

The list of requirement typed issues in Jira should be already extend across some pages and you identified the ones with most impact on your system design. Now the paths will split, depending on the resulting product. If it has some GUI, like many HMI projects tend to have nowadays, you should get some experienced Design Thinking engineer that possibly starts with paper prototypes or even more wired stuff. But this is not the focus of this post...

We know should define a few components. At first HW, SW and possible ME (Mechanical Engineering) will serve well. We can put more granularity in later on. Now try to assign your requirements to these components. If you did this, let the engineers of these disciplines have a look on every requirement that belongs to their component and let them comment on their understanding. Pull in the stakeholders (or their avatars) again to dicuss the requirements, should something be unclear.

## Thougts about the Software Project

Now it is time to start the software project, isn't it? Well, if you can tell, what a software project is! No, I don't talk about the "Create project..."-button of your IDE. First we need to step back quite some distance to get a better overview on it.

We already defined some requirements above and assigned them components. The ones tagged with the SW-Component are the base for our user stories. Maybe we already defined some of them when we talked with the stakeholders, but now it's time to check, if we have important requirements left, that have not been addresses by a story. But collecting these stories is another topic, we will not address in this post...

So, why I'm talking about that...? Because there should be some requirements and stories hanging around, that could conflict with the tools (and IDEs) we tend to use. If you are using e.g. Keil µVision and your have the requirement to do intensive testing (e.g. because there is some SIL-level required), then you should definitely rethink your decision using this IDE. Or if a customer requires a close feedback loop and high delivery rates (daily in extreme situations), then you need some continuous integration pipeline, which is hard to establich using GUI-driven IDEs.

Let me give an example. You have a project with many parties involved (maybe different companies in extreme). Think of a smart home system. Different companies design the sensor nodes, another the central (headless) unit, you design the HMI-unit and another company designs the GUI using a propritary tool for GUI design, sending you some pieces of API code and some static libraries to be linked in. You get a delivery every week and need to integrate it. The customer wants to test the new functionality of the GUI's HMI (e.g. this week switch on light) as soon as possible. Many of the new functionalities and bug fixes from the GUI do not need your intervention, because they do not affect the API between embedded system and GUI. But not having an automated CI pipeline requires you to integrate the new GUI in your IDE and test it with every week's delivery MANUALLY! **I would hate your job from the bottom of my heart!**

But you are an engineer and you love to solve problems immediately. Don't make a project out of it, just raise an impediment (use this issue type in Jira) and find people to help solving it (Scrum-Master for communications and mental support, your boss for budget, IT employee for Jenkins,...).

The essence of this example is: If there are large parts of the development that could be automated using other tools (ot toolchains), start today changing your tools. Engineering should not consist of repetitive tasks, it should challenge your creativity with new tasks every week, every day,... every second. Switch over to CI and TDD, there is nothing giving you more satisfaction in your daily job as a software engineer. When mentioning TDD, already a few years old, but still very valueable is James W. Grenning's book [Test-Driven Development for Embedded C](https://pragprog.com/book/jgade/test-driven-development-for-embedded-c).

So before you start, choose the right toolchain. I highly recommend using GCC together with Eclipse and/or Makefiles. Why? Because it is platform independend, can be automated (even headless) and does not require a license. The licensing problem is not about the price, it is about the problem that you need one with anything or anybody involved in the development process. Even your Jenkins host needs a license, when you use commercial tools. And requiring a license makes it nearly impossible to spin up a fresh docker container for running a build. So, don't shut the door on amazing technologies you don't know yet but could make your life easier, like the wheel did six thousand years ago.

## What's next...?

In this post, I talked about starting an embedded project. Next post will be about starting the (non-GUI) embedded software of it.
