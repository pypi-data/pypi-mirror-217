import unittest

import numpy as np
import torch

from torch_pp import StandardScaler
from torch_pp.minmaxscaler import MinMaxScaler


class TestScalers(unittest.TestCase):
    def test_standard_scaler_transform(self):
        input_x = torch.from_numpy(np.array([[20., 1.], [-3., 700.], [-11., 3.]])).to(dtype=torch.double)
        scaler = StandardScaler()
        transformed_x = scaler.fit_transform(input_x)
        transformed_back_x = scaler.inverse_transform(transformed_x)
        torch.testing.assert_close(input_x, transformed_back_x)

    def test_minmax_scaler_transform(self):
        input_x = torch.from_numpy(np.array([[20., 1.], [-3., 700.], [-11., 3.]])).to(dtype=torch.float64)
        scaler = MinMaxScaler()
        transformed_x = scaler.fit_transform(input_x)
        transformed_back_x = scaler.inverse_transform(transformed_x)
        torch.testing.assert_close(input_x, transformed_back_x)


if __name__ == '__main__':
    unittest.main()
