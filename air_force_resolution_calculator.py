# air force resolution chart

import numpy as np
import astropy.units as u

class UsafResoliveingPowerCalculator:
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

    



if __name__ == '__main__':
    chart = UsafResoliveingPowerCalculator(-5, 8)
    gnum = -4
    g = chart.get_group(gnum)
    g2 = chart.get_group(gnum+4)
    # print(chart.resolution)
    print(1/g)
    print(1/g2)
    print(chart.get_group(3))
    print(g2/g)