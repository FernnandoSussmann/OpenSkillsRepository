---
name: design-doc-creator
description: Creates design docs to implement a project based in product specification
---

Create Design Documents to implement functionality described in $ARGUMENTS file. The generated documents must be save in a folder called `design_docs` in the root of the project.


# What are design docs?

Design docs are lightweight planning documents written before implementing code to solicit feedback, derive alignment, and create documentation.

# Design Docs guideline
- Make sure all that is specified is present in at least one design doc created.
- Make sure all Design Doc generated has guardrails and security validations described in it.
- It doesn't have to have code written in it, but technical and business specification that is core to the functionality.

# Anatomy of a design doc

Design docs are informal documents and thus don’t follow a strict guideline for their content. Rule #1 is: Write them in whatever form makes the most sense for the particular project.

Having said that, a certain structure has established itself as really useful.

## Context and scope

This section gives the reader a very rough overview of the landscape in which the new system is being built and what is actually being built. This isn’t a requirements doc. Keep it succinct! The goal is that readers are brought up to speed but some previous knowledge can be assumed and detailed info can be linked to. This section should be entirely focused on objective background facts.

## Goals and non-goals

A short list of bullet points of what the goals of the system are, and, sometimes more importantly, what non-goals are. Note, that non-goals aren’t negated goals like “The system shouldn’t crash”, but rather things that could reasonably be goals, but are explicitly chosen not to be goals. A good example would be “ACID compliance”; when designing a database, you’d certainly want to know whether that is a goal or non-goal. And if it is a non-goal you might still select a solution that provides it, if it doesn’t introduce trade-offs that prevent achieving the goals.

## The actual design

This section should start with an overview and then go into details.

Visualization of how to draw an owl. First picture: two circles labelled "1. Draw some circles". Second picture: Picture of an own labelled "2. Draw the rest of the fucking owl"

The design doc is the place to write down the trade-offs you made in designing your software. Focus on those trade-offs to produce a useful document with long-term value. That is, given the context (facts), goals and non-goals (requirements), the design doc is the place to suggest solutions and show why a particular solution best satisfies those goals.

The point of writing a document over a more formal medium is to provide the flexibility to express the problem set at hand in an appropriate manner. Because of this, there is no explicit guidance for how to actually describe the design.

Having said that, a few best practices and repeating topics have emerged that make sense for a large percentage of design docs:

# APIs

If the system under design exposes an API, then sketching out that API is usually a good idea. In most cases, however, one should withstand the temptation to copy-paste formal interface or data definitions into the doc as these are often verbose, contain unnecessary detail and quickly get out of date. Instead focus on the parts that are relevant to the design and its trade-offs.

# Data storage

Systems that store data should likely discuss how and in what rough form this happens. Similar to the advice on APIs, and for the same reasons, copy-pasting complete schema definitions should be avoided. Instead focus on the parts that are relevant to the design and its trade-offs.

# Code and pseudo-code

Design docs should rarely contain code, or pseudo-code except in situations where novel algorithms are described. As appropriate, link to prototypes that show the implementability of the design.

# Degree of constraint

One of the primary factors that would influence the shape of a software design and hence the design doc, is the degree of constraint of the solution space.

On one end of the extreme is the “greenfield software project”, where all we know are the goals, and the solution can be whatever makes the most sense. Such a document may be wide-ranging, but it also needs to quickly define a set of rules that allow zooming in on a manageable set of solutions.

On the other end are systems where the possible solutions are very well defined, but it isn’t at all obvious how they could even be combined to achieve the goals. This may be a legacy system that is difficult to change and wasn’t designed to do what you want it to do or a library design that needs to operate within the constraints of the host programming language.

In this situation you may be able to enumerate all the things you can do relatively easily, but you need to creatively put those things together to achieve the goals. There may be multiple solutions, and none of them are really great, and hence such a document should focus on selecting the best way given all identified trade-offs.

# Security

Make sure to pinpoint every security concert the project must have. Also include security checks that must be made to guarantee that the feature will not expose some sensitive information.

# Task division
Create from 1 to 5 max Design Docs, try to balance the workload between them. Less than 5 is better. All DD documents must relate to an entire feature. For example a design doc shouldn't state the creation for all APIs and another all Frontend pages. A DD should include an endpoint, database changes and html/css/js files related to this feature (thinking in a web application).

Examples:
Data pipeline must include read source data, manipulate information, create ddl to target table, create documentation related to the created data and if scheduling is in the same repository must create it's scheduling and artefacts.

An web application of a pet shop that has a feature of scheduling an appointment must have in this design doc the endpoint related to this feature, the modifications to it's database, cache calls if needed and the updates to the scheduling page (or creation if doesn't exists).

# Other important points
- Never ask to create empty files or folder structure, leave it to be created only when needed.
- Always tells what test should be made to ensure this feature is correct.
- Never write code explicitly.
- Ask whenever in doubt.
- Create a guidance check-list/definition of done for each design doc.
- Add a TL;DR session in the beginning of the document summarizing what it says.
