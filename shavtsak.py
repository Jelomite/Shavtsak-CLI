class Shavtsak:
    def __init__(self, soldiers: list, days=None, watches=None, name=''):
        """
        Constructor for the data structure. It's basically a nested dictionary with lists.
        All you need to do is to specify the soldiers that are in the schedule.
        You can later reduce the soldiers for a specific day or period of time.
        """
        self.days = days if days else ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        self.watches = watches if watches else ['kitchen', 'morning', 'noon', 'night']
        # building the schedule dictionary based on two lists, the days and the watches.
        self.schedule = {day: {watch: [] for watch in self.watches} for day in self.days}
        self.soldiers = soldiers  # full list of all soldiers .
        self.reduced = []  # the segments in which the soldiers may differ.
        self.name = name

    def explicit_checker(f):
        """ function decorator to check if an optional value is being set, even if it's default """
        varnames = f.__code__.co_varnames

        def wrapper(*a, **kw):
            kw['explicit_params'] = list(varnames[:len(a)]) + list(kw.keys())
            return f(*a, **kw)
        return wrapper

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
            sday = self.days.index(sday)

        if type(swatch) is str:
            swatch = self.watches.index(swatch)

        if type(eday) is str:
            eday = self.days.index(eday)

        if type(ewatch) is str:
            ewatch = self.watches.index(ewatch)

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
            day = self.days.index(day)

        if type(watch) is str:
            watch = self.watches.index(watch)

        # we assume that we don't have two reductions of the same soldier at the same day.
        # If it does, it'll raise an error of ValueError, because the soldier will be removed from the list
        # hence, he can't be removed again at later iteration.
        # this is a simple representation of the watch and day of week.
        current_watch_id = day * 4 + watch
        new_soldiers = self.soldiers.copy()
        for soldiers, start, end in self.reduced:
            # in case the current watch is in range of a reduced amount of soldiers,
            # we return the new soldiers that are listed in out list
            if current_watch_id in range(start, end + 1):
                new_soldiers = [soldier for soldier in new_soldiers if soldier not in soldiers]


        # once we removed all the relevant soldiers from our list, we can return it.
        return new_soldiers

    def _sort(self, day, watch):
        """
        sorts the soldiers by their last watch, first is the most "do-nothing".
        :return: list of soldiers
        """
        skey = lambda s: self.last(s, day, watch)[0]
        sorted_soldiers = sorted(self._gen_soldiers(day, watch), key=skey, reverse=True)
        if watch in (3, 'night'):
            if type(day) is str:
                day = self.days.index(day)
            sorted_soldiers = [soldier for soldier in sorted_soldiers if soldier not in self.get(day + 1, 0)]

        sorted_soldiers = [soldier for soldier in sorted_soldiers if soldier not in self.get(day, 0)]
        return sorted_soldiers

    def autoa(self, day, watch, debug=False):
        """
        auto assignment - it creates an assignment based on pre-defined rules.
        """
        # type conversion from string to int. for iteration purposes.
        if type(day) is str:
            day = self.days.index(day)

        if type(watch) is str:
            watch = self.watches.index(watch)

        # lets get the next watch, we'll do it with the watch ID algorithmselfself.
        # if the next watch is kitchen, we simply go another one.
        wid = day * len(self.watches) + watch + 1
        if not wid % len(self.watches):
            wid += 1

        previous_wid = day * len(self.watches) + watch - 1
        if not previous_wid % len(self.watches):
            previous_wid -= 1

        # we just create sorts and available soldiers.
        current_sort = self._sort(day, watch)
        next_sort = self._sort(int(wid / len(self.watches)), wid % len(self.watches))
        current_soldiers = self._gen_soldiers(day, watch)
        next_soldiers = self._gen_soldiers(int(wid / len(self.watches)), wid % len(self.watches))
        next_assignment = self.get(int(wid / len(self.watches)), wid % len(self.watches))
        previous_assignment = self.get(int(previous_wid / len(self.watches)), previous_wid % len(self.watches))
        # create a difference array by subtructing next from current.
        diff = [soldier for soldier in current_sort if soldier not in next_sort]

        # now we remove the difference from the current so we won't get any duplicates in soldiers.
        new_curr = [soldier for soldier in current_sort if soldier not in diff]
        modified = diff + new_curr
        modified = [soldier for soldier in modified if soldier not in previous_assignment]

        # and remove the soldiers from the next assignment so we wont get a conflicting situation
        return [soldier for soldier in modified if soldier not in next_assignment]

    def _sort_kitchen(self, day):
        if type(day) is int:
            day = self.days[day]
        skey = lambda soldier: self.last_kitchen(soldier, day) + self.next_kitchen(soldier, day)
        filtered_soldiers = filter(lambda sl: sl.pazam < 2, self._gen_soldiers(day, 0))
        sf = sorted(filtered_soldiers, key=skey, reverse=True)
        return sf


    def get(self, day: (str, int), watch: (str, int)):
        """
        Gets us the content of a specific watch in the schedule.
        :param day: desired day of the week, can be str and can be ID
        :param watch: desired watch, str or ID (0 - kitchen, 1 - morning... 2 - night)
        :return: list of soldiers in the desired watch
        """
        try:
            if type(day) is int:
                day = self.days[day]

            if type(watch) is int:
                watch = self.watches[watch]
        except IndexError:
            return []

        return self.schedule[day][watch]

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
            day = self.days[day]

        if type(watch) is int:
            watch = self.watches[watch]

        before_assignment = self.schedule[day][watch]
        self.schedule[day][watch] = soldiers

        if not before_assignment:
            return True

        return False

    def reset(self):
        """Resets the entire schedule"""
        self.schedule = {day: {watch: [] for watch in self.watches} for day in self.days}
        return None

    def append(self, day: str, index=None):
        """Appends another day to the schedule, if index isn't None, it can append it to a specific position"""
        # Can't append an existing day to the schedule.
        if day in self.day:
            raise ValueError('Day already exists in schedule')

        # Because index is none, we want to insert the day at the end of our days listself.
        if index is None:
            index = len(self.days)

        self.days.insert(index, day)
        # Sipmle addition of our watches dictionary to the new day that was created.
        self.schedule[day] = {watch: [] for watch in self.watches}
        return None

    def last(self, soldier, day: (str, int), watch: (str, int)):
        """
        checks last assignment of desired soldier, including the current watch
        :param soldier: desired soldier to check
        :param day: desired day of the week, can be str and can be ID
        :param watch: desired watch, str or ID (0 - kitchen, 1 - morning... 2 - night)
        :return: amount of assignments the soldier didn't do and the last assignment he did.
        """
        if type(day) is str:
            day = self.days.index(day)
        if type(watch) is str:
            watch = self.watches.index(watch)

        watch_id = day * 4 + watch

        for wid in reversed(range(watch_id)):
            if soldier in self.get(int(wid / len(self.watches)), wid % 4):
                n = watch_id - wid
                last_watch = self.watches[wid % len(self.watches)]
                n = n if last_watch is not 'kitchen' else n - 1
                return n, last_watch
        return watch_id, None

    def next(self, soldier, day: (str, int), watch: (str, int)):
        """
        just like self.last(), but returns the next assignment of soldier.
        """
        if type(day) is str:
            day = self.days.index(day)
        if type(watch) is str:
            watch = self.watches.index(watch)

        watch_id = day * 4 + watch

        for wid in range(watch_id, 28):
            if soldier in self.get(int(wid / len(self.watches)), wid % 4):
                return wid - watch_id, self.watches[wid % 4]
        return watch_id, None

    def last_kitchen(self, soldier, day: str):
        """
        gives us the number of days before the last kitchen
        """
        for iday in self.days[self.days.index(day)::-1]:
            if soldier in self.schedule[iday]['kitchen']:
                return self.days.index(day) - self.days.index(iday) - 1
        return self.days.index(day)

    def next_kitchen(self, soldier, day: str):
        """
        just as last_kitchen, returns the number of days untill the next last_kitchenself.
        """
        for iday in self.days[self.days.index(day):]:
            if soldier in self.schedule[iday]['kitchen']:
                return self.days.index(day) - self.days.index(iday) - 1
        return self.days.index(day)

    def kitchen(self, day, n_soldiers):
        """
        This function will try to guess the optimal soldier to be assigned to the kitchen.
        It is determined by using the sorting algorithm and some basic rules for fairness,
        the rules are hardcoded, but they're pretty simple:
        - Only people with pazam smaller than 2 (only 0 and 1).
        - A solider cannot be assigned to the kitchen after two days of kitchen.
        :param day: the day in which the algorithm will calculate the optimal soldier for the kitchen
        :param n_soldiers: amount of soldiers to assign to kitchen.
        :return: calculated Soldier for the kitchen to be assigned.
        """
        sort = self._sort_kitchen(day)
        return sort[:n_soldiers]

    @explicit_checker
    def predict(self, day, watch, n_soldiers=2, force=False, explicit_params=None):
        """
        predicts the watch that should be on the assigned day and watch
        :param day: desired day for prediction
        :param watch: desired watch for prediction
        :param n_soldiers: amount of soldiers to assign
        :param force: if this flag is true, it will overwrite the watch no matter what
        :return: returns a list of soldiers for assignment based on number of soldiers
        """
        if watch in (0, 'kitchen'):
            return self._sort_kitchen(day)[:n_soldiers if 'n_soldiers' in explicit_params else 1]
        else:
            return self.autoa(day, watch)[:n_soldiers]

    def fill(self):
        """Fills all empty spaces in schedule. NOTE: it uses the default values."""
        # first we fill in the kitchen
        for day in self.schedule.keys():
            if not self.get(day, 0):
                soldiers = self.predict(day, 0)
                self.assign(soldiers, day, 0)

        # now it's time to fill in the rest
        for day in self.schedule.keys():
            for watch in list(self.schedule[day].keys())[1:]:
                if not self.get(day, watch):
                    soldiers = self.predict(day, watch)
                    self.assign(soldiers, day, watch)

    def switch(self, s1: tuple, s2: tuple):
        """Switches between two soldiers at specific positions"""
        # get first target soldiers list from schedule
        soldier1, day1, watch1 = s1
        soldiers1 = self.get(day1, watch1)
        # get second target soldiers list from schedule
        soldier2, day2, watch2 = s2
        soldiers2 = self.get(day2, watch2)
        # re-assign the watches with a new list of soldiers, while replaceing the selected soldiers
        # and keeping the same exact order they where before.
        self.assign([soldier if soldier is not soldier1 else soldier2 for soldier in soldiers1], day1, watch1)
        self.assign([soldier if soldier is not soldier2 else soldier1 for soldier in soldiers2], day2, watch2)
        return None

    def copy(self):
        """creates new instance of shavtsak"""
        new = Shavtsak(self.soldiers)
        new.days = self.days.copy()
        new.watches = self.watches.copy()
        new.schedule = {day: {watch: self.schedule[day][watch].copy() for watch in self.watches} for day in self.days}
        new.reduced = self.reduced.copy()
        new.name = '' + self.name
        return new

    def parse(self) -> str:
        """made for single string export into whatsapp, in an ugly manner"""
        out = "--------"
        for day in s.schedule.keys():
            out += f'\n{day}:\n'
            for watch in s.schedule[day].keys():
                out += f'{watch}: ' + ', '.join(s.schedule[day][watch]) + '\n'

        return out

    def __str__(self):
        from tabulate import tabulate
        # you know it's gonna be the real deal when you import tabulate
        table = [[self.name] + self.watches]
        assignments = table[0][1:]  # pass by value...

        for day in self.days:
            watches = [day]
            for watch in assignments:
                watches.append(', '.join(map(str, self.schedule[day][watch])))
            table.append(watches)

        return tabulate(table, tablefmt='fancy_grid', stralign='center')


class Soldier:
    def __init__(self, name, pazam):
        self.name = name
        self.pazam = pazam

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)
