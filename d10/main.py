def compute_score_incomplete_line(opened_chunks):
    score = 0
    while len(opened_chunks) > 0:
        score *= 5
        char = opened_chunks.pop()
        if char == '(':
            score += 1
        if char == '[':
            score += 2
        if char == '{':
            score += 3
        if char == '<':
            score += 4
    return score


if __name__ == "__main__":
    with open('input', 'r') as fd:
        lines = [line.strip() for line in fd.readlines()]
        illegal_char_to_score = {')': 3, ']': 57, '}': 1197, '>': 25137}
        illegal_character_scores = []
        scores_incomplete_lines = []
        for line in lines:
            is_corrupted_line = False
            opened_chunks = []
            for char in line:
                if char in "({[<":
                    opened_chunks.append(char)
                else:
                    if (char == ')' and opened_chunks.pop() != '('
                            or char == '}' and opened_chunks.pop() != '{'
                            or char == ']' and opened_chunks.pop() != '['
                            or char == '>' and opened_chunks.pop() != '<'):
                        illegal_character_scores.append(illegal_char_to_score[char])
                        is_corrupted_line = True
                        break
            if not is_corrupted_line:
                scores_incomplete_lines.append(compute_score_incomplete_line(opened_chunks))

        print("Syntax error score is:", sum(illegal_character_scores))
        print("Incomplete lines middle score is:", sorted(scores_incomplete_lines)[len(scores_incomplete_lines)//2])
