def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', empty='-'):
    percents = f'{100 * (iteration / float(total)):.{decimals}f}'
    filledLength = int(length * iteration // total)
    bar = f'{fill * filledLength}{empty * (length-filledLength)}'

    print(f'{prefix} |{bar}| {percents}% {suffix}', end='\r')

    if iteration == total:
        print()
