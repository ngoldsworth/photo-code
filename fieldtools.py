import numpy as np
import astropy.units as u

class UsafResolvingPowerCalculator:
    """For calculating line widths on a 1951 USAF resolution chart
    https://en.wikipedia.org/wiki/1951_USAF_resolution_test_chart
    
    Example:
    chart = UsafResolvingPowerCalculator(-5, 8)
    chart.get_group(5)
    """
    def __init__(self, group_lo:int, group_hi:int):
        self.groups = np.arange(group_lo, group_hi+1, dtype=int)
        self.elements = np.arange(6, dtype=int)+1

        gg, ee = np.meshgrid(self.groups, self.elements)
        self.resolution = 2 ** (gg + (ee-1)/6) / u.mm

    @property
    def line_width(self):
        # return the width of single black line (half the pair width)
        return 1 / self.resolution

    def get_group(self, group_num ):
        if not (self.groups[0] <= group_num <= self.groups[-1]):
            raise ValueError(f"Group {group_num} not included in this chart")
        
        j = np.searchsorted(self.groups, group_num)
        print(j, self.groups[j])
        
        return self.resolution[:,j]

def depth_of_field(subject_distance, focal_length, f_number, circle_of_confusion):
    """Approximation of depth of field. Takes int, floar, u.Quantity, or np.ndarray"""
    return 2 * (subject_distance/focal_length)**2 * f_number * circle_of_confusion