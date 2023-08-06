"""Valuation optimizer class."""
from __future__ import division, print_function, absolute_import
from quest_eras.quest_library.utilities.pomo import optimizer
from quest_eras.quest_library.utilities.pomo.valuation.caiso.constraints import (
    ExpressionsBlock,
)
import logging
import pyomo.environ as pom
import pandas as pd
import numpy as np


class ValuationOptimizerCAISO(optimizer.Optimizer):
    """A framework wrapper class for creating Pyomo ConcreteModels for valuating energy storage in CAISO electricity market."""

    def __init__(
        self,
        price_electricity=None,  # Price of 1 MWh in energy market [$/MWh]
        price_reg_up=None,  # Price of 1MW being available for regulation up in regulation market [$/MW]
        price_reg_down=None,  # Price of 1MW being available for regulation down in regulation market [$/MW]
        price_reg_serv_up=None,  # Price of 1MW being deployed for regulation up in regulation market [$/MW]
        price_reg_serv_down=None,  # Price of 1MW being deployed for regulation down in regulation market [$/MW]
        cost_charge=None,  # Cost for charging [$]
        cost_discharge=None,  # Cost for discharing [$]
        mileage_mult_ru=None,  # Regulation-up mileage multiplication factor[-]
        mileage_mult_rd=None,  # Regulation-down mileage multiplication factor[-]
        perf_score_ru=None,  # Performance score of following regulation up signal [0,1]
        perf_score_rd=None,  # Performance score of following regulation down signal [0,1]
        fraction_reg_up=None,  # Fraction of available capacity actually deployed for regulation up [0,1]
        fraction_reg_down=None,  # Fraction of available capacity actually deployed for regulation down [0,1]
        market_type="arbitrage",  # Market type, default = energy arbitrage
        solver="glpk",  # Optimization solver, default = glpk
    ):

        self._model = pom.ConcreteModel()
        self._market_type = market_type
        self._solver = solver

        self._expressions_block = None

        self._price_electricity = price_electricity

        self._price_reg_up = price_reg_up
        self._price_reg_down = price_reg_down

        self._price_reg_serv_up = price_reg_serv_up
        self._price_reg_serv_down = price_reg_serv_down

        self._cost_charge = cost_charge
        self._cost_discharge = cost_discharge

        self._mileage_mult_ru = mileage_mult_ru
        self._mileage_mult_rd = mileage_mult_rd

        self._perf_score_ru = perf_score_ru
        self._perf_score_rd = perf_score_rd

        self._fraction_reg_up = fraction_reg_up
        self._fraction_reg_down = fraction_reg_down

        self._results = None
        self._gross_revenue = None

    @property
    def price_electricity(self):
        """Price of 1 MWh in energy market [$/MWh]."""
        return self._price_electricity

    @price_electricity.setter
    def price_electricity(self, value):
        """Set value for price_electricity."""
        self._price_electricity = value

    @property
    def price_reg_up(self):
        """Price of 1MW being available for regulation up in regulation market [$/MW]."""
        return self._price_reg_up

    @price_reg_up.setter
    def price_reg_up(self, value):
        """Set value for price_reg_up."""
        self._price_reg_up = value

    @property
    def price_reg_down(self):
        """Price of 1MW being available for regulation down in regulation market [$/MW]."""
        return self._price_reg_down

    @price_reg_down.setter
    def price_reg_down(self, value):
        """Set value for price_reg_down."""
        self._price_reg_down = value

    @property
    def price_reg_serv_up(self):
        """Price of 1MW being deployed for regulation up in regulation market [$/MW]."""
        return self._price_reg_serv_up

    @price_reg_serv_up.setter
    def price_reg_serv_up(self, value):
        """Set value for price_reg_serv_up."""
        self._price_reg_serv_up = value

    @property
    def price_reg_serv_down(self):
        """Price of 1MW being deployed for regulation down in regulation market [$/MW]."""
        return self._price_reg_serv_down

    @price_reg_serv_down.setter
    def price_reg_serv_down(self, value):
        """Set value for price_reg_serv_down."""
        self._price_reg_serv_down = value

    @property
    def cost_charge(self):
        """Cost for charging [$]."""
        return self._cost_charge

    @cost_charge.setter
    def cost_charge(self, value):
        """Set value for cost_charge."""
        self._cost_charge = value

    @property
    def cost_discharge(self):
        """Cost for discharging [$]."""
        return self._cost_discharge

    @cost_discharge.setter
    def cost_discharge(self, value):
        """Set value for cost_discharge."""
        self._cost_discharge = value

    @property
    def mileage_mult_ru(self):
        """Regulation-up mileage multiplication factor[-]."""
        return self._mileage_mult_ru

    @mileage_mult_ru.setter
    def mileage_mult_ru(self, value):
        """Set value for mileage_mult_ru."""
        self._mileage_mult_ru = value

    @property
    def mileage_mult_rd(self):
        """Regulation-down mileage multiplication factor[-]."""
        return self._mileage_mult_rd

    @mileage_mult_rd.setter
    def mileage_mult_rd(self, value):
        """Set value for mileage_mult_rd."""
        self._mileage_mult_rd = value

    @property
    def perf_score_ru(self):
        """Performance-score of following regulation up signal [0,1]."""
        return self._perf_score_ru

    @perf_score_ru.setter
    def perf_score_ru(self, value):
        """Set value for perf_score_ru."""
        self._perf_score_ru = value

    @property
    def perf_score_rd(self):
        """Performance-score of following regulation down signal [0,1]."""
        return self._perf_score_rd

    @perf_score_rd.setter
    def perf_score_rd(self, value):
        """Set value for perf_score_rd."""
        self._perf_score_rd = value

    @property
    def fraction_reg_up(self):
        """Fraction of available capacity actually deployed for regulation up [0,1]."""
        return self._fraction_reg_up

    @fraction_reg_up.setter
    def fraction_reg_up(self, value):
        """Set value for fraction_reg_up."""
        self._fraction_reg_up = value

    @property
    def fraction_reg_down(self):
        """Fraction of available capacity actually deployed for regulation down [0,1]."""
        return self._fraction_reg_down

    @fraction_reg_down.setter
    def fraction_reg_down(self, value):
        """Set value for fraction_reg_down."""
        self._fraction_reg_down = value

    @property
    def solver(self):
        """Optimization solver."""
        return self._solver

    @solver.setter
    def solver(self, value):
        """Setvalue for solver."""
        self._solver = value

    @property
    def expressions_block(self):
        """Contain model objectives and constraints."""
        return self._expressions_block

    @expressions_block.setter
    def expressions_block(self, value):
        """Set value for expressions_block."""
        self._expressions_block = value

    @property
    def market_type(self):
        """Market type, default = energy arbitrage."""
        return self._market_type

    @market_type.setter
    def market_type(self, value):
        """Set value to market_type."""
        if isinstance(value, str):
            self._market_type = value
        else:
            raise TypeError("market_type property must be of type str.")

    @property
    def results(self):
        """Pandas DataFrame containing results."""
        return self._results

    @results.setter
    def results(self, value):
        if isinstance(value, pd.DataFrame):
            self._results = value
        else:
            raise TypeError("results must be a Pandas DataFrame.")

    @property
    def gross_revenue(self):
        """Net revenue generated over the time period as solved for in the optimization."""
        return self._gross_revenue

    @gross_revenue.setter
    def gross_revenue(self, value):
        self._gross_revenue = value

    def _set_model_param(self):
        """Set the model params for the Pyomo ConcreteModel."""
        m = self.model

        # Check if params common to all formulations are set.
        if not hasattr(m, "Power_rating"):
            # Power rating; equivalently, the maximum energy charged in one hour [MW].
            logging.debug(
                "ValuationOptimizer: No Power_rating provided, setting default..."
            )
            m.Power_rating = 20

        if not hasattr(m, "R"):
            # Discount/interest rate [hour^(-1)].
            logging.debug("ValuationOptimizer: No R provided, setting default...")
            m.R = 0

        if not hasattr(m, "Energy_capacity"):
            # Energy capacity [MWh].
            logging.debug(
                "ValuationOptimizer: No Energy_capacity provided, setting default..."
            )
            m.Energy_capacity = 5

        if not hasattr(m, "Self_discharge_efficiency"):
            # Fraction of energy maintained over one time period.
            logging.debug(
                "ValuationOptimizer: No Self_discharge_efficiency provided, setting default..."
            )
            m.Self_discharge_efficiency = 1.00
        elif getattr(m, "Self_discharge_efficiency") > 1.0:
            logging.warning(
                "ValuationOptimizer: Self_discharge_efficiency provided is greater than 1.0, interpreting as percentage..."
            )
            m.Self_discharge_efficiency = m.Self_discharge_efficiency / 100

        if not hasattr(m, "Round_trip_efficiency"):
            # Fraction of input energy that gets stored over one time period.
            logging.debug(
                "ValuationOptimizer: No Round_trip_efficiency provided, setting default..."
            )
            m.Round_trip_efficiency = 0.85
        elif getattr(m, "Round_trip_efficiency") > 1.0:
            logging.warning(
                "ValuationOptimizer: Round_trip_efficiency provided is greater than 1.0, interpreting as percentage..."
            )
            m.Round_trip_efficiency = m.Round_trip_efficiency / 100

        if not hasattr(m, "Reserve_reg_min"):
            # Fraction of q_reg bid to increase state of charge minimum by.
            logging.debug(
                "ValuationOptimizer: No Reserve_reg_min provided, setting default..."
            )
            m.Reserve_reg_min = 0
        elif getattr(m, "Reserve_reg_min") > 1.0:
            logging.warning(
                "ValuationOptimizer: Reserve_reg_min provided is greater than 1.0, interpreting as percentage..."
            )
            m.Reserve_reg_min = m.Reserve_reg_min / 100

        if not hasattr(m, "Reserve_reg_max"):
            # Fraction of q_reg bid to decrease state of charge maximum by.
            logging.debug(
                "ValuationOptimizer: No Reserve_reg_max provided, setting default..."
            )
            m.Reserve_reg_max = 0
        elif getattr(m, "Reserve_reg_max") > 1.0:
            logging.warning(
                "ValuationOptimizer: Reserve_reg_max provided is greater than 1.0, interpreting as percentage..."
            )
            m.Reserve_reg_max = m.Reserve_reg_max / 100

        if not hasattr(m, "State_of_charge_min"):
            # Fraction of energy capacity representing the minimum state of charge.
            logging.debug(
                "ValuationOptimizer: No State_of_charge_min provided, setting default..."
            )
            m.State_of_charge_min = 0
        elif getattr(m, "State_of_charge_min") > 1.0:
            logging.warning(
                "ValuationOptimizer: State_of_charge_min provided is greater than 1.0, interpreting as percentage..."
            )
            m.State_of_charge_min = m.State_of_charge_min / 100

        if not hasattr(m, "State_of_charge_max"):
            # Fraction of energy capacity representing the maximum state of charge.
            logging.debug(
                "ValuationOptimizer: No State_of_charge_max provided, setting default..."
            )
            m.State_of_charge_max = 1
        elif getattr(m, "State_of_charge_max") > 1.0:
            logging.warning(
                "ValuationOptimizer: State_of_charge_max provided is greater than 1.0, interpreting as percentage..."
            )
            m.State_of_charge_max = m.State_of_charge_max / 100

        if not hasattr(m, "State_of_charge_init"):
            # Initial state of charge as a fraction of energy capacity.
            logging.debug(
                "ValuationOptimizer: No State_of_charge_init provided, setting default..."
            )
            m.State_of_charge_init = 0.5
        elif getattr(m, "State_of_charge_init") > 1.0:
            logging.warning(
                "ValuationOptimizer: State_of_charge_init provided is greater than 1.0, interpreting as percentage..."
            )
            m.State_of_charge_init = m.State_of_charge_init / 100

        try:
            if not getattr(m, "fraction_reg_up", None):
                logging.debug(
                    "ValuationOptimizer: No fraction_reg_up provided, setting default..."
                )
                m.fraction_reg_up = 0.25
        except ValueError:  # fraction_reg_up is array-like
            if np.isnan(m.fraction_reg_up).any():
                logging.debug(
                    "ValuationOptimizer: fraction_reg_up array-like provided has None values, setting default..."
                )
                m.fraction_reg_up = 0.25

        try:
            if not getattr(m, "fraction_reg_down", None):
                logging.debug(
                    "ValuationOptimizer: No fraction_reg_down provided, setting default..."
                )
                m.fraction_reg_down = 0.25
        except ValueError:  # fraction_reg_down is array-like
            if np.isnan(m.fraction_reg_down).any():
                logging.debug(
                    "ValuationOptimizer: fraction_reg_down array-like provided has None values, setting default..."
                )
                m.fraction_reg_down = 0.25

        # Converts fraction_reg_up and fraction_reg_down to arrays.
        try:
            m.fraction_reg_up[len(m.price_electricity) - 1]
        except TypeError:
            m.fraction_reg_up = np.array([m.fraction_reg_up] * len(m.price_electricity))

        try:
            m.fraction_reg_down[len(m.price_electricity) - 1]
        except TypeError:
            m.fraction_reg_down = np.array(
                [m.fraction_reg_down] * len(m.price_electricity)
            )

        try:
            if not getattr(m, "perf_score_ru", None):
                logging.debug(
                    "ValuationOptimizer: No perf_score_ru provided, setting default..."
                )
                m.perf_score_ru = 0.95
        except ValueError:  # fraction_reg_up is array-like
            if np.isnan(m.perf_score_ru).any():
                logging.debug(
                    "ValuationOptimizer: perf_score_ru array-like provided has None values, setting default..."
                )
                m.perf_score_ru = 0.95

        # Performance score for regulation up and down services for pay-for-performance models.
        try:
            if not getattr(m, "perf_score_rd", None):
                logging.debug(
                    "ValuationOptimizer: No perf_score_rd provided, setting default..."
                )
                m.perf_score_rd = 0.95
        except ValueError:  # fraction_reg_up is array-like
            if np.isnan(m.perf_score_rd).any():
                logging.debug(
                    "ValuationOptimizer: perf_score_rd array-like provided has None values, setting default..."
                )
                m.perf_score_rd = 0.95

        # Converts perf_score_ru and perf_score_rd to arrays.
        try:
            m.perf_score_ru[len(m.price_electricity) - 1]
        except TypeError:
            m.perf_score_ru = np.array([m.perf_score_ru] * len(m.price_electricity))
        except IndexError:
            logging.warning(
                "ValuationOptimizer: A perf_score_ru array was provided but is shorter than the price_electricity array."
            )
            raise (
                IncompatibleDataException(
                    "ValuationOptimizer: There was a mismatch in array sizes between perf_score_ru and price_electricity."
                )
            )

        try:
            m.perf_score_rd[len(m.price_electricity) - 1]
        except TypeError:
            m.perf_score_rd = np.array([m.perf_score_rd] * len(m.price_electricity))
        except IndexError:
            logging.warning(
                "ValuationOptimizer: A perf_score_rd array was provided but is shorter than the price_electricity array."
            )
            raise (
                IncompatibleDataException(
                    "ValuationOptimizer: There was a mismatch in array sizes between perf_score_rd and price_electricity."
                )
            )

    def _set_model_var(self):
        """Set the model vars for the Pyomo ConcreteModel."""
        m = self.model

        if not hasattr(m, "s"):

            def _s_init(_m, t):
                """Initialize energy storage device's state of charge [MWh]."""
                return m.State_of_charge_init * m.Energy_capacity

            m.s = pom.Var(m.soc_time, initialize=_s_init, within=pom.NonNegativeReals)

        if not hasattr(m, "q_r"):

            def _q_r_init(_m, t):
                """Initialize energy buy (chargey) from energy market [MWh]."""
                return 0.0

            m.q_r = pom.Var(m.time, initialize=_q_r_init, within=pom.NonNegativeReals)

        if not hasattr(m, "q_d"):

            def _q_d_init(_m, t):
                """Initialize energy sell (discharge) to energy market [MWh]."""
                return 0.0

            m.q_d = pom.Var(m.time, initialize=_q_d_init, within=pom.NonNegativeReals)

        if not hasattr(m, "q_ru"):

            def _q_ru_init(_m, t):
                """Initialize energy capacity available to regulation up market [MWh(1 MW capacity available for 1 hour)]."""
                return 0.0

            m.q_ru = pom.Var(m.time, initialize=_q_ru_init, within=pom.NonNegativeReals)

        if not hasattr(m, "q_rd"):

            def _q_rd_init(_m, t):
                """Initialize energy capacity available to regulation down market [MWh(1 MW capacity available for 1 hour)]."""
                return 0.0

            m.q_rd = pom.Var(m.time, initialize=_q_rd_init, within=pom.NonNegativeReals)

    def instantiate_model(self):
        """Instantiate the Pyomo ConcreteModel and populates it with supplied time series data."""
        if not hasattr(self, "model"):
            self.model = pom.ConcreteModel()

        m = self.model

        try:
            m.time = pom.RangeSet(0, len(self.price_electricity) - 1)
            m.soc_time = pom.RangeSet(0, len(self.price_electricity))
        except TypeError:
            # self.price_electricity is of type 'NoneType'
            m.time = []
            m.soc_time = []

        m.price_electricity = self.price_electricity

        m.price_reg_up = self.price_reg_up
        m.price_reg_down = self.price_reg_down

        m.price_reg_serv_up = self.price_reg_serv_up
        m.price_reg_serv_down = self.price_reg_serv_down

        m.cost_charge = self.cost_charge
        m.cost_discharge = self.cost_discharge

        m.mi_mult_ru = self.mileage_mult_ru
        m.mi_mult_rd = self.mileage_mult_rd

        # If fraction_reg_up/fraction_reg_down are provided to the instance, set them in the ConcreteModel.
        if self.fraction_reg_up is not None:
            m.fraction_reg_up = self.fraction_reg_up
        if self.fraction_reg_down is not None:
            m.fraction_reg_down = self.fraction_reg_down

        if self.perf_score_ru is not None:
            m.perf_score_ru = self.perf_score_ru
        if self.perf_score_rd is not None:
            m.perf_score_rd = self.perf_score_rd

    def populate_model(self):
        """Populate the Pyomo ConcreteModel based on the specified market_type."""
        self.model.objective_expr = 0.0

        self._set_model_param()
        self._set_model_var()

        self.expressions_block = ExpressionsBlock(self.market_type)

        try:
            self.expressions_block.set_expressions(self.model)
        except IndexError:
            # Array-like object(s) do(es) not match the length of the price_electricity array-like.
            raise (
                IncompatibleDataException(
                    "At least one of the array-like parameter objects is not the expected length. (It should match the length of the price_electricity object.)"
                )
            )
        else:
            self.model.objective = pom.Objective(
                expr=self.model.objective_expr, sense=pom.maximize
            )

        # if self.model.objective.value == 0.0:
        #     # Detect constant objective function value.
        #     raise(IncompatibleDataException('The objective function was ill-formed, resulting in a constant objective function.'))

    def _process_results(self):
        """Process optimization results for further evaluation."""
        m = self.model

        t = m.time
        q_r = [m.q_r[n].value for n in m.time]
        q_d = [m.q_d[n].value for n in m.time]
        q_ru = [m.q_ru[n].value for n in m.time]
        q_rd = [m.q_rd[n].value for n in m.time]
        soc = [m.s[n].value for n in m.time]
        price_electricity = [m.price_electricity[n] for n in m.time]

        run_results = {
            "time": t,
            "q_r": q_r,
            "q_d": q_d,
            "q_ru": q_ru,
            "q_rd": q_rd,
            "state of charge": soc,
            "price of electricity": price_electricity,
        }

        if self.market_type == "pfp":
            rev_arb = np.cumsum(
                np.array(
                    [
                        m.price_electricity[t] * (m.q_d[t].value - m.q_r[t].value)
                        for t in m.time
                    ]
                )
            )
            rev_reg = np.cumsum(
                np.array(
                    [
                        m.price_reg_up[t] * m.q_ru[t].value
                        + m.price_reg_down[t] * m.q_rd[t].value
                        + m.perf_score_ru[t] * m.mi_mult_ru[t] * m.price_reg_serv_up[t]
                        + m.perf_score_rd[t]
                        * m.mi_mult_rd[t]
                        * m.price_reg_serv_down[t]
                        + m.price_electricity[t]
                        * (
                            m.q_ru[t].value * m.fraction_reg_up[t]
                            - m.q_rd[t].value * m.fraction_reg_down[t]
                        )
                        for t in m.time
                    ]
                )
            )

            revenue = rev_arb + rev_reg

            run_results["rev_arb"] = rev_arb
            run_results["rev_reg"] = rev_reg
            run_results["revenue"] = revenue
        else:
            rev_arb = np.cumsum(
                np.array(
                    [
                        m.price_electricity[t] * (m.q_d[t].value - m.q_r[t].value)
                        for t in m.time
                    ]
                )
            )
            rev_reg = np.cumsum(np.array([0 for t in m.time]))

            revenue = rev_arb + rev_reg

            run_results["rev_arb"] = rev_arb
            run_results["rev_reg"] = rev_reg
            run_results["revenue"] = revenue

        try:
            self.gross_revenue = revenue[-1]
        except IndexError:
            # Revenue is of length-0, likely due to no price_electricity array-like being given before solving.
            self.gross_revenue = 0

        self.results = pd.DataFrame(run_results)

    def get_results(self):
        """Return the decision variables and derived quantities in a DataFrame, plus the net revenue."""
        return self.results, self.gross_revenue


class BadParameterException(Exception):
    pass


class IncompatibleDataException(Exception):
    pass


if __name__ == "__main__":
    with open("valuation_optimizer.log", "w"):
        pass

    logging.basicConfig(
        filename="valuation_optimizer.log",
        format="[%(levelname)s] %(asctime)s: %(message)s",
        level=logging.INFO,
    )
