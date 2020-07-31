from abc import ABC, abstractmethod
from mark_dataset.data_pair import DataPair
import numpy as np


class MarkDataset(ABC):

    def __init__(self, dataset_name):
        self.meta = {"name": dataset_name,
                     "authors": None,
                     "year": None,
                     "num_marks": None,
                     "num_samples": None}
        self.image_files = None
        self.mark_files = None
        self.key_marks_indices = None
        super().__init__()

    def __str__(self):
        # This function overridden makes the instance printable.
        description = "".join("{}: {}\n".format(k, v)
                              for k, v in self.meta.items())
        return description

    @abstractmethod
    def populate_dataset(self):
        """An abstract method to be overridden. This function should populate
        the dataset with essential data, including:

        * `image_files` This is a list of dataset image file paths. It should
        contain all the image samples.

        * `mark_files`. This is a list of dataset mark file paths. It should
        contain all the mark files. Note alignment of image and mark files is
        **required**. For instance:
            image_files: ["a.jpg", "b.jpg", "c.jpg"]
            mark_files; ["a.json", "b.json", "c.json"]

        * `key_mark_indices` This is a list of indices of specific marks.
        Currently they are: left eye left corner, left eye right corner, right
        eye left corner, right eye right corner, mouse left corner, mouse right
        corner.

        Remember to set the meta data, even this is optional.
        """
        pass

    @abstractmethod
    def get_marks_from_file(self, mark_file):
        """This function should read the mark file and return the marks as a
        numpy array in form of [[x, y, z], [x, y, z]]."""
        pass

    def pick_one(self):
        """Randomly pick a data pair."""
        # Pick a number randomly.
        straw = np.random.randint(0, len(self.image_files))

        # Get the coresponding marks.
        marks = self.get_marks_from_file(self.mark_files[straw])

        # Construct a datapair.
        return DataPair(self.image_files[straw], marks, self.key_marks_indices)

    def all_samples(self):
        """A generator yields one data pair a time."""
        for index in range(len(self.image_files)):
            # Get the coresponding marks.
            marks = self.get_marks_from_file(self.mark_files[index])

            # Construct a datapair.
            yield DataPair(self.image_files[index], marks, self.key_marks_indices)
