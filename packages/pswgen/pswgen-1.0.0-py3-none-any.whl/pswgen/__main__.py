import random
from optparse import OptionParser

chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
uppercase = chars[:26]
lowercase = chars[26:52]
digits = chars[52:62]
punct = chars[62:]

def __og():
    while 1:
        yield uppercase
        yield lowercase
        yield digits
        yield punct

def main():
    parser = OptionParser(version="1.0.0")
    parser.add_option("-n", "--lenght", dest="lenght", type='int',
                      help="choose the lenght of the generating password", metavar="LENGHT", default=10)

    options, args = parser.parse_args()
    lenght = options.lenght
    if lenght < 6:
        print("password too short")
        raise SystemExit
    og = __og()
    result = []
    for i in range(lenght):
        result.append(random.choice(next(og)))
    random.shuffle(result)
    print("".join(result))

if __name__ == "__main__":
    main()
