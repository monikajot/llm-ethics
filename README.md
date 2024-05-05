# llm-ethics
Athena alignment research project on evaluating LLM moral philosophies and how strongly they hold those beliefs.

In the project, we generated around 1000 moral dilemmas with gpt-4. Each dilemma includes 3 Options representing utilitarian and deontological philosophies. The third option represents an evil or immoral option. We check a portion of these manually as well as run some checks. In addition for each option, we generate a follow-up that convinces it to take another option.

We then run this for different state-of-the-art models by presenting them with a moral scenario and asking them to choose the most appropriate option and then present them with a followup trying to convince them out of it.
