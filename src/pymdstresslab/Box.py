from pymdstresslab.shared_objects import pymdstresslab as _pmsl_so


class Box:
    """
    This is an example Python class wrapping the compiled artifacts as a hidden class.

    :param number_of_particles: Initialize using number of particles. If not provided, it defaults to -1. During read function call, it then 
    reads from file.
    :param reference_and_final: Assigns 1 for True, 0 for False, 
    :param config_file: filename for configuration file
    """
    def __init__(self, number_of_particles:int=-1, reference_and_final:bool = True, config_file:str = None) -> None:
        self.number_of_particles = number_of_particles
        self.reference_and_final = 1 if reference_and_final else 0
        self.config_file = config_file

        self._read_config()

        self._body = _pmsl_so.BoxConfiguration(self.number_of_particles, self.reference_and_final)

    def _read_config(self):
        """
        This routine just checks if number of particles is a positive integer or not. If not then 
        it initializes it from the [config_file]
        :raises ValueError: If file not found and particle number negative.
        """
        if (self.number_of_particles < 0):
            if self.config_file:
                with open(self.config_file) as f:
                    self.number_of_particles = int(f.readline())

    def read(self,box_file:str)->None:
        if self.number_of_particles < 0:
            raise ValueError("Number of particles not defined")
        self._body.read(box_file, self.reference_and_final)