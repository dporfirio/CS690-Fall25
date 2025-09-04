# Downloading and running a (very) small LLM

I recommend ollama. Here are the steps.

## Download

ollama should be cross-platform. 

1. Download it from [here](https://ollama.com).
2. Run the installation.
3. When it's done, it might pop up a GUI. You can close this.

## Install a model

Let's try llama 3.2 1B. I think most modern machines should be able to run this.

1. Fire up a command line terminal.
2. Run `ollama run llama3.2:1b`. The terminal should show installation progress.

## Try it out

Llama 3.2 1B (pretrained) is pretty weak, but it does well for being so lightweight. I put in the following prompt and it spit out the ensuing text.

### Prompt

```
You are a robot that can perform the following actions: moveTo, grab, and put. The objects in the environment are: cup, table, and countertop. The cup is on the table, the table is in the living room, and the countertop is in the kitchen. You are in the living room. Your goal is: object_at(cup, countertop). Create a list of steps to achieve this goal.
```

### Response that I got

```
1. moveTo(table)
2. grab(cup)
3. put(cup) at countertop
```

Not bad! Kind of. The formatting is a little off (``put(cup) at countertop'' is a weird way to format a command). You can imagine that with some prompt engineering, it might be better.