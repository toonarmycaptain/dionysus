# score entry:

def score_entry(min=0, max=100):


    while True:
        score = input("Enter student score: ")

        if score == '_':
            return None # do not include student in graph eg if absent

        try:
            score_float = float(score)
        except ValueError:
            print("InputError: please enter a number or '_' to exclude student.")
            continue
        # else:
        if score_float < min or score_float > max:
            print(f'InputError: Please enter a number between {min} and {max}.')
            continue
        return score_float


def test_score_entry():
    test_dict = {'_': None,
                 0: 0,
                 1: 1,
                 5: 5,
                 99: 99,
                 100: 100,
                 101: 'how to test loop?',
                 'i am bad data': 'how to test loop?',
                }

    for i in test_dict:
        pass



print(score_entry())



