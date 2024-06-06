import json


def main():    
    with open("score.json", "w") as outfile:
        outfile.write(json.dumps({'accepted': True, 'score': 0, 'detail': '0', 'comment_type': 'score'}))


if __name__ == '__main__':
    main()
