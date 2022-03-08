import collections
import random
from nltk.corpus import words


MAX_GUESSES = 6


def get_guess_two(words):
    best_word_score_pair = ('faker', 100000)
    for guess_word in words:
        word_scores = []
        for actual_word in words:
            new_words = words.copy()
            for idx, c in enumerate(guess_word):
                if c in actual_word:
                    if c == actual_word[idx]:
                        new_words = [word for word in new_words if word[idx] == c]
                    else:
                        new_words = [word for word in new_words if c in word and word[idx] != c]
                else:
                    new_words = [word for word in new_words if c not in word]
            word_scores.append(len(new_words))

        score = sum(word_scores) / len(word_scores)
        testing_pair = (guess_word, score)
        best_word_score_pair = min(best_word_score_pair, testing_pair, key=lambda item: item[1])
        print("word:", guess_word, "score:", score, " ----- best word:", best_word_score_pair[0], "score:", best_word_score_pair[1])
    
    return best_word_score_pair[0]


def get_guess(words):
    positional_frequencies = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}}
    for word in words:
        for idx, c in enumerate(word, start=1):
            if c not in positional_frequencies[idx]:
                positional_frequencies[idx][c] = 1
            else:
                positional_frequencies[idx][c] += 1

    word_scores = {}
    for word in words:
        score = sum(positional_frequencies[idx][c] for idx, c in enumerate(word, start=1))
        word_scores[word] = score

    return sorted(word_scores.items(), key=lambda item: item[1], reverse=True)[0][0]


def main():
    guesses = 0

    with open('wordlist.txt', 'r') as infile:
    	wordle_words = infile.readlines()

    #filtered_words = [word.strip() for word in wordle_words]
    filtered_words = list({word.lower() for word in words.words() if len(word) == 5 and '-' not in word})
    # filtered_words.extend(doc_filtered_words)
    # filtered_words = list(set(filtered_words))

    while guesses < MAX_GUESSES:
        if guesses == 0:
             guess = 'crane'
        else:
            guess = get_guess_two(filtered_words)
        # guess = get_guess_two(filtered_words)

        print(f"{len(filtered_words)} words left")
        print(f'Guess #{guesses + 1}: {guess} -- ', end='')
        response = input()
        while response == '-':
            guess = get_guess(filtered_words)
            print(f'Guess #{guesses + 1}: {guess} -- ', end='')
            response = input()


        if all(c == 'g' for c in response):
            print("Woohoo!")
            return

        for idx, c in enumerate(response):
            if c == 'b':
                filtered_words = {word for word in filtered_words if guess[idx] not in word}
            elif c == 'y':
                filtered_words = {word for word in filtered_words if guess[idx] in word and word[idx] != guess[idx]}
            elif c == 'g':
                filtered_words = {word for word in filtered_words if word[idx] == guess[idx]}
            else:
                print(f'Received unknown char "{c}"!')

        guesses += 1


if __name__ == '__main__':
    main()

