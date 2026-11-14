---
title: "The Collapse of Open Source"
slug: "the-collapse-of-open-source"
description: "I still read open source every day. I've mostly stopped installing it. What a rewrite into your own codebase buys you, where it stops working, and what that does to open source and to the profession."
cover_motif: "graph"
cover_accent: "amber"
date: 2026-11-14
categories: ["ai", "security"]
tags: ["open-source", "supply-chain", "agents", "rust", "software-engineering", "hexa"]
---

*I still read open source every day. I've mostly stopped installing it.*

### How I build now

When I build something now, I go looking for how other people solved the problem. I read their code. Then I close the tab and have a model write the part I need into my own codebase.

No package. No dependency tree underneath it.

I should say where I stand before going on. I publish open source myself. [hexa](https://gaberger.github.io/hexa/) is MIT-licensed and alpha, one of a lot of tools trying to [tame the genie](/2026/10/inside-the-ai-harness/#taming-the-genie). I'm not arguing against publishing. I'm describing a change in how I consume.

This piece is about why I think a lot of us end up here, what it buys you, and where it stops working.

### Why we installed things

We took dependencies because writing code was expensive. Nobody could afford their own database or TLS stack, so we shared one.

Erik Meijer, the computer scientist behind LINQ and Reactive Extensions, said it bluntly in a talk at AI DevCon in New York: we did open source because code was expensive to develop, and it isn't anymore.\[1\] He calls what comes next the AI chop shop. Before the industrial revolution things were custom and expensive. Mass production made them cheap and generic. AI makes them custom and cheap.

His database example stuck with me. A typical company runs a handful of tables and a handful of queries. It doesn't need a general-purpose SQL parser and optimizer. A model can generate an application for those tables and those queries and throw most of the engine away. His line: "the safest code is the code that you never run."

He gives it a formal footing in partial evaluation. Take a program, fix the input that never changes, and specialize the program to it. Your framework is the input that never changes.

Is the cost really gone? Mostly. Anthropic released Claude Fable 5.2 on November 9. On a benchmark that asks whether open source maintainers would merge a model's changes, it scores 49.1 percent, up from 32.4 for the version before.\[2\] That's the best any released model has done, and it means half the changes wouldn't get in.

So the code is cheap. It isn't finished. Hold that thought.

### The surface area is mine

In 2022 a contributor calling himself Jia Tan started sending patches to xz Utils, a compression library with one overstretched maintainer. Two years later he had release rights, and versions 5.6.0 and 5.6.1 shipped with a backdoor aimed at SSH.\[3\]\[4\] It scored a 10, the maximum. Andres Freund, a Postgres developer, found it by accident while chasing a performance problem.

Almost nobody running those systems chose xz. It came along underneath something else.

That's the risk a rewrite removes. If the code is in my repository because I asked for it, there's no maintainer to compromise and no package to poison. Every line has a reason to be there, and I can read all of them.

### I get to pick the language

A rewrite isn't a copy. I get to choose what it's written in.

Write it in Rust and I inherit a class of protections the original may never have had. The industry rule of thumb is that about 70 percent of serious vulnerabilities in large C and C++ codebases are memory safety bugs. Google reports that in Android the share fell from 76 percent in 2019 to under 20 percent in 2025 as new code moved to Rust.\[5\]\[6\]

Here's the detail that matters. Google got there by writing new code in Rust, not by rewriting the old code, because rewriting was too expensive. That's the sum that changed. Anthropic says a team of agents moved one of its own production services from Python to Rust.\[2\]

The compiler is a verifier I get for free. It isn't the whole job. Rust doesn't know my authorization logic is wrong, and if I pull in forty crates I've rebuilt the problem I was leaving.

### The attacker loses the map

A public library is a public target. One flaw, found once, works against everyone who installed it.

And models now read open source at scale. In May, Anthropic reported that its Mythos Preview model had scanned more than 1,000 open source projects and flagged an estimated 23,019 vulnerabilities. Independent firms had triaged 1,752 of the serious ones and confirmed 1,587 as real.\[7\] PostgreSQL 19 is late this year because LLMs are turning up old bugs faster than the committers can fix them.\[8\]

Today that capability is pointed at defense. I don't assume it stays there.

Code I never published has to be attacked the hard way, without the source, one target at a time.

### Where it stops

That's a higher cost for the attacker. It isn't a shield, and I'd be kidding myself to call it one.

An attacker can probe a running system without the source. He can fuzz it or pull apart a binary, and models make all of that cheaper too.

Code nobody else has read is code nobody else has checked. When a model finds a bug in upstream wolfSSL, everyone running upstream gets the fix. My carved copy is mine alone.

There's a worry I can't put a number on. If everyone's model writes the same idea the same way, the flaws line up again, and we've rebuilt the monoculture one layer down.

And some things I won't rewrite. Cryptography. Kernels. Compilers. Their value is that everyone runs the same artifact and everyone audits it. Kate Holterhoff of RedMonk found the same instinct when she surveyed project AI policies: the further down the stack you go, the stricter they get.\[9\]

Leaves, yes. Trunk, no.

### So you prove it

Go back to that 49.1 percent. If half of a model's changes wouldn't pass a maintainer, then the rewrite only pays off when I check what came back.

That's the work of taming the genie. Tests I've watched fail. Boundaries a machine enforces. A second model reviewing the first.

Glasswing's own lesson points the same way. Finding vulnerabilities stopped being the bottleneck. Confirming and patching them became the bottleneck, at about two weeks per serious bug.\[7\] Generation scaled. Assurance didn't.

Meijer's answer is formal methods, and there's a sign he's right. A tester quoted in the Fable 5.2 launch describes the model building a hypervisor whose isolation core carries more than 3,500 machine-checked proofs.\[2\] A proof is the part you can trust without reading the code.

### What happens to open source

It doesn't die. It changes jobs. It stops being a supply chain and becomes a library of ideas.

The contribution side is already going. In a Linux Foundation survey, maintainers estimated a quarter of incoming pull requests are low-quality slop.\[10\] Projects are cancelling bug bounties and closing their queues to outsiders.\[9\] Scott Shambaugh, a matplotlib contributor, said why: if an agent can turn an issue into a pull request in thirty seconds, the maintainers could run the agent themselves.

The patch was the gift. The patch is now free.

Meijer goes further and argues that code a model writes can't be protected at all. The base rule is right. Copyright needs a human author, and in March the Supreme Court let that stand.\[11\] But AI-assisted work where a person did enough of the shaping still registers, and nobody has drawn the line. I'm not a lawyer and neither is he. Licenses don't evaporate. They get harder to enforce against code that's been read once and written fresh.

### What's left for us

If the model writes the code, the job is deciding what to build, proving it's right, and signing for it. A model can't be paged at 3 a.m.

One thing I don't have an answer to. Open source was the apprenticeship. It's where people learned by having bad code turned down by someone who cared, and that door is closing.

I still read open source every day. I think the reading is the part that lasts.

------------------------------------------------------------------------

> Gary Berger is Global Field CTO at Forward and the author of hexa, which is open source under the MIT license and, at the time of writing, alpha software.

### References

1.  Erik Meijer, [The AI Chop Shop: Everything You Ship Will Be Stolen](https://vimeo.com/1244199152/dddc1376d2), AI DevCon New York, 2026
2.  Anthropic, [Claude Fable 5.2 and Mythos 5.2](https://www.anthropic.com/claude-fable-and-mythos-5-2), November 9, 2026. Benchmark figures and customer quotes are the vendor's own
3.  Lasse Collin, [XZ Utils backdoor](https://tukaani.org/xz-backdoor/), the original maintainer's account
4.  Checkmarx, [Backdoor discovered in xz](https://checkmarx.com/blog/backdoor-discovered-in-xz-the-most-advanced-supply-chain-attack-known-to-date/), 2024. Timeline of the Jia Tan account
5.  Jeff Vander Stoep, [Rust in Android: move fast and fix things](https://blog.google/security/rust-in-android-move-fast-fix-things/), Google, November 13, 2025
6.  Thomas Claburn, [Google's Rust belts bugs out of Android](https://www.theregister.com/2024/09/25/google_rust_safe_code_android), The Register, September 25, 2024. Source for the 76 percent and 70 percent figures
7.  Anthropic, [Project Glasswing: An initial update](https://www.anthropic.com/research/glasswing-initial-update), May 22, 2026
8.  Hardware Busters, [PostgreSQL 19 Slips to November 19 as AI-Found Bugs Swamp Its Human Reviewers](https://hwbusters.com/news/postgresql-19-slips-to-november-19-as-ai-found-bugs-swamp-its-human-reviewers/), reporting on Robert Haas's post "Postgres 19 is late, and it's AI's fault"
9.  Bill Doerrfeld, [96% of codebases rely on open source, and AI slop is putting them at risk](https://thenewstack.io/ai-slop-open-source/), The New Stack, March 29, 2026
10. Linux Foundation Research, [press release on its generative AI and open source survey](https://www.linuxfoundation.org/press/new-lf-research-survey-shows-generative-ai-cuts-open-source-coding-time-in-half-but-25-of-incoming-pull-requests-are-considered-ai-slop), October 20, 2026
11. Mayer Brown, [Supreme Court Denies Review in AI Authorship Case](https://www.jdsupra.com/legalnews/supreme-court-denies-review-in-ai-2865518/), March 2026. Covers Thaler v. Perlmutter
