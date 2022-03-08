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


def main():
    guesses = 0

    filtered_words = list({word.lower() for word in words.words() if len(word) == 5 and '-' not in word})

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

