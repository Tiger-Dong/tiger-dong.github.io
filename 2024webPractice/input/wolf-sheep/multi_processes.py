import concurrent.futures
from ruamel import yaml
import os
from loguru import logger
import numpy as np
import wolf_sheep


def main():
    # this parameters is for testing different values of a configuration
    # e.g. for "ALPHA", low, high, step = 0.1, 1.6, 0.2
    parameters = {
        # "ALPHA": [0.11, 0.16, 0.02],
        # "N_WOLF": [8, 10, 1],
        "Gamma": [500, 2000, 500],
        # "BETA": [100, 500, 50],
    }
    with open("config.yml", "r") as f:
        configs = yaml.load(f, Loader=yaml.Loader)

    futures = set()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for parameter_name in parameters:
            low, high, step = parameters[parameter_name]
            parameter_values = np.arange(low, high, step)
            for value in parameter_values:
                # change type and round np.float to for dumping value to yaml
                # otherwise, value might be 15.00000000002, and can't dump to yaml
                if isinstance(value, np.int_):
                    v = int(value)
                elif isinstance(value, np.float):
                    v = float(np.around(value, 4))
                dir_name = os.path.join("history", f"{parameter_name}-{v}")
                if os.path.exists(dir_name):
                    raise Exception(f"{dir_name} exists. We tried not to overwrite previous output")
                else:
                    os.makedirs(dir_name)
                configs[parameter_name] = v
                config_file = os.path.join(dir_name, "config.yml")
                with open(config_file, 'w') as f:
                    yaml.dump(configs, f, Dumper=yaml.RoundTripDumper)

                logger.info(f"submitting with config {config_file}")
                future = executor.submit(wolf_sheep.main, config_file)
                futures.add(future)

    try:
        for future in concurrent.futures.as_completed(futures):
            err = future.exception()
            if err is not None:
                raise err
    except KeyboardInterrupt:
        print("stopped by hand")


if __name__ == '__main__':
    main()
