import numpy as np
import pytest
from pprint import pprint
from datetime import datetime

def group_adjust(vals, groups, weights):

    # check precondition that weights list and groups length are the same
    if len(weights) == len(groups):
        # Multiply weights numpy array with the values matrix
        reshaped_weights = np.array(weights, dtype=float).reshape(-1, 1)
        original_val_matrix = np.tile(vals, (len(groups), 1))
        weighted_val_matrix = reshaped_weights * original_val_matrix

        # Iterate through each group. Create 2 lists. The list groupCounts contains the list
        # of non-NaN elements in the group. The list groupCountsWithNaN contains the list
        # of all elements (including NaN) in the group
        for group, weighted_val_row in zip(groups, weighted_val_matrix):
            group_dict = {}
            group_counts = []
            group_counts_with_NaN = []
            for zipped_group, zipped_val in zip(group, weighted_val_row):
                if zipped_group not in group_dict:
                    group_dict[zipped_group] = True
                    group_counts.append(0)
                    group_counts_with_NaN.append(0)
                if not np.isnan(zipped_val):
                    group_counts[-1] += 1
                group_counts_with_NaN[-1] += 1
            
            # Calculate the mean for each group and update the matrix in-place. Use np.nansum() to treat np.NaN as zeros.
            # Use the values in groupCountsWithNaN for indexing and use the values in groupCounts for division
            start_index = 0
            for count, count_with_NaN in zip(group_counts, group_counts_with_NaN):
                weighted_val_row[start_index:(start_index+count_with_NaN)] = np.nansum(weighted_val_row[start_index:(start_index+count_with_NaN)]) / count
                start_index += count_with_NaN 

        # Subtract the original values from weighted means, summed by their columns
        demeaned_vals = vals - weighted_val_matrix.sum(axis=0)
        return demeaned_vals

    else:
        raise ValueError

def test_three_groups():
    vals = [1, 2, 3, 8, 5]
    grps_1 = ['USA', 'USA', 'USA', 'USA', 'USA']
    grps_2 = ['MA', 'MA', 'MA', 'RI', 'RI']
    grps_3 = ['WEYMOUTH', 'BOSTON', 'BOSTON', 'PROVIDENCE', 'PROVIDENCE']
    weights = [.15, .35, .5]

    adj_vals = group_adjust(vals, [grps_1, grps_2, grps_3], weights)
    # 1 - (USA_mean*.15 + MA_mean * .35 + WEYMOUTH_mean * .5)
    # 2 - (USA_mean*.15 + MA_mean * .35 + BOSTON_mean * .5)
    # 3 - (USA_mean*.15 + MA_mean * .35 + BOSTON_mean * .5)
    # etc ...
    # Plug in the numbers ...
    # 1 - (.15 * 3.8 + .35 * 2.0 + .5 * 1.0) = -0.770
    # 2 - (.15 * 3.8 + .35 * 2.0 + .5 * 2.5) = -0.520
    # 3 - (.15 * 3.8 + .35 * 2.0 + .5 * 2.5) =  0.480
    # etc...

    answer = [-0.770, -0.520, 0.480, 1.905, -1.095]
    for ans, res in zip(answer, adj_vals):
        assert abs(ans - res) < 1e-5


def test_two_groups():
    vals = [1, 2, 3, 8, 5]
    grps_1 = ['USA', 'USA', 'USA', 'USA', 'USA']
    grps_2 = ['MA', 'RI', 'CT', 'CT', 'CT']
    weights = [.65, .35]

    adj_vals = group_adjust(vals, [grps_1, grps_2], weights)
    # 1 - (.65 * 3.8 + .35 * 1.0) = -1.82
    # 2 - (.65 * 3.8 + .35 * 2.0) = -1.17
    # 3 - (.65 * 3.8 + .35 * 5.33333) = -1.33666
    answer = [-1.82, -1.17, -1.33666, 3.66333, 0.66333]
    for ans, res in zip(answer, adj_vals):
        assert abs(ans - res) < 1e-5

def test_missing_vals():
    # If you're using NumPy or Pandas, use np.NaN
    # If you're writing pyton, use None
    vals = [1, np.NaN, 3, 5, 8, 7]
    #vals = [1, None, 3, 5, 8, 7]
    grps_1 = ['USA', 'USA', 'USA', 'USA', 'USA', 'USA']
    grps_2 = ['MA', 'RI', 'RI', 'CT', 'CT', 'CT']
    weights = [.65, .35]

    adj_vals = group_adjust(vals, [grps_1, grps_2], weights)

    # This should be None or np.NaN depending on your implementation
    # please feel free to change this line to match yours
    answer = [-2.47, np.NaN, -1.170, -0.4533333, 2.54666666, 1.54666666]
    #answer = [-2.47, None, -1.170, -0.4533333, 2.54666666, 1.54666666]

    for ans, res in zip(answer, adj_vals):
        if ans is None:
            assert res is None
        elif np.isnan(ans):
            assert np.isnan(res)
        else:
            assert abs(ans - res) < 1e-5

def test_weights_len_equals_group_len():
    # Need to have 1 weight for each group

    vals = [1, np.NaN, 3, 5, 8, 7]
    #vals = [1, None, 3, 5, 8, 7]
    grps_1 = ['USA', 'USA', 'USA', 'USA', 'USA', 'USA']
    grps_2 = ['MA', 'RI', 'RI', 'CT', 'CT', 'CT']
    weights = [.65]

    with pytest.raises(ValueError):
        group_adjust(vals, [grps_1, grps_2], weights)

def test_group_len_equals_vals_len():
    # The groups need to be same shape as vals
    vals = [1, None, 3, 5, 8, 7]
    grps_1 = ['USA']
    grps_2 = ['MA', 'RI', 'RI', 'CT', 'CT', 'CT']
    weights = [.65]

    with pytest.raises(ValueError):
        group_adjust(vals, [grps_1, grps_2], weights)

def test_performance():
    # vals = 1000000*[1, None, 3, 5, 8, 7]
    # If you're doing numpy, use the np.NaN instead
    vals = 1000000 * [1, np.NaN, 3, 5, 8, 7]
    grps_1 = 1000000 * [1, 1, 1, 1, 1, 1]
    grps_2 = 1000000 * [1, 1, 1, 1, 2, 2]
    grps_3 = 1000000 * [1, 2, 2, 3, 4, 5]
    weights = [.20, .30, .50]

    start = datetime.now()
    group_adjust(vals, [grps_1, grps_2, grps_3], weights)
    end = datetime.now()
    diff = end - start
