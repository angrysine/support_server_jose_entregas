import re

def item_feedback(text=None):

    intent_dict = {
        r"(?:(prego|torneira|fazol|torata))": "item",
    }

    #add action dict later, outside function?

    for key, value in intent_dict.items():
        pattern = re.compile(key)
        groups = pattern.findall(text)

        if groups:
            return groups
        else:
            return f"não achei nenhum match de palavras"
            break
    print()
