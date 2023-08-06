# pylint: disable=unused-argument,abstract-method

import random
from statistics import mean, median

import numpy as np
import statsmodels.api as sm
from numpy import linspace

from ..field import extra_var
from ..utils import get_logger
from .chain import ChainNetwork, ChainNode, ChainSource, ChainTrial, ChainTrialMaker

logger = get_logger()


class GibbsNetwork(ChainNetwork):
    """
    A Network class for Gibbs sampler chains.

    Attributes
    ----------

    vector_length : int
        Must be overridden with the length of the free parameter vector
        that is manipulated during the Gibbs sampling procedure.
    """

    vector_length = None

    def make_definition(self):
        return {}

    def random_sample(self, i: int):
        """
        (Abstract method, to be overridden)
        Randomly samples a new value for the ith element of the
        free parameter vector.
        This is used for initialising the participant's response options.

        Parameters
        ----------

        i
            The index of the element that is being resampled.

        Returns
        -------

        float
            The new parameter value.
        """
        raise NotImplementedError


class GibbsTrial(ChainTrial):
    """
    A Trial class for Gibbs sampler chains.

    Attributes
    ----------

    resample_free_parameter : bool
        If ``True`` (default), the starting value of the free parameter
        is resampled on each trial. Disable this behaviour
        by setting this parameter to ``False`` in the definition of
        the custom :class:`~psynet.trial.gibbs.GibbsTrial` class.

    initial_vector : list
        The starting vector that is presented to the participant
        at the beginning of the trial.

    active_index : int
        The index of the parameter that the participant manipulates
        on this trial.

    reverse_scale : bool
        Whether the response scale should be reversed.
        This reversal should be implemented on the front-end,
        with the correct numbers still being reported to the back-end.

    updated_vector : list
        The updated vector after the participant has responded.
    """

    __extra_vars__ = ChainTrial.__extra_vars__.copy()

    resample_free_parameter = True

    def choose_reverse_scale(self):
        return bool(random.randint(0, 1))

    def make_definition(self, experiment, participant):
        """
        In the Gibbs sampler, a trial's definition is created by taking the
        definition from the source
        :class:`~psynet.trial.gibbs.GibbsNode`,
        modifying it such that the free parameter has a randomised
        starting value, and adding a randomised Boolean determining whether the
        corresponding slider (or similar) has its direction reversed.
        Note that different trials at the same
        :class:`~psynet.trial.gibbs.GibbsNode` will have the same
        free parameters but different starting values for those free parameters.

        Parameters
        ----------

        experiment
            An instantiation of :class:`psynet.experiment.Experiment`,
            corresponding to the current experiment.

        participant
            Optional participant with which to associate the trial.

        Returns
        -------

        object
            The trial's definition, equal to the node's definition
            with the free parameter randomised.

        """
        vector = self.node.definition["vector"].copy()
        active_index = self.node.definition["active_index"]
        reverse_scale = self.choose_reverse_scale()

        if self.resample_free_parameter:
            vector[active_index] = self.network.random_sample(active_index)

        definition = {
            "vector": vector,
            "active_index": active_index,
            "reverse_scale": reverse_scale,
        }

        return definition

    @property
    @extra_var(__extra_vars__)
    def initial_vector(self):
        return self.definition["vector"]

    @property
    @extra_var(__extra_vars__)
    def active_index(self):
        return self.definition["active_index"]

    @property
    @extra_var(__extra_vars__)
    def reverse_scale(self):
        return self.definition["reverse_scale"]

    @property
    @extra_var(__extra_vars__)
    def updated_vector(self):
        if self.answer is None:
            return None
        new = self.initial_vector.copy()
        new[self.active_index] = self.answer
        return new

    def summarize(self):
        return {
            "trial_id": self.id,
            "node_id": self.origin.id,
            "network_id": self.network.id,
            "network_definition": self.network.definition,
            "initial_vector": self.initial_vector,
            "active_index": self.active_index,
            "reverse_scale": self.reverse_scale,
            "answer": self.answer,
            "updated_vector": self.updated_vector,
        }


class GibbsNode(ChainNode):
    """
    A Node class for Gibbs sampler chains.
    """

    @property
    def vector(self):
        return self.definition["vector"]

    @property
    def active_index(self):
        return self.definition["active_index"]

    @staticmethod
    def parallel_mean(*vectors):
        return [mean(x) for x in zip(*vectors)]

    @staticmethod
    def get_unique(x):
        assert len(set(x)) == 1
        return x[0]

    # mean, median, kernel
    summarize_trials_method = "mean"

    def summarize_trial_dimension(self, observations):
        method = self.summarize_trials_method
        logger.debug("Summarizing observations using method %s...", method)

        self.var.summarize_trial_method = method

        if method == "mean":
            return mean(observations)
        elif method == "median":
            return median(observations)
        elif method == "kernel_mode":
            return self.kernel_summarize(observations, method="mode")
        else:
            raise NotImplementedError

    # can be a number, or normal_reference, cv_ml, cv_ls (see https://www.statsmodels.org/devel/generated/statsmodels.nonparametric.kernel_density.KDEMultivariate.html)
    kernel_width = "cv_ls"

    def kernel_summarize(self, observations, method):
        assert isinstance(observations, list)

        kernel_width = self.kernel_width
        if (not isinstance(kernel_width, str)) and (np.ndim(kernel_width) == 0):
            kernel_width = [kernel_width]

        density = sm.nonparametric.KDEMultivariate(
            data=observations, var_type="c", bw=kernel_width
        )
        points_to_evaluate = linspace(min(observations), max(observations), num=501)
        pdf = density.pdf(points_to_evaluate)

        if method == "mode":
            index_max = np.argmax(pdf)
            mode = points_to_evaluate[index_max]

            self.var.summary_kernel = {
                "bandwidth": kernel_width,
                "index_max": int(index_max),
                "mode": float(mode),
                "observations": observations,
                "pdf_locations": points_to_evaluate.tolist(),
                "pdf_values": pdf.tolist(),
            }
            return mode
        else:
            raise NotImplementedError

    def summarize_trials(self, trials: list, experiment, participant):
        """
        This method summarizes the answers to the provided trials.
        The default method averages over all the provided parameter vectors,
        and will typically not need to be overridden.

        Parameters
        ----------
        trials
            Trials to be summarized. By default only trials that are completed
            (i.e. have received a response) and processed
            (i.e. aren't waiting for an asynchronous process)
            are provided here.

        experiment
            An instantiation of :class:`psynet.experiment.Experiment`,
            corresponding to the current experiment.

        participant
            The participant who initiated the creation of the node.

        Returns
        -------

        dict
            A dictionary of the following form:

            ::

                {
                    "vector": summary_vector,
                    "active_index": active_index
                }

            where ``summary_vector`` is the summary of all the vectors,
            and ``active_index`` is an integer identifying which was the
            free parameter.
        """
        self.var.summarize_trials_used = [t.id for t in trials]
        active_index = trials[0].active_index
        observations = [t.updated_vector[active_index] for t in trials]

        summary = self.summarize_trial_dimension(observations)
        self.var.summarize_trials_output = summary

        vector = trials[0].updated_vector.copy()
        vector[active_index] = summary

        return {"vector": vector, "active_index": active_index}

    def create_definition_from_seed(self, seed, experiment, participant):
        """
        Creates a :class:`~psynet.trial.gibbs.GibbsNode` definition
        from the seed passed by the previous :class:`~psynet.trial.gibbs.GibbsNode`
        or :class:`~psynet.trial.gibbs.GibbsSource` in the chain.
        The vector of parameters is preserved from the seed,
        but the 'active index' is increased by 1 modulo the length of the vector,
        meaning that the next parameter in the vector is chosen as the current free parameter.
        This method will typically not need to be overridden.


        Returns
        -------

        dict
            A dictionary of the following form:

            ::

                {
                    "vector": vector,
                    "active_index": new_index
                }

            where ``vector`` is the vector passed by the seed,
            and ``new_index`` identifies the position of the new free parameter.
        """
        vector = seed["vector"]
        dimension = len(vector)
        original_index = seed["active_index"]
        new_index = (original_index + 1) % dimension
        return {"vector": vector, "active_index": new_index}


class GibbsSource(ChainSource):
    """
    A Source class for Gibbs sampler chains.
    """

    def generate_seed(self, network, experiment, participant):
        """
        Generates the seed for the :class:`~psynet.trial.gibbs.GibbsSource`.
        By default the method samples the vector of parameters by repeatedly
        applying :meth:`~psynet.trial.gibbs.GibbsNetwork.random_sample`,
        and randomly chooses one of these parameters to be the free parameter (``"active_index"``).
        Note that the source itself doesn't receive trials,
        and the first proper node in the chain will actually have
        the free parameter after this one (i.e. if there are 5 elements in the vector,
        and the :class:`~psynet.trial.gibbs.GibbsSource` has an ``"active_index"`` of
        2, then the first trials in the chain will have an ``"active_index"`` of 3.
        This method will not normally need to be overridden.

        Parameters
        ----------

        network
            The network with which the :class:`~psynet.trial.gibbs.GibbsSource` is associated.

        experiment
            An instantiation of :class:`psynet.experiment.Experiment`,
            corresponding to the current experiment.

        participant:
            An instantiation of :class:`psynet.participant.Participant`,
            corresponding to the current participant.

        Returns
        -------

        dict
            A dictionary of the following form:

            ::

                {
                    "vector": vector,
                    "active_index": active_index
                }

            where ``vector`` is the initial vector
            and ``active_index`` identifies the position of the free parameter.
        """
        if network.vector_length is None:
            raise ValueError(
                "network.vector_length must not be None. Did you forget to set it?"
            )
        return {
            "vector": [network.random_sample(i) for i in range(network.vector_length)],
            "active_index": random.randint(0, network.vector_length - 1),
        }


class GibbsTrialMaker(ChainTrialMaker):
    """
    A TrialMaker class for Gibbs sampler chains;
    see the documentation for
    :class:`~psynet.trial.chain.ChainTrialMaker`
    for usage instructions.
    """
