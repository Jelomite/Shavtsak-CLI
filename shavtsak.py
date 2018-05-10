class Shavtsak:
    def __init__(self, soldiers: list):
        """
        Constructor for the data structure. It's basically a nested dictionary with lists.
        All you need to do is to specify the soldiers that are in the schedule.
        You can later reduce the soldiers for a specific day or period of time.
        """
        # heck of a data structure
        self.schedule = {
            'sunday': {
                'kitchen': [],
                'morning': [],
                'evening': [],
                'night': []
            },
            'monday': {
                'kitchen': [],
                'morning': [],
                'evening': [],
                'night': []
            },
            'tuesday': {
                'kitchen': [],
                'morning': [],
                'evening': [],
                'night': []
            },
            'wednesday': {
                'kitchen': [],
                'morning': [],
                'evening': [],
                'night': []
            },
            'thursday': {
                'kitchen': [],
                'morning': [],
                'evening': [],
                'night': []
            },
            'friday': {
                'kitchen': [],
                'morning': [],
                'evening': [],
                'night': []
            },
            'saturday': {
                'kitchen': [],
                'morning': [],
                'evening': [],
                'night': []
            },
        }
        # TODO: this is just for a week, we need to make this timeless!
        self.soldiers = soldiers  # full list of all soldiers .
        self.reduced = []  # the segments in which the soldiers may differ.

    def __str__(self):
        from tabulate import tabulate
        # you know it's gonna be the real deal when you import tabulate
        table = [['/', 'kitchen', 'morning', 'evening', 'night']]
        assignments = table[0][1:]  # pass by value...
        days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

        for day in days:
            watches = [day]
            for watch in assignments:
                watches.append(', '.join(map(str, self.schedule[day][watch])))
            table.append(watches)

        return tabulate(table, tablefmt='fancy_grid', stralign='center')

    def assign(self, soldiers: list, day: (str, int), watch: (str, int)):
        """
        Adds data to the schedule dictionary.
        :param soldiers: list of soldiers to assign for the mission.
        :param day: day of the week to assign the soldiers.
        :param watch: can be morning, evening, night or kitchen.
        :return: True if value before assignment was empty, in case of overwrite, returns False

        We can use both strings and ID's in assignment, strings are more readable but can be quite long to type.
        For example - Sunday is 0, and Saturday is 6.
        Furthermore, the watch can be assigned using it's index in the day.
        In that case we get: 0, 1, 2, 3 for kitchen, morning evening and night.

        Lets see a simple example for calling the assign function:
        assign([soldier1, soldier2], 0, 1) -> this will assign soldier1 & soldier2 to the morning watch of sunday.
        We can do it another way and expect the exact result as before:
        assign([soldier1, soldier2], 'sunday', 'morning')
        """

        # if there's only one soldier to assign, this wont make it a necessity to wrap it in a list
        if type(soldiers) is Soldier:
            soldiers = [soldiers]

        # All soldiers must be in self.soldiers, we cant just add new soldiers in random places.
        for soldier in soldiers:
            if soldier not in self.soldiers:
                raise ValueError

        if type(day) is int:
            day = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'][day]

        if type(watch) is int:
            watch = ['kitchen', 'morning', 'evening', 'night'][watch]

        before_assignment = self.schedule[day][watch]
        self.schedule[day][watch] = soldiers

        if not before_assignment:
            return True

        return False

    def get(self, day: (str, int), watch: (str, int)):
        """
        Gets us the content of a specific watch in the schedule.
        :param day: desired day of the week, can be str and can be ID
        :param watch: desired watch, str or ID (0 - kitchen, 1 - morning... 2 - night)
        :return: list of soldiers in the desired watch
        """
        if type(day) is int:
            day = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'][day]

        if type(watch) is int:
            watch = ['kitchen', 'morning', 'evening', 'night'][watch]

        return self.schedule[day][watch]

    def last(self, soldier, day: (str, int), watch: (str, int)):
        """
        checks last assignment of desired soldier, including the current watch
        :param soldier: desired soldier to check
        :param day: desired day of the week, can be str and can be ID
        :param watch: desired watch, str or ID (0 - kitchen, 1 - morning... 2 - night)
        :return: amount of assignments the soldier didn't do and the last assignment he did.
        """
        days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        watches = ['kitchen', 'morning', 'evening', 'night']
        if type(day) is str:
            day = days.index(day)
        if type(watch) is str:
            watch = watches.index(watch)

        watch_id = day * 4 + watch

        for wid in reversed(range(watch_id)):
            if soldier in self.get(int(wid / 4), wid % 4):
                return watch_id - wid, watches[wid % 4]
        return watch_id, None

    def next(self, soldier, day: (str, int), watch: (str, int)):
        """
        just like self.last(), but returns the next assignment of soldier.
        """
        days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        watches = ['kitchen', 'morning', 'evening', 'night']
        if type(day) is str:
            day = days.index(day)
        if type(watch) is str:
            watch = watches.index(watch)

        watch_id = day * 4 + watch

        for wid in range(watch_id, 28):
            if soldier in self.get(int(wid / 4), wid % 4):
                return wid - watch_id, watches[wid % 4]
        return watch_id, None

    def _sort(self, day, watch):
        """
        sorts the soldiers by their last watch, first is the most "do-nothing".
        :return: list of soldiers
        """
        soldiers = self._gen_soldiers(day, watch)
        skey = lambda s: self.last(s, day, watch)[0] + self.next(s, day, watch)[0]
        sorted_s = sorted(soldiers, key=skey, reverse=True)
        # remove the kitchen soldier in that day, a soldier that is in kitchen shouldn't be checked.
        try:
            today_kitchen = self.get(day, 'kitchen')
            for soldier in today_kitchen:
                sorted_s.remove(soldier)

        except IndexError:
            pass

        return list(sorted_s)

    def kitchen(self, day, n_soldiers):
        """
        This function will try to guess the optimal soldier to be assigned to the kitchen.
        It is determined by using the sorting algorithm and some basic rules for fairness,
        the rules are hardcoded, but they're pretty simple:
        - Only people with pazam smaller than 2 (only 0 and 1).
        - A solider cannot be assigned to the kitchen two days in a row
        :param day: the day in which the algorithm will calculate the optimal soldier for the kitchen
        :param n_soldiers: amount of soldiers to assign to kitchen.
        :return: calculated Soldier for the kitchen to be assigned.
        """
        if day in ('sunday', 0):  # the week starts at sunday, we can't just check the previous day
            # until this is fixed we just raise this shitty error
            raise NotImplementedError

        if type(day) is str:
            # We want to iterate to the previous day. Assumption made that it's not the first day.
            # In that case, we will never get ID of day - 1
            day = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'].index(day)

        s = self._sort(day, 'kitchen')  # getting the current day sort

        # remove previous day soldiers from kitchen
        for ksoldier in self.get(day - 1, 0):
            if ksoldier in s:
                s.remove(ksoldier)

        # we cant allow people with pazam to be assigned to kitchen, so we have to filter them out.
        filtered = filter(lambda soldier: soldier.pazam < 2, s)

        # all that's left is to assign the first n soldiers to the kitchen
        return list(filtered)[0:n_soldiers]

    def add_reduced(self, soldiers: list, sday, swatch, eday, ewatch):
        """
        We can add periods in the schedule where we don't have the full list of soldiers.
        It can be for a single watch, or for an extended amount of watches and days.
        :param soldiers: list of soldiers to remove from the list.
        :return: True if the addition was successful. Otherwise it throws an exception.
        """
        # TODO: this should be a smart function with good a design.
        # Currently it is not.

        # we want to convert the days and the watches to int so we could convert them into IDs
        # TODO: find a better conversion method.

        if type(sday) is str:
            days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
            sday = days.index(sday)

        if type(swatch) is str:
            swatch = ['kitchen', 'morning', 'evening', 'night'].index(swatch)

        if type(eday) is str:
            days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
            eday = days.index(eday)

        if type(ewatch) is str:
            ewatch = ['kitchen', 'morning', 'evening', 'night'].index(ewatch)

        start_id = sday * 4 + swatch
        end_id = eday * 4 + ewatch

        # TODO: add check for if the period of time is conflicting with the other entries.
        self.reduced.append((soldiers, start_id, end_id))

    def _gen_soldiers(self, day: (int, str), watch: (int, str)):
        """
        Based on the reduced soldiers, total soldiers and other parameters, this func will calculate the
        actual list of soldiers that are currently available for assignment.
        :param day: desired day of week
        :param watch: desired watch to check
        :return: list of new soldiers that are available for assignment.
        """

        # we want to convert the days and the watches to int so we could convert them into IDs
        if type(day) is str:
            days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
            day = days.index(day)

        if type(watch) is str:
            watch = ['kitchen', 'morning', 'evening', 'night'].index(watch)

        # we assume that we don't have two reductions of the same soldier at the same day.
        # If it does, it'll raise an error of ValueError, because the soldier will be removed from the list
        # hence, he can't be removed again at later iteration.
        current_watch_id = day * 4 + watch  # this is a simple representation of the watch and day of week.
        new_soldiers = self.soldiers.copy()
        for soldiers, start, end in self.reduced:
            # in case the current watch is in range of a reduced amount of soldiers,
            # we return the new soldiers that are listed in out list
            if current_watch_id in range(start, end + 1):
                for soldier in soldiers:
                    new_soldiers.remove(soldier)

        # once we removed all the relevant soldiers from our list, we can return it.
        return new_soldiers

    def predict(self, day, watch, n_soldiers=2, force=False):
        """
        predicts the watch that should be on the assigned day and watch
        :param day: desired day for prediction
        :param watch: desired watch for prediction
        :param n_soldiers: amount of soldiers to assign
        :param force: if this flag is true, it will overwrite the watch no matter what
        :return: returns a list of soldiers for assignment based on number of soldiers
        """
        if type(day) is int:
            day = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'][day]

        if type(watch) is int:
            watch = ['kitchen', 'morning', 'evening', 'night'][watch]

        if self.schedule[day][watch] and not force and n_soldiers is 2:
            # if there's an assignment in this particular day and watch
            # raise an error, because we cant predict something that isn't this day
            return self.schedule[day][watch]

        soldiers = self._sort(day, watch)
        return soldiers[:n_soldiers]


class Soldier:
    def __init__(self, name, pazam):
        self.name = name
        self.pazam = pazam
        self.sad = 0

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)
