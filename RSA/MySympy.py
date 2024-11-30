import re

class ModInverse:
    def __init__(self, r0: int, r1: int):
        """Enter r0 and r1. If r1 is larger, swap."""
        if r0 < r1:
            self.r0_fixed, self.r1_fixed = r1, r0
        else:
            self.r0_fixed, self.r1_fixed = r0, r1
        print(f"Calculating gcd({r0}, {r1})")
        self.steps = []
        self.result = self.compute_gcd(self.r0_fixed, self.r1_fixed)

    def compute_gcd(self, r0, r1):
        """
        Calculate gcd as mod step by step 
        and store it as a dictionary for each step. 
        At this time, if it is disjoint, 
        proceed to the process of finding the inverse.
        """
        while True:
            mod_times = 0
            if r0 >= r1:
                mod_times = r0 // r1
                r0 = r0 % r1
                print(f"Current step: gcd({r0}, {r1})")
                
            r0_factor = 1
            r1_factor = mod_times
            mod_res = r0
            self.steps.append({
                "r0_factor": r0_factor,
                "r1_factor": r1_factor,
                "r0": r0 + mod_times * r1,
                "r1": r1,
                "mod_result": mod_res
            })
            print(f"{mod_res} = {r0 + mod_times * r1} - {mod_times} * {r1}")
            r0, r1 = r1, r0
            if r1 == 1:
                return self.calculate_mod_inverse()
            elif r1 == 0:
                raise ValueError("The gcd of the two numbers is not 1. No modular inverse exists.")

    def calculate_mod_inverse(self):
        """
        This is the process of taking information for each saved step 
        and expressing 1 as an equation for r0 and r1.
        """
        expressions, results = [], []
        for step in self.steps:
            r0, r1 = step['r0'], step['r1']
            r0_factor, r1_factor = step['r0_factor'], step['r1_factor']
            expressions.append(step["mod_result"])
            for i, expr in enumerate(expressions):
                if expr == step['r0']:
                    r0 = results[i]
                if expr == step['r1']:
                    r1 = results[i]
            results.append(self.symbols(r0, r1, r0_factor, r1_factor))
        print(f"gcd({self.r0_fixed}, {self.r1_fixed}) = {results[-1]}")
        
        mod_inverse_match = re.findall(r'([-+]?\d+)\s*\*\s*', results[-1])
        result = int(mod_inverse_match[1])
        return result if result > 0 else result % self.r0_fixed
    
    def parse_factors(self, expr):
        """
        This is a function 
        that extracts a and b when the expression is "a*r0+b*r1".
        """
        factors = re.findall(r'([-+]?\d+)\s*\*\s*', expr)
        if len(factors) == 2:
            return int(factors[0]), int(factors[1])
        else:
            raise ValueError(f"Could not find two factors in the expression '{expr}'.")

    def symbols(self, x, y, a, b, var_name1="r0", var_name2="r1"):
        """
        When two variable names are input, 
        polynomial operation is implemented using string and regular expression.
        """
        if isinstance(x, int) and isinstance(y, int):
            if x == self.r0_fixed:
                return f"{int(a)} * {var_name1} + {-int(b)} * {var_name2}"
            elif x == self.r1_fixed:
                return f"{int(b)} * {var_name1} + {-int(a)} * {var_name2}"
        elif isinstance(x, int) or isinstance(y, int):
            poly_expr = y if isinstance(x, int) else x
            other_factor = -b if isinstance(x, int) else a
            try:
                c1, c2 = self.parse_factors(poly_expr)
                return f"{other_factor * c1} * {var_name1} + {1 + other_factor * c2} * {var_name2}"
            except ValueError as e:
                return str(e)
        else:
            try:
                a1, b1 = self.parse_factors(x)
                a2, b2 = self.parse_factors(y)
                return f"{a * a1 + (-b) * a2} * {var_name1} + {a * b1 + (-b) * b2} * {var_name2}"
            except ValueError as e:
                return str(e)

if __name__ == "__main__":
    print(ModInverse(79, 37).result)
