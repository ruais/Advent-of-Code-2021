# advent of code day 7 by Ruma (Lynn)

with open(r'.\input\day08.txt') as file:
    data = file.read()

testdata = '''
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
'''

def parse_data(data):
    data = data.split('\n')
    parsed = []
    for line in data:
        if line:
            line = line.split(' ')
            delim = line.index('|')
            patterns = tuple(line[:delim])
            numbers = tuple(line[delim+1:])
            parsed.append((patterns, numbers))
    return tuple(parsed)

def findnums(data):
    ebf = {4: 'e', 6: 'b', 9: 'f'}
    digits = [ 'abcefg',      'cf',   'acdeg',   'acdfg',    'bcdf',
                'abdfg',  'abdefg',     'acf', 'abcdefg',  'abcdfg']
    numsout = []
    for patterns, numbers in data:
        key = [0, 0, 0, 0, 0, 0, 0]
        dic = {}
        # binary representations of numbers for disambiguation
        numeric = []
        for pattern in patterns:
            number = 0
            # count the amount of times each segment appears in the patterns
            for letter in pattern:
                index = ord(letter)-97
                key[index] += 1
                number += 64 >> index
            numeric.append(number)

        # binary representation of positions of e, b, f (finds us 0, 6, 8)
        sort_068 = 0
        # identify segments e, b, f by amount of appearances of segments
        for i in range(7):
            if key[i] in ebf:
                sort_068 += 64 >> i
                # add e, b, f to dictionary with cyphered key
                dic[chr(i+97)] = ebf[key[i]]

        # disambiguate d, g (7 appearances each) and c, a (8 appearances each)
        for letters, val in ((('d', 'g'), 7), (('c', 'a'), 8)):
            i = key.index(val)
            test = sort_068 + (64 >> i)
            # a, g are both present in all numbers 0, 6, 8. c, d are not
            inall = len([n for n in numeric if test & n == test]) == 3
            dic[chr(i+97)] = letters[inall]
            key[i] = 0
            i = key.index(val)
            # add a, c, d, g to dictionary with cyphered key
            dic[chr(i+97)] = letters[not inall]

        numbers = list(numbers)

        for i in range(len(numbers)):
            decode = ''
            # decode cyphered segments using $dic
            for letter in numbers[i]:
                decode += dic[letter]

            # replace line segment notation with digits
            numbers[i] = str(digits.index(''.join(sorted(decode))))

        numsout.append(int(''.join(numbers)))

    return tuple(numsout)

# # 8A
# onefourseveneight = 0
# for num in findnums(parse_data(data)):
#     for digit in str(num):
#         if any(int(digit) == x for x in (1, 4, 7, 8)):
#             onefourseveneight += 1
#
# print(onefourseveneight)

# 8B
print(sum(findnums(parse_data(data))))
