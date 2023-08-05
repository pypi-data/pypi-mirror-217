from pycatalicism.calc.calculator import Calculator
from pycatalicism.calc.cooxidationcalculator import COOxidationCalculator
from pycatalicism.calc.co2hydrogenationcalculator import CO2HydrogenationCalculator
from pycatalicism.calc.co2hydrogenationproductsbasiscalculator import CO2HydrogenationProductsBasisCalculator
from pycatalicism.calc.calculatorexception import CalculatorException

"""
Factory to create calculator for proper reaction.
"""

def get_calculator(reaction:str, products_basis:bool) -> Calculator:
    """
    Create calculator for reaction to calculate conversion, selectivity or activity vs. temperature data.

    parameters
    ----------
    reaction:str {co-oxidation|co2-hydrogenation}
        Chemical reaction for which to calculate results
    products_basis:bool
        If True, return calculator, which calculates conversion based on products composition

    returns
    -------
    calculator:Calculator
        Calculator to use for catalyst characteristics calculation

    raises
    ------
    exception:Exception
        if reaction is not known
    """
    if reaction == 'co-oxidation':
        return COOxidationCalculator()
    elif reaction == 'co2-hydrogenation':
        if products_basis:
            return CO2HydrogenationProductsBasisCalculator()
        else:
            return CO2HydrogenationCalculator()
    else:
        raise CalculatorException(f'Cannot create calculator for reaction {reaction}')
