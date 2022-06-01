import sys
import pandas as pd
import aug_helpers as aug


class VtlpAug:
    # CONSTANTS
    name = "Vtlp_Aug"
    # action=Action.SUBSTITUTE,
    # method=Method.AUDIO,
    device = "cpu"
    aug_p = 0.1
    include_detail = False
    verbose = 0
    stateless = True
    aug_min = None
    aug_max = None
    parent_change_seq = 0
    duration = None

    def __init__(
        self,
        sampling_rate,
        zone=(0.2, 0.8),
        coverage=0.1,
        fhi=4800,
        factor_range=(0.9, 1.1),
    ):
        self.sampling_rate = sampling_rate
        self.fhi = fhi
        self.factor_range = factor_range
        self.zone = zone
        self.coverage = coverage

    def augment(self, data, n=1):
        """
        :param object/list data: Data for augmentation. It can be list of data (e.g. list
            of string or numpy) or single element (e.g. string or numpy). Numpy format only
            supports audio or spectrogram data. For text data, only support string or
            list of string.
        :param int n: Default is 1. Number of unique augmented output. Will be force to 1
            if input is list of data
        # :param int num_thread: Number of thread for data augmentation. Use this option
        #     when you are using CPU and n is larger than 1
        :return: Augmented data

        >>> augmented_data = aug.augment(data)

        """
        max_retry_times = (
            3  # max loop times of n to generate expected number of outputs
        )
        aug_num = 1 if isinstance(data, list) else n
        expected_output_num = len(data) if isinstance(data, list) else aug_num

        if data is None or len(data) == 0:
            sys.stdout("Length of data is 0")
            sys.exit(1)

        clean_data = data

        for _ in range(max_retry_times + 1):
            augmented_results = []

            # Multi inputs
            if isinstance(data, list):
                augmented_results = [self._substitute(d) for d in clean_data]

            # Single input with/without multiple input
            else:
                augmented_results = [self._substitute(clean_data) for _ in range(n)]

            if len(augmented_results) >= expected_output_num:
                break

        # TODO: standardize output to list even though n=1 from 1.0.0
        if len(augmented_results) == 0:
            # if not result, return itself
            if n == 1:
                return data
            # Single input with/without multiple input
            else:
                return [data]

        if isinstance(augmented_results, pd.DataFrame):
            return augmented_results
        else:
            if isinstance(data, list):
                return augmented_results
            else:
                if n == 1:
                    return augmented_results[0]
                return augmented_results[:n]

    def _substitute(self, data):
        start_pos, end_pos = aug.get_augment_range_by_coverage(
            data, self.zone, self.coverage
        )

        warp_factor = aug.get_random_factor(self.factor_range[0], self.factor_range[1])
        print(warp_factor)

        return aug.manipulate(
            data,
            start_pos=start_pos,
            end_pos=end_pos,
            sampling_rate=self.sampling_rate,
            warp_factor=warp_factor,
        )
