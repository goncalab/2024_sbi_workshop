import numpy as np
import torch
import torch.nn as nn
from scipy import stats as spstats


# based on https://github.com/mackelab/neuralgbi/blob/main/gbi/hh/HodgkinHuxleyStatsMoments.py
class HodgkinHuxleyStatsMoments:
    """Moment based SummaryStats class for the Hodgkin-Huxley model
    Calculates summary statistics
    """

    def __init__(self, t_on, t_off, n_mom=5, t_min=0.0, t_max=120.0, dt=0.01):
        """See SummaryStats.py for docstring"""
        self.t_on = t_on
        self.t_off = t_off
        self.n_mom = n_mom
        self.t_min = t_min
        self.t_max = t_max
        self.dt = dt

    def calc(self, repetition_list):
        """Calculate summary statistics
        Parameters
        ----------
        repetition_list : list of dictionaries, one per repetition
            data list, returned by `gen` method of Simulator instance
        Returns
        -------
        np.array, 2d with n_reps x n_summary
        """
        stats = []

        # NOTE: not vectorized, but this is not the bottle neck
        for r in range(len(repetition_list)):
            x = repetition_list[r]

            t = np.arange(self.t_min, self.t_max + self.dt, self.dt)
            t_on = self.t_on
            t_off = self.t_off

            # initialise array of spike counts
            v = x.copy()

            # put everything to -10 that is below -10 or has negative slope
            ind = np.where(v < -10)
            v[ind] = -10
            ind = np.where(np.diff(v) < 0)
            v[ind] = -10

            # remaining negative slopes are at spike peaks
            ind = np.where(np.diff(v) < 0)
            spike_times = np.array(t)[ind]
            spike_times_stim = spike_times[(spike_times > t_on) & (spike_times < t_off)]

            # number of spikes
            if spike_times_stim.shape[0] > 0:
                spike_times_stim = spike_times_stim[
                    np.append(1, np.diff(spike_times_stim)) > 0.5
                ]

            # resting potential and std
            rest_pot = np.mean(x[t < t_on])
            rest_pot_std = np.std(x[int(0.9 * t_on / self.dt) : int(t_on / self.dt)])

            std_pw = np.power(
                np.std(x[(t > t_on) & (t < t_off)]),
                np.linspace(3, self.n_mom, self.n_mom - 2),
            )
            std_pw = np.concatenate((np.ones(1), std_pw))
            moments = (
                spstats.moment(
                    x[(t > t_on) & (t < t_off)],
                    np.linspace(2, self.n_mom, self.n_mom - 1),
                )
                / std_pw
            )

            # concatenation of summary statistics
            sum_stats_vec = np.concatenate(
                (
                    np.array([spike_times_stim.shape[0]]),
                    np.array(
                        [
                            rest_pot,
                            # rest_pot_std, # NOTE not used at the moment
                            np.mean(x[(t > t_on) & (t < t_off)]),
                        ]
                    ),
                    moments,
                )
            )

            stats.append(sum_stats_vec)

        return np.asarray(stats)
