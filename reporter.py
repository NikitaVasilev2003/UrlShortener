import os
import json
import requests


if __name__ == "__main__":
    print(
        os.environ["CALLBACK_URL"],
        os.environ["REPO_ID"],
        len(os.environ["LMS_TOKEN"]),
    )

    with open("score.json") as f:
        test_report = json.load(f)
    test_report['fork_id'] = os.environ["REPO_ID"]
    solution_id = os.environ.get("SOLUTION_ID", "")
    if solution_id and int(solution_id):
        solution_id = int(solution_id)
        test_report['solution_id'] = solution_id

    score = json.dumps(test_report)

    print(score)

    headers = {
        "Authorization": "Token " + os.environ["LMS_TOKEN"],
        "Content-type": "application/json",
    }
    resp = requests.post(os.environ["CALLBACK_URL"], headers=headers, data=score)
    print(os.environ["CALLBACK_URL"])
    print("solution_id", solution_id)
    print(headers)
    print(resp)
    print(resp.status_code)
    print(resp.content)
