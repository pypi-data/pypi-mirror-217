def few_shot(prompt, chains):
    
    few_shot_prompt = prompt + "\n\n"
    
    for chain in chains:
        few_shot_prompt += "Chain:" + "\n"
        few_shot_prompt += "Character: {}\n".format(chain["character"])
        few_shot_prompt += "Setting: {}\n".format(chain["setting"])
        few_shot_prompt += "Question: {}\n".format(chain["question"])
        few_shot_prompt += "Answer: {}\n".format(chain["answer"])
    
    return few_shot_prompt

"""
The chains object is a list that contains multiple chain objects. Each chain object represents a prompt chain with the character, setting, question, and answer.

Example execution

prompt = "I want to write a story. Please help me come up with some ideas. Start with a character and a setting."

chains = [
    {
        "character": "A detective",
        "setting": "A small town",
        "question": "What is the detective's first impression of the town?",
        "answer": "The detective is struck by how quiet and peaceful the town seems on the surface, despite the fact that there is clearly something sinister lurking beneath the surface."
    },
    {
        "character": "The town's mayor",
        "setting": "The mayor's office",
        "question": "What is the mayor's greatest fear?",
        "answer": "The mayor is terrified of being exposed as a fraud, and will stop at nothing to protect his reputation and maintain his grip on power."
    },
    {
        "character": "The owner of the local diner",
        "setting": "The diner",
        "question": "What is the owner's relationship with the town's residents like?",
        "answer": "The owner of the diner is well-liked by most of the residents, but has a strained relationship with one of the families involved in the long-standing feud that is tearing the town apart."
    }
]

few_shot_prompt = generate_few_shot_prompt(prompt, chains)

print(few_shot_prompt)
"""