from os import getcwd
import json
import random
import datetime


def severity_gen():

    return random.choice(["moderate", "severe"])


def type_gen():
    return random.choice(["Wind", "Rain", "Snow", "Low Temperatures", "Fog", "High Temperatures", "Thunderstorms"])


def rand_time_delta():
    dict = {'days': random.randint(0, 1), 'hours': random.randint(0, 9), 'minutes': random.randint(0, 59)}
    return datetime.timedelta(**dict)


def randomise_demo_dates():
    strformat = lambda x: x.strftime("%Y-%m-%dT%H:%M:%S%z") + "+00:00"
    now = datetime.datetime.now()
    with open(getcwd() + '\\' + "demo_weather_warning.json", "r") as f:
        data = json.loads(f.read())
    for i in range(4):
        data[i]["type"] = type_gen()
        data[i]["updated"] = strformat(now)
        data[i]["issued"] = strformat((now - rand_time_delta()))
        if i in [0, 2, 3]:  # Normal. Expires in Future, Onset in  Future
            data[i]["onset"] = strformat((now + rand_time_delta()))
            data[i]["expiry"] = strformat(
                datetime.datetime.strptime(data[i]["onset"], "%Y-%m-%dT%H:%M:%S+00:00") + rand_time_delta()
            )
        elif i == 1:  # Expired. Onset in past, Expiry in past
            a = rand_time_delta()
            data[1]["onset"] = strformat((now - a))
            data[1]["expiry"] = strformat(
                datetime.datetime.strptime(data[1]["onset"], "%Y-%m-%dT%H:%M:%S+00:00") - a / 2)

    with open(getcwd() + '\\' + "demo_weather_warning.json", "w") as f:
        json.dump(data, f, indent=0)


if __name__ == '__main__':
    randomise_demo_dates()
