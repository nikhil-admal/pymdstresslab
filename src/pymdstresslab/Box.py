from pymdstresslab.shared_objects import pymdstresslab as _pmsl_so


def Box(config_file:str, reference_and_final:bool = True, ):
    """
    This is an example Python function wrapping the compiled artifacts as a hidden class.

    :param number_of_particles: Initialize using number of particles. If not provided, it defaults to -1. During read function call, it then reads from file.
    :param reference_and_final: Assigns 1 for True, 0 for False,  
    :param config_file: filename for configuration file

    """
    reference_and_final = 1 if reference_and_final else 0

    with open(config_file) as f:
        number_of_particles = int(f.readline())
            
    if number_of_particles > 0:
        _body = _pmsl_so.BoxConfiguration(number_of_particles, reference_and_final)
    else:
        raise ValueError("Config file does not correctly lists number of particles")
    _body.read(config_file, reference_and_final)
    return _body
