# advent of code day 3 by Ruma (Lynn)

with open(r'.\input\day03.txt') as file:
    data = file.read()

# # 3A
# def power_consumption(report):
#     report = [r for r in report.split('\n') if r]
#     bitlength = max(map(len, report))
#     report = [int(b, 2) for b in report]
#
#     i = 1
#     most_common = lambda: int(bit >= len(report) * i / 2)
#     gamma = 0
#     while i.bit_length() <= bitlength:
#         bit = 0
#         for b in report:
#             bit += i & b
#         gamma += most_common() * i
#         i <<= 1
#     epsilon = gamma ^ 2**bitlength - 1
#     return gamma, epsilon

# 3B
def diagnostics(report):
    report = [r for r in report.split('\n') if r]
    bitlength = max(map(len, report))
    report = [int(b, 2) for b in report]

    most_common = lambda bit, set: int(bit >= len(set) * i / 2)
    gamma = 0
    ogr = set(report) # oxygen generator rating
    csr = set(report) # CO2 scrubber rating
    i = 2 ** (bitlength-1)
    while i > 0:
        bit = 0
        ogr_bit = 0
        csr_bit = 0
        i_is_0 = []
        i_is_1 = []

        for b in report:
            bit += i & b
            if b in ogr: ogr_bit += i & b
            if b in csr: csr_bit += i & b
            (i_is_0, i_is_1)[bool(i & b)].append(b)

        gamma += most_common(bit, report) * i
        if len(ogr) > 1:
            # remove the least common from set
            ogr -= set((i_is_0, i_is_1)[not most_common(ogr_bit, ogr)])
        if len(csr) > 1:
            # remove the most common from set
            csr -= set((i_is_0, i_is_1)[most_common(csr_bit, csr)])

        i >>= 1

    epsilon = gamma ^ 2**bitlength - 1

    return gamma, epsilon, tuple(ogr)[0], tuple(csr)[0]

print(int.__mul__(*diagnostics(data)[2:]))
