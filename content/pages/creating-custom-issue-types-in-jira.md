---
title: Creating custom issue types for JIRA
date: '2018-08-19'
description: ''
---

## Introduction

Custom issue types are one of the most powerful features of Jira. Since issues can be queried and linked with other issues, confluence pages or anything else that can have an URL, you can use it for many different purposes, which usually require a seperate tool. Examples are impediments and requirements. Impediments will move to the Scrum Masters backlog,  requirements tend to link to user stories that try to satisfy that single requirement.

## Creating a custom issue type

![](/images/blog/2018/08/image-2.png)

To create a custom issue type for a project, you first need to get into the projects settings (click the bottom left corner of the prject page).

A part of the settings page shows the issue types already present in this project.

![](/images/blog/2018/08/image-3.png)

If you click on the Issue types menu item in the left menu, you get a more detailed overview on the types:

![](/images/blog/2018/08/image-4.png)

The Actions button in the top right corner is what you need. On the next screen, you can pull in issue types you already defined into the current project.

![](/images/blog/2018/08/image-5.png)

If the issue type is not yet defined, you can define one with help of the top right button "Add issue type".

![](/images/blog/2018/08/image-7.png)

![](/images/blog/2018/08/image-8.png)

When you defined your new issue type, reload the page to make it appear in the "Available issue types" column. Now you can move it over to "Issue Types for Current Scheme" column.

![](/images/blog/2018/08/image-9.png)

Now you should click on "Save". If you don't like the icon of the new issue type, you need to step over to the global "Issue" settings of Jira, search for your new type in the list and click "Edit".

![](/images/blog/2018/08/image-10.png)

You can now "select image" to change the icon and then select "Update" to save the changes.

![](/images/blog/2018/08/image-11.png)

After this and creating a new requirement, it is easy to use the filters to find requirements that are not addressed by some task/story/test/...

## Query requirements with JQL

![](/images/blog/2018/08/image-12.png)

If you want to only show requirements without links, you need some plugin. I suggest the [Script Runner Plugin](https://marketplace.atlassian.com/apps/6820/scriptrunner-for-jira) from Adaptavist. It provides a JQL function *hasLinks()* to filter the issues regarding their links.

## Issue Type Workflow

For some issue types, it is favorable to assign or create another workflow. e.g. requirements are never "Done". They start with a draft or documentation phase, most often require a review (management, customer, user,...) and get into a demand state. When the requirement has been satisfied once (e.g. through implementation in software), it is in some active state, where (hopefully automated) tests ensure, that the requirements keeps satisfied.

How to define a workflow is part of another tutorial.

## Further reading

- https://confluence.atlassian.com/adminjiracloud/adding-editing-and-deleting-an-issue-type-844500747.html