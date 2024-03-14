class Timer:
    def __init__(self, image_list, start_index=0, delta=6, looponce=False):
        self.image_list = image_list
        self.delta = delta
        self.looponce = looponce
        self.start_index = start_index
        self.index = start_index
        self.time = 0
        # self.index = start_index if start_index < len(image_list) - 1 else 0

    def update_index(self):
        self.time += 1
        if self.time >= self.delta:
            self.index += 1
            self.time = 0
            if self.index > len(self.image_list) - 1 and not self.finished():
                self.index = 0

    def finished(self):
        finished = self.looponce and self.index >= len(self.image_list) - 1
        return finished

    def current_index(self):
        return self.index

    def current_image(self):  # self.time = 0
        if self.finished():
            return self.image_list[-1]
        self.update_index()
        return self.image_list[self.index]

    def reset(self):
        self.index = (
            self.start_index if self.start_index < len(self.image_list) - 1 else 0
        )


# TODO: test if dictionary works
# class TimerDict(Timer):
#     def __init__(self, dictionary, start_key, delta=6, looponce=False):
#         super().__init__(
#             image_list=dictionary[start_key],start_index=0, delta=delta, looponce=looponce
#         )
#         self.dictionary = dictionary
#         self.start_key = start_key
#         self.current_key = start_key

#     def has_name(self, name):
#         return name in self.dictionary

#     def keys(self):
#         return self.dictionary.keys()

#     def switch_to(self, key, looponce=False):
#         self.image_list = self.dictionary[key]
#         self.index = 0
#         self.time = 0
#         self.looponce = looponce
#         self.current_key = key

# TODO: remove the methods below
#     def update_index(self):
#         return super().update_index()

#     def finished(self):
#         return super().finished()

#     def current_index(self):
#         return super().current_index()

#     def current_image(self):
#         return super().current_image()
