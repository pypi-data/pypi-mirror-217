import torch


def _handle_zeros_in_scale(scale: torch.Tensor):
    constant_mask = scale < 10 * torch.finfo(scale.dtype).eps
    scale[constant_mask] = 1.0
    return scale


class MinMaxScaler:

    def __init__(self, feature_range=(0, 1)):
        self.data_range_ = None
        self.min_ = None
        self.scale_ = None
        self.n_samples_seen_ = 0
        self.data_max_ = torch.Tensor([float('-inf')])
        self.data_min_ = torch.Tensor([float('inf')])
        self.feature_range = feature_range
        if feature_range[0] >= feature_range[1]:
            raise ValueError("Minimum of desired feature range must be smaller than maximum.")

    def reset(self):
        self.n_samples_seen_ = 0
        return self

    def fit_transform(self, _input: torch.Tensor) -> torch.Tensor:
        self.partial_fit(_input)
        return self.transform(_input)

    def partial_fit(self, x: torch.Tensor):
        feature_range = self.feature_range

        data_min = torch.min(x, dim=0).values
        data_max = torch.max(x, dim=0).values

        if self.n_samples_seen_ == 0:
            self.n_samples_seen_ = x.shape[0]
        else:
            data_min = torch.minimum(self.data_min_, data_min)
            data_max = torch.maximum(self.data_max_, data_max)
            self.n_samples_seen_ += x.shape[0]

        data_range = data_max - data_min
        self.scale_ = (feature_range[1] - feature_range[0]) / _handle_zeros_in_scale(data_range)
        self.min_ = feature_range[0] - data_min * self.scale_
        self.data_min_ = data_min
        self.data_max_ = data_max
        self.data_range_ = data_range
        return self

    def transform(self, x: torch.Tensor):
        x_out = x.clone()
        x_out *= self.scale_
        x_out += self.min_
        return x_out

    def inverse_transform(self, x: torch.Tensor):
        x_out = x.clone()
        x_out -= self.min_
        x_out /= self.scale_
        return x_out
