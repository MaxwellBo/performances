from dataclasses import dataclass
import itertools
import datetime

def flatten(xs):
    """
    >>> list(flatten([[1],[2,3]]))
    [1, 2, 3]
    """
    return list(itertools.chain.from_iterable(xs)) 

def sliding_window(xss):
    """
    >>> list(sliding_window([1,2,3]))
    [(1, 2), (2, 3)]
    """

    for i in range(len(xss) - 1):
        x = xss[i]
        y = xss[i + 1]

        yield (x, y)

def merge_adjacent(xss):
    if len(xss) >= 2:
        [x, y, *xs] = xss
        #       ^ this contains all the other elements that aren't the first and second

        if x.name == y.name:
            return merge_adjacent([ x.merge(y) ] + xs)
        else:
            return [x, *merge_adjacent([y] + xs)]
    else:
        return xss

@dataclass
class Performance(object):
    start: datetime
    end: datetime
    priority: int
    name: str

    def __contains__(self, date):
        return self.start <= date < self.end

@dataclass
class Attendance(object):
    start: datetime
    end: datetime
    name: str

    def merge(self, other):
        return Attendance(
            start=self.start,
            end=other.end,
            name=other.name
        )

def generate_schedule(performances):
    def get_time_highest_priority_performance(time):
        candidates = [ i for i in performances if time in i ]
        return candidates[0] if candidates != [] else None

    # get every unique timestamp
    stamps = sorted(set(flatten([ [i.start, i.end ] for i in performances ])))

    # between every timestamp, attend the highest priority performance, if there is one
    schedule = [ 
        Attendance(
            start=start,
            end=end,
            name=get_time_highest_priority_performance(start).name
        )
        for (start, end) in sliding_window(stamps) if get_time_highest_priority_performance(start)
    ]

    # don't list redundant attendances if we're not swapping between performances
    return merge_adjacent(schedule)

def main():
    DATE_OF_EVENT = datetime.datetime(2018, 1, 1)

    performances = sorted(
        [
            Performance(
                start=DATE_OF_EVENT.replace(hour=1),
                end=DATE_OF_EVENT.replace(hour=2),
                name="XTC",
                priority=9
            ),

            Performance(
                start=DATE_OF_EVENT.replace(hour=3),
                end=DATE_OF_EVENT.replace(hour=10),
                name="Anderson Paak",
                priority=3
            ),
            Performance(
                start=DATE_OF_EVENT.replace(hour=5),
                end=DATE_OF_EVENT.replace(hour=6),
                name="Slowdive",
                priority=8
            ),
            Performance(
                start=DATE_OF_EVENT.replace(hour=6),
                end=DATE_OF_EVENT.replace(hour=7),
                name="MBV",
                priority=10
            ),
            Performance(
                start=DATE_OF_EVENT.replace(hour=5, minute=30),
                end=DATE_OF_EVENT.replace(hour=6, minute=30),
                name="Linkin Park",
                priority=1
            ),
            Performance(
                start=DATE_OF_EVENT.replace(hour=5, minute=45),
                end=DATE_OF_EVENT.replace(hour=6, minute=45),
                name="Sweet Trip",
                priority=10
            )
        ],
        key=lambda i: i.priority,
        reverse=True
    )

    attendences = generate_schedule(performances)

    for i in attendences:
        print(i)


if __name__ == "__main__":
    main()
