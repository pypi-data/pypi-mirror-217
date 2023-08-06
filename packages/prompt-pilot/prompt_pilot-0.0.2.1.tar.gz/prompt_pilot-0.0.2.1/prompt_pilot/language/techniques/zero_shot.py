def zero_shot(prompt, character, setting, plot):
























































































































    zero_shot_prompt = prompt + "\n\n" + "Chain:" + "\n"
    zero_shot_prompt += "Character: {}\n".format(character)
    zero_shot_prompt += "Setting: {}\n".format(setting)
    zero_shot_prompt += "Plot: {}\n".format(plot)
    
    return zero_shot_prompt

"""
In the case of the zero-shot prompt, using a "Chain" object wouldn't be technically accurate since there is only a single chain described. The purpose of the "Chain" label in the few-shot prompt is to indicate a series of prompts and answers that follow a specific character and setting. However, in the zero-shot prompt, there is no sequence or multiple chains involved.

Example execution:

prompt = "I want to write a story. Please help me come up with some ideas. Start with a character and a setting."
character = "A detective"
setting = "A small town"
plot = "The detective discovers a murder case that everyone else in town has ignored because of a long-standing feud between two families."

zero_shot_prompt = generate_zero_shot_prompt(prompt, character, setting, plot)

print(zero_shot_prompt)
"""

