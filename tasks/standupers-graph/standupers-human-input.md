I like Polish standup, but it seems I have a unique taste - everybody likes Abelard Giza or Lotek, but for me they are boring. The standupers I ~~like~~ love are scattered along the first 40 positions on standupedia.pl.
Since I have tokens to burn, I want a relations graph of the first 100 standupers from the standupedia.pl ranking. It should show each standuper in closer relation to others based on their fans' preferences (similar to how music platforms make suggestions: "you like band A, other people who like band A also tend to like bands B and C").

## main agent task

Main agent is responsible for researching the best way to do this. The main work should be handled by a swarm of low-tier subagents, probably one or two agents per standuper, that will somehow establish relations between them based on fan opinions.

Since this may be a huge task, it should be handled in batches (10 standupers each), and a new batch is fired on my command. Main agent should:
- grab the list of standupers and save it
- prepare the framework: what the subagents' prompt will be, what tier should be used, and how state should be preserved
- after each batch, create an updated graph using available tools (let's try the excalidraw MCP; if not feasible, switch to other tools proposed by the agent) and save it in this project
- ??? I don't know what more, this is just for funsies XD

## files

This file is untouchable for agents working on this project (the only allowed action is fixing the writing on my explicit request), but I strongly encourage the main agent to create a framework that enforces storing state as a set of context files, notes, message boards, etc. I may be using a few different conversations and providers for this, so everything should be stored somehow. Dear main agent, apart from this file, this is your playground. Organize it however you want, I just want to have my graph ;)